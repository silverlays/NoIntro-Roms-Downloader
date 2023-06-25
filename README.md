# NoIntro-Roms-Downloader
![NoIntro Roms Downloader UI](https://i.ibb.co/8Y9nGkD/image-2022-12-18-121345339.png)

## NEWS ##
### 06/26/2023: Good news! I may have finally found a viable alternative to using the "archive.org" site. If all goes to plan, you'll have a TON of new systems available, and download speeds will be GREATLY improved. I'll share with you more soon!
### 02/12/2023: Time has finally come !!</i> v2.0.0 RC1 is up **[HERE](https://github.com/silverlays/NoIntro-Roms-Downloader/releases/tag/v2.0-RC1)** (Carefully read the release description to know how to use it).
<br/>

## Description
Download "datted" ROMs directly from the NoIntro libraries on [Internet Archive](https://archive.org). Lastest binaries are available [here](https://github.com/silverlays/NoIntro-Roms-Downloader/releases/latest) or you can just clone the repo and launch it under Windows and Linux. (see below)

If you want to see changes since the beginning of this project, see [CHANGELOG.md](https://github.com/silverlays/NoIntro-Roms-Downloader/blob/master/CHANGELOG.md).

## Supported platforms on 02/13/23
- [Atari 2600](https://archive.org/details/nointro.atari-2600)
- [Atari 5200](https://archive.org/details/nointro.atari-5200)
- [Atari 7800](https://archive.org/details/nointro.atari-7800)
- [NEC - PC Engine - TurboGrafx 16](https://archive.org/details/nointro.tg-16)
- [Nintendo - Nintendo 64](https://archive.org/details/nointro.n64)
- [Nintendo - Nintendo 64DD](https://archive.org/details/nointro.n64dd)
- [Nintendo - Nintendo Entertainment System (Headered)](https://archive.org/details/nointro.nes-headered)
- [Nintendo - Nintendo Game Boy](https://archive.org/details/nointro.gb)
- [Nintendo - Nintendo Game Boy Advance](https://archive.org/details/nointro.gba)
- [Nintendo - Nintendo Game Boy Color](https://archive.org/details/nointro.gbc)
- [Nintendo - Super Nintendo Entertainment System (Combined)](https://archive.org/details/nointro.snes)
- [Nintendo - Virtual Boy](https://archive.org/details/nointro.vb)
- [Sega - 32X](https://archive.org/details/nointro.32x)
- [Sega - Game Gear](https://archive.org/details/nointro.gg)
- [Sega - Master System - Mark III](https://archive.org/details/nointro.ms-mkiii)
- [Sega - Mega Drive - Genesis](https://archive.org/details/nointro.md)

*NB: Playstation 1, 2 and 3 are ready to use, but because of the size of files, multi-connections must be implemented before, sorry.*

## Launch without PyInstaller (Windows/Linux/MacOS)
### Step one
```
git clone https://github.com/silverlays/NoIntro-Roms-Downloader
cd ./NoIntro-Roms-Downloader
python3 -m venv .venv
```

### Step two
* For Windows: ```.venv\Scripts\activate.bat```
* For Linux/MacOS: ```source .venv/bin/activate```

### Step three
```
pip install -r requirements.txt
python3 app.pyw
```

## Feedback
If you found a bug (not listed on the status above), feel free to create an issue [here](https://github.com/silverlays/NoIntro-Roms-Downloader/issues).
