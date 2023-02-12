# Qt
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

# Helpers
from _constants import *
from _platforms import PlatformsHelper
from _settings import SettingsHelper
from _debug import *


class CacheGenerator():
  class PlatformWorker(QObject):
    platform = []
    finished = pyqtSignal(str)


    def __init__(self, platform: list, output_cache_json: dict):
      super().__init__(None)
      self.platform = platform
      self.output_cache_json = output_cache_json


    def run(self):
      if len(self.platform) == 3: # SINGLE PART
        self.id_name = self.platform[0]
        self.format = self.platform[1]
        self.parts = 1
        self.url = f"https://archive.org/details/{self.platform[2]}&output=json"
        self.output_cache_json[self.id_name] = {}
        DebugHelper.print(DebugType.TYPE_DEBUG, f"Processing <{self.id_name}>", "CACHE")
        self._ProcessPart(part_id=self.platform[2])
      elif len(self.platform) == 4: # MULTI PART
        self.id_name = self.platform[0]
        self.format = self.platform[1]
        self.parts = self.platform[2]
        self.output_cache_json[self.id_name] = {}
        
        DebugHelper.print(DebugType.TYPE_DEBUG, f"Processing <{self.id_name}>", "CACHE")
        for i in range(1, self.parts+1):
          parts_id = str(self.platform[3]).replace('$$', str(i))
          self.url = f"https://archive.org/details/{parts_id}&output=json"
          self._ProcessPart(part_id=parts_id, part_number=i)
      self.finished.emit(self.id_name)


    def _ProcessPart(self, part_id: str, part_number: int = 1):
      import requests, json
      try:
        content_request = requests.get(self.url).content
        content_json = json.loads(content_request)
        part_files = content_json['files']
        for file in part_files:
          if str(file).find(self.format) != -1:
            output_file = {
              "source_id": part_id,
              "size": int(part_files[file]['size']),
              "md5": part_files[file]['md5'],
              "crc32": part_files[file]['crc32'],
              "sha1": part_files[file]['sha1'],
              "format": part_files[file]['format'],
            }
            self.output_cache_json[self.id_name][file[1:-(len(self.format)+1)]] = output_file
      except: pass


  app: QApplication = None
  parent: QSplashScreen = None
  output_cache_json = {}
  threads = []
  workers = []
  download_completed = 0


  def __init__(self, app: QApplication, parent: QSplashScreen) -> None:
    self.app = app
    self.parent = parent


  def run(self):
    import pickle

    # Create workers and run them in separate threads (for speed)
    [self.threads.append(QThread()) for _ in range(len(ARCHIVE_PLATFORMS_DATA))]

    for i in range(len(ARCHIVE_PLATFORMS_DATA)):
      self.workers.append(CacheGenerator.PlatformWorker(ARCHIVE_PLATFORMS_DATA[i], self.output_cache_json))
      self.workers[i].moveToThread(self.threads[i])
      self.threads[i].started.connect(self.workers[i].run)
      self.workers[i].finished.connect(self._updateMessage)
      self.workers[i].finished.connect(self.threads[i].quit)
      self.threads[i].finished.connect(self.threads[i].deleteLater)
      self.threads[i].start()

    # Wait until workers finished
    while self.download_completed != len(self.threads): self.app.processEvents()
    
    # Sort the data before writing
    temp_dict = sorted(self.output_cache_json)
    new_output_cache_json = {}
    for i in range(len(temp_dict)):
      temp_name = temp_dict[i]
      for j in range(len(self.output_cache_json)):
        output_name = list(self.output_cache_json)[j]
        if temp_name == output_name:
          new_output_cache_json[temp_name] = {}
          new_output_cache_json[temp_name] = self.output_cache_json[temp_name]
    self.output_cache_json = new_output_cache_json
    
    # And finally write to file
    with open("database_cache.dat", "wb") as fp: pickle.dump(self.output_cache_json, fp)


  def _updateMessage(self, platform_name: str):
    self.download_completed += 1
    self.parent.showMessage(f"({self.download_completed}/{len(self.threads)}) [{platform_name}] completed.",
      color=Qt.GlobalColor.white,
      alignment=(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)
    )



class RomDownload():
  platform_name = ""
  rom_name = ""
  rom_url = ""
  rom_format = ""

  def __init__(self, settings: SettingsHelper, platforms: PlatformsHelper, platform: str, rom_index: int) -> None:
    import requests
    from urllib.parse import quote

    self.platform_name = platform
    self.rom_name = platforms.getRomName(platform, rom_index)
    self.rom_format = platforms.getRom(platform, self.rom_name)['format']
    self.rom_url = f"https://archive.org/download/{platforms.getRom(platform, self.rom_name)['source_id']}/{quote(self.rom_name)}.{self.rom_format}"
    DebugHelper.print(DebugType.TYPE_INFO, f"Downloading [{self.platform_name}] {self.rom_name}", "downloader")
    with open(os.path.join(settings.get('download_path'), f"{self.rom_name}.{self.rom_format}"), "wb") as of:
      DebugHelper.print(DebugType.TYPE_DEBUG, f"Downloading from [{self.rom_url}]", "downloader")
      of.write(requests.get(self.rom_url).content)



class Unzip():
  def __init__(self, settings: SettingsHelper, filename: str) -> None:
    from py7zr import SevenZipFile
    path = settings.get('download_path')
    full_path = os.path.join(path, filename)
    DebugHelper.print(DebugType.TYPE_INFO, f"Unzipping [{full_path}]...", "unzip")
    SevenZipFile(full_path).extractall(path)
    os.remove(full_path)
    


class Tools():
  def convertSizeToReadable(size: int) -> str:
    if size < 1000:
      return '%i' % size + 'B'
    elif 1000 <= size < 1000000:
      return '%.1f' % float(size/1000) + ' KB'
    elif 1000000 <= size < 1000000000:
      return '%.1f' % float(size/1000000) + ' MB'
    elif 1000000000 <= size < 1000000000000:
      return '%.1f' % float(size/1000000000) + ' GB'
    elif 1000000000000 <= size:
      return '%.1f' % float(size/1000000000000) + ' TB'


  def isCacheValid(validity_days: int) -> bool:
    import os
    from datetime import datetime, timedelta

    cache_mdate = os.path.getmtime("database_cache.dat")
    cache_mdate = datetime.fromtimestamp(cache_mdate)
    today_date = datetime.today()
    expiration_date = cache_mdate + timedelta(days=validity_days)

    if expiration_date > today_date: return True
    else: return False
