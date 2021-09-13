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
