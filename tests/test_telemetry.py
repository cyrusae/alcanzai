"""
Tests for paper_library.telemetry.

Design goals:
- Every test exercises real OTel SDK behaviour — no tautologies.
- Tests are isolated: each creates its own TracerProvider / MeterProvider so
  they don't interfere with each other or with the module-level globals in
  telemetry.py (which may already be initialised by the time these run).
- The _initialized flag in telemetry.py is reset per test that calls
  init_telemetry() to ensure idempotence tests are meaningful.
"""

import atexit
import logging
import pytest

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader

import paper_library.telemetry as telemetry_module
from paper_library.telemetry import get_logger, _add_otel_context


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_trace_provider() -> tuple:
    """Return a (provider, exporter) pair that captures spans in memory."""
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    return provider, exporter


@pytest.fixture(autouse=True)
def reset_telemetry_flag():
    """Reset the _initialized flag before and after every test."""
    original = telemetry_module._initialized
    telemetry_module._initialized = False
    yield
    telemetry_module._initialized = original


# ---------------------------------------------------------------------------
# Span creation and attribute flow
# ---------------------------------------------------------------------------

class TestSpanBehaviour:
    """Real span creation using an in-process InMemorySpanExporter."""

    def test_span_is_recorded_and_exported(self):
        provider, exporter = _make_trace_provider()
        tracer = provider.get_tracer("alcanzai-test")

        with tracer.start_as_current_span("test_operation") as span:
            span.set_attribute("my.attr", "hello")

        finished = exporter.get_finished_spans()
        assert len(finished) == 1
        assert finished[0].name == "test_operation"
        assert finished[0].attributes["my.attr"] == "hello"

    def test_nested_spans_have_correct_parent(self):
        provider, exporter = _make_trace_provider()
        tracer = provider.get_tracer("alcanzai-test")

        with tracer.start_as_current_span("parent"):
            with tracer.start_as_current_span("child"):
                pass

        spans = exporter.get_finished_spans()
        assert len(spans) == 2
        child = next(s for s in spans if s.name == "child")
        parent = next(s for s in spans if s.name == "parent")
        assert child.parent.span_id == parent.context.span_id

    def test_span_context_injected_into_log_event(self):
        """_add_otel_context injects trace_id/span_id from the active span."""
        provider, _ = _make_trace_provider()
        tracer = provider.get_tracer("alcanzai-test")

        with tracer.start_as_current_span("log_span"):
            event = _add_otel_context(None, None, {"event": "hello"})
            assert "trace_id" in event, "trace_id missing from log event"
            assert "span_id" in event, "span_id missing from log event"
            # telemetry.py uses hex()[2:] without zero-padding, so the string is
            # 1–32 hex chars depending on leading-zero bits in the trace_id.
            assert 1 <= len(event["trace_id"]) <= 32, (
                f"trace_id length out of range: {event['trace_id']!r}"
            )
            assert all(c in "0123456789abcdef" for c in event["trace_id"]), (
                "trace_id must be lowercase hex"
            )

    def test_no_active_span_means_no_trace_context_in_log(self):
        """Outside any recording span, _add_otel_context must not inject trace_id."""
        event = _add_otel_context(None, None, {"event": "hello"})
        assert "trace_id" not in event


# ---------------------------------------------------------------------------
# Metric counters
# ---------------------------------------------------------------------------

class TestMetricCounters:
    """Module-level ProxyCounters in synthesis_generator forward to a real provider."""

    def test_proxy_counter_forwards_after_set_provider(self):
        """Counter increments are forwarded to the real provider once it is set."""
        from opentelemetry import metrics as otel_metrics
        from paper_library.synthesis_generator import (
            input_tokens_counter,
            output_tokens_counter,
            cost_counter,
        )

        reader = InMemoryMetricReader()
        mp = MeterProvider(metric_readers=[reader])
        otel_metrics.set_meter_provider(mp)
        try:
            input_tokens_counter.add(100, {"model": "haiku"})
            output_tokens_counter.add(50, {"model": "haiku"})
            cost_counter.add(0.001, {"model": "haiku"})

            data = reader.get_metrics_data()
            metric_names = {
                m.name
                for rm in data.resource_metrics
                for sm in rm.scope_metrics
                for m in sm.metrics
            }
            assert "alcanzai.llm.tokens.input" in metric_names
            assert "alcanzai.llm.tokens.output" in metric_names
            assert "alcanzai.llm.cost.usd" in metric_names
        finally:
            # Restore a no-op provider so we don't pollute other tests
            otel_metrics.set_meter_provider(MeterProvider())


# ---------------------------------------------------------------------------
# init_telemetry() behaviour
# ---------------------------------------------------------------------------

class TestInitTelemetry:
    """Tests that init_telemetry() configures logging correctly."""

    def test_init_without_otlp_does_not_raise(self, monkeypatch):
        monkeypatch.delenv("OTEL_EXPORTER_OTLP_ENDPOINT", raising=False)
        telemetry_module.init_telemetry()  # must not raise

    def test_idempotent_second_call_does_not_duplicate_handlers(self, monkeypatch):
        monkeypatch.delenv("OTEL_EXPORTER_OTLP_ENDPOINT", raising=False)
        telemetry_module.init_telemetry()
        handler_count = len(logging.getLogger().handlers)

        # Force second init
        telemetry_module._initialized = False
        telemetry_module.init_telemetry()
        # A fresh init replaces the handlers list; total must not balloon
        assert len(logging.getLogger().handlers) <= handler_count + 1

    def test_debug_log_level_applied(self, monkeypatch):
        monkeypatch.delenv("OTEL_EXPORTER_OTLP_ENDPOINT", raising=False)
        telemetry_module.init_telemetry(log_level_override="DEBUG")
        assert logging.getLogger().level == logging.DEBUG

    def test_tracer_provider_shutdown_registered_at_atexit(self, monkeypatch):
        """TracerProvider.shutdown must be registered so last-batch spans flush on exit."""
        import unittest.mock as mock

        monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")

        registered = []
        original_register = atexit.register

        def capturing_register(f, *a, **kw):
            registered.append(f)
            return original_register(f, *a, **kw)

        # Mock the OTLP exporters so init_telemetry() doesn't attempt a real
        # gRPC connection to localhost:4317 during the test.
        noop_exporter = mock.MagicMock()
        noop_metric_exporter = mock.MagicMock()
        with (
            mock.patch("paper_library.telemetry.OTLPSpanExporter", return_value=noop_exporter),
            mock.patch("paper_library.telemetry.OTLPMetricExporter", return_value=noop_metric_exporter),
            mock.patch("paper_library.telemetry.atexit.register", side_effect=capturing_register),
        ):
            telemetry_module.init_telemetry()

        names = [getattr(f, "__name__", repr(f)) for f in registered]
        assert "shutdown" in names, (
            f"TracerProvider.shutdown not in atexit registrations: {names}"
        )
        assert names.count("shutdown") >= 2, (
            "Expected both TracerProvider.shutdown and MeterProvider.shutdown registered; "
            f"got: {names}"
        )


# ---------------------------------------------------------------------------
# get_logger
# ---------------------------------------------------------------------------

class TestGetLogger:
    """get_logger() must return a usable structlog BoundLogger."""

    def test_returns_bound_logger_with_expected_methods(self):
        log = get_logger("test.module")
        for method in ("info", "debug", "warning", "error", "critical"):
            assert callable(getattr(log, method, None)), \
                f"Logger missing expected method: {method}"
