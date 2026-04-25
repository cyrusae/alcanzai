import os
import atexit
import logging
from typing import Optional
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import structlog
from paper_library import __version__

# Global tracer and meter
# These will be no-ops until a provider is set via init_telemetry()
tracer = trace.get_tracer("alcanzai")
meter = metrics.get_meter("alcanzai")

# Flag to prevent multiple initializations
_initialized = False

def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger."""
    return structlog.get_logger(name)

def init_telemetry(log_level_override: Optional[str] = None) -> None:
    """
    Initialize OpenTelemetry and structlog.
    Idempotent — safe to call multiple times.
    """
    global _initialized
    if _initialized:
        return

    # Configuration from environment
    otel_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    service_name = os.getenv("OTEL_SERVICE_NAME", "alcanzai")
    log_level = log_level_override or os.getenv("ALCANZAI_LOG_LEVEL", "INFO").upper()
    log_file = os.getenv("ALCANZAI_LOG_FILE")

    # Resource common to all telemetry
    resource = Resource.create({
        "service.name": service_name,
        "service.version": __version__,
    })

    if otel_endpoint:
        # Trace Provider
        tp = TracerProvider(resource=resource)
        tp.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=otel_endpoint)))
        trace.set_tracer_provider(tp)

        # Meter Provider
        mp = MeterProvider(
            resource=resource,
            metric_readers=[PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=otel_endpoint))]
        )
        metrics.set_meter_provider(mp)
        
        # Ensure meter provider shuts down at exit
        atexit.register(mp.shutdown)

        # Auto-instrument requests
        RequestsInstrumentor().instrument()
        
        renderer = structlog.processors.JSONRenderer()
    else:
        # No-op providers are default, but we log that export is disabled
        logging.basicConfig(level=log_level)
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    # Configure structlog
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        # OTel trace context processor
        _add_otel_context,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Bridge structlog with stdlib logging
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
        ],
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(log_level)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_formatter = structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=[
                structlog.stdlib.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
            ],
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.processors.JSONRenderer(),
            ],
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    _initialized = True

    if not otel_endpoint:
        get_logger(__name__).info("telemetry_export_disabled", reason="OTEL_EXPORTER_OTLP_ENDPOINT not set")

def _add_otel_context(_, __, event_dict):
    """Inject OTel trace_id and span_id into log events if an active span exists."""
    span = trace.get_current_span()
    if span and span.is_recording():
        ctx = span.get_span_context()
        if ctx.is_valid:
            event_dict["trace_id"] = hex(ctx.trace_id)[2:]
            event_dict["span_id"] = hex(ctx.span_id)[2:]
    return event_dict
