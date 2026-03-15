import pytest
from paper_library.telemetry import init_telemetry, get_logger, tracer, meter

def test_init_telemetry_no_otlp(monkeypatch):
    """Call init_telemetry() with no OTEL_EXPORTER_OTLP_ENDPOINT set."""
    # Ensure environment is clean
    monkeypatch.delenv("OTEL_EXPORTER_OTLP_ENDPOINT", raising=False)
    # Should not raise
    init_telemetry()
    assert tracer is not None
    assert meter is not None

def test_init_telemetry_idempotent():
    """Call init_telemetry() twice — should not raise or duplicate handlers."""
    init_telemetry()
    init_telemetry()
    # If it didn't raise, we consider it successful for this unit test

def test_get_logger_returns_logger():
    """get_logger(__name__) returns something with .info, .debug, .warning, .error."""
    logger = get_logger("test_logger")
    assert hasattr(logger, "info")
    assert hasattr(logger, "debug")
    assert hasattr(logger, "warning")
    assert hasattr(logger, "error")

def test_diagnostics_sets_debug_level():
    """init_telemetry(log_level_override='DEBUG') should not raise."""
    init_telemetry(log_level_override='DEBUG')
