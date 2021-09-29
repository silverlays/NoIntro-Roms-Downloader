# NoIntro-Roms-Downloader
Download "official" roms from NoIntro on Internet Archive (archive.org)

Last binaries available [here](https://github.com/silverlays/NoIntro-Roms-Downloader/releases/latest) or you can just clone the repo and launch it under Windows and Linux (see below)

See [CHANGELOG.md](https://github.com/silverlays/NoIntro-Roms-Downloader/blob/master/CHANGELOG.md)

![NoIntro Roms Downloader screenshot](https://i.ibb.co/FxvMgFy/No-Intro-Roms-Downloader.jpg)

___
Building (Windows/Linux):
```
git clone https://github.com/silverlays/NoIntro-Roms-Downloader
cd ./NoIntro-Roms-Downloader
pip install -r requirements.txt
pyinstaller -Fn "NoIntro Roms Downloader" -i "app.ico" main.pyw
```
Your executable will be in **./dist** folder (you can remove **./build** folder after generation)

___
Launch without building (require Python3):
```
git clone https://github.com/silverlays/NoIntro-Roms-Downloader
cd ./NoIntro-Roms-Downloader
pip install -r requirements.txt
py main.pyw
```
