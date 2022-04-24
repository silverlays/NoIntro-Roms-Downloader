import PySimpleGUI as sg
import math


def length_to_unit_string(length: float) -> str:
  unit = "b"
  one_kilobytes = math.pow(1024, 1)
  one_megabytes = math.pow(1024, 2)
  one_gigabytes = math.pow(1024, 3)

  if length > one_kilobytes and length < one_megabytes:
    length /= one_kilobytes
    unit = "Kb"
  if length > one_megabytes and length < one_gigabytes:
    length /= one_megabytes
    unit = "Mb"
  if length > one_gigabytes:
    length /= one_gigabytes
    unit = "Gb"
  
  return "{:.1f}{}".format(length, unit)


def create_hyperlink(url: str, key: str, text: str=None, tooltip: str=None, **kargs) -> sg.Text:
  if not text: text = url
  if not tooltip: tooltip = url
  hyperlink = sg.Text(text, key=f"HYPERLINK::{key}", metadata=url, font=("", 10, "bold underline"), tooltip=tooltip, enable_events=True, **kargs)
  return hyperlink


def open_hyperlink(url: str) -> None:
  import webbrowser
  webbrowser.open(url)


def create_modal_title(title: str) -> list:
  return [
    [sg.Text(title.upper(), font=("", 20, "bold"), expand_x=True, justification="center", pad=(5, 0))],
    [sg.HorizontalSeparator(pad=(5, (0, 20)))],
  ]