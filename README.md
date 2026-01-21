# Optimal Samples Selection System

A Python desktop application that solves the **Optimal Samples Selection** combinatorial optimization problem via **Integer Linear Programming (ILP)**, with a PyQt5 GUI and SQLite result storage.

## Documentation

- User Manual: `docs/User_Manual.md`
- Project Report: `docs/Project_Report.md`

## Quick Start

1. (Recommended) Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip3 install -r requirements.txt
   ```

3. Run the GUI:

   ```bash
   python3 main.py
   ```

Alternatively:

```bash
./run.sh
```

## Project Structure

- `core/`: optimization solver (ILP / OR-Tools)
- `gui/`: PyQt5 desktop UI
- `database/`: SQLite persistence
- `results/`: saved `.db` result files
- `docs/`: documentation


## Mobile (Android/iOS)

- Source: `mobile/`
- Notes: offline exact solving (Branch-and-Bound) can be slow for larger `n`.
- Build instructions: `mobile/README.md`

## Windows Installer

- Packaging scripts: `packaging/windows/`
- CI workflow: `.github/workflows/windows-installer.yml` (PyInstaller + Inno Setup)
