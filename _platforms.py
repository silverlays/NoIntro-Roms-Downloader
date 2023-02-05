import os, pickle

# Helpers
from _debug import *



PLATFORMS_CACHE_FILENAME = "database_cache.dat"



class PlatformsHelper():
  _platformsCache = {}


  def __init__(self):
    if os.path.exists(PLATFORMS_CACHE_FILENAME):
      try:
        with open(PLATFORMS_CACHE_FILENAME, 'rb') as fp: self._platformsCache = pickle.load(fp)
        DebugHelper.print(DebugType.TYPE_INFO, f"<{PLATFORMS_CACHE_FILENAME}> sucessfully loaded!", "PLATFORMS")
      except Exception as e: DebugHelper.print(DebugType.TYPE_ERROR, f"Error: {list(e.args)}", "EXCEPTION")

  
  def platformsCount(self) -> int:
    return len(self._platformsCache)
  
  
  def getRomsCount(self, platform_name: str) -> int:
    return len(self._platformsCache[platform_name])


  def getPlatformName(self, index: int) -> str:
    return list(self._platformsCache.keys())[index]
  

  def getRomName(self, platform_name: str, index: int) -> str:
    return list(self._platformsCache[platform_name].keys())[index]


  def getRom(self, platform_name: str, rom_name: str) -> dict:
    return self._platformsCache[platform_name][rom_name]
