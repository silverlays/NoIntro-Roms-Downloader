# NoIntro-Roms-Downloader v2.0 (Qt)
Download "datted" ROMs from NoIntro fullsets on Internet Archive ([archive.org](https://archive.org))

## Development status
- Cache generation is fully operational.
- Settings are working perfectly including: Cache expiration in days; Download folder; Decompress after download ; Check for updates
- Browsing, selections, filter and regions work fine.
- Download queue is operational but need polish.
- Menu is complete for now.
- UI is almost finished (minor fixes needed).
- Download queue is fully operational.
- Download work (no download speed at the moment)
- Auto update not working until release

## Beta testing
If you want to test the actual status of the development by yourself, follow the instructions below:
```
git clone https://github.com/silverlays/NoIntro-Roms-Downloader -b v2.0-Qt
cd ./NoIntro-Roms-Downloader
python -m venv .venv
.venv\Scripts\activate.bat  # FOR WINDOWS
source .venv\bin\activate  # FOR LINUX / MACOSX
pip install -r requirements.txt
python app.pyw
```

## Feedback
If you found a bug (not listed on the status above), feel free to create an issue [here](https://github.com/silverlays/NoIntro-Roms-Downloader/issues).
