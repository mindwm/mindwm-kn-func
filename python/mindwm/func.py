import os
import sys
import re
sys.path.append(os.path.abspath('mindwm-sdk-python'))

from parliament import Context, event
import neomodel
import MindWM
from cloudevents.http import from_http
from cloudevents import abstract, conversion

# logs and traces
import otlp
from otlp import logger,tracer
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

@event
def main(context: Context):
#    event = from_http(context.request.headers, context.request.data)
    event = context.cloud_event
    # NOTE: need to fetch a traceId part from the `traceparent` field value
    ctx = TraceContextTextMapPropagator().extract(carrier=event)

    with tracer.start_as_current_span("processing", context=ctx) as span:
        logger.debug(f"start processing: {event}")
        #logger.debug(conversion.to_json(event))

    with tracer.start_as_current_span("reply", context=ctx) as span:
        return context.cloud_event.data

