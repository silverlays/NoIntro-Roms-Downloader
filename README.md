# NoIntro-Roms-Downloader
## Description
Download "datted" ROMs from NoIntro fullsets on Internet Archive (archive.org). Lastest binaries are available [here](https://github.com/silverlays/NoIntro-Roms-Downloader/releases/latest) or you can just clone the repo and launch it under Windows and Linux. (see below)

If you want to see changes since the beginning of this project, see [CHANGELOG.md](https://github.com/silverlays/NoIntro-Roms-Downloader/blob/master/CHANGELOG.md).

![NoIntro Roms Downloader screenshot](https://i.ibb.co/FxvMgFy/No-Intro-Roms-Downloader.jpg)

## Supported platforms on 11/01/21
- [Atari 2600](https://archive.org/details/nointro.atari-2600)
- [Atari 5200](https://archive.org/details/nointro.atari-5200)
- [Atari 7800](https://archive.org/details/nointro.atari-7800)
- [NEC - PC Engine - TurboGrafx 16](https://archive.org/details/nointro.tg-16)
- [Nintendo - Family Computer Disk System](https://archive.org/details/nointro.fds)
- [Nintendo - Nintendo 64](https://archive.org/details/nointro.n64)
- [Nintendo - Nintendo 64DD](https://archive.org/details/nointro.n64dd)
- [Nintendo - Nintendo Entertainment System](https://archive.org/details/nointro.nes)
- [Nintendo - Nintendo Game Boy](https://archive.org/details/nointro.gb)
- [Nintendo - Nintendo Game Boy Advance](https://archive.org/details/nointro.gba)
- [Nintendo - Nintendo Game Boy Advance (Multiboot)](https://archive.org/details/nointro.gba-multiboot)
- [Nintendo - Nintendo Game Boy Color](https://archive.org/details/nointro.gbc)
- [Nintendo - Pokemon-Mini](https://archive.org/details/nointro.poke-mini)
- [Nintendo - Super Nintendo Entertainment System (Combined)](https://archive.org/details/nointro.snes)
- [Nintendo - Virtual Boy](https://archive.org/details/nointro.vb)
- [Nintendo - e-Reader](https://archive.org/details/nointro.e-reader)
- [Sega - 32X](https://archive.org/details/nointro.32x)
- [Sega - Game Gear](https://archive.org/details/nointro.gg)
- [Sega - Master System - Mark III](https://archive.org/details/nointro.ms-mkiii)
- [Sega - Mega Drive - Genesis](https://archive.org/details/nointro.md)

## Building (Windows/Linux) (require Python3)
```
git clone https://github.com/silverlays/NoIntro-Roms-Downloader
cd ./NoIntro-Roms-Downloader
pip install -r requirements.txt
pyinstaller -Fn "NoIntro Roms Downloader" -i "app.ico" main.pyw
```
Your executable will be in **./dist** folder (you can remove **./build** folder after generation)

## Launch without building (require Python3):
```
git clone https://github.com/silverlays/NoIntro-Roms-Downloader
cd ./NoIntro-Roms-Downloader
pip install -r requirements.txt
py main.pyw
```
