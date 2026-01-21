[app]

# (str) Title of your application
title = Optimal Samples Selection

# (str) Package name
package.name = optimalsamplesselection

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (if empty, defaults to all)
source.include_exts = py,kv,md

# (str) Application versioning
version = 1.0

# (list) Application requirements
# Note: mobile build runs offline and does NOT require PyQt5/ortools.
requirements = python3,kivy

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (bool) Fullscreen mode
fullscreen = 0

# (android) Permissions
android.permissions =

# (android) Target API
android.api = 33

# (android) Min API
android.minapi = 21

# (android) NDK API
android.ndk_api = 21

