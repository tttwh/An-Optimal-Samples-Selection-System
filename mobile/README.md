# Mobile App (Kivy)

This folder contains the **mobile (Android/iOS) UI** for the Optimal Samples Selection System.

## Notes

- The mobile build is **offline** and uses the solver fallback (**exact Branch-and-Bound**) by calling:
  `solve_ilp(prefer_ortools=False, allow_pulp=False)`.
- Exact solving can be slow for large `n`. Keep `n` small on mobile.

## Android (Buildozer)

Prerequisites (Linux recommended; macOS may work but is less common):

- Python 3
- Buildozer + Android SDK/NDK dependencies

Build steps (example):

```bash
cd mobile
buildozer -v android debug
```

The APK will be created under `mobile/bin/`.

## iOS (kivy-ios)

Prerequisites:

- macOS + Xcode
- kivy-ios toolchain

High-level steps:

1. Install and set up `kivy-ios`.
2. Build a toolchain and required recipes.
3. Generate an Xcode project for this app.
4. Build/run from Xcode (signing required).

(Exact steps depend on your Xcode/iOS toolchain versions.)
