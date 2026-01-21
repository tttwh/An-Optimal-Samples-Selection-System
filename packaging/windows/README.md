# Windows Packaging

This project can be packaged for Windows as a GUI application and distributed as an installer.

## Local Build (Windows)

Prerequisites:

- Windows 10/11 x64
- Python 3.10+ (64-bit)
- Inno Setup 6 (for installer)

Build steps:

```powershell
pip install -r requirements.txt
pip install pyinstaller

pyinstaller --noconfirm --windowed --name OptimalSamplesSelection --collect-all PyQt5 --collect-all ortools main.py

# Compile installer (requires Inno Setup installed and ISCC in PATH)
ISCC.exe packaging\\windows\\installer.iss
```

Output:

- App folder: `dist\\OptimalSamplesSelection\\`
- Installer EXE: `dist-installer\\OptimalSamplesSelectionSetup.exe`
