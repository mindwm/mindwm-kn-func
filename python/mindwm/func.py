import os
import sys
import re
#sys.path.append(os.path.abspath('mindwm-sdk-python/neomodel'))
#sys.path.append(os.path.abspath('mindwm-sdk-python/MindWM'))

sys.path.append(os.path.abspath('mindwm-sdk-python'))

from parliament import Context, event
import neomodel
import MindWM
from cloudevents.http import from_http
from cloudevents import abstract, conversion
# Logs and traces
import logging
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


func_name = "demo_func"
resource = Resource(attributes={ SERVICE_NAME: func_name })
# NOTE: OTEL_EXPORTER_OTLP_ENDPOINT env var should be defined to export logs
# i.e. `http://10.20.30.11:4317/v1/traces`
span_processor = BatchSpanProcessor(OTLPSpanGrpcExporter())
trace_provider = TracerProvider(resource=resource, active_span_processor=span_processor)
trace.set_tracer_provider(trace_provider)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s [%(levelname)s] %(message)s')
logger = logging.getLogger(func_name)
tracer = trace.get_tracer(func_name)


@event
def main(context: Context):
    # NOTE: need to fetch a traceId part from the `traceparent` field value
    event = from_http(context.request.headers, context.request.data)
    ctx = TraceContextTextMapPropagator().extract(carrier=event)

    with tracer.start_as_current_span("processing", context=ctx) as span:
        logger.debug(conversion.to_json(event))

    with tracer.start_as_current_span("reply", context=ctx) as span:
        return context.cloud_event.data

