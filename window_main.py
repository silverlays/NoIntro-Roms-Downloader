import os
import threading
import PySimpleGUI as sg
import archive_platforms as platforms
import archive_games as games
import archive_download as download
from window_game_info  import WindowGameInfo


__PROGRAM_VERSION__ = "1.2"
__PROGRAM_TITLE__ = f"NoIntro Roms Downloader v{__PROGRAM_VERSION__}"

APP_ICON_BASE64 = b"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAED0lEQVRIx61WvU5qSxSevz1s2BKwQkNhTKTkESwsLFQ6KUzUxGew8xF8AuNbGIilJRZGITGWaGJEiRYiDYTN/Jzig3Hc6Lnn3nNXocPsNev/W2tRxpgxhhDCObfWUkoJIbgRQhhjrLXGGCEE55wQQgjRWuOeUmqtJYTglbXWXTLGIIf6n3ELJv+Scz4ajYhHqVTKTIkQwhiDdEjDGdIganIlhIBQrTX5SsVisVKprKystNvtWq3W7XYTDIwxFwxjDOIxsRVCpZRxHLsHlNJUKrWxsVGtVkulUj6fX1paAs/j42O/32+1Wufn541Go9frzRoEsdT9Q3zX19ejKCqXy2tra6urq+TPyBhTq9Xq9frr62uz2ex2u5xzYwwcmoTIGCOlPD4+FkKoKWmt7ZRgCghpJ4QEQcAYo5QGQSCl5Jyfnp7e3t5yzuETpVQgMwji29sb0oBnsxnzma21SikYNxgMlFJBEOC5XzjEJTqTydi/psPDQ9QYwk4pFU6V1vry8nI0Gg2HwzAMs9kspVQp1ev1CCH5fD4IAq01Y6zf78dxHEVRFEWEkDiOPz4+tNaFQuH+/t4VutaaUkqcKmgql8vVanV5edl5WqlUtra2/KyWy+Xt7e1isZjgcVF1fxljBDhCFRUKhXa7ba09OTlJpVKc84ODA/i+t7cnhAiCYGFh4eHhwVpbr9fT6bQQYn9/Hzy7u7uUUiEEjIZM4VeIlNIYE8fx4uIigpbJZACOXC6nlEL/GI/HcRxLKQkhSqlcLgeefD5vrUUJudoTfpHANSnl3NwctGqtIWg8HrsaZYxJKRFlfPJ5XM/AWfhX7gMA4t/4OAAIEpfuJ766hyIBS1/5T/c4o6E63LnOmiCRMNxZ9y13wt7PhjOl7xXMuvkb6ZTSBKqdHz964DS7DjHL6lvnDIcmv6/MJkYklH/rZiIZfuhRab+JqnC2+4nC9PD1uQNgP0Hp9CZx8EMtMHpghUuyO+CNP+OMMTg7e90nINFFbzLYUW2A32ygx+MxRoez10HEHfB2tsNP5oEfryAI0um0P2PDMIRoKSUOYRiGYUgISafT4AmCAI6iS8P8L63Chb7T6VxdXUVRdHFxMRwOCSHNZrPT6Vhrb25u4PLT0xN4Go3GYDAghLRarefnZ2vt9fU1Mu8m5WToM8a01pzzUqmEqYR5CSZkNY5jhBU7EloeVKJ9YcC9vLz0ej1/6/kEZDab/fuJdnR0BH0OH18Wr83NTRRVYv36CRA+KrELNRqN9/d3B0CttUAZKKXOzs4KhYJSChvjP+LO3+Ncgc3Pz+/s7Nzd3QkhMBWEj/hiseiK9c89cOSWDB+wn4sf+f/IQX2yVUChW2n+VX/1QwROpZTvHE2g10X/vxnuZx5R+QW5F6NjoSC40gAAAABJRU5ErkJggg=="


class WindowMain():
  def __init__(self):
    sg.set_global_icon(APP_ICON_BASE64)
    self.unzip = False
    self.thread: threading.Thread = None
  

  def show(self):
    self._create_window()

    while True:
      event, values = self.window.read()
      #print(event)
      #print(values)

      if event == sg.WIN_CLOSED: break
      if event == "combo_platforms": self._combo_platforms_clicked(values['combo_platforms'])
      if event == "listbox_games": self._listbox_games_select_changed(values['listbox_games'])
      if event == "listbox_games::DBLCLICK" and len(values['listbox_games']) > 0: self._listbox_games_double_click(values['listbox_games'][0])
      if event == "input_filter::RETURN": self._input_filter_returned(values['input_filter'])
      if event == "button_region_europe":
        self.window['input_filter'].update("Europe")
        self._input_filter_returned("Europe")
      if event == "button_region_usa":
        self.window['input_filter'].update("USA")
        self._input_filter_returned("USA")
      if event == "button_region_japan":
        self.window['input_filter'].update("Japan")
        self._input_filter_returned("Japan")
      if event == "button_clear": self._button_clear_pressed()
      if event == "input_output_folder": self.window['button_browse'].initialFolder = values['input_output_folder']
      if event == "checkbox_unzip": self.unzip = values['checkbox_unzip']
      if event == "button_download": self._button_download_pressed(values['listbox_games'], values['input_output_folder'])

    sg.popup_no_titlebar("CLOSING, PLEASE WAIT...", font=("", 24, "bold"), grab_anywhere=False, non_blocking=True, button_type=sg.POPUP_BUTTONS_NO_BUTTONS)
    if self.thread and self.thread.is_alive():
      download.abort_thread = True
      self.window.read(100)
      self.thread.join()


  def _create_window(self):
    column_download_layout = sg.Column(
      [
        [sg.HorizontalSeparator()],
        [sg.Text("Download progress", expand_x=True, justification="center", pad=(5, 0))],
        [sg.ProgressBar(10, key="progressbar_download", size=(0, 20), expand_x=True)],
        [sg.Text("0Kb / 0Kb", key="text_download", expand_x=True, justification="center", pad=(5, 0))],
        [sg.HorizontalSeparator()]
      ], key="column_download", expand_x=True, visible=False)

    frame_layout = [
      [sg.Column(
        [
          [
            sg.Text("Platform", pad=((0,5), 0)),
            sg.Combo([platform for platform in platforms.platforms_dict], key="combo_platforms", enable_events=True, readonly=True, expand_x=True, pad=0)
          ]
        ], expand_x=True, pad=(5, 0))
      ],
      [sg.HorizontalSeparator()],
      [sg.Listbox([], key="listbox_games", expand_x=True, expand_y=True, enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED, font=("", 10, "bold"), text_color="#008040")],
      [sg.Column(
        [
          [
            sg.Text("Total", pad=0),
            sg.Text("n/a", key="text_total", font=("", 10, "bold"), text_color="#80ff80", pad=0)
          ]
        ], pad=(5, 0)),
      sg.Column(
        [
          [
            sg.Text("Selected", pad=0),
            sg.Text("0", key="text_selected", font=("", 10, "bold"), text_color="#80ff80", pad=0)
          ]
        ], expand_x=True, element_justification="center", pad=(5, 0)),
      sg.Column(
        [
          [
            sg.Text("Filtered", pad=0),
            sg.Text("n/a", key="text_filtered", font=("", 10, "bold"), text_color="#80ff80", pad=0)
          ]
        ], pad=(5, 0))
      ],
      [sg.HorizontalSeparator()],
      [sg.Column(
        [
          [sg.Text("Region")],
          [sg.Text("Filter")]
        ], element_justification="right", vertical_alignment="bottom",pad=0),
        sg.Column(
        [
          [
            sg.Button("Europe", key="button_region_europe", expand_x=True),
            sg.Button("USA", key="button_region_usa", expand_x=True),
            sg.Button("Japan", key="button_region_japan", expand_x=True)
          ],
          [sg.Input(key="input_filter", expand_x=True)]
        ], expand_x=True, pad=0),
        sg.Column(
        [
          [sg.Button("Clear", key="button_clear", pad=((0, 5), 0), expand_y=True)],
        ], vertical_alignment="bottom", pad=0)
      ],
      [sg.HorizontalSeparator()],
      [sg.Column(
        [
          [
            sg.Text("Output folder", pad=((0,5), 0)),
            sg.Input(os.getcwd(), key="input_output_folder", enable_events=True, readonly=True, expand_x=True, pad=0),
            sg.FolderBrowse(key="button_browse")
          ]
        ], expand_x=True, pad=(5, 0))
      ],
      [sg.Column(
        [
          [
            sg.Text("Options:", pad=((0,5), 0)),
            sg.Checkbox("Unzip?", key="checkbox_unzip", enable_events=True, pad=0)
          ]
        ], expand_x=True, pad=(5, 0))
      ],
      [sg.HorizontalSeparator()],
      [sg.Button("Download", key="button_download", expand_x=True)],
      [sg.pin(column_download_layout, expand_x=True)],
      [sg.StatusBar("Ready!", key="statusbar_status", font=("", 10, "bold italic"), justification="center", relief=sg.RELIEF_SUNKEN, expand_x=True, auto_size_text=False)]
    ]

    self.window = sg.Window(__PROGRAM_TITLE__, frame_layout, size=(600, 800), finalize=True, resizable=True)
    self.window.set_min_size(self.window.size)
    self.window['button_download'].set_cursor("hand2")
    self.window['button_clear'].set_cursor("hand2")
    self.window['button_browse'].set_cursor("hand2")
    self.window['input_filter'].bind("<Return>", "::RETURN")
    self.window['listbox_games'].bind("<Double-Button-1>", "::DBLCLICK")


  def _combo_platforms_clicked(self, platform_name: str):
    self.window.set_cursor("watch")
    self.window.read(0)
    self.platform_id = platforms.platforms_dict[platform_name]
    games.create_games_dict(platforms.download_platform_details(self.platform_id)['files'])
    self.window.set_cursor("arrow")
    self.window['listbox_games'].update(games.games_names())
    self.window['text_total'].update(games.games_count())
    self.window['text_filtered'].update(games.games_count())
    self.window['text_selected'].update(0)
    self.window['input_filter'].update("")


  def _listbox_games_select_changed(self, listbox_selection: list):
    self.window['text_selected'].update(len(listbox_selection))


  def _listbox_games_double_click(self, selected_game: str):
    WindowGameInfo(selected_game).show()


  def _input_filter_returned(self, input_keywords: str):
    filtered = games.filter_games(input_keywords)
    self.window['listbox_games'].update(filtered)
    self.window['text_selected'].update(0)
    self.window['text_filtered'].update(len(filtered))


  def _button_clear_pressed(self):
    self.window['input_filter'].update("")
    self._input_filter_returned("")


  def _button_download_pressed(self, selected_games: list, output_folder: str):
    self.window['column_download'].update(visible=True)
    self.thread =threading.Thread(target=download.download_files, args=(
      self.platform_id,
      selected_games,
      output_folder,
      self.unzip,
      self.window['progressbar_download'],
      self.window['statusbar_status'],
      self.window['text_download'],
      self._download_callback,))
    self.thread.start()


  def _download_callback(self, count: int, max: int, failed: int):
    self.window['statusbar_status'].update(f"Download completed! ({count}/{max} successful, {failed} failed)")
    self.window['column_download'].update(visible=False)
