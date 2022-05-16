import os
import boto3
import random
from typing import List

from model_monitor.configuration import Configuration
from model_monitor.handlers.base_handler import LogsHandler, LogRecord

class S3Handler(LogsHandler):
  def handle_logs(self, records: List[LogRecord]) -> bool:
    if not (Configuration.s3_bucket and records):
      return False
    
    key = S3Handler.get_key_name(records)
    data = S3Handler.format_records(records)

    s3 = boto3.client('s3')
    s3.put_object(Body=data, Bucket=Configuration.s3_bucket, Key=key)
    return True
    

  @staticmethod
  def get_key_name(records: List[LogRecord]):
    print(records)
    start_time = min(r.log_time for r in records)
    log_directory = f"monitor/{start_time.year}/{start_time.month}/{start_time.day}/{start_time.hour}"
    return f"{log_directory}-{random.random()}"

  @staticmethod
  def format_records(records: List[LogRecord]) -> bytes:
    return "\n".join(map(S3Handler._format_record, records)).encode()

  @staticmethod
  def _format_record(r: LogRecord):
    return f"{r.log_time.isoformat()} : {r.inputs} : {r.results}"
  