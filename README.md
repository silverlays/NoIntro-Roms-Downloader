# NoIntro-Roms-Downloader v2.0 (Qt)
Download "datted" ROMs from NoIntro fullsets on Internet Archive ([archive.org](https://archive.org))

## Development status
- Cache generation is fully operational.
- Settings are working (more settings must be implemented until release).
- Browsing, selections, filter and regions are working fine.
- Download queue is operational but need polish.
- Menu is almost complete (Settings, About, About Qt completed).
- UI is almost finished (minor fixes are required).
- UI works, but download isn't yet implemented... coming soon.

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
