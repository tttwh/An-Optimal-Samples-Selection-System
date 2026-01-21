"""Mobile UI entry point (Kivy).

Targets Android/iOS builds.

This mobile app runs offline and uses the solver fallback (exact Branch-and-Bound)
by calling:

    solve_ilp(prefer_ortools=False, allow_pulp=False)

Exact solving can be slow; keep n small on mobile.
"""

from __future__ import annotations

import os
import sys
import random
import threading
from typing import List

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from core.solver import OptimalSamplesSolver
from database.db_manager import DatabaseManager


def _parse_int(text: str, name: str) -> int:
    try:
        return int(str(text).strip())
    except Exception:
        raise ValueError(f"Invalid integer for {name}: {text!r}")


def _parse_samples(text: str) -> List[int]:
    text = str(text or "").strip()
    if not text:
        return []
    parts = [p.strip() for p in text.split(",") if p.strip()]
    return [int(p) for p in parts]


class ComputeScreen(Screen):
    m_text = StringProperty("45")
    n_text = StringProperty("9")
    k_text = StringProperty("6")
    j_text = StringProperty("4")
    s_text = StringProperty("4")

    mode = StringProperty("Random")
    samples_text = StringProperty("")
    status_text = StringProperty("Ready")
    results_text = StringProperty("")

    _samples: List[int] = []
    _last_groups = None
    _last_solve_time = 0.0
    _last_method = ""

    def generate_samples(self) -> None:
        try:
            m = _parse_int(self.ids.m_in.text, "m")
            n = _parse_int(self.ids.n_in.text, "n")

            if n <= 0:
                raise ValueError("n must be positive")
            if m <= 0:
                raise ValueError("m must be positive")

            if self.mode == "Random":
                if n > m:
                    raise ValueError("n must be <= m")
                self._samples = sorted(random.sample(range(1, m + 1), n))
            else:
                raw = self.ids.manual_samples.text
                samples = _parse_samples(raw)
                if len(samples) != n:
                    raise ValueError(f"Please enter exactly {n} samples")
                if len(set(samples)) != len(samples):
                    raise ValueError("Duplicate samples are not allowed")
                if any(x < 1 or x > m for x in samples):
                    raise ValueError(f"All samples must be between 1 and {m}")
                self._samples = sorted(samples)

            self.samples_text = ", ".join(map(str, self._samples))
            self.status_text = f"Selected {len(self._samples)} samples"
            self.results_text = ""
            self._last_groups = None
        except Exception as e:
            self.status_text = f"Error: {e}"

    def solve(self) -> None:
        if not self._samples:
            self.status_text = "Please generate/select samples first"
            return

        self.status_text = "Solving (exact, offline)..."
        self.results_text = ""

        def _run() -> None:
            try:
                n = _parse_int(self.ids.n_in.text, "n")
                k = _parse_int(self.ids.k_in.text, "k")
                j = _parse_int(self.ids.j_in.text, "j")
                s = _parse_int(self.ids.s_in.text, "s")

                solver = OptimalSamplesSolver(n=n, k=k, j=j, s=s, samples=self._samples)
                groups, solve_time, method = solver.solve_ilp(
                    time_limit_seconds=300.0,
                    prefer_ortools=False,
                    allow_pulp=False,
                )

                lines = [
                    f"Method: {method}",
                    f"Time: {solve_time:.3f}s",
                    f"Groups: {len(groups)}",
                    "",
                ]
                for idx, g in enumerate(groups, 1):
                    members = ", ".join(map(str, g))
                    lines.append(f"{idx}. {members}")

                def _update(_dt):
                    self._last_groups = groups
                    self._last_solve_time = solve_time
                    self._last_method = method
                    self.status_text = f"Done: {len(groups)} groups"
                    self.results_text = "\n".join(lines)

                Clock.schedule_once(_update, 0)
            except Exception as e:
                Clock.schedule_once(lambda _dt: setattr(self, "status_text", f"Solver error: {e}"), 0)

        threading.Thread(target=_run, daemon=True).start()

    def save_to_db(self) -> None:
        try:
            if not self._samples:
                self.status_text = "No samples selected"
                return
            if not self._last_groups:
                self.status_text = "No results to save"
                return

            m = _parse_int(self.ids.m_in.text, "m")
            n = _parse_int(self.ids.n_in.text, "n")
            k = _parse_int(self.ids.k_in.text, "k")
            j = _parse_int(self.ids.j_in.text, "j")
            s = _parse_int(self.ids.s_in.text, "s")

            app = App.get_running_app()
            db_folder = os.path.join(app.user_data_dir, "results")
            db = DatabaseManager(db_folder=db_folder)

            filename = db.save_result(
                m=m,
                n=n,
                k=k,
                j=j,
                s=s,
                samples=self._samples,
                groups=self._last_groups,
                solve_time=float(self._last_solve_time),
                method=str(self._last_method or "B&B"),
            )
            self.status_text = f"Saved: {filename}"
        except Exception as e:
            self.status_text = f"Save error: {e}"


class DatabaseScreen(Screen):
    filenames = ListProperty([])
    selected_filename = StringProperty("")
    preview_text = StringProperty("")

    def _get_db(self) -> DatabaseManager:
        app = App.get_running_app()
        db_folder = os.path.join(app.user_data_dir, "results")
        return DatabaseManager(db_folder=db_folder)

    def refresh(self) -> None:
        try:
            db = self._get_db()
            rows = db.list_results()
            self.filenames = [r["filename"] for r in rows]
            if self.filenames and (self.selected_filename not in self.filenames):
                self.selected_filename = self.filenames[0]
            self.preview_text = f"DB folder: {db.get_db_folder()}\nFiles: {len(self.filenames)}"
        except Exception as e:
            self.preview_text = f"Error: {e}"

    def preview(self) -> None:
        try:
            if not self.selected_filename:
                self.preview_text = "No file selected"
                return
            db = self._get_db()
            r = db.load_result(self.selected_filename)
            if not r:
                self.preview_text = "Failed to load"
                return

            lines = [
                f"File: {self.selected_filename}",
                f"Parameters: m={r[m]} n={r[n]} k={r[k]} j={r[j]} s={r[s]}",
                f"Samples: {r[samples]}",
                f"Method: {r[method]} Time: {r[solve_time]:.3f}s",
                f"Created: {r[created_at]}",
                f"Groups: {r[num_groups]}",
                "",
            ]
            for i, g in enumerate(r["groups"], 1):
                members = ", ".join(map(str, g))
                lines.append(f"{i}. {members}")

            self.preview_text = "\n".join(lines)
        except Exception as e:
            self.preview_text = f"Error: {e}"

    def load_into_compute(self) -> None:
        try:
            if not self.selected_filename:
                self.preview_text = "No file selected"
                return
            db = self._get_db()
            r = db.load_result(self.selected_filename)
            if not r:
                self.preview_text = "Failed to load"
                return

            compute = self.manager.get_screen("compute")

            compute.ids.m_in.text = str(r["m"])
            compute.ids.n_in.text = str(r["n"])
            compute.ids.k_in.text = str(r["k"])
            compute.ids.j_in.text = str(r["j"])
            compute.ids.s_in.text = str(r["s"])

            compute._samples = list(r["samples"])
            compute.samples_text = ", ".join(map(str, r["samples"]))

            lines = [
                f"Loaded: {self.selected_filename}",
                f"Method: {r[method]}",
                f"Time: {r[solve_time]:.3f}s",
                f"Groups: {r[num_groups]}",
                "",
            ]
            for idx, g in enumerate(r["groups"], 1):
                members = ", ".join(map(str, g))
                lines.append(f"{idx}. {members}")

            compute._last_groups = r["groups"]
            compute._last_solve_time = r["solve_time"]
            compute._last_method = r["method"]
            compute.results_text = "\n".join(lines)
            compute.status_text = "Loaded from DB"

            self.manager.current = "compute"
        except Exception as e:
            self.preview_text = f"Error: {e}"

    def delete_selected(self) -> None:
        try:
            if not self.selected_filename:
                self.preview_text = "No file selected"
                return
            db = self._get_db()
            ok = db.delete_result(self.selected_filename)
            if ok:
                deleted = self.selected_filename
                self.selected_filename = ""
                self.refresh()
                self.preview_text = f"Deleted: {deleted}"
            else:
                self.preview_text = "Delete failed"
        except Exception as e:
            self.preview_text = f"Error: {e}"


class MobileApp(App):
    def build(self):
        return Builder.load_file(os.path.join(os.path.dirname(__file__), "app.kv"))


if __name__ == "__main__":
    MobileApp().run()
