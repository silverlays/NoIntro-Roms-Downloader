import PySimpleGUI as sg
import common_functions as common
import archive_games as games
from threading import Thread


class FileHashCheckerToolWindow():
  def __init__(self, path: str):
    self.path = path
    self.abort = False
    self.thread: Thread = None


  def show(self):
    self._create_window()
    self.window.read(100)
    self.thread = Thread(target=self._launch_task)
    self.thread.start()
    
    while True:
      event, values = self.window.read()

      if event == "Close":
        self.window.close()
        break


  def _create_window(self):
    window_layout = [
      [common.create_modal_title("File checker tool")],
      [sg.Multiline("", key="multiline_log", disabled=True, autoscroll=True, expand_x=True, expand_y=True)],
      [sg.Button("Close", expand_x=True, font=("", 10, "bold"), border_width=3, pad=(0, (10, 5)))]
    ]

    self.window = sg.Window("", window_layout, grab_anywhere=True, size=(600, 400), disable_close=True, disable_minimize=True, finalize=True)
    self.window['Close'].set_cursor("hand2")


  def _launch_task(self):
    def add_line(text: str):
      self.window['multiline_log'].update(f"{text}\n", append=True)
    
    import os, fnmatch, hashlib
    format = list(games.games_dict.values())[0]['format']

    for file in fnmatch.filter(os.listdir(self.path), f"*.{format}"):
      try:
        with open(file, "rb") as stream: local_file_md5 = hashlib.md5(stream.read(-1)).hexdigest()
        add_line("".join("-" for _ in range(100)))
        add_line(f"Filename: {file}")
        add_line(f"File Hash (md5): {local_file_md5}")
        found = False
        for game in games.games_dict:
          if games.games_dict[game]['md5'] == local_file_md5:
            add_line(f"Status: Found ({game})")
            found = True
            break
        if not found: add_line(f"Status: Not found")
      except OSError as error: add_line(f"{file} cannot be opened. ({error.strerror})")
