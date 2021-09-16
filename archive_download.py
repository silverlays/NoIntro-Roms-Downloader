import os
import time
import py7zr
import PySimpleGUI as sg
import common_functions as common
import archive_games as games
from urllib.parse import quote
from urllib.request import urlretrieve
from http.client import HTTPResponse


_base_url = "https://archive.org"
abort_thread = False

def download_files(platform_id: str, filenames: list, output_folder: str, unzip: bool, cb_progressbar: sg.ProgressBar, cb_statusbar: sg.StatusBar, cb_text_status: sg.Text, cb_function):
  def download(filename: str):
    filename_quoted = quote(filename)
    full_url = f"{_base_url}/download/{platform_id}/{filename_quoted}"
    urlretrieve(url=full_url, filename=os.path.join(output_folder, filename))
    
  global abort_thread
  failed = 0
  count = 1
  max = len(filenames)
  downloaded_size = float(0)
  total_size = float(0)
  for filename in filenames: total_size += float(games.game_info(filename)['size'])
  cb_progressbar.update(0, max)
  cb_text_status.update(f"0% (0Kb / {common.length_to_unit_string(total_size)})")
  
  for filename in filenames:
    if not abort_thread:
      str_counter = f"({count}/{max} failed:{failed})"
      tronqued_filename = f"{filename[:40]}{'...' if len(filename) > 40 else ''}"
      cb_statusbar.update(f"Downloading {tronqued_filename} " + str_counter)
      try:
        download(filename)
        progress_pourcent = int((count / max) * 100)
        downloaded_size += float(games.game_info(filename)['size'])
        cb_progressbar.update(count, max)
        cb_text_status.update(f"{'{:02d}'.format(progress_pourcent)}% ({common.length_to_unit_string(downloaded_size)} / {common.length_to_unit_string(total_size)})")
        if unzip:
          cb_statusbar.update(f"Extracting {tronqued_filename}" + str_counter)
          py7zr.SevenZipFile(os.path.join(output_folder, filename)).extractall(output_folder)
          cb_statusbar.update(f"Extraction completed! Deleting archive {tronqued_filename}" + str_counter)
          os.remove(os.path.join(output_folder, filename))
        count+=1
      except:      
        failed+=1
        cb_statusbar.update(f"Downloading of {tronqued_filename} Failed!" + str_counter)
        time.sleep(2)
    else:
      abort_thread = False
      return
  
  cb_function(count, max, failed)
