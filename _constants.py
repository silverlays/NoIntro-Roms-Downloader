import os

VERSION_MAJOR = 2
VERSION_MINOR = 0
VERSION_REVISION = "0 RC1"

RESOURCES_FILE = os.path.join(os.path.split(__file__)[0], "resources.rcc")
SETTINGS_FILE = 'settings.dat'
PLATFORMS_CACHE_FILENAME = "database_cache.dat"

ARCHIVE_PLATFORMS_DATA = [
    [ 'Nintendo - NES', '7z', 'nointro.nes-headered' ],
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
    # [ 'Sony - Playstation', 'zip', 'non-redump_sony_playstation' ],
    # [ 'Sony - Playstation', '7z', 'redump-sony-playstation-pal'],
    # [ 'Sony - Playstation 2', 'zip', 27, 'PS2_COLLECTION_PART$$' ],
    # [ 'Sony - Playstation 3', 'zip', 8, 'PS3_NOINTRO_EUR_$$' ],
  ]
