import PySimpleGUI as sg
import time
import platforms
import scrapper
from threading import Thread


__PROGRAM_VERSION__ = "1.0"
__PROGRAM_TITLE__ = f"NoIntro Roms Downloader v{__PROGRAM_VERSION__}"


class MainWindow():
  def __init__(self):
      sg.theme("DarkGrey14")
      self.pb_fetch_value = 0
      self.pb_download_value = 0

  def show(self):
    self.window = self._create_window()
    #self.window['input_search_game'].bind("<Return>", lambda: self.window['search_button'].click())
    self.window['input_search_game'].bind("<Return>", "::RETURN")
    self._disable_frame("all")

    while True:
      event, values = self.window.read()
      #print(event)
      #print(values)

      if event == sg.WIN_CLOSED: break
      
      if event == "combo_platform":
        self._disable_frame("all")

        platform_id = platforms.PLATFORM_IDENTIFIERS[values['combo_platform']]
        self.window['text_platform'].update(platform_id)
        thread = Thread(target=scrapper.download_platform_data, args=(platform_id,), daemon=True)
        thread.start()
        while thread.is_alive():
          self._update_progress_bar(self.window['progress_bar_fetch'])
          time.sleep(0.5)
        self._update_progress_bar(self.window['progress_bar_fetch'], finished=True)
        self.window['text_games_count'].update(len(scrapper.platform_games_buffer))
        self._enable_frame("frame2")
      
      if (event == "search_button" or event == "input_search_game::RETURN") and self.window['input_search_game'] != "":
        games_count = scrapper.search_game(values['input_search_game'])
        self.window['text_search_game'].update(games_count)
        self._enable_frame("frame3")
        self.window['combo_select_game'].update(values=[game for game in scrapper.games_found])
      
      if event == "select_button":
        self.window['text_select_game'].update(values['combo_select_game'])
        self._enable_frame("frame4")
      
      if event == "output_folder":
        self._enable_frame("frame5")
      
      if event == "download_button":
        thread = Thread(target=scrapper.download_file, args=(self.window['text_platform'].DisplayText, self.window['text_select_game'].DisplayText, values['output_folder'],))
        thread.start()
        while thread.is_alive():
          self._update_progress_bar(self.window['progress_bar_download'])
          time.sleep(0.5)
        self._update_progress_bar(self.window['progress_bar_download'], finished=True)


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
  

  def _update_progress_bar(self, pb: sg.ProgressBar, finished=False):
    if pb.Key == "progress_bar_fetch":
      if finished: self.pb_fetch_value = pb.MaxValue
      else:
        if self.pb_fetch_value < pb.MaxValue: self.pb_fetch_value+=1
        else: self.pb_fetch_value = 0
      pb.update(self.pb_fetch_value)
    elif pb.Key == "progress_bar_download":
      if finished: self.pb_download_value = pb.MaxValue
      else:
        if self.pb_download_value < pb.MaxValue: self.pb_download_value+=1
        else: self.pb_download_value = 0
      pb.update(self.pb_download_value)

  
  def _disable_frame(self, frame: str):
    if frame == "frame2" or frame == "all":
      self.window['input_search_game'].update(disabled=True)
      self.window['search_button'].update(disabled=True)
    if frame == "frame3" or frame == "all":
      self.window['combo_select_game'].update(disabled=True)
      self.window['select_button'].update(disabled=True)
    if frame == "frame4" or frame == "all":
      self.window['output_folder'].update(disabled=True)
      self.window['browse_button'].update(disabled=True)
    if frame == "frame5" or frame == "all":
      self.window['download_button'].update(disabled=True)      
      
  
  def _enable_frame(self, frame: str):
    if frame == "frame2" or frame == "all":
      self.window['input_search_game'].update(disabled=False)
      self.window['search_button'].update(disabled=False)
    if frame == "frame3" or frame == "all":
      self.window['combo_select_game'].update(disabled=False)
      self.window['select_button'].update(disabled=False)
    if frame == "frame4" or frame == "all":
      self.window['output_folder'].update(disabled=False)
      self.window['browse_button'].update(disabled=False)
    if frame == "frame5" or frame == "all":
      self.window['download_button'].update(disabled=False)


  @property
  def AvailablePlatforms(self):
    list = []
    for platform in platforms.PLATFORM_IDENTIFIERS:
      list.append(platform)
    return list