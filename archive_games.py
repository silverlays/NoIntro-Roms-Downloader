games_dict = {}


def create_games_dict(platform_games_dict: dict):
  global games_dict
  games_dict = {}
  for game_name in platform_games_dict:
    if platform_games_dict[game_name]['format'] != "Metadata" and platform_games_dict[game_name]['format'] != "Archive BitTorrent":
      games_dict[str(game_name).removeprefix("/")] = platform_games_dict[game_name]
  pass


def game_info(game_name: str) -> dict:
  return games_dict[game_name]


def games_names() -> list:
  return [game for game in games_dict]


def filter_games(keywords: str) -> list:
  filtered_list = []
  keywords = keywords.lower().split(" ")
  for game in games_dict:
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
          filtered_list.append(game)
          break
  return filtered_list


def games_count():
  return len(games_dict)
