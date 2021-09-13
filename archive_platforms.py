import json
from http.client import HTTPResponse
from urllib.request import urlopen


platforms_dict = {}
platform_details_dict = {}

_base_url = "https://archive.org"
_json_platforms_url = f"{_base_url}/advancedsearch.php?q=identifier%3Anointro.*&fl%5B%5D=identifier&fl%5B%5D=title&sort%5B%5D=titleSorter+asc&sort%5B%5D=&sort%5B%5D=&rows=2000&page=1&output=json"


_platforms_request: HTTPResponse = urlopen(_json_platforms_url)
for platform in json.load(_platforms_request)['response']['docs']:
  platform['title'] = str(platform['title'])[0:str(platform['title']).find(' (')].removeprefix("[No-Intro] ")
  platforms_dict[platform['title']] = platform['identifier']


def download_platform_details(platform_id: str) -> dict:
  import json
  from http.client import HTTPResponse
  from urllib.request import urlopen
  json_url = f"{_base_url}/details/{platform_id}&output=json"
  request: HTTPResponse = urlopen(json_url)
  platform_details = json.load(request)
  return platform_details


def get_platform_games_count() -> int:
  if platform_details_dict != {}: return int(platform_details_dict['item']['files_count'] - 4)
  else: raise Exception("No platform in memory! Scrap first.")
