import os, requests, json, pickle
from datetime import datetime, timedelta

# Qt
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

# Helpers
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



  platforms = [
    [ 'Nintendo - NES', '7z', 'nointro.nes' ],
    [ 'Nintendo - SNES', '7z', 'nointro.snes' ],
    [ 'Nintendo - 64', '7z', 'nointro.n64' ],
    [ 'Nintendo - 64DD', '7z', 'nointro.n64dd' ],
    [ 'Nintendo - VirtualBoy', '7z', 'nointro.vb' ],
    [ 'Nintendo - GameBoy', '7z', 'nointro.gb' ],
    [ 'Nintendo - GameBoy Color', '7z', 'nointro.gbc' ],
    [ 'Nintendo - GameBoy Advance', '7z', 'nointro.gba' ],
    [ 'Sega - Master System / Mark III', '7z', 'nointro.ms-mkiii' ],
    [ 'Sega - Megadrive / Genesis', '7z', 'nointro.md' ],
    [ 'Sega - 32X', '7z', 'nointro.32x' ],
    [ 'Sega - Game Gear', '7z', 'nointro.gg' ],
    [ 'Atari 2600', '7z', 'nointro.atari-2600' ],
    [ 'Atari 5200', '7z', 'nointro.atari-5200' ],
    [ 'Atari 7800', '7z', 'nointro.atari-7800' ],
    [ 'Sony - Playstation', 'zip', 'non-redump_sony_playstation' ],
    [ 'Sony - Playstation', '7z', 'redump-sony-playstation-pal'],
    [ 'Sony - Playstation 2', 'zip', 27, 'PS2_COLLECTION_PART$$' ],
    [ 'Sony - Playstation 3', 'zip', 8, 'PS3_NOINTRO_EUR_$$' ],
  ]
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
    # Create workers and run them in separate threads (for speed)
    [self.threads.append(QThread()) for _ in range(len(self.platforms))]

    for i in range(len(self.platforms)):
      self.workers.append(CacheGenerator.PlatformWorker(self.platforms[i], self.output_cache_json))
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
    cache_mdate = os.path.getmtime("database_cache.dat")
    cache_mdate = datetime.fromtimestamp(cache_mdate)
    today_date = datetime.today()
    expiration_date = cache_mdate + timedelta(days=validity_days)

    if expiration_date > today_date:
      return True
    else:
      return False