import os
from PyQt6.QtCore import qDebug
from enum import Enum
from typing import Literal


class DebugType(Enum):
  TYPE_INFO = "INFO"
  TYPE_WARNING = "WARNING"
  TYPE_ERROR = "ERROR"
  TYPE_DEBUG = "DEBUG"

class DebugHelper():
  def print(debug_type: Literal[DebugType.TYPE_INFO, DebugType.TYPE_WARNING, DebugType.TYPE_ERROR], debug_message: str, debug_module: str = None):
    if os.environ['DEBUG'] == "0": return
    elif os.environ['DEBUG'] == "1" and (debug_type != DebugType.TYPE_ERROR): return
    elif os.environ['DEBUG'] == "2" and (debug_type != DebugType.TYPE_ERROR and debug_type != DebugType.TYPE_WARNING): return
    elif os.environ['DEBUG'] == "3" and (debug_type != DebugType.TYPE_ERROR and debug_type != DebugType.TYPE_WARNING and debug_type != DebugType.TYPE_INFO): return
    else:
      message = ''.join(f"[{debug_type.value}]")
      if debug_module: message += f"[{debug_module.upper()}]"
      message += f" {debug_message}"
      qDebug(message)