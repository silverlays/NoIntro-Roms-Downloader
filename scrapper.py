import PySimpleGUI as sg
import os
import math
import json
from http.client import HTTPResponse
from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import HTTPError


_base_url = "https://archive.org/download"
platforms_list = {}
platform_details = {}
games_found = {}


def download_platforms() -> dict:
  global platforms_list
  json_url = "https://archive.org/advancedsearch.php?q=identifier%3Anointro.*&fl%5B%5D=identifier&fl%5B%5D=title&sort%5B%5D=titleSorter+asc&sort%5B%5D=&sort%5B%5D=&rows=2000&page=1&output=json"
  request: HTTPResponse = urlopen(json_url)
  json_data = json.load(request)
  for platform in json_data['response']['docs']:
    platform['title'] = str(platform['title'])[0:str(platform['title']).find(' (')].removeprefix("[No-Intro] ")
    platforms_list[platform['title']] = platform['identifier']
  return platforms_list


def download_platform_details(platform_id: str) -> dict:
  global platform_details
  json_url = f"https://archive.org/details/{platform_id}&output=json"
  request: HTTPResponse = urlopen(json_url)
  platform_details = json.load(request)
  return platform_details


def get_platform_games_count() -> int:
  if platform_details != {}: return int(platform_details['item']['files_count'] - 4)
  else: raise Exception("No platform in memory! Scrap first.")


def search_game(keywords: str) -> int:
  global games_found
  games_found = {}
  keywords = keywords.lower().split(" ")
  for game in platform_details['files']:
    game: str
    game_lowered = game.lower()

    for k in keywords:
      found = True
      if game_lowered.find(k) != -1:
        for kk in keywords:
          if game_lowered.find(kk) == -1:
            found = False
            break
        if found and platform_details['files'][game]['format'] != "Metadata" and platform_details['files'][game]['format'] != "Archive BitTorrent":
          game_name_cleaned = game.removeprefix('/')
          game_infos = {
            "format": platform_details['files'][game]['format'],
            "size": platform_details['files'][game]['size']
          }
          games_found[game_name_cleaned] = game_infos
          break
  return len(games_found)


def download_file(platform_id: str, filename: str, output_folder: str, cb_progressbar: sg.ProgressBar, cb_text_status: sg.Text, cb_function):
  filename_quoted = quote(filename)
  full_url = f"{_base_url}/{platform_id}/{filename_quoted}"
  output_stream = open(file=os.path.join(output_folder, filename), mode="wb")
  file_request: HTTPResponse = urlopen(full_url)
  file_length = file_request.length
  buffer_length = int(file_length / 10)
  position = 0
  
  while True:
    bytes_read = file_request.read(buffer_length)
    output_stream.write(bytes_read)
    output_stream.flush()
    position += len(bytes_read)
    cb_progressbar.update(position, file_length)
    cb_text_status.update(f"{length_to_unit_string(position)} / {length_to_unit_string(file_length)}")
    if len(bytes_read) < buffer_length: break
  
  file_request.close()
  output_stream.close()
  while not file_request.closed and not output_stream.closed: pass

  cb_function()


def get_file_length(filename: str) -> float:
  return float(games_found[filename]['size'])


def length_to_unit_string(length: float) -> str:
  unit = "b"
  one_kilobytes = math.pow(1024, 1)
  one_megabytes = math.pow(1024, 2)
  one_gigabytes = math.pow(1024, 3)

  if length > one_kilobytes and length < one_megabytes:
    length /= one_kilobytes
    unit = "Kb"
  if length > one_megabytes and length < one_gigabytes:
    length /= one_megabytes
    unit = "Mb"
  if length > one_gigabytes:
    length /= one_gigabytes
    unit = "Gb"
  
  return "{:.1f}{}".format(length, unit)
