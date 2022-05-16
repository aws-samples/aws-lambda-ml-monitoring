#!/usr/bin/env python3

import json
import os
import requests
import signal
import sys
from pathlib import Path

from model_monitor.logs_subscriber import subscribe_to_ipc
from model_monitor.logs_manager import LogsManager

# global variables
# extension name has to match the file's parent directory name)
LAMBDA_EXTENSION_NAME = Path(__file__).parent.name


def execute_custom_processing(event):
  print(f"[{LAMBDA_EXTENSION_NAME}] Received event: {json.dumps(event)}", flush=True)
  LogsManager.get_manager().send_batch_if_needed()

def execute_custom_shutdown(event):
  print(f"[{LAMBDA_EXTENSION_NAME}] Received SHUTDOWN event. Exiting.", flush=True)
  LogsManager.get_manager().send_batch()

### boiler plate code below ###
def handle_signal(signal, frame):
  # if needed pass this signal down to child processes
  print(f"[{LAMBDA_EXTENSION_NAME}] Received signal={signal}. Exiting.", flush=True)
  sys.exit(0)

def register_extension():
  print(f"[{LAMBDA_EXTENSION_NAME}] Registering...", flush=True)
  headers = {
    'Lambda-Extension-Name': LAMBDA_EXTENSION_NAME,
  }
  payload = {
    'events': [
      'INVOKE',
      'SHUTDOWN'
    ],
  }
  response = requests.post(
    url=f"http://{os.environ['AWS_LAMBDA_RUNTIME_API']}/2020-01-01/extension/register",
    json=payload,
    headers=headers
  )
  ext_id = response.headers['Lambda-Extension-Identifier']
  print(f"[{LAMBDA_EXTENSION_NAME}] Registered with ID: {ext_id}", flush=True)

  return ext_id

def process_events(ext_id):
  headers = {
    'Lambda-Extension-Identifier': ext_id
  }
  while True:
    print(f"[{LAMBDA_EXTENSION_NAME}] Waiting for event...", flush=True)
    response = requests.get(
      url=f"http://{os.environ['AWS_LAMBDA_RUNTIME_API']}/2020-01-01/extension/event/next",
      headers=headers,
      timeout=None
    )
    event = json.loads(response.text)
    if event['eventType'] == 'SHUTDOWN':
      execute_custom_shutdown(event)
      sys.exit(0)
    else:
      execute_custom_processing(event)


def main():
  # handle signals
  signal.signal(signal.SIGINT, handle_signal)
  signal.signal(signal.SIGTERM, handle_signal)

  # start http server for IPC
  subscribe_to_ipc()

  # execute extensions logic
  extension_id = register_extension()
  process_events(extension_id)


if __name__ == "__main__":
  main()