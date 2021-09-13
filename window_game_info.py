import PySimpleGUI as sg
import archive_games as games
import common_functions as common


class WindowGameInfo():
  def __init__(self, filename: str):
    self.game_filename = filename
    self.game_format = games.game_info(filename)['format']
    self.game_name = filename[:-(len(self.game_format)+1)]
    self.game_size = float(games.game_info(filename)['size'])
    self.game_md5 = str(games.game_info(filename)['md5']).upper()
    self.game_crc32 = str(games.game_info(filename)['crc32']).upper()
    self.game_sha1 = str(games.game_info(filename)['sha1']).upper()


  def show(self):
    self._create_window()

    while True:
      event, values = self.window.read()
      if event == sg.WIN_CLOSED or event == "button_close": break

    self.window.close()


  def _create_window(self):
    col1 = [
      [sg.Text("FILENAME", font=("", 10, "bold"), relief=sg.RELIEF_RIDGE, pad=(0,5), expand_x=True, justification="center")],
      [sg.Text("FORMAT", font=("", 10, "bold"), relief=sg.RELIEF_RIDGE, pad=(0,5), expand_x=True, justification="center")],
      [sg.Text("SIZE", font=("", 10, "bold"), relief=sg.RELIEF_RIDGE, pad=(0,5), expand_x=True, justification="center")],
      [sg.Text("MD5", font=("", 10, "bold"), relief=sg.RELIEF_RIDGE, pad=(0,5), expand_x=True, justification="center")],
      [sg.Text("CRC32", font=("", 10, "bold"), relief=sg.RELIEF_RIDGE, pad=(0,5), expand_x=True, justification="center")],
      [sg.Text("SHA1", font=("", 10, "bold"), relief=sg.RELIEF_RIDGE, pad=(0,5), expand_x=True, justification="center")]
    ]
    col2 = [
      [sg.Text(self.game_filename, key="input_filename", pad=(0,5), expand_x=True, relief=sg.RELIEF_SUNKEN)],
      [sg.Text(self.game_format, key="input_format", pad=(0,5), expand_x=True, relief=sg.RELIEF_SUNKEN)],
      [sg.Text(common.length_to_unit_string(self.game_size), key="input_size", pad=(0,5), expand_x=True, relief=sg.RELIEF_SUNKEN)],
      [sg.Text(self.game_md5, key="input_md5", pad=(0,5), expand_x=True, relief=sg.RELIEF_SUNKEN)],
      [sg.Text(self.game_crc32, key="input_crc32", pad=(0,5), expand_x=True, relief=sg.RELIEF_SUNKEN)],
      [sg.Text(self.game_sha1, key="input_sha1", pad=(0,5), expand_x=True, relief=sg.RELIEF_SUNKEN)]
    ]
    file_details_frame_layout = [
      [sg.Column(col1), sg.Column(col2, expand_x=True, pad=((0, 5), 0))]
    ]
    layout = [
      [sg.Text(self.game_name, key="text_game_title", font=("", 24, "bold italic"), expand_x=True, justification="center")],
      [sg.Frame("File details", file_details_frame_layout, relief=sg.RELIEF_RAISED, border_width=2, expand_x=True)],
      [sg.Button("CLOSE", key="button_close", expand_x=True, font=("", 10, "bold"))]
    ]

    self.window = sg.Window(f"{self.game_name} - Details", layout, modal=True, finalize=True)
    self.window['button_close'].set_cursor("hand2")