import asyncio
from asyncio.streams import StreamReader, StreamWriter
from http.client import HTTPResponse
import PySimpleGUI as sg
import os
import math
from urllib.request import urlopen, urlretrieve
from urllib.parse import quote
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer, Tag


_base_url = "https://archive.org/download"
platform_games_buffer = []
games_found = []


def download_platform_data(platform_id: str, cb_progressbar: sg.ProgressBar, cb_function):
  global platform_games_buffer
  dom: BeautifulSoup = None
  internaL_count = 0
  internal_max = 100

  def update():
    nonlocal internaL_count
    internaL_count += 33
    cb_progressbar.update(internaL_count, internal_max)

  with urlopen(f"{_base_url}/{platform_id}") as response:
    update()
    dom = BeautifulSoup(response, features="html.parser", parse_only=SoupStrainer("a"))
    update()

  for query in dom.contents:
    query: Tag
    if query.text.find(".7z") != -1: platform_games_buffer.append(query.text)

  update()
  cb_function()


def search_game(keywords: str) -> int:
  global games_found
  games_found = []
  keywords = keywords.lower().split(" ")
  for game in platform_games_buffer:
    game: str
    game_lowered = game.lower()

    for k in keywords:
      found = True
      if game_lowered.find(k) != -1:
        for kk in keywords:
          if game_lowered.find(kk) == -1:
            found = False
            break
        if found:
          games_found.append(game)
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


def get_file_length(platform_id: str, filename: str) -> float:
  filename_quoted = quote(filename)
  full_url = f"{_base_url}/{platform_id}/{filename_quoted}"

  try:
    with urlopen(url=full_url, timeout=2) as response: return float(response.length)
  except HTTPError: return float(0)


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
