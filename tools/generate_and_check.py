import os, sys, argparse, json, bson, requests
from datetime import datetime, timedelta


# FOR SINGLE PART ARCHIVE, USE THIS TEMPLATE : [ 'title', 'ext', 'archive_id' ]
# FOR MULTIPLE PARTS ARCHIVE, USE THIS TEMPLATE : [ 'title', 'ext', number_of_parts(int), 'archive_$$_id' ]
#   WHERE '$$' WILL BE REPLACED BY THE PART'S NUMBER BY THE SCRIPT.
IDENTIFIERS = [
  [ 'Nintendo - NES', '7z', 'nointro.nes' ],
  [ 'Nintendo - SNES', '7z', 'nointro.snes' ],
  [ 'Nintendo - 64', '7z', 'nointro.n64' ],
  [ 'Nintendo - 64DD', '7z', 'nointro.n64dd' ],
  [ 'Nintendo - VirtualBoy', '7z', 'nointro.vb' ],
  [ 'Nintendo - GameBoy', '7z', 'nointro.gb' ],
  [ 'Nintendo - GameBoy Color', '7z', 'nointro.gbc' ],
  [ 'Nintendo - GameBoy Advance', '7z', 'nointro.gba' ],
  [ 'Sega - Master System / Mark III', '7z', 'nointro.ms-mkiii' ],
  [ 'Sega - Megadrive / Genesis', '7z', 'nointro.md' ],
  [ 'Sega - 32X', '7z', 'nointro.32x' ],
  [ 'Sega - Game Gear', '7z', 'nointro.gg' ],
  [ 'Atari 2600', '7z', 'nointro.atari-2600' ],
  [ 'Atari 5200', '7z', 'nointro.atari-5200' ],
  [ 'Atari 7800', '7z', 'nointro.atari-7800' ],
  [ 'Sony - Playstation', 'zip', 'non-redump_sony_playstation' ],
  [ 'Sony - Playstation 2', 'zip', 27, 'PS2_COLLECTION_PART$$' ],
  [ 'Sony - Playstation 3', 'zip', 8, 'PS3_NOINTRO_EUR_$$' ],
]

BASE_URL = 'https://archive.org'
DATABASE_FILENAME = "database.json"
CACHE_FILENAME = "database_cache.dat"


def generateDatabase():
  ouput_database_json = {}

  print("Generating database... ", end='')
  for id in IDENTIFIERS:
    title = id[0]
    ext = id[1]

    output_title_json = {
      "files extension": ext,
      "parts count": 1,
      "parts url": []
    }
    output_title_json['parts url'] = [] # NOT NEEDED EXCEPT FOR INTELLISENSE

    if type(id[2]) == int:
      parts_count: int = id[2]
      part_id: str = id[3]
      output_title_json['parts count'] = parts_count

      for part_number in range(parts_count):
        replaced_part_id = part_id.replace('$$', f'{part_number+1}')
        output_title_json['parts url'].append(f"{BASE_URL}/details/{replaced_part_id}&output=json")
    else:
      part_id: str = id[2]
      output_title_json['parts url'].append(f"{BASE_URL}/details/{part_id}&output=json")

    ouput_database_json[title] = output_title_json
  
  try:
    with open(DATABASE_FILENAME, 'w') as fp:
      json.dump(ouput_database_json, fp)
  except:
    print("\nAn error occured. Please try to generate database and cache, then try again.")
    exit(-1)
  
  print("Done!")
  exit(0)  


def generateCache():
  output_cache_json = {}

  print("Generating cache...")
  if os.path.exists(DATABASE_FILENAME):
    with open(DATABASE_FILENAME, 'r') as fp_db:
      database_json: dict = json.load(fp_db)

      for id_name in database_json.keys():
        id: dict = database_json[id_name]
        output_cache_json[id_name] = {}

        print(f"Processing <{id_name}>... ", end='')
        part_number = 0
        for part in id['parts url']:
          part_number += 1
          try:
            content_request = requests.get(part).content
            content_json = json.loads(content_request)
            part_files = content_json['files']
            for file in part_files:
              ext = id['files extension']
              
              if str(file).find(ext) != -1:
                output_file = {
                  "size": int(part_files[file]['size']),
                  "md5": part_files[file]['md5'],
                  "crc32": part_files[file]['crc32'],
                  "sha1": part_files[file]['sha1'],
                  "format": part_files[file]['format'],
                }
                output_cache_json[id_name][file[1:-(len(ext)+1)]] = output_file
          except: print(f"Error in part #{part_number} ", end='')
        print("Done!")
    
    with open(CACHE_FILENAME, 'wb') as fp_cache:
      output_cache_bytes = bson.dumps(output_cache_json)
      fp_cache.write(output_cache_bytes)
    
    print("\nCache successfully created!")
    exit(0)
  else:
    print(f"<{DATABASE_FILENAME}> File not found. Please generate first.")
    exit(-1)


def checkCacheExpiration():
  print("Cheking cache expiration... ", end='')
  if os.path.exists(CACHE_FILENAME):
    cache_mdate = os.path.getmtime(CACHE_FILENAME)
    cache_mdate = datetime.fromtimestamp(cache_mdate)
    today_date = datetime.today()
    expiration_date = cache_mdate + timedelta(days=30)

    if expiration_date > today_date:
      print("No need to refresh.")
      exit(0)
    else:
      print("Need refresh!")
      exit(1)
  else:
    print(f"<{CACHE_FILENAME}> is not found. Please generate first.")
    exit(-1)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description='Handle the database & cache for NoIntro Roms Downloader',
    add_help=False
  )
  parser.add_argument(
    'action',
    action='store',
    choices=['database', 'cache', 'check']
    )

  if len(sys.argv) > 1:
    args = parser.parse_args()
    if args.action == 'database': generateDatabase()
    elif args.action == 'cache': generateCache()
    elif args.action == 'check': checkCacheExpiration()
  else:
    parser.print_help()
  