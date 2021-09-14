import os
import time
import py7zr
import PySimpleGUI as sg
import common_functions as common
from urllib.parse import quote
from urllib.request import urlopen
from http.client import HTTPResponse


_base_url = "https://archive.org"


def download_files(platform_id: str, filenames: list, output_folder: str, unzip: bool, cb_progressbar: sg.ProgressBar, cb_statusbar: sg.StatusBar, cb_text_status: sg.Text, cb_function):
  def download(filename: str):
    filename_quoted = quote(filename)
    full_url = f"{_base_url}/download/{platform_id}/{filename_quoted}"
    output_stream = open(file=os.path.join(output_folder, filename), mode="wb")
    file_request: HTTPResponse = urlopen(full_url)
    file_length = file_request.length
    buffer_length = int(file_length / 10)
    position = 0
    
    while True:
      bytes_read = file_request.read(buffer_length)
      output_stream.write(bytes_read)
      output_stream.flush()
      position += len(bytes_read)
      cb_progressbar.update(position, file_length)
      cb_text_status.update(f"{common.length_to_unit_string(position)} / {common.length_to_unit_string(file_length)}")
      if len(bytes_read) < buffer_length: break
    
    file_request.close()
    output_stream.close()
    while not file_request.closed and not output_stream.closed: pass

  failed = 0
  count = 1
  max = len(filenames)
  for filename in filenames:
    str_counter = f" ({count}/{max})"
    tronqued_filename = f"{filename[:50]}{'...' if len(filename) > 50 else ''}"
    cb_progressbar.update(0, 0)
    cb_text_status.update("0Kb / 0Kb")
    cb_statusbar.update(f"Downloading {tronqued_filename}" + str_counter)
    try:
      download(filename)
      if unzip:
        cb_statusbar.update(f"Extracting {tronqued_filename}" + str_counter)
        py7zr.SevenZipFile(os.path.join(output_folder, filename)).extractall(output_folder)
        cb_statusbar.update(f"Extraction completed! Deleting archive {tronqued_filename}" + str_counter)
        os.remove(os.path.join(output_folder, filename))
      count+=1
    except:      
      failed+=1
      cb_text_status.update(f"Downloading of {tronqued_filename} Failed!" + str_counter)
      time.sleep(2)
  
  cb_function(count, max, failed)
