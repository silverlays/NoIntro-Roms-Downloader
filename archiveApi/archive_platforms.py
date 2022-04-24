import time
import json
from http.client import HTTPResponse
from urllib.request import urlopen


base_url = "https://archive.org"
_json_platforms_url = f"{base_url}/advancedsearch.php?q=identifier%3Anointro.*&fl%5B%5D=identifier&fl%5B%5D=title&sort%5B%5D=titleSorter+asc&sort%5B%5D=&sort%5B%5D=&rows=2000&page=1&output=json"


class Platform():
  platform_id: str = ''
  platform_name: str = ''
  platform_updated: str = ''
  roms_data = []

  def __init__(self, id: str, name: str, updated: str) -> None:
    self.platform_id = id
    self.platform_name = name
    self.platform_updated = updated


def download_platforms() -> list:
  platforms_list = []
  platforms_request: HTTPResponse = urlopen(_json_platforms_url)
  for platform in json.load(platforms_request)['response']['docs']:
    try:
      platform_updated_time = platform['title'][(str(platform['title']).rfind("(")+1):-1]
      platform_updated_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(platform_updated_time, "%Y%m%d-%H%M%S"))

      platforms_list.append({
        'id': platform['identifier'],
        'name': str(platform['title'])[0:str(platform['title']).rfind(' (')].removeprefix("[No-Intro] "),
        'updated': platform_updated_time
      })
    except: pass
  return platforms_list

def download_platform_files(platform_id: str) -> list:
  roms_data = []
  json_url = f"{base_url}/details/{platform_id}&output=json"
  request: HTTPResponse = urlopen(json_url)
  platform_files: dict = json.load(request)['files']
  
  for file in platform_files.items():
    rom_name: str = file[0]
    rom_details: dict = file[1]

    if rom_name.rfind('.xml') == -1 and rom_name.rfind('.sqlite') == -1 and rom_name.rfind('.torrent') == -1:
      roms_data.append({
        'name': rom_name[1:].rstrip(f'.{rom_details["format"]}'),
        'format': rom_details['format'],
        'size': int(rom_details['size']),
        'md5': rom_details['md5'],
        'crc32': rom_details['crc32'],
        'sha1': rom_details['sha1'],
      })
  
  return roms_data
