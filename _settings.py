import os, pickle
from typing import Any, Tuple

# Helper
from _constants import *
from _debug import *



class SettingsHelper():
  full_path = SETTINGS_FILE
  _settings = {
    "cache_expiration": 30,
    "check_updates": True,
    "download_path": os.getcwd(),
    "unzip": True,
  }


  def __init__(self):
    if os.path.exists(self.full_path):
      self._read()
    else:
      DebugHelper.print(DebugType.TYPE_WARNING, f"<{SETTINGS_FILE}> not found.", "SETTINGS")
      self.write()


  def get(self, option: str):
    for op in self._settings:
      if option == op: return self._settings[option]
    raise ValueError(f"Setting <{option}> not found.")


  def update(self, option: Tuple[str, Any]):
    key, value = option

    for op in self._settings:
      if op == key:
        self._settings[key] = value
        DebugHelper.print(DebugType.TYPE_DEBUG, f"'{key}' updated to {value}.", "SETTINGS")
        return
    raise ValueError(f"Setting <{key}> not found.")


  def write(self):
    with open(self.full_path, 'wb') as fp:
      pickle.dump(self._settings, fp)
      DebugHelper.print(DebugType.TYPE_INFO, f"<{SETTINGS_FILE}> wrote.", "SETTINGS")


  def _read(self):
    try:
      with open(self.full_path, 'rb') as fp:
        temp_settings: dict = pickle.load(fp)
        if len(temp_settings.keys()) != len(self._settings.keys()): self._fix(temp_settings)
        else: self._settings = temp_settings
        DebugHelper.print(DebugType.TYPE_INFO, f"<{SETTINGS_FILE}> loaded.", "SETTINGS")
        for option in self._settings: DebugHelper.print(DebugType.TYPE_DEBUG, f"'{option}': {str(self._settings[option])}")
    except EOFError: pass


  def _fix(self, old_settings: dict):
    DebugHelper.print(DebugType.TYPE_WARNING, f"Application and file mismatch. Trying to fix...", "SETTINGS")
    for key in old_settings:
      try:
        if self._settings[key]: self._settings[key] = old_settings[key]
        DebugHelper.print(DebugType.TYPE_WARNING, f"'{key}' recovered.", "SETTINGS")
      except KeyError:
        DebugHelper.print(DebugType.TYPE_ERROR, f"'{key}' cannot be recovered.", "SETTINGS")
    self.write()
