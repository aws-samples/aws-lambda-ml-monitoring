from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
import json

@dataclass(frozen=True)
class LogRecord:
  log_time: datetime
  request_id: str
  inputs: List
  results: List

  @staticmethod
  def parse(record: Dict[str, str]) -> "LogRecord":
    return LogRecord(
      log_time = datetime.now(),
      request_id = record['request_id'],
      inputs = record['inputs'] if 'inputs' in record.keys() else None,
      results = record['results'] if 'results' in record.keys() else None,
    )
  
  @staticmethod
  def merge(first: "LogRecord", other: "LogRecord") -> "LogRecord":
    if first.request_id != other.request_id:
      raise KeyError("Request IDs do not match")
    elif first.__eq__(other):
      raise KeyError("Log records are the same, nothing to merge")

    return LogRecord(
      log_time = first.log_time,
      request_id = first.request_id,
      inputs = first.inputs or other.inputs,
      results = first.results or other.results,
    )


class LogsHandler(ABC):
  @abstractmethod
  def handle_logs(self, records: List[LogRecord]):
    raise NotImplementedError()
