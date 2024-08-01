import os
import sys
import re
sys.path.append(os.path.abspath('mindwm-sdk-python/neomodel'))
sys.path.append(os.path.abspath('mindwm-sdk-python/MindWM'))

from parliament import Context, event

import neomodel_data
import MindWM
import pprint

from cloudevents.http import from_http
from cloudevents import abstract, conversion



@event
def main(context: Context):

    event = from_http(context.request.headers, context.request.data)
    pprint.pprint(conversion.to_json(event), stream=sys.stderr)


    return context.cloud_event.data
