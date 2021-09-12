import PySimpleGUI as sg
import time
import scrapper
from threading import Thread


__PROGRAM_VERSION__ = "1.0"
__PROGRAM_TITLE__ = f"NoIntro Roms Downloader v{__PROGRAM_VERSION__}"

APP_ICON_BASE64 = b"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAED0lEQVRIx61WvU5qSxSevz1s2BKwQkNhTKTkESwsLFQ6KUzUxGew8xF8AuNbGIilJRZGITGWaGJEiRYiDYTN/Jzig3Hc6Lnn3nNXocPsNev/W2tRxpgxhhDCObfWUkoJIbgRQhhjrLXGGCEE55wQQgjRWuOeUmqtJYTglbXWXTLGIIf6n3ELJv+Scz4ajYhHqVTKTIkQwhiDdEjDGdIganIlhIBQrTX5SsVisVKprKystNvtWq3W7XYTDIwxFwxjDOIxsRVCpZRxHLsHlNJUKrWxsVGtVkulUj6fX1paAs/j42O/32+1Wufn541Go9frzRoEsdT9Q3zX19ejKCqXy2tra6urq+TPyBhTq9Xq9frr62uz2ex2u5xzYwwcmoTIGCOlPD4+FkKoKWmt7ZRgCghpJ4QEQcAYo5QGQSCl5Jyfnp7e3t5yzuETpVQgMwji29sb0oBnsxnzma21SikYNxgMlFJBEOC5XzjEJTqTydi/psPDQ9QYwk4pFU6V1vry8nI0Gg2HwzAMs9kspVQp1ev1CCH5fD4IAq01Y6zf78dxHEVRFEWEkDiOPz4+tNaFQuH+/t4VutaaUkqcKmgql8vVanV5edl5WqlUtra2/KyWy+Xt7e1isZjgcVF1fxljBDhCFRUKhXa7ba09OTlJpVKc84ODA/i+t7cnhAiCYGFh4eHhwVpbr9fT6bQQYn9/Hzy7u7uUUiEEjIZM4VeIlNIYE8fx4uIigpbJZACOXC6nlEL/GI/HcRxLKQkhSqlcLgeefD5vrUUJudoTfpHANSnl3NwctGqtIWg8HrsaZYxJKRFlfPJ5XM/AWfhX7gMA4t/4OAAIEpfuJ766hyIBS1/5T/c4o6E63LnOmiCRMNxZ9y13wt7PhjOl7xXMuvkb6ZTSBKqdHz964DS7DjHL6lvnDIcmv6/MJkYklH/rZiIZfuhRab+JqnC2+4nC9PD1uQNgP0Hp9CZx8EMtMHpghUuyO+CNP+OMMTg7e90nINFFbzLYUW2A32ygx+MxRoez10HEHfB2tsNP5oEfryAI0um0P2PDMIRoKSUOYRiGYUgISafT4AmCAI6iS8P8L63Chb7T6VxdXUVRdHFxMRwOCSHNZrPT6Vhrb25u4PLT0xN4Go3GYDAghLRarefnZ2vt9fU1Mu8m5WToM8a01pzzUqmEqYR5CSZkNY5jhBU7EloeVKJ9YcC9vLz0ej1/6/kEZDab/fuJdnR0BH0OH18Wr83NTRRVYv36CRA+KrELNRqN9/d3B0CttUAZKKXOzs4KhYJSChvjP+LO3+Ncgc3Pz+/s7Nzd3QkhMBWEj/hiseiK9c89cOSWDB+wn4sf+f/IQX2yVUChW2n+VX/1QwROpZTvHE2g10X/vxnuZx5R+QW5F6NjoSC40gAAAABJRU5ErkJggg=="

PLATFORM_IDENTIFIERS = {
  "Atari 2600": "nointro.atari-2600",
  "Atari 5200": "nointro.atari-5200",
  "Atari 7800": "nointro.atari-7800",
  "Nintendo - e-Reader": "nointro.e-reader",
  "Nintendo - Family Computer Disk System": "nointro.fds",
  "Nintendo - Game Boy": "nointro.gb",
  "Nintendo - Game Boy Advance": "nointro.gba",
  "Nintendo - Game Boy Advance (Multiboot)": "nointro.gba-multiboot",
  "Nintendo - Game Boy Color": "nointro.gbc",
  "Nintendo - Nintendo 64": "nointro.n64",
  "Nintendo - Nintendo 64DD": "nointro.n64dd",
  "Nintendo - Nintendo Entertainment System": "nointro.nes",
  "Nintendo - Pokemon-Mini": "nointro.poke-mini",
  "Nintendo - Super Nintendo Entertainment System (Combined)": "nointro.snes",
  "Nintendo - Virtual Boy": "nointro.vb",
  "NEC - PC Engine - TurboGrafx 16": "nointro.tg-16",
  "Sega - 32X": "nointro.32x",
  "Sega - Game Gear": "nointro.gg",
  "Sega - Master System - Mark III": "nointro.ms-mkiii",
  "Sega - Mega Drive - Genesis": "nointro.md",
}


class MainWindow():
  def __init__(self):
      sg.theme("DarkGrey14")
      sg.set_global_icon(APP_ICON_BASE64)
      self.pb_fetch_value = 0
      self.pb_download_value = 0


  def show(self):
    self.window = self._create_window()
    self.window['input_search_game'].bind("<Return>", "::RETURN")
    self._switch_disabled_frame("all", True)

    while True:
      event, values = self.window.read()

      if event == sg.WIN_CLOSED: break
      if event == "combo_platform": self._combo_platform_changed(values['combo_platform'])
      if (event == "search_button" or event == "input_search_game::RETURN") and self.window['input_search_game'] != "": self._search_button_clicked(values['input_search_game'])
      if event == "select_button": self._select_button_clicked(values['combo_select_game'])
      if event == "output_folder": self._switch_disabled_frame("frame5", False)
      if event == "download_button": self._download_button_clicked(values['output_folder'])


  def _create_window(self):
    frame1_layout = [
      [sg.Combo(self.AvailablePlatforms, key="combo_platform", readonly=True, enable_events=True, expand_x=True)],
      [sg.Text("Platform:", pad=((5, 0), 5)), sg.Text("n/a", key="text_platform", pad=((0, 5), 5)), sg.ProgressBar(10, key="progress_bar_fetch", expand_x=True, size=(0, 15)), sg.Text("Games count:", pad=((5, 0), 5)), sg.Text("n/a", key="text_games_count", pad=((0, 5), 5), justification="right")]
    ]

    frame2_layout = [
      [sg.Input(key="input_search_game", expand_x=True), sg.Button("Search", key="search_button")],
      [sg.Text("Games found:", pad=((5, 0), 5)), sg.Text("n/a", key="text_search_game", pad=((0, 5), 5))]
    ]

    frame3_layout = [
      [sg.Combo([], key="combo_select_game", readonly=True, expand_x=True), sg.Button("Select", key="select_button")],
      [sg.Text("Selected game:", pad=((5, 0), 5)), sg.Text("n/a", key="text_select_game", pad=((0, 5), 5))]
    ]

    frame4_layout = [
      [sg.Input(key="output_folder", expand_x=True, enable_events=True), sg.FolderBrowse(key="browse_button")]
    ]

    frame5_layout = [
      [sg.Button("DOWNLOAD", key="download_button", expand_x=True)]
    ]

    layout = [
      [sg.Frame("1. Select the platform", frame1_layout, key="frame1", expand_x=True)],
      [sg.Frame("2. Search game(s) by keywords", frame2_layout, key="frame2", expand_x=True)],
      [sg.Frame("3. Select game", frame3_layout, key="frame3", expand_x=True)],
      [sg.Frame("4. Select output folder", frame4_layout, key="frame4", expand_x=True)],
      [sg.Frame("5. Download game", frame5_layout, key="frame5", expand_x=True)],
      [sg.ProgressBar(10, key="progress_bar_download", size=(0, 15), expand_x=True)]
    ]

    return sg.Window(__PROGRAM_TITLE__, layout, finalize=True)


  def _combo_platform_changed(self, value: str):
    self._reset_values()
    platform_id = PLATFORM_IDENTIFIERS[value]
    self.window['text_platform'].update(platform_id)
    thread = Thread(target=scrapper.download_platform_data, args=(platform_id,), daemon=True)
    thread.start()
    while thread.is_alive():
      self._update_progress_bar(self.window['progress_bar_fetch'], self.pb_fetch_value)
      time.sleep(0.5)
    self._update_progress_bar(self.window['progress_bar_fetch'], self.pb_fetch_value, finished=True)
    self.window['text_games_count'].update(len(scrapper.platform_games_buffer))
    self._switch_disabled_frame("frame2", False)


  def _search_button_clicked(self, value: str):
    games_count = scrapper.search_game(value)
    self.window['text_search_game'].update(games_count)
    self._switch_disabled_frame("frame3", False)
    self.window['combo_select_game'].update(values=[game for game in scrapper.games_found])


  def _select_button_clicked(self, value: str):
    self.window['text_select_game'].update(value)
    self._switch_disabled_frame("frame4", False)


  def _download_button_clicked(self, value: str):
    thread = Thread(target=scrapper.download_file, args=(self.window['text_platform'].DisplayText, self.window['text_select_game'].DisplayText, value,))
    thread.start()
    while thread.is_alive():
      self._update_progress_bar(self.window['progress_bar_download'], self.pb_download_value)
      time.sleep(0.5)
    self._update_progress_bar(self.window['progress_bar_download'], self.pb_download_value, finished=True)


  def _update_progress_bar(self, pb: sg.ProgressBar, current_value: int, finished=False):
    if finished: current_value = pb.MaxValue
    else:
      if current_value < pb.MaxValue: current_value+=1
      else: current_value = 0
    pb.update(current_value)


  def _reset_values(self):
    self._switch_disabled_frame("all", True)
    self.window['text_platform'].update("n/a")
    self.window['progress_bar_fetch'].update(0)
    self.window['text_games_count'].update("n/a")
    self.window['input_search_game'].update("")
    self.window['text_search_game'].update("n/a")
    self.window['combo_select_game'].update([])
    self.window['text_select_game'].update("n/a")
    self.window['progress_bar_download'].update(0)
    self.window['output_folder'].update("")


  def _switch_disabled_frame(self, frame: str, make_disabled: bool):
    if frame == "frame2" or frame == "all":
      self.window['input_search_game'].update(disabled=make_disabled)
      self.window['search_button'].update(disabled=make_disabled)
    if frame == "frame3" or frame == "all":
      self.window['combo_select_game'].update(disabled=make_disabled)
      self.window['select_button'].update(disabled=make_disabled)
    if frame == "frame4" or frame == "all":
      self.window['output_folder'].update(disabled=make_disabled)
      self.window['browse_button'].update(disabled=make_disabled)
    if frame == "frame5" or frame == "all":
      self.window['download_button'].update(disabled=make_disabled)


  @property
  def AvailablePlatforms(self):
    return [platform for platform in PLATFORM_IDENTIFIERS]
