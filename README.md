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

## Known Cover Cache

The application uses `results/known_covers.sqlite` as a reusable cache for:

- La Jolla Covering Repository standard covers `C(v,k,t)` when `s == j`.
- Previously solved project instances `(n,k,j,s)` mapped onto canonical samples `1..n`.

To refresh the La Jolla cache for the assignment parameter range:

```bash
python3 scripts/import_ljcr_covers.py --min-v 7 --max-v 25 --min-k 4 --max-k 7 --min-t 3 --max-t 7
```

Cached La Jolla results are returned directly only when they are proven optimal. Otherwise they are used as feasible upper bounds / solver hints.

## Large Instances

The GUI estimates `C(n,j) * C(n,k)` before starting an exact local solve. If the estimate is too large, it avoids constructing the full coverage matrix to prevent freezes or crashes. In that case, it returns a cached cover when available, or asks the user to reduce the parameters.


## Mobile (Android/iOS)

- Source: `mobile/`
- Notes: offline exact solving (Branch-and-Bound) can be slow for larger `n`.
- Build instructions: `mobile/README.md`

## Windows Installer

- Packaging scripts: `packaging/windows/`
- CI workflow: `.github/workflows/windows-installer.yml` (PyInstaller + Inno Setup)
