import os
from typing import Optional


def load_from_env(env_var_name:str, default:Optional[str]=None) -> Optional[str]:
  return os.environ.get(env_var_name, default)

def load_from_env_to_int(env_var_name:str, default: int) -> int:
  try:
    return int(load_from_env(env_var_name) or default)
  except Exception:
    print('Could not load environment variable')
    return default

class Configuration:
  # Batch size ... default to 100, do not send until batch size is reached
  batch_size: int = load_from_env_to_int("MODEL_MONITOR_BATCH_SIZE", 100)

  # Batch window ... wait for this long before sending, default to 1 minute
  batch_window: float = load_from_env_to_int("MODEL_MONITOR_BATCH_WINDOW", 60000) / 1000

  # S3 bucket ... for S3 Handler, write data to this bucket, optional
  s3_bucket: Optional[str] = load_from_env("MODEL_MONITOR_S3_BUCKET", None)
  
