# User Manual
# An Optimal Samples Selection System

---

## Group Information

| Role | Name | Student ID |
|------|------|------------|
| Member 1 | [Name] | [ID] |
| Member 2 | [Name] | [ID] |
| Member 3 | [Name] | [ID] |
| Member 4 | [Name] | [ID] |

**Group Number:** [To be assigned]

**Course:** CS360/SE360 Artificial Intelligence

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [System Requirements](#2-system-requirements)
3. [Installation Guide](#3-installation-guide)
4. [Starting the Application](#4-starting-the-application)
5. [User Interface Guide](#5-user-interface-guide)
6. [Step-by-Step Usage](#6-step-by-step-usage)
7. [Database Operations](#7-database-operations)
8. [Mobile Version](#8-mobile-version)
9. [Troubleshooting](#9-troubleshooting)
10. [FAQ](#10-faq)

---

## 1. System Overview

The **Optimal Samples Selection System** is a software application designed to solve the combinatorial optimization problem of selecting the minimum number of k-sample groups that cover all j-subsets with at least s overlapping elements.

### Key Features

- **Parameter Configuration**: Support for all valid parameter combinations (m, n, k, j, s)
- **Sample Selection**: Random or manual sample selection
- **Optimal Solving**: Uses Integer Linear Programming (ILP) with OR-Tools for guaranteed optimal solutions
- **Database Storage**: Save, load, and manage results
- **User-Friendly Interface**: Intuitive PyQt5 desktop GUI
- **Mobile Support**: Kivy-based mobile application (Android/iOS)

---

## 2. System Requirements

### Desktop Version

| Component | Requirement |
|-----------|-------------|
| Operating System | Windows 10+, macOS 10.14+, Linux |
| Python | Python 3.8 or higher |
| RAM | Minimum 4GB |
| Disk Space | 500MB |

### Required Python Packages

- PyQt5 >= 5.15.0
- ortools >= 9.0.0
- numpy >= 1.20.0

### Mobile Version

| Component | Requirement |
|-----------|-------------|
| Android | Android 5.0+ |
| iOS | iOS 11.0+ |
| RAM | Minimum 2GB |

---

## 3. Installation Guide

### Step 1: Install Python

Download and install Python 3.8+ from [python.org](https://www.python.org/downloads/)

Verify installation:
```bash
python3 --version
```

### Step 2: Extract Project Files

Extract the USB contents to your desired location, e.g.:
```
/path/to/OptimalSamplesSelection/
```

### Step 3: Install Dependencies

Open terminal/command prompt and navigate to the project folder:

```bash
cd /path/to/OptimalSamplesSelection
```

Install required packages:

```bash
pip3 install -r requirements.txt
```

Or install manually:

```bash
pip3 install PyQt5 ortools numpy
```

### Step 4: Verify Installation

```bash
python3 -c "import PyQt5; import ortools; print('Installation successful!')"
```

---

## 4. Starting the Application

### Method 1: Using Python directly

```bash
cd /path/to/OptimalSamplesSelection
python3 main.py
```

### Method 2: Using the run script (macOS/Linux)

```bash
cd /path/to/OptimalSamplesSelection
./run.sh
```

### Method 3: Double-click (Windows)

Double-click `run.bat` file.

---

## 5. User Interface Guide

### Main Window Layout

```
┌─────────────────────────────────────────────────────────────┐
│           An Optimal Samples Selection System               │
├─────────────────────────────────────────────────────────────┤
│  [Computation Tab]  [Database Tab]                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────────────────────┐  │
│  │   Parameters    │  │      Sample Selection           │  │
│  │  m: [45-54]     │  │  ○ Random Selection             │  │
│  │  n: [7-25]      │  │  ○ Manual Input                 │  │
│  │  k: [4-7]       │  │  [_________________________]    │  │
│  │  j: [s-k]       │  │  [Generate/Select Samples]      │  │
│  │  s: [3-7]       │  │  Selected: 1,2,3,4,5,6,7,8,9    │  │
│  └─────────────────┘  └─────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  [Solve (Find Optimal Groups)] [Save Results] [Clear]       │
├─────────────────────────────────────────────────────────────┤
│  Results:  Method: OR-Tools | Time: 0.05s | Groups: 12      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Group # │ Members                                   │    │
│  │    1    │ 1, 2, 3, 4, 5, 6                         │    │
│  │    2    │ 1, 2, 3, 4, 5, 7                         │    │
│  │   ...   │ ...                                      │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Parameter Descriptions

| Parameter | Range | Description |
|-----------|-------|-------------|
| m | 45-54 | Total number of samples in the pool |
| n | 7-25 | Number of samples to select |
| k | 4-7 | Size of each output group |
| j | s to k | Size of subsets to cover |
| s | 3-7 | Minimum overlap required |

### Constraint Rules

- s ≤ j ≤ k
- n ≤ m
- All parameters must be positive integers

---

## 6. Step-by-Step Usage

### Example: Finding Optimal Groups for n=9, k=6, j=4, s=4

#### Step 1: Set Parameters

1. Set m = 45 (or any value 45-54)
2. Set n = 9
3. Set k = 6
4. Set j = 4
5. Set s = 4

#### Step 2: Select Samples

**Option A: Random Selection**
1. Select "Random Selection" radio button
2. Click "Generate/Select Samples"
3. System randomly selects 9 numbers from 1-45

**Option B: Manual Input**
1. Select "Manual Input" radio button
2. Enter 9 comma-separated numbers, e.g., `1,2,3,4,5,6,7,8,9`
3. Click "Generate/Select Samples"

#### Step 3: Solve

1. Click "Solve (Find Optimal Groups)" button
2. Wait for the solver to complete (progress bar will show)
3. Results appear in the table below

#### Step 4: View Results

The results table shows:
- Group number (1, 2, 3, ...)
- Members of each group

Statistics displayed:
- Algorithm used (OR-Tools CP-SAT)
- Solving time
- Total number of groups

#### Step 5: Save Results

1. Click "Save Results to DB"
2. File is saved with format: `m-n-k-j-s-run-groups.db`
3. Example: `45-9-6-4-4-1-12.db`

---

## 7. Database Operations

### Accessing the Database Tab

Click the "Database" tab at the top of the window.

### Viewing Saved Results

The table displays all saved results with:
- Filename
- Parameters (m, n, k, j, s)
- Run number
- Number of groups

### Loading a Result

1. Click on a row in the table to select it
2. Click "Load/Execute" button
3. Result is loaded into the Computation tab
4. Preview is shown in the Preview panel

### Deleting a Result

1. Select a row in the table
2. Click "Delete" button
3. Confirm deletion in the popup dialog

### Database File Location

Results are stored in: `OptimalSamplesSelection/results/`

---

## 8. Mobile Version

The mobile version is provided as source code under `mobile/` (Kivy).

### Key Notes

- The mobile app runs **offline** and solves using the exact Branch-and-Bound fallback
  (no OR-Tools / no PuLP on mobile builds).
- Exact solving may be slow for larger `n`; keep `n` small on mobile.

### Build (Android)

Build the APK with Buildozer (recommended on Linux):

```bash
cd mobile
buildozer -v android debug
```

The APK will be produced under `mobile/bin/`.

### Build (iOS)

Build via `kivy-ios` on macOS + Xcode (signing required).

See `mobile/README.md` for the high-level process.

---

## 9. Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'PyQt5'"

**Solution:**
```bash
pip3 install PyQt5
```

### Problem: "ModuleNotFoundError: No module named 'ortools'"

**Solution:**
```bash
pip3 install ortools
```

### Problem: Application crashes on startup

**Solution:**
1. Verify Python version: `python3 --version` (must be 3.8+)
2. Reinstall dependencies: `pip3 install -r requirements.txt --force-reinstall`

### Problem: Solver takes too long

**Solution:**
- For large n values (>15), solving may take longer
- The solver has a 5-minute timeout
- Try smaller parameter values for faster results

### Problem: "No solution found"

**Solution:**
- This occurs when parameters create an infeasible problem
- Verify that s ≤ j ≤ k
- Try different parameter combinations

---

## 10. FAQ

**Q: What algorithm does the system use?**

A: The system uses Integer Linear Programming (ILP) solved by Google OR-Tools CP-SAT solver. This guarantees optimal (minimum) solutions.

**Q: How long does solving take?**

A: Solving time depends on parameters:
- Small problems (n≤10): < 1 second
- Medium problems (n=10-15): 1-30 seconds
- Large problems (n>15): May take several minutes

**Q: Can I use letters instead of numbers?**

A: No, the system uses positive integers (1, 2, 3, ..., 54) as specified in the project requirements.

**Q: Where are my results saved?**

A: Results are saved in SQLite database files in the `results/` folder with the naming format `m-n-k-j-s-run-groups.db`.

**Q: Can I export results to other formats?**

A: Currently, results are stored in SQLite format. You can view and copy results from the application interface.

---

## Contact

For technical support or questions, please contact your course instructor.

---

*Document Version: 1.0*
*Last Updated: January 2026*
