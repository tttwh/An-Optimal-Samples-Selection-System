import pathlib
import re

p = pathlib.Path(__file__).resolve().parents[1] / "docs" / "User_Manual.md"
t = p.read_text(encoding="utf-8")

pat = re.compile(r"## 8\. Mobile Version\n\n.*?\n---\n\n## 9\.", re.S)

rep = """## 8. Mobile Version

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

## 9."""

new = pat.sub(rep, t, count=1)
if new == t:
    raise SystemExit("Mobile section pattern not found")

p.write_text(new, encoding="utf-8")
print("Updated", p)
