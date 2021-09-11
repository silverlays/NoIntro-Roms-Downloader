import os
from urllib.parse import quote
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer, Tag


_base_url = "https://archive.org/download"
platform_games_buffer = []
games_found = []


def download_platform_data(platform_id: str) -> int:
  global platform_games_buffer
  platform_games_buffer, buffer_temp = ([], [])
  with urlopen(f"{_base_url}/{platform_id}") as response:
    dom = BeautifulSoup(response, features="html.parser", parse_only=SoupStrainer("a"))
  for query in dom.contents:
    query: Tag
    if query.text.find(".7z") != -1:
      buffer_temp.append(query.text)
  platform_games_buffer = buffer_temp


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


def download_file(patform_id: str, filename: str, output_folder: str):
  filename_quoted = quote(filename)
  urlretrieve(url=f"{_base_url}/{patform_id}/{filename_quoted}", filename=os.path.join(output_folder, filename))
