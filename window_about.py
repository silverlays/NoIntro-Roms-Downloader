import PySimpleGUI as sg
import common_functions as common

class AboutWindow():
  def __init__(self, program_title: str, base64_icon: bytes):
    self.program_title = program_title
    self.base64_icon = base64_icon
    self.description = """If you like this product, consider visiting my social networks (links below)."""
  
  
  def show(self):
    self._create_window()
    
    while True:
      event, values = self.window.read()
      #print(event)

      if event == sg.WIN_CLOSED: break
      if str(event).startswith("HYPERLINK::"): common.open_hyperlink(self.window[event].metadata)

  
  def _create_window(self):
    links_layout = sg.Column([
      [
        sg.Column([
          [sg.Text("My YouTube:")],
          [sg.Text("My Twitch:")],
          [sg.Text("My Discord:")],
        ], element_justification="right"),
        sg.Column([
          [common.create_hyperlink("https://www.youtube.com/channel/UC9pLDlEx1XI0WNo-K23aH7A", "youtube", text_color="orange")],
          [common.create_hyperlink("https://www.twitch.tv/silv3r_ow", "twitch", text_color="orange")],
          [common.create_hyperlink("https://discord.gg/DHjzxMh", "discord", text_color="orange")],
        ])
      ]
    ], pad=(0, (20, 10)))
    
    window_layout = [
      [sg.Image(self.base64_icon), sg.Text(self.program_title, font=("", 24, "bold"), pad=((5, 0), 0))],
      [sg.Text(), sg.Text(self.description, font=("", 10, "italic"), pad=((10, 0), 0))],
      [links_layout]
    ]

    self.window = sg.Window("About...", window_layout, modal=True, disable_minimize=True, finalize=True)
    
    for element in self.window.AllKeysDict:
      if str(element).startswith("HYPERLINK"): self.window[element].set_cursor("hand2")
  

