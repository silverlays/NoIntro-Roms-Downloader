import PySimpleGUI as sg
import common_functions as common
import archive_games as games
from threading import Thread


class FullsetComparerToolWindow():
  def __init__(self, path: str, listbox_values: list):
    self.path = path
    self.listbox_values = listbox_values
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
      [common.create_modal_title("Fullset Comparer tool")],
      [sg.Multiline("", key="multiline_log", disabled=True, autoscroll=True, expand_x=True, expand_y=True)],
      [sg.Button("Close", expand_x=True, font=("", 10, "bold"), border_width=3, pad=(0, (10, 5)))]
    ]

    self.window = sg.Window("", window_layout, grab_anywhere=True, size=(600, 400), disable_close=True, disable_minimize=True, finalize=True)
    self.window['Close'].set_cursor("hand2")


  def _launch_task(self):
    def add_line(text: str):
      self.window['multiline_log'].update(f"{text}\n", append=True)
    
    import os

    local_game_list = ['{}.7z'.format(file[:file.rfind(".")]) for file in os.listdir(self.path)]
    nointro_list = self.listbox_values
    [add_line(n) for n in nointro_list if n not in local_game_list]
