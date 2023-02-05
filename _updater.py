import requests

# Helpers
from _constants import *
from _debug import *


class UpdaterHelper():
  LASTEST_MAJOR = VERSION_MAJOR
  LASTEST_MINOR = VERSION_MINOR
  LASTEST_REVISION = VERSION_REVISION
  

  def __init__(self) -> None:
    try:
      self.last_release_version: str = requests.get('https://api.github.com/repos/silverlays/NoIntro-Roms-Downloader/releases').json()[0]['name']
      self.last_release_version = self.last_release_version.removeprefix('v').split('.')
      
      self.LASTEST_MAJOR = int(self.last_release_version[0])
      self.LASTEST_MINOR = int(self.last_release_version[1][0:1]) # TO BE MODIFIED WHEN v1.3a WILL BE GONE
      self.LASTEST_REVISION = 0 # THIS ONE TOO...
    except Exception as e:
      DebugHelper.print(DebugType.TYPE_ERROR, list(e.args), "EXCEPTION")


  def updateAvailable(self) -> bool:
    if VERSION_MAJOR < self.LASTEST_MAJOR:
      DebugHelper.print(DebugType.TYPE_INFO, "Update available!", "UPDATER")
      return True
    elif (VERSION_MINOR < self.LASTEST_MINOR) and (VERSION_MAJOR == self.LASTEST_MAJOR):
      DebugHelper.print(DebugType.TYPE_INFO, "Update available!", "UPDATER")
      return True
    else:
      DebugHelper.print(DebugType.TYPE_INFO, "You have the lastest version.", "UPDATER")
      return False


  def currentVersionString(self) -> str:
    return f"v{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_REVISION}"
  
  def lastestVersionString(self) -> str:
    return f"v{self.LASTEST_MAJOR}.{self.LASTEST_MINOR}.{self.LASTEST_REVISION}"