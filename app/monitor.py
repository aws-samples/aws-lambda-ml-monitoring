import json
import requests

from typing import List
from enum import Enum

LOGGING_ENDPOINT = 'http://127.0.0.1:2772'


class LogType(str, Enum):
    INPUTS = "INPUTS"
    RESULTS = "RESULTS"


def log_inputs_for(request_id: str, inputs: List):
    requests.post(
        LOGGING_ENDPOINT,
        json={
            'type': LogType.INPUTS,
            'request_id': request_id,
            'inputs': json.dumps(inputs)
        }
    )


def log_outputs_for(request_id: str, results: List):
    requests.post(
        LOGGING_ENDPOINT,
        json={
            'type': LogType.RESULTS,
            'request_id': request_id,
            'results': json.dumps(results)
        }
    )
