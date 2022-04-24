PROGRAM_TITLE = 'NoIntro Roms Downloader'
PROGRAM_VERSION = '2.0'
PROGRAM_ICON = './app.ico'
PROGRAM_WIDTH = 1200
PROGRAM_HEIGHT = 765
PROGRAM_DEFAULT_STYLE = './default_style.qss'


# 
# STATIC INTERNAL FUNCTIONS (do not edit)
# 
def size_format(b):
  if b < 1000:
    return '%i' % b + 'B'
  elif 1000 <= b < 1000000:
    return '%.1f' % float(b/1000) + 'KB'
  elif 1000000 <= b < 1000000000:
    return '%.1f' % float(b/1000000) + 'MB'
  elif 1000000000 <= b < 1000000000000:
    return '%.1f' % float(b/1000000000) + 'GB'
  elif 1000000000000 <= b:
    return '%.1f' % float(b/1000000000000) + 'TB'