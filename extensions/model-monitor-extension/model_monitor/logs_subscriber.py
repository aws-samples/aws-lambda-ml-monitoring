import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from concurrent.futures.thread import ThreadPoolExecutor

from model_monitor.logs_manager import LogsManager

def subscribe_to_ipc():
  server = HTTPServer(("0.0.0.0", 2772), ModelMonitorRequestHandler)
  server.server_activate()
  ThreadPoolExecutor().submit(server.serve_forever)

class ModelMonitorRequestHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    content_length = int(self.headers.get("Content-Length", "0"))
    record = json.loads(self.rfile.read(content_length))
    LogsManager.get_manager().add_records([ record ])

    self.send_response(200)
    self.end_headers()

  def log_message(self, *args):
    # doing nothing
    return

  