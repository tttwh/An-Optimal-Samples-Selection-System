# Build Windows app and installer.
# Run in PowerShell from the repo root.

$ErrorActionPreference = "Stop"

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

pyinstaller --noconfirm --windowed --name OptimalSamplesSelection --collect-all PyQt5 --collect-all ortools main.py

# Inno Setup compiler must be installed and available as ISCC.exe / iscc.exe
iscc.exe packaging\windows\installer.iss

Write-Host "Built installer: dist-installer\OptimalSamplesSelectionSetup.exe"
