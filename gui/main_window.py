"""
Main Window for the Optimal Samples Selection System.
<<<<<<< HEAD
=======

Provides a user-friendly GUI for:
- Parameter input (m, n, k, j, s)
- Sample selection (random or manual)
- Result display
- Database operations
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
"""

import sys
import random
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
<<<<<<< HEAD
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QGroupBox, QRadioButton, QLineEdit, QMessageBox, QStatusBar,
    QTabWidget, QSplitter, QProgressBar,
    QComboBox, QHeaderView, QAbstractItemView, QFileDialog,
    QScrollArea, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal, QElapsedTimer
from PyQt5.QtGui import QFont, QColor

import os
import tempfile
=======
    QLabel, QSpinBox, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem,
    QGroupBox, QRadioButton, QLineEdit, QMessageBox, QStatusBar,
    QTabWidget, QListWidget, QListWidgetItem, QSplitter, QProgressBar,
    QComboBox, QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal, QElapsedTimer
from PyQt5.QtGui import QFont, QIntValidator

import os
import sys
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.solver import OptimalSamplesSolver, estimate_coverage_generation
from database.db_manager import DatabaseManager

<<<<<<< HEAD
# Write a tiny SVG triangle arrow to a temp file; used as ::down-arrow image in QSS.
# This is the only reliable way to show a custom arrow on macOS with Qt5 Fusion style.
_ARROW_SVG_PATH = os.path.join(tempfile.gettempdir(), "ossl_combo_arrow.svg")
with open(_ARROW_SVG_PATH, "w") as _f:
    _f.write(
        '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="6">'
        '<polygon points="0,0 10,0 5,6" fill="#6B7280"/>'
        '</svg>'
    )

=======
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba

MAX_GUI_COVER_RELATION_CHECKS = 20_000_000
MAX_DISPLAYED_GROUPS = 5000

<<<<<<< HEAD
# ── Accent colours (indigo/slate palette) ──────────────────────────────────────
C_ACCENT      = "#4F6AF5"   # primary blue-indigo
C_ACCENT_HOV  = "#3B56E0"
C_ACCENT_DARK = "#2D44C8"
C_SEL         = "#E8ECFF"   # light selected background
C_BG          = "#F5F6FA"   # page background
C_CARD        = "#FFFFFF"
C_BORDER      = "#E2E5EF"
C_TEXT        = "#1A1D2E"
C_MUTED       = "#6B7280"
C_DANGER      = "#EF4444"
C_DANGER_HOV  = "#DC2626"

_SS_ACCENT = (
    f"QPushButton{{background:{C_ACCENT};color:white;border:none;"
    f"font-weight:bold;font-size:13px;padding:10px 18px;border-radius:6px;}}"
    f"QPushButton:hover{{background:{C_ACCENT_HOV};}}"
    f"QPushButton:disabled{{background:#B0BBF0;color:rgba(255,255,255,0.6);}}"
)
_SS_ACCENT_SM = (
    f"QPushButton{{background:{C_ACCENT};color:white;border:none;"
    f"font-weight:bold;font-size:12px;padding:6px 14px;border-radius:6px;}}"
    f"QPushButton:hover{{background:{C_ACCENT_HOV};}}"
    f"QPushButton:disabled{{background:#B0BBF0;}}"
)
_SS_DANGER = (
    f"QPushButton{{background:white;color:{C_DANGER};"
    f"border:1px solid {C_DANGER};border-radius:6px;"
    f"font-size:12px;padding:6px 14px;}}"
    f"QPushButton:hover{{background:#FEF2F2;}}"
)

APP_STYLE = f"""
QMainWindow, QDialog {{
    background: {C_BG};
}}
QTabWidget::pane {{
    border: none;
    background: {C_BG};
}}
QTabBar::tab {{
    background: transparent;
    color: {C_MUTED};
    padding: 10px 32px;
    min-width: 160px;
    font-size: 13px;
    border-bottom: 2px solid transparent;
    margin-right: 4px;
}}
QTabBar::tab:selected {{
    color: {C_ACCENT};
    border-bottom: 2px solid {C_ACCENT};
    font-weight: bold;
}}
QTabBar::tab:hover:!selected {{
    color: {C_TEXT};
}}
QGroupBox {{
    background: {C_CARD};
    border: 1px solid {C_BORDER};
    border-radius: 10px;
    margin-top: 6px;
    padding: 10px 12px 12px 12px;
    font-size: 12px;
    font-weight: bold;
    color: {C_TEXT};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 14px;
    top: -2px;
    color: {C_MUTED};
    font-size: 11px;
    font-weight: normal;
    letter-spacing: 0.5px;
}}
QPushButton {{
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 12px;
    color: {C_TEXT};
    background: {C_CARD};
    border: 1px solid {C_BORDER};
}}
QPushButton:hover {{
    background: #EAECF5;
    border-color: #C5CAE0;
}}
QPushButton#accent {{
    background: {C_ACCENT};
    color: white;
    border: none;
    font-weight: bold;
    font-size: 13px;
    padding: 10px 18px;
}}
QPushButton#accent:hover {{
    background: {C_ACCENT_HOV};
}}
QPushButton#accent:disabled {{
    background: #B0BBF0;
}}
QPushButton#danger {{
    background: white;
    color: {C_DANGER};
    border: 1px solid {C_DANGER};
}}
QPushButton#danger:hover {{
    background: #FEF2F2;
}}
QComboBox {{
    border: 1px solid {C_BORDER};
    border-radius: 6px;
    padding: 4px 8px;
    background: {C_CARD};
    color: {C_TEXT};
    font-size: 13px;
    min-height: 28px;
}}
QComboBox:focus {{
    border-color: {C_ACCENT};
}}
QComboBox::drop-down {{
    border: none;
    width: 22px;
}}
QComboBox::down-arrow {{
    image: url("{_ARROW_SVG_PATH}");
    width: 10px;
    height: 6px;
}}
QComboBox QAbstractItemView {{
    border: 1px solid {C_BORDER};
    border-radius: 4px;
    selection-background-color: {C_SEL};
    selection-color: {C_ACCENT};
}}
QTableWidget {{
    border: none;
    background: transparent;
    gridline-color: {C_BORDER};
    font-size: 12px;
    color: {C_TEXT};
    outline: none;
}}
QTableWidget::item {{
    padding: 5px 8px;
    border-bottom: 1px solid {C_BORDER};
}}
QTableWidget::item:selected {{
    background: {C_SEL};
    color: {C_ACCENT};
}}
QHeaderView::section {{
    background: {C_BG};
    border: none;
    border-bottom: 1px solid {C_BORDER};
    padding: 6px 8px;
    font-size: 11px;
    color: {C_MUTED};
    font-weight: normal;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
QScrollArea {{
    border: none;
    background: transparent;
}}
QScrollBar:vertical {{
    background: transparent;
    width: 6px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: #CDD1E0;
    border-radius: 3px;
    min-height: 24px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: transparent;
    height: 6px;
}}
QScrollBar::handle:horizontal {{
    background: #CDD1E0;
    border-radius: 3px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
QProgressBar {{
    border: none;
    border-radius: 5px;
    background: #E2E5EF;
    text-align: center;
    height: 10px;
    font-size: 10px;
}}
QProgressBar::chunk {{
    border-radius: 5px;
    background: {C_ACCENT};
}}
QStatusBar {{
    background: {C_CARD};
    border-top: 1px solid {C_BORDER};
    font-size: 11px;
    color: {C_MUTED};
}}
QLabel {{
    color: {C_TEXT};
}}
QRadioButton {{
    color: {C_TEXT};
    font-size: 12px;
    spacing: 6px;
}}
QRadioButton::indicator {{
    width: 14px;
    height: 14px;
    border: 2px solid {C_BORDER};
    border-radius: 7px;
    background: white;
}}
QRadioButton::indicator:checked {{
    border-color: {C_ACCENT};
    background: {C_ACCENT};
}}
"""


class SolverThread(QThread):
    finished = pyqtSignal(list, float, str, str)
    error = pyqtSignal(str)
    progress = pyqtSignal(int, int, int)
    round_progress = pyqtSignal(int, int, int)

    TIME_LIMIT_PER_ROUND = 70.0

    def __init__(self, solver, initial_solution=None,
                 initial_solution_status="FEASIBLE", num_rounds=1):
=======

class SolverThread(QThread):
    """Background thread for running the solver (supports multi-round training)."""
    finished = pyqtSignal(list, float, str, str)
    error = pyqtSignal(str)
    progress = pyqtSignal(int, int, int)
    round_progress = pyqtSignal(int, int, int)  # current_round, total_rounds, best_size

    TIME_LIMIT_PER_ROUND = 70.0

    def __init__(self, solver, initial_solution=None, initial_solution_status="FEASIBLE",
                 num_rounds=1):
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
        super().__init__()
        self.solver = solver
        self.initial_solution = initial_solution
        self.initial_solution_status = initial_solution_status
        self.num_rounds = max(1, num_rounds)

    def run(self):
        try:
<<<<<<< HEAD
=======
            import time as _time
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
            best_result = self.initial_solution
            best_status = self.initial_solution_status
            best_method = "Cached upper bound"
            total_time = 0.0

            for rnd in range(1, self.num_rounds + 1):
                result, solve_time, method = self.solver.solve_ilp(
                    progress_callback=lambda d, c, b: self.progress.emit(d, c, b),
                    initial_solution=best_result,
                    initial_solution_status=best_status,
                    time_limit_seconds=self.TIME_LIMIT_PER_ROUND,
<<<<<<< HEAD
                    relative_gap_limit=0.05,
                    extension_seconds=5.0,
                    early_stop_gap=0.02,
=======
                    relative_gap_limit=0.10,
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
                )
                total_time += solve_time
                current_status = self.solver.last_status

                if best_result is None or len(result) < len(best_result):
                    best_result = result
                    best_status = current_status
                    best_method = f"{method} (round {rnd}/{self.num_rounds})"

                self.round_progress.emit(rnd, self.num_rounds,
                                         len(best_result) if best_result else -1)
<<<<<<< HEAD
=======

>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
                if current_status == "OPTIMAL":
                    break

            self.finished.emit(best_result, total_time, best_method, best_status)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
<<<<<<< HEAD
=======
    """Main application window."""
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba

    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.db_manager.seed_builtin_known_covers()
        self.current_samples = []
        self.current_results = []
        self.solver_thread = None
<<<<<<< HEAD
=======

>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
        self.last_solve_time = 0.0
        self.last_method = ""
        self.last_status = "NOT_SOLVED"

<<<<<<< HEAD
        # sample-pool state
        self._pool_buttons: dict[int, QPushButton] = {}
        self._pool_selected: set[int] = set()

=======
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
        self._progress_timer = QTimer(self)
        self._progress_timer.setInterval(8)
        self._progress_timer.timeout.connect(self._tick_progress)
        self._elapsed = QElapsedTimer()
        self._total_budget_ms = 0

<<<<<<< HEAD
        self.setStyleSheet(APP_STYLE)
        self.init_ui()

    # ── helpers ───────────────────────────────────────────────────────────────

    def _card(self, title=""):
        box = QGroupBox(title)
        return box

    def _stat_card(self, label_text: str, value_text: str) -> QWidget:
        """Return a small stat card widget."""
        w = QWidget()
        w.setObjectName("statCard")
        w.setStyleSheet(f"""
            QWidget#statCard {{
                background: {C_CARD};
                border: 1px solid {C_BORDER};
                border-radius: 8px;
                min-width: 90px;
            }}
        """)
        ly = QVBoxLayout(w)
        ly.setContentsMargins(12, 10, 12, 10)
        ly.setSpacing(2)
        lbl = QLabel(label_text.upper())
        lbl.setStyleSheet(f"background:transparent; color:{C_MUTED}; font-size:10px; letter-spacing:0.5px;")
        val = QLabel(value_text)
        val.setStyleSheet(f"background:transparent; color:{C_TEXT}; font-size:20px; font-weight:bold;")
        val.setObjectName("statVal")
        ly.addWidget(lbl)
        ly.addWidget(val)
        return w

    # ── main UI ───────────────────────────────────────────────────────────────

    def init_ui(self):
        self.setWindowTitle("An Optimal Samples Selection System")
        self.setMinimumSize(1100, 700)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── App header ──────────────────────────────────────────────────────
        header = QWidget()
        header.setFixedHeight(52)
        header.setStyleSheet(f"background:{C_CARD}; border-bottom:1px solid {C_BORDER};")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(20, 0, 20, 0)
        app_title = QLabel("An Optimal Samples Selection System")
        f = QFont()
        f.setPointSize(14)
        f.setBold(True)
        app_title.setFont(f)
        app_title.setStyleSheet(f"color:{C_TEXT};")
        hl.addWidget(app_title)
        hl.addStretch()
        root.addWidget(header)

        # ── Tabs ────────────────────────────────────────────────────────────
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        root.addWidget(self.tab_widget)

        self.create_main_tab()
        self.create_database_tab()

=======
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("An Optimal Samples Selection System")
        self.setMinimumSize(1000, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Title
        title_label = QLabel("An Optimal Samples Selection System")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Create tabs
        self.create_main_tab()
        self.create_database_tab()

        # Status bar
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

<<<<<<< HEAD
    # ── Computation tab ──────────────────────────────────────────────────────

    def create_main_tab(self):
        tab = QWidget()
        tab.setStyleSheet(f"background:{C_BG};")
        outer = QHBoxLayout(tab)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(14)

        # ──────── LEFT PANEL ────────────────────────────────────────────────
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setFixedWidth(500)
        left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        left_scroll.setStyleSheet("background:transparent; border:none;")
        left_inner = QWidget()
        left_inner.setStyleSheet("background:transparent;")
        lv = QVBoxLayout(left_inner)
        lv.setContentsMargins(0, 0, 4, 0)
        lv.setSpacing(12)
        left_scroll.setWidget(left_inner)

        # ── Parameters card  (horizontal "dial strip") ─────────────────────────
        param_card = self._card("Parameters")
        param_vbox = QVBoxLayout(param_card)
        param_vbox.setContentsMargins(12, 18, 12, 12)
        param_vbox.setSpacing(6)

        _COMBO_LE_BASE = (
            f"font-size:16px; font-weight:bold; color:{C_TEXT}; "
            f"background:transparent; border:none; "
            f"qproperty-alignment: AlignCenter;"
        )

        def make_param_combo(lo, hi, default):
            c = QComboBox()
            c.setEditable(True)
            for v in range(lo, hi + 1):
                c.addItem(str(v))
            c.setCurrentText(str(default))
            c.lineEdit().setPlaceholderText(f"{lo}–{hi}")
            c.lineEdit().setAlignment(Qt.AlignCenter)
            c.lineEdit().setStyleSheet(_COMBO_LE_BASE)
            # Per-widget arrow override (ensures macOS respects our SVG arrow)
            c.setStyleSheet(
                f'QComboBox::drop-down{{border:none;width:20px;}}'
                f'QComboBox::down-arrow{{image:url("{_ARROW_SVG_PATH}");width:10px;height:6px;}}'
            )

            def _val(text, mn=lo, mx=hi):
                if not text.strip():
                    # Empty while typing — keep neutral styling, just update button state
                    c.lineEdit().setStyleSheet(_COMBO_LE_BASE)
                    self._update_param_buttons_state()
                    return
                try:
                    v = int(text)
                    in_range = mn <= v <= mx
                except ValueError:
                    in_range = False
                if in_range:
                    c.lineEdit().setStyleSheet(_COMBO_LE_BASE)
                else:
                    c.lineEdit().setStyleSheet(
                        _COMBO_LE_BASE +
                        f"color:{C_DANGER};"
                    )
                self._update_param_buttons_state()

            c.currentTextChanged.connect(_val)
            return c

        self.m_combo = make_param_combo(45, 54, 45)
        self.n_combo = make_param_combo(7, 25, 9)
        self.k_combo = make_param_combo(4, 7, 6)
        self.j_combo = make_param_combo(3, 7, 4)
        self.s_combo = make_param_combo(3, 7, 4)
        self.r_combo = make_param_combo(1, 20, 1)

        params_def = [
            ("m", "45–54", "Pool",    self.m_combo),
            ("n", "7–25",  "Samples", self.n_combo),
            ("k", "4–7",   "Group",   self.k_combo),
            ("j", "3–7",   "Subset",  self.j_combo),
            ("s", "3–7",   "Overlap", self.s_combo),
            ("r", "1–20",  "Rounds",  self.r_combo),
        ]

        strip = QGridLayout()
        strip.setHorizontalSpacing(0)
        strip.setVerticalSpacing(0)
        for i, (key, rng, desc, combo) in enumerate(params_def):
            grid_row = i // 3
            grid_col = i % 3

            # Vertical separator between columns (except first column of each row)
            if grid_col > 0:
                sep = QFrame()
                sep.setFrameShape(QFrame.VLine)
                sep.setFixedWidth(1)
                sep.setStyleSheet(
                    f"background:{C_BORDER}; border:none; margin:4px 0px;")
                strip.addWidget(sep, grid_row, grid_col * 2 - 1)

            pcol = QWidget()
            pcol.setStyleSheet("background:transparent;")
            pv = QVBoxLayout(pcol)
            pv.setContentsMargins(6, 4, 6, 6)
            pv.setSpacing(2)
            pv.setAlignment(Qt.AlignTop)

            # Large bold parameter letter
            key_lbl = QLabel(key)
            key_lbl.setAlignment(Qt.AlignCenter)
            key_lbl.setStyleSheet(
                f"color:{C_ACCENT}; font-size:22px; font-weight:bold;")

            # Human-readable name
            desc_lbl = QLabel(desc.upper())
            desc_lbl.setAlignment(Qt.AlignCenter)
            desc_lbl.setStyleSheet(
                f"color:{C_TEXT}; font-size:10px; letter-spacing:0.6px;")

            # Range hint
            rng_lbl = QLabel(rng)
            rng_lbl.setAlignment(Qt.AlignCenter)
            rng_lbl.setStyleSheet(
                f"color:{C_MUTED}; font-size:9px;")

            pv.addWidget(key_lbl)
            pv.addWidget(desc_lbl)
            pv.addWidget(rng_lbl)
            pv.addWidget(combo)
            strip.addWidget(pcol, grid_row, grid_col * 2, 1, 1)
            strip.setColumnStretch(grid_col * 2, 1)

        param_vbox.addLayout(strip)

        self.k_combo.currentTextChanged.connect(self.update_constraints)
        self.j_combo.currentTextChanged.connect(self.update_constraints)
        self.s_combo.currentTextChanged.connect(self.update_constraints)
        self.m_combo.currentTextChanged.connect(self._on_m_changed)

        self.constraint_label = QLabel("")
        self.constraint_label.setStyleSheet(
            f"color:{C_MUTED}; font-size:10px;")
        self.constraint_label.setWordWrap(True)
        param_vbox.addWidget(self.constraint_label)
        lv.addWidget(param_card)

        # Sample mode + generate
        mode_card = self._card("Sample Selection")
        mv = QVBoxLayout(mode_card)
        mv.setContentsMargins(12, 18, 12, 12)
        mv.setSpacing(8)

        mode_row = QHBoxLayout()
        self.random_radio = QRadioButton("Random")
        self.random_radio.setChecked(True)
        self.manual_radio = QRadioButton("Manual  (click numbers below)")
        mode_row.addWidget(self.random_radio)
        mode_row.addWidget(self.manual_radio)
        mode_row.addStretch()
        mv.addLayout(mode_row)

        self.generate_btn = QPushButton("Generate / Select Samples")
        self.generate_btn.setStyleSheet(_SS_ACCENT)
        self.generate_btn.clicked.connect(self.generate_samples)
        mv.addWidget(self.generate_btn)

        # Pool header
        pool_hdr = QHBoxLayout()
        pool_lbl = QLabel("SAMPLE POOL")
        pool_lbl.setStyleSheet(
            f"background:transparent; color:{C_MUTED}; font-size:10px; letter-spacing:0.5px;")
        self._pool_count_label = QLabel("")
        self._pool_count_label.setStyleSheet(
            f"background:transparent; color:{C_ACCENT}; font-size:11px; font-weight:bold;")
        pool_hdr.addWidget(pool_lbl)
        pool_hdr.addStretch()
        pool_hdr.addWidget(self._pool_count_label)
        mv.addLayout(pool_hdr)

        # Pool scroll area + grid
        self._pool_scroll = QScrollArea()
        self._pool_scroll.setWidgetResizable(True)
        self._pool_scroll.setFixedHeight(220)
        self._pool_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._pool_scroll.setStyleSheet("background:transparent; border:none;")
        self._pool_widget = QWidget()
        self._pool_widget.setStyleSheet("background:transparent;")
        self._pool_grid = QGridLayout(self._pool_widget)
        self._pool_grid.setSpacing(4)
        self._pool_grid.setContentsMargins(0, 0, 0, 0)
        self._pool_scroll.setWidget(self._pool_widget)
        mv.addWidget(self._pool_scroll)

        # Selected samples text (editable in manual mode)
        self.samples_display = QLineEdit()
        self.samples_display.setPlaceholderText(
            "Samples shown here — type numbers (comma/space) in Manual mode…")
        self.samples_display.setStyleSheet(
            f"border:1px solid {C_BORDER}; border-radius:6px; "
            f"padding:4px 8px; background:{C_CARD}; color:{C_TEXT}; font-size:11px;")
        self.samples_display.textEdited.connect(self._on_samples_text_edited)
        mv.addWidget(self.samples_display)
        lv.addWidget(mode_card)

        # Action buttons
        btn_card = self._card()
        bv = QVBoxLayout(btn_card)
        bv.setContentsMargins(12, 12, 12, 12)
        bv.setSpacing(8)

        self.solve_btn = QPushButton("Solve  —  Find Optimal Groups")
        self.solve_btn.setStyleSheet(_SS_ACCENT)
        self.solve_btn.clicked.connect(self.solve)
        bv.addWidget(self.solve_btn)

        btn_row = QHBoxLayout()
        self.save_btn = QPushButton("Save to DB")
        self.save_btn.clicked.connect(self.save_results)
        self.save_btn.setEnabled(False)
        self.print_btn = QPushButton("Export")
        self.print_btn.clicked.connect(self.print_results)
        self.print_btn.setEnabled(False)
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_all)
        btn_row.addWidget(self.save_btn)
        btn_row.addWidget(self.print_btn)
        btn_row.addWidget(self.clear_btn)
        bv.addLayout(btn_row)

        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setTextVisible(False)
        bv.addWidget(self.progress_bar)
        self.round_label = QLabel("")
        self.round_label.setAlignment(Qt.AlignCenter)
        self.round_label.setStyleSheet(f"color:{C_MUTED}; font-size:11px;")
        self.round_label.setVisible(False)
        bv.addWidget(self.round_label)
        lv.addWidget(btn_card)
        lv.addStretch()

        outer.addWidget(left_scroll)

        # ──────── RIGHT PANEL ───────────────────────────────────────────────
        right_w = QWidget()
        right_w.setStyleSheet("background:transparent;")
        rv = QVBoxLayout(right_w)
        rv.setContentsMargins(0, 0, 0, 0)
        rv.setSpacing(12)

        # Stats row
        self._stats_row = QHBoxLayout()
        self._stats_row.setSpacing(10)

        self._stat_groups = self._stat_card("Groups", "—")
        self._stat_time   = self._stat_card("Time", "—")
        self._stat_status = self._stat_card("Status", "—")
        self._stats_row.addWidget(self._stat_groups)
        self._stats_row.addWidget(self._stat_time)
        self._stats_row.addWidget(self._stat_status)
        self._stats_row.addStretch()
        rv.addLayout(self._stats_row)

        # Status help
        self.status_help_label = QLabel(
            "OPTIMAL = proven minimum.  "
            "FEASIBLE = valid solution (target gap ≤5%).  "
            "FEASIBLE_CACHED = loaded from cache."
        )
        self.status_help_label.setWordWrap(True)
        self.status_help_label.setStyleSheet(
            f"color:{C_MUTED}; font-size:10px;")
        rv.addWidget(self.status_help_label)

        # Results card
        results_card = self._card("Results")
        rcv = QVBoxLayout(results_card)
        rcv.setContentsMargins(10, 18, 10, 10)
        rcv.setSpacing(8)

        # Placeholder shown before first solve
        self._results_placeholder = QLabel(
            "Awaiting execution\n\n"
            "Set parameters on the left, pick or randomise your\n"
            "n samples, then press Solve to compute the optimal\n"
            "k-sample coverage."
        )
        self._results_placeholder.setAlignment(Qt.AlignCenter)
        self._results_placeholder.setStyleSheet(
            f"color:{C_MUTED}; font-size:13px; padding:40px;")
        rcv.addWidget(self._results_placeholder)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Group #", "Members"])
        self.results_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.results_table.setVisible(False)
        rcv.addWidget(self.results_table)
        rv.addWidget(results_card, stretch=1)

        outer.addWidget(right_w, stretch=1)

        self.tab_widget.addTab(tab, "Computation")
        self._rebuild_pool()

    # ── Database tab ─────────────────────────────────────────────────────────

    def create_database_tab(self):
        tab = QWidget()
        tab.setStyleSheet(f"background:{C_BG};")
        outer = QHBoxLayout(tab)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(14)

        # ──── LEFT: file list ────────────────────────────────────────────────
        list_card = self._card("Data Base Rounds")
        lv = QVBoxLayout(list_card)
        lv.setContentsMargins(10, 18, 10, 10)
        lv.setSpacing(8)

        # buttons above list
        top_btn = QHBoxLayout()
        self.display_btn = QPushButton("Display")
        self.display_btn.setStyleSheet(_SS_ACCENT_SM)
        self.display_btn.clicked.connect(self._display_selected_db)
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setStyleSheet(_SS_DANGER)
        self.delete_btn.clicked.connect(self.delete_from_db)
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_db_list)
        top_btn.addWidget(self.display_btn)
        top_btn.addWidget(self.delete_btn)
        top_btn.addStretch()
        top_btn.addWidget(refresh_btn)
        lv.addLayout(top_btn)

        self.db_list = QTableWidget()
        self.db_list.setColumnCount(1)
        self.db_list.setHorizontalHeaderLabels(["Filename"])
        self.db_list.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch)
        self.db_list.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.db_list.verticalHeader().setVisible(False)
        self.db_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.db_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.db_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.db_list.cellClicked.connect(self._on_db_row_clicked)
        lv.addWidget(self.db_list)

        # folder path
        path_lbl = QLabel(f"Folder: {self.db_manager.get_db_folder()}")
        path_lbl.setStyleSheet(
            f"color:{C_MUTED}; font-size:10px;")
        path_lbl.setWordWrap(True)
        lv.addWidget(path_lbl)

        list_card.setMinimumWidth(360)
        list_card.setMaximumWidth(460)
        outer.addWidget(list_card)

        # ──── RIGHT: detail panel ────────────────────────────────────────────
        self.detail_group = QGroupBox()
        self.detail_group.setStyleSheet(
            f"QGroupBox{{background:{C_CARD};border:1px solid {C_BORDER};"
            f"border-radius:10px; padding:12px;}}")
        dv = QVBoxLayout(self.detail_group)
        dv.setContentsMargins(12, 14, 12, 12)
        dv.setSpacing(10)

        # header row
        det_hdr = QHBoxLayout()
        self.detail_file_label = QLabel("")
        self.detail_file_label.setWordWrap(True)
        self.detail_file_label.setStyleSheet(
            f"background:transparent; font-weight:bold; color:{C_TEXT}; font-size:13px;")
        det_hdr.addWidget(self.detail_file_label, stretch=1)

        self.detail_load_btn = QPushButton("Load into Computation")
        self.detail_load_btn.setStyleSheet(_SS_ACCENT_SM)
        self.detail_load_btn.clicked.connect(self.load_from_db)
        det_back_btn = QPushButton("Back")
        det_back_btn.clicked.connect(self._clear_db_detail)
        det_print_btn = QPushButton("Export")
        det_print_btn.clicked.connect(self.print_db_result)
        det_hdr.addWidget(self.detail_load_btn)
        det_hdr.addWidget(det_back_btn)
        det_hdr.addWidget(det_print_btn)
        dv.addLayout(det_hdr)

        # Stat cards row
        self._db_stats_row = QHBoxLayout()
        self._db_stats_row.setSpacing(10)
        self._db_stat_groups  = self._stat_card("Groups",  "—")
        self._db_stat_time    = self._stat_card("Time",    "—")
        self._db_stat_status  = self._stat_card("Status",  "—")
        self._db_stats_row.addWidget(self._db_stat_groups)
        self._db_stats_row.addWidget(self._db_stat_time)
        self._db_stats_row.addWidget(self._db_stat_status)
        self._db_stats_row.addStretch()
        dv.addLayout(self._db_stats_row)

        # Pool chips
        pool_row_w = QWidget()
        pool_row_w.setStyleSheet("background:transparent;")
        self._db_pool_layout = QHBoxLayout(pool_row_w)
        self._db_pool_layout.setContentsMargins(0, 0, 0, 0)
        self._db_pool_layout.setSpacing(4)
        pool_prefix = QLabel("POOL")
        pool_prefix.setStyleSheet(
            f"background:transparent; color:{C_MUTED}; font-size:10px; letter-spacing:0.5px;")
        self._db_pool_layout.addWidget(pool_prefix)
        self._db_pool_chip_container = QHBoxLayout()
        self._db_pool_chip_container.setSpacing(4)
        self._db_pool_layout.addLayout(self._db_pool_chip_container)
        self._db_pool_layout.addStretch()
        dv.addWidget(pool_row_w)

        # Groups scroll area with card grid
        grp_scroll = QScrollArea()
        grp_scroll.setWidgetResizable(True)
        grp_scroll.setStyleSheet("background:transparent; border:none;")
        self._grp_container = QWidget()
        self._grp_container.setStyleSheet("background:transparent;")
        self._grp_card_layout = QGridLayout(self._grp_container)
        self._grp_card_layout.setSpacing(10)
        self._grp_card_layout.setContentsMargins(0, 0, 0, 0)
        self._grp_card_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        grp_scroll.setWidget(self._grp_container)
        dv.addWidget(grp_scroll, stretch=1)

        self.detail_group.setVisible(False)
        outer.addWidget(self.detail_group, stretch=1)

        # Placeholder shown when nothing is selected
        self._db_placeholder = QLabel(
            "Select a record from the list\nand press Display (or click a row)."
        )
        self._db_placeholder.setAlignment(Qt.AlignCenter)
        self._db_placeholder.setStyleSheet(
            f"color:{C_MUTED}; font-size:13px;")
        outer.addWidget(self._db_placeholder, stretch=1)

        self.tab_widget.addTab(tab, "Data Base Rounds")
        self.refresh_db_list()

    # ── Sample pool ────────────────────────────────────────────────────────────

    def _rebuild_pool(self):
        try:
            m = int(self.m_combo.currentText())
        except ValueError:
            return

        # remove buttons no longer in range
        to_remove = [num for num in list(self._pool_buttons) if num > m]
        for num in to_remove:
            btn = self._pool_buttons.pop(num)
            self._pool_grid.removeWidget(btn)
            btn.deleteLater()
        self._pool_selected.difference_update(to_remove)

        cols = 10
        for num in range(1, m + 1):
            if num not in self._pool_buttons:
                btn = QPushButton(str(num))
                btn.setFixedSize(40, 36)
                btn.setCheckable(True)
                btn.clicked.connect(lambda _, n=num: self._toggle_pool(n))
                self._pool_buttons[num] = btn
                row, col = divmod(num - 1, cols)
                self._pool_grid.addWidget(btn, row, col)

        self._refresh_pool_display()

    def _refresh_pool_display(self):
        n_target = self._safe_int(self.n_combo, 9)
        selected = sorted(self._pool_selected)
        count = len(selected)
        self._pool_count_label.setText(f"{count} / {n_target}")

        for num, btn in self._pool_buttons.items():
            active = num in self._pool_selected
            btn.setChecked(active)
            btn.setStyleSheet(
                f"QPushButton{{border-radius:6px; font-size:12px; font-weight:bold;"
                f"border:none; background:{C_ACCENT}; color:white;"
                f"padding:0px;}}"
                if active else
                f"QPushButton{{border-radius:6px; font-size:12px; font-weight:600;"
                f"border:1px solid {C_BORDER}; background:#EEF0FC; color:#1A1D2E;"
                f"padding:0px;}}"
                f"QPushButton:hover{{background:#DDE0F8; color:#1A1D2E;}}"
            )

    def _toggle_pool(self, num: int):
        if self.random_radio.isChecked():
            return
        n_target = self._safe_int(self.n_combo, 9)
        if num in self._pool_selected:
            self._pool_selected.discard(num)
        else:
            if len(self._pool_selected) >= n_target:
                QMessageBox.information(
                    self, "Limit reached",
                    f"You can only select {n_target} samples (n = {n_target}).")
                return
            self._pool_selected.add(num)
        self._refresh_pool_display()
        self.samples_display.setText(
            ", ".join(map(str, sorted(self._pool_selected))))

    def _on_m_changed(self, _):
        self._rebuild_pool()

    def _update_param_buttons_state(self):
        """Disable Generate and Solve if any parameter combo is out of range."""
        combos_ranges = [
            (self.m_combo, 45, 54),
            (self.n_combo, 7, 25),
            (self.k_combo, 4, 7),
            (self.j_combo, 3, 7),
            (self.s_combo, 3, 7),
            (self.r_combo, 1, 20),
        ]
        all_valid = True
        for combo, lo, hi in combos_ranges:
            try:
                v = int(combo.currentText())
                if not (lo <= v <= hi):
                    all_valid = False
                    break
            except ValueError:
                all_valid = False
                break
        self.generate_btn.setEnabled(all_valid)
        self.solve_btn.setEnabled(all_valid)

    def _on_samples_text_edited(self, text: str):
        """Sync typed sample numbers → pool selection (manual mode only)."""
        if not self.manual_radio.isChecked():
            return
        m = self._safe_int(self.m_combo, 54)
        nums = []
        for part in text.replace(',', ' ').split():
            try:
                v = int(part.strip())
                if 1 <= v <= m:
                    nums.append(v)
            except ValueError:
                pass
        self._pool_selected = set(nums)
        self._refresh_pool_display()

    @staticmethod
    def _safe_int(combo: QComboBox, default: int) -> int:
        try:
            return int(combo.currentText())
        except ValueError:
            return default

    # ── Parameter validation ──────────────────────────────────────────────────

    def update_constraints(self):
        try:
            k = int(self.k_combo.currentText())
            j = int(self.j_combo.currentText())
            s = int(self.s_combo.currentText())
        except ValueError:
            return
        if j > k:
            self.j_combo.setCurrentText(str(k))
            j = k
        if s > j:
            self.s_combo.setCurrentText(str(j))

    # ── Sample generation ─────────────────────────────────────────────────────

    def generate_samples(self):
        try:
            m = int(self.m_combo.currentText())
            n = int(self.n_combo.currentText())
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid m or n value.")
            return

        if self.random_radio.isChecked():
            chosen = sorted(random.sample(range(1, m + 1), n))
            self._pool_selected = set(chosen)
            self._refresh_pool_display()
            self.current_samples = chosen
            self.samples_display.setText(", ".join(map(str, chosen)))
            self.status_bar.showMessage(f"Randomly selected {n} samples from 1–{m}")
        else:
            # Manual mode: validate pool selection
            if len(self._pool_selected) != n:
                QMessageBox.warning(
                    self, "Selection mismatch",
                    f"Please select exactly {n} numbers from the pool "
                    f"(currently {len(self._pool_selected)} selected).")
                return
            chosen = sorted(self._pool_selected)
            self.current_samples = chosen
            self.samples_display.setText(", ".join(map(str, chosen)))
            self.status_bar.showMessage(
                f"Confirmed {n} manually selected samples")

    # ── Solve ─────────────────────────────────────────────────────────────────

    def solve(self):
        if not self.current_samples:
            QMessageBox.warning(self, "Error",
                                "Please generate or select samples first.")
            return

        n = self._safe_int(self.n_combo, 9)
        k = self._safe_int(self.k_combo, 6)
        j = self._safe_int(self.j_combo, 4)
        s = self._safe_int(self.s_combo, 4)

        if len(self.current_samples) != n:
            QMessageBox.warning(
                self, "Error",
                "Sample count doesn't match n. Please regenerate samples.")
            return

        try:
            cached_solution, cached_status, cached_message = \
                self.get_precomputed_solution()
            if cached_solution and cached_status == "OPTIMAL":
                self.on_solve_finished(
                    cached_solution, 0.0, cached_message, cached_status)
                self.status_bar.showMessage(
                    f"Loaded {len(cached_solution)} proven optimal groups from cache")
=======
    def create_main_tab(self):
        """Create the main computation tab."""
        main_tab = QWidget()
        layout = QVBoxLayout(main_tab)

        # Top section: Parameters and Sample Selection
        top_splitter = QSplitter(Qt.Horizontal)

        # Left: Parameters
        param_group = QGroupBox("Parameters")
        param_layout = QGridLayout(param_group)

        # Parameter inputs
        self.m_spin = QSpinBox()
        self.m_spin.setRange(45, 54)
        self.m_spin.setValue(45)

        self.n_spin = QSpinBox()
        self.n_spin.setRange(7, 25)
        self.n_spin.setValue(9)

        self.k_spin = QSpinBox()
        self.k_spin.setRange(4, 7)
        self.k_spin.setValue(6)

        self.j_spin = QSpinBox()
        self.j_spin.setRange(3, 7)
        self.j_spin.setValue(4)

        self.s_spin = QSpinBox()
        self.s_spin.setRange(3, 7)
        self.s_spin.setValue(4)

        self.r_spin = QSpinBox()
        self.r_spin.setRange(1, 20)
        self.r_spin.setValue(1)
        self.r_spin.setToolTip("Number of training rounds. Each round uses the previous best solution as a warm-start hint.")

        # Add labels and spinboxes
        param_layout.addWidget(QLabel("m (Total samples, 45-54):"), 0, 0)
        param_layout.addWidget(self.m_spin, 0, 1)

        param_layout.addWidget(QLabel("n (Select samples, 7-25):"), 1, 0)
        param_layout.addWidget(self.n_spin, 1, 1)

        param_layout.addWidget(QLabel("k (Group size, 4-7):"), 2, 0)
        param_layout.addWidget(self.k_spin, 2, 1)

        param_layout.addWidget(QLabel("j (Subset size, s <= j <= k):"), 3, 0)
        param_layout.addWidget(self.j_spin, 3, 1)

        param_layout.addWidget(QLabel("s (Min overlap, 3-7):"), 4, 0)
        param_layout.addWidget(self.s_spin, 4, 1)

        param_layout.addWidget(QLabel("r (Training rounds, ≥1):"), 5, 0)
        param_layout.addWidget(self.r_spin, 5, 1)

        # Connect spinbox changes for validation
        self.k_spin.valueChanged.connect(self.update_constraints)
        self.j_spin.valueChanged.connect(self.update_constraints)
        self.s_spin.valueChanged.connect(self.update_constraints)

        top_splitter.addWidget(param_group)

        # Right: Sample Selection
        sample_group = QGroupBox("Sample Selection")
        sample_layout = QVBoxLayout(sample_group)

        # Selection mode
        mode_layout = QHBoxLayout()
        self.random_radio = QRadioButton("Random Selection")
        self.random_radio.setChecked(True)
        self.manual_radio = QRadioButton("Manual Input")
        mode_layout.addWidget(self.random_radio)
        mode_layout.addWidget(self.manual_radio)
        sample_layout.addLayout(mode_layout)

        # Manual input field
        manual_layout = QHBoxLayout()
        manual_layout.addWidget(QLabel("Enter samples (comma-separated):"))
        self.manual_input = QLineEdit()
        self.manual_input.setPlaceholderText("e.g., 1,2,3,4,5,6,7,8,9")
        self.manual_input.setEnabled(False)
        manual_layout.addWidget(self.manual_input)
        sample_layout.addLayout(manual_layout)

        # Connect radio buttons
        self.random_radio.toggled.connect(lambda: self.manual_input.setEnabled(False))
        self.manual_radio.toggled.connect(lambda: self.manual_input.setEnabled(True))

        # Generate/Select button
        self.generate_btn = QPushButton("Generate/Select Samples")
        self.generate_btn.clicked.connect(self.generate_samples)
        sample_layout.addWidget(self.generate_btn)

        # Display selected samples
        self.samples_display = QLineEdit()
        self.samples_display.setReadOnly(True)
        self.samples_display.setPlaceholderText("Selected samples will appear here...")
        sample_layout.addWidget(self.samples_display)

        top_splitter.addWidget(sample_group)
        layout.addWidget(top_splitter)

        # Control buttons
        btn_layout = QHBoxLayout()

        self.solve_btn = QPushButton("Solve (Find Optimal Groups)")
        self.solve_btn.clicked.connect(self.solve)
        self.solve_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        btn_layout.addWidget(self.solve_btn)

        self.save_btn = QPushButton("Save Results to DB")
        self.save_btn.clicked.connect(self.save_results)
        self.save_btn.setEnabled(False)
        btn_layout.addWidget(self.save_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_all)
        btn_layout.addWidget(self.clear_btn)

        layout.addLayout(btn_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.round_label = QLabel("")
        self.round_label.setAlignment(Qt.AlignCenter)
        self.round_label.setVisible(False)
        layout.addWidget(self.round_label)

        # Results section
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout(results_group)

        # Statistics
        self.stats_label = QLabel("")
        results_layout.addWidget(self.stats_label)

        self.status_help_label = QLabel(
            "Status: OPTIMAL = proven minimum; FEASIBLE = valid solution within ≤10% of optimal; "
            "FEASIBLE_CACHED = cached upper-bound result."
        )
        self.status_help_label.setWordWrap(True)
        self.status_help_label.setStyleSheet("color: #555;")
        results_layout.addWidget(self.status_help_label)

        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Group #", "Members"])
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        results_layout.addWidget(self.results_table)

        layout.addWidget(results_group)

        self.tab_widget.addTab(main_tab, "Computation")

    def create_database_tab(self):
        """Create the database management tab."""
        db_tab = QWidget()
        layout = QVBoxLayout(db_tab)

        # Database path display
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Database Folder:"))
        self.db_path_label = QLabel(self.db_manager.get_db_folder())
        self.db_path_label.setStyleSheet("color: blue;")
        path_layout.addWidget(self.db_path_label)
        path_layout.addStretch()
        layout.addLayout(path_layout)

        # Refresh button
        refresh_btn = QPushButton("Refresh List")
        refresh_btn.clicked.connect(self.refresh_db_list)
        layout.addWidget(refresh_btn)

        # Database list
        self.db_list = QTableWidget()
        self.db_list.setColumnCount(8)
        self.db_list.setHorizontalHeaderLabels(["Filename", "m", "n", "k", "j", "s", "Run#", "Groups"])
        self.db_list.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.db_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.db_list.setSelectionMode(QAbstractItemView.SingleSelection)
        layout.addWidget(self.db_list)

        # Action buttons
        action_layout = QHBoxLayout()

        self.load_btn = QPushButton("Load/Execute")
        self.load_btn.clicked.connect(self.load_from_db)
        action_layout.addWidget(self.load_btn)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_from_db)
        action_layout.addWidget(self.delete_btn)

        layout.addLayout(action_layout)

        # Preview section
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout(preview_group)
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        preview_layout.addWidget(self.preview_text)
        layout.addWidget(preview_group)

        self.tab_widget.addTab(db_tab, "Database")

        # Initial refresh
        self.refresh_db_list()

    def update_constraints(self):
        """Update parameter constraints based on current values."""
        k = self.k_spin.value()
        j = self.j_spin.value()
        s = self.s_spin.value()

        # j must be <= k
        self.j_spin.setMaximum(k)
        if j > k:
            self.j_spin.setValue(k)

        # s must be <= j
        self.s_spin.setMaximum(self.j_spin.value())
        if s > self.j_spin.value():
            self.s_spin.setValue(self.j_spin.value())

    def generate_samples(self):
        """Generate or parse sample selection."""
        m = self.m_spin.value()
        n = self.n_spin.value()

        if self.random_radio.isChecked():
            # Random selection
            self.current_samples = sorted(random.sample(range(1, m + 1), n))
        else:
            # Manual input
            try:
                text = self.manual_input.text().strip()
                samples = [int(x.strip()) for x in text.split(',')]

                if len(samples) != n:
                    QMessageBox.warning(self, "Error", f"Please enter exactly {n} samples.")
                    return

                if len(set(samples)) != len(samples):
                    QMessageBox.warning(self, "Error", "Duplicate samples are not allowed.")
                    return

                if any(s < 1 or s > m for s in samples):
                    QMessageBox.warning(self, "Error", f"All samples must be between 1 and {m}.")
                    return

                self.current_samples = sorted(samples)

            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid input. Please enter comma-separated integers.")
                return

        self.samples_display.setText(", ".join(map(str, self.current_samples)))
        self.status_bar.showMessage(f"Selected {n} samples from 1-{m}")

    def solve(self):
        """Run the solver to find optimal groups."""
        if not self.current_samples:
            QMessageBox.warning(self, "Error", "Please generate or select samples first.")
            return

        n = self.n_spin.value()
        k = self.k_spin.value()
        j = self.j_spin.value()
        s = self.s_spin.value()

        # Validate
        if len(self.current_samples) != n:
            QMessageBox.warning(self, "Error", "Sample count doesn't match n. Please regenerate samples.")
            return

        try:
            cached_solution, cached_status, cached_message = self.get_precomputed_solution()
            if cached_solution and cached_status == "OPTIMAL":
                self.on_solve_finished(cached_solution, 0.0, cached_message, cached_status)
                self.status_bar.showMessage(f"Loaded {len(cached_solution)} proven optimal groups from cache")
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
                return

            estimate = self.estimate_problem_size(n, k, j, s)
            if estimate['relation_checks'] > MAX_GUI_COVER_RELATION_CHECKS:
                if cached_solution:
<<<<<<< HEAD
                    self.on_solve_finished(
                        cached_solution, 0.0, cached_message, cached_status)
                    self.status_bar.showMessage(
                        f"Problem too large; loaded {len(cached_solution)} cached groups")
                    return
                QMessageBox.warning(
                    self, "Problem Too Large",
                    "This parameter set is too large for the current solver.\n\n"
                    f"j-subsets: {estimate['num_j_subsets']:,}\n"
                    f"k-groups: {estimate['num_k_groups']:,}\n"
                    f"Coverage entries: {estimate['optimized_coverage_entries']:,}\n\n"
                    "Reduce n/k/j or import a known cover.")
                self.status_bar.showMessage("Problem too large")
=======
                    self.on_solve_finished(cached_solution, 0.0, cached_message, cached_status)
                    self.status_bar.showMessage(
                        f"Problem is too large for exact solving; loaded {len(cached_solution)} cached feasible groups"
                    )
                    return

                QMessageBox.warning(
                    self,
                    "Problem Too Large",
                    "This parameter set is too large for the current exact local solver.\n\n"
                    f"j-subsets: {estimate['num_j_subsets']:,}\n"
                    f"k-groups: {estimate['num_k_groups']:,}\n"
                    f"Coverage entries: {estimate['optimized_coverage_entries']:,}\n"
                    f"Naive pair checks avoided: {estimate['naive_relation_checks']:,}\n\n"
                    "Import a known cover, reduce n/k/j, or use a smaller instance for demonstration."
                )
                self.status_bar.showMessage("Problem too large; solving was not started")
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
                return

            solver = OptimalSamplesSolver(n, k, j, s, self.current_samples)
            stats = solver.get_statistics()
<<<<<<< HEAD
            initial_solution, initial_status, cache_message = \
                self.get_cached_solution_hint(solver)

            if initial_solution and initial_status == "OPTIMAL":
                self.on_solve_finished(
                    initial_solution, 0.0, cache_message, "OPTIMAL")
                self.status_bar.showMessage(
                    f"Loaded {len(initial_solution)} optimal groups from cache")
                return

            r = self._safe_int(self.r_combo, 1)
            self.status_bar.showMessage(
                f"Solving {r} round(s)… "
                f"(j-subsets: {stats['num_j_subsets']}, "
                f"k-groups: {stats['num_k_groups']})")
            self._total_budget_ms = int(
                (SolverThread.TIME_LIMIT_PER_ROUND + 5.0) * r * 1000)
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 1000)
            self.progress_bar.setValue(0)
=======
            initial_solution, initial_status, cache_message = self.get_cached_solution_hint(solver)

            if initial_solution and initial_status == "OPTIMAL":
                self.on_solve_finished(initial_solution, 0.0, cache_message, "OPTIMAL")
                self.status_bar.showMessage(f"Loaded {len(initial_solution)} optimal groups from cache")
                return

            r = self.r_spin.value()
            self.status_bar.showMessage(
                f"Solving {r} round(s)... (j-subsets: {stats['num_j_subsets']}, k-groups: {stats['num_k_groups']})"
            )
            self._total_budget_ms = int(SolverThread.TIME_LIMIT_PER_ROUND * r * 1000)
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 1000)
            self.progress_bar.setValue(0)
            self.progress_bar.setFormat("%p%")
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
            self.round_label.setText(f"Round 0 / {r}")
            self.round_label.setVisible(True)
            self.solve_btn.setEnabled(False)
            self._elapsed.start()
            self._progress_timer.start()

<<<<<<< HEAD
            self.solver_thread = SolverThread(
                solver, initial_solution, initial_status, num_rounds=r)
=======
            # Run solver in background thread
            self.solver_thread = SolverThread(solver, initial_solution, initial_status,
                                              num_rounds=r)
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
            self.solver_thread.finished.connect(self.on_solve_finished)
            self.solver_thread.error.connect(self.on_solve_error)
            self.solver_thread.round_progress.connect(self.on_round_progress)
            self.solver_thread.start()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def on_round_progress(self, current_round, total_rounds, best_size):
<<<<<<< HEAD
        size_str = f"  Best so far: {best_size}" if best_size >= 0 else ""
        self.round_label.setText(
            f"Round {current_round} / {total_rounds}{size_str}")
        self.status_bar.showMessage(
            f"Completed round {current_round} / {total_rounds}…")

    def _tick_progress(self):
=======
        """Update round label after each training round completes."""
        size_str = f" | Best so far: {best_size}" if best_size >= 0 else ""
        self.round_label.setText(f"Round {current_round} / {total_rounds}{size_str}")
        self.status_bar.showMessage(f"Completed round {current_round} / {total_rounds}...")

    def _tick_progress(self):
        """Advance the progress bar based on elapsed wall-clock time."""
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
        if self._total_budget_ms <= 0:
            return
        elapsed = self._elapsed.elapsed()
        value = min(999, int(elapsed * 1000 / self._total_budget_ms))
        self.progress_bar.setValue(value)

    def estimate_problem_size(self, n, k, j, s):
<<<<<<< HEAD
        est = estimate_coverage_generation(n, k, j, s)
        est['relation_checks'] = est['optimized_coverage_entries']
        return est

    def get_precomputed_solution(self):
        n = self._safe_int(self.n_combo, 9)
        k = self._safe_int(self.k_combo, 6)
        j = self._safe_int(self.j_combo, 4)
        s = self._safe_int(self.s_combo, 4)
=======
        estimate = estimate_coverage_generation(n, k, j, s)
        estimate['relation_checks'] = estimate['optimized_coverage_entries']
        return estimate

    def get_precomputed_solution(self):
        """Return a trusted cached result before building the expensive solver object."""
        n = self.n_spin.value()
        k = self.k_spin.value()
        j = self.j_spin.value()
        s = self.s_spin.value()
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba

        cached = self.db_manager.get_project_result(n, k, j, s)
        if cached:
            groups = self.map_canonical_groups_to_samples(cached['groups'])
            if cached['status'] == "OPTIMAL":
                return groups, "OPTIMAL", "Project result cache"
            best_groups = groups
            best_status = cached['status']
            best_message = "Project result cache"
        else:
            best_groups = None
            best_status = "FEASIBLE"
            best_message = "Cached upper bound"

        standard_t = j if s == j else s
        standard = self.db_manager.get_standard_cover(n, k, standard_t)
        if standard:
            groups = self.map_canonical_groups_to_samples(standard['blocks'])
            if s == j and standard['is_proven_optimal']:
                self.db_manager.save_project_result(
                    n, k, j, s, standard['blocks'], "OPTIMAL",
                    method="La Jolla Covering Repository",
<<<<<<< HEAD
                    source=standard['source_url'])
                return groups, "OPTIMAL", "La Jolla exact cover cache"
=======
                    source=standard['source_url'],
                )
                return groups, "OPTIMAL", "La Jolla exact cover cache"

>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
            if best_groups is None or len(groups) < len(best_groups):
                best_groups = groups
                best_status = "FEASIBLE_CACHED"
                best_message = "La Jolla upper-bound cache"

        return best_groups, best_status, best_message

    def get_cached_solution_hint(self, solver):
<<<<<<< HEAD
        n = self._safe_int(self.n_combo, 9)
        k = self._safe_int(self.k_combo, 6)
        j = self._safe_int(self.j_combo, 4)
        s = self._safe_int(self.s_combo, 4)
=======
        """Return a cached exact result or a feasible hint for OR-Tools."""
        n = self.n_spin.value()
        k = self.k_spin.value()
        j = self.j_spin.value()
        s = self.s_spin.value()
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba

        cached = self.db_manager.get_project_result(n, k, j, s)
        if cached:
            groups = self.map_canonical_groups_to_samples(cached['groups'])
            if solver.verify_solution(groups):
                if cached['status'] == "OPTIMAL":
                    return groups, "OPTIMAL", "Project result cache"
                best_groups = groups
                best_status = cached['status']
            else:
                best_groups = None
                best_status = "FEASIBLE"
        else:
            best_groups = None
            best_status = "FEASIBLE"

        standard_t = j if s == j else s
        standard = self.db_manager.get_standard_cover(n, k, standard_t)
        if standard:
            groups = self.map_canonical_groups_to_samples(standard['blocks'])
            if solver.verify_solution(groups):
                if s == j and standard['is_proven_optimal']:
                    self.db_manager.save_project_result(
                        n, k, j, s, standard['blocks'], "OPTIMAL",
                        method="La Jolla Covering Repository",
<<<<<<< HEAD
                        source=standard['source_url'])
                    return groups, "OPTIMAL", "La Jolla exact cover cache"
=======
                        source=standard['source_url'],
                    )
                    return groups, "OPTIMAL", "La Jolla exact cover cache"

>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
                if best_groups is None or len(groups) < len(best_groups):
                    best_groups = groups
                    best_status = "FEASIBLE_CACHED"

        return best_groups, best_status, "Cached upper bound"

    def map_canonical_groups_to_samples(self, groups):
        samples = sorted(self.current_samples)
<<<<<<< HEAD
        return [tuple(samples[i - 1] for i in group) for group in groups]

    def map_sample_groups_to_canonical(self, groups):
        idx = {s: i + 1 for i, s in enumerate(sorted(self.current_samples))}
        return [tuple(sorted(idx[v] for v in group)) for group in groups]

    def on_solve_finished(self, result, solve_time, method, status):
        self._progress_timer.stop()
=======
        return [tuple(samples[index - 1] for index in group) for group in groups]

    def map_sample_groups_to_canonical(self, groups):
        index_by_sample = {sample: i + 1 for i, sample in enumerate(sorted(self.current_samples))}
        return [tuple(sorted(index_by_sample[value] for value in group)) for group in groups]

    def on_solve_finished(self, result, solve_time, method, status):
        """Handle solver completion."""
        self._progress_timer.stop()
        self.progress_bar.setValue(1000)
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
        self.progress_bar.setVisible(False)
        self.round_label.setVisible(False)
        self.solve_btn.setEnabled(True)
        self.current_results = result
<<<<<<< HEAD
=======

>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
        self.last_solve_time = solve_time
        self.last_method = method
        self.last_status = status

<<<<<<< HEAD
        sample_set = set(self.current_samples)
        if all(v in sample_set for group in result for v in group):
            canonical = self.map_sample_groups_to_canonical(result)
            self.db_manager.save_project_result(
                self._safe_int(self.n_combo, 9),
                self._safe_int(self.k_combo, 6),
                self._safe_int(self.j_combo, 4),
                self._safe_int(self.s_combo, 4),
                canonical, status, method=method, source="local solve/cache")

=======
        canonical_groups = self.map_sample_groups_to_canonical(result)
        self.db_manager.save_project_result(
            self.n_spin.value(), self.k_spin.value(), self.j_spin.value(), self.s_spin.value(),
            canonical_groups, status, method=method, source="local solve/cache",
        )

        # Update stats
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
        solver = getattr(self.solver_thread, 'solver', None) if self.solver_thread else None
        best_bound = getattr(solver, 'last_best_bound', None) if solver else None
        gap_str = ""
        if best_bound and best_bound > 0 and len(result) > 0:
<<<<<<< HEAD
            gap = (len(result) - best_bound) / len(result) * 100
            gap_str = f" ({gap:.1f}% gap)"

        # Update stat cards
        self._stat_groups.findChild(QLabel, "statVal").setText(str(len(result)))
        self._stat_time.findChild(QLabel, "statVal").setText(f"{solve_time:.1f}s")
        self._stat_status.findChild(QLabel, "statVal").setText(status[:8])

=======
            gap = (len(result) - best_bound) / best_bound * 100
            gap_str = f" | Gap: {gap:.1f}%"

        self.stats_label.setText(
            f"Method: {method} | Status: {status} | Time: {solve_time:.3f}s | "
            f"Groups found: {len(result)}{gap_str}"
        )

        # Update table
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
        display_rows = min(len(result), MAX_DISPLAYED_GROUPS)
        self.results_table.setRowCount(display_rows)
        for i, group in enumerate(result[:display_rows]):
            self.results_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
<<<<<<< HEAD
            self.results_table.setItem(
                i, 1, QTableWidgetItem(", ".join(map(str, group))))

        self._results_placeholder.setVisible(False)
        self.results_table.setVisible(True)

        self.save_btn.setEnabled(True)
        self.print_btn.setEnabled(True)
        msg = (f"Found {len(result)} groups in {solve_time:.3f}s  |  "
               f"Method: {method}  |  Status: {status}{gap_str}")
        if len(result) > MAX_DISPLAYED_GROUPS:
            msg += f"  |  Showing first {MAX_DISPLAYED_GROUPS}"
        self.status_bar.showMessage(msg)

    def on_solve_error(self, error_msg):
=======
            self.results_table.setItem(i, 1, QTableWidgetItem(", ".join(map(str, group))))

        if len(result) > MAX_DISPLAYED_GROUPS:
            self.stats_label.setText(
                self.stats_label.text() +
                f" | Showing first {MAX_DISPLAYED_GROUPS} rows"
            )

        self.save_btn.setEnabled(True)
        if status == "OPTIMAL":
            self.status_bar.showMessage(f"Found {len(result)} proven optimal groups in {solve_time:.3f}s using {method}")
        else:
            self.status_bar.showMessage(f"Found {len(result)} feasible groups in {solve_time:.3f}s using {method}; optimality not proven")

    def on_solve_error(self, error_msg):
        """Handle solver error."""
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
        self._progress_timer.stop()
        self.progress_bar.setVisible(False)
        self.round_label.setVisible(False)
        self.solve_btn.setEnabled(True)
        QMessageBox.critical(self, "Solver Error", error_msg)
        self.status_bar.showMessage("Solver failed")

    def save_results(self):
<<<<<<< HEAD
        if not self.current_results:
            QMessageBox.warning(self, "Error", "No results to save.")
            return
        m = self._safe_int(self.m_combo, 45)
        n = self._safe_int(self.n_combo, 9)
        k = self._safe_int(self.k_combo, 6)
        j = self._safe_int(self.j_combo, 4)
        s = self._safe_int(self.s_combo, 4)
        try:
            filename = self.db_manager.save_result(
                m, n, k, j, s,
                self.current_samples, self.current_results,
                self.last_solve_time, self.last_method or "ILP",
                self.last_status or "UNKNOWN")
            QMessageBox.information(self, "Success", f"Saved to: {filename}")
            self.refresh_db_list()
            self.status_bar.showMessage(f"Saved to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {e}")

    def clear_all(self):
        self.current_samples = []
        self.current_results = []
        self._pool_selected.clear()
        self._refresh_pool_display()
        self.samples_display.clear()
        self.results_table.setRowCount(0)
        self.results_table.setVisible(False)
        self._results_placeholder.setVisible(True)
        self._stat_groups.findChild(QLabel, "statVal").setText("—")
        self._stat_time.findChild(QLabel, "statVal").setText("—")
        self._stat_status.findChild(QLabel, "statVal").setText("—")
        self.save_btn.setEnabled(False)
        self.print_btn.setEnabled(False)
        self.status_bar.showMessage("Cleared")

    # ── Database operations ───────────────────────────────────────────────────

    def refresh_db_list(self):
        results = self.db_manager.list_results()
        self.db_list.setRowCount(len(results))
        for i, r in enumerate(results):
            item = QTableWidgetItem(r['filename'].replace('.db', ''))
            item.setData(Qt.UserRole, r['filename'])
            self.db_list.setItem(i, 0, item)

    def load_from_db(self):
=======
        """Save current results to database."""
        if not self.current_results:
            QMessageBox.warning(self, "Error", "No results to save.")
            return

        m = self.m_spin.value()
        n = self.n_spin.value()
        k = self.k_spin.value()
        j = self.j_spin.value()
        s = self.s_spin.value()

        try:
            filename = self.db_manager.save_result(
                m, n, k, j, s,
                self.current_samples,
                self.current_results,
                self.last_solve_time,  # solve_time
                self.last_method or "ILP",  # method
                self.last_status or "UNKNOWN",
            )
            QMessageBox.information(self, "Success", f"Results saved to: {filename}")
            self.refresh_db_list()
            self.status_bar.showMessage(f"Saved to {filename}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")

    def clear_all(self):
        """Clear all inputs and results."""
        self.current_samples = []
        self.current_results = []
        self.samples_display.clear()
        self.manual_input.clear()
        self.results_table.setRowCount(0)
        self.stats_label.setText("")
        self.save_btn.setEnabled(False)
        self.status_bar.showMessage("Cleared")

    def refresh_db_list(self):
        """Refresh the database list."""
        results = self.db_manager.list_results()
        self.db_list.setRowCount(len(results))

        for i, r in enumerate(results):
            self.db_list.setItem(i, 0, QTableWidgetItem(r['filename']))
            self.db_list.setItem(i, 1, QTableWidgetItem(str(r['m'])))
            self.db_list.setItem(i, 2, QTableWidgetItem(str(r['n'])))
            self.db_list.setItem(i, 3, QTableWidgetItem(str(r['k'])))
            self.db_list.setItem(i, 4, QTableWidgetItem(str(r['j'])))
            self.db_list.setItem(i, 5, QTableWidgetItem(str(r['s'])))
            self.db_list.setItem(i, 6, QTableWidgetItem(str(r['run'])))
            self.db_list.setItem(i, 7, QTableWidgetItem(str(r['num_groups'])))

    def load_from_db(self):
        """Load selected result from database."""
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
        selected = self.db_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Error", "Please select a result to load.")
            return
<<<<<<< HEAD
        row = selected[0].row()
        filename = self.db_list.item(row, 0).data(Qt.UserRole)
        result = self.db_manager.load_result(filename)
        if not result:
            QMessageBox.critical(self, "Error", "Failed to load result.")
            return

        self.m_combo.setCurrentText(str(result['m']))
        self.n_combo.setCurrentText(str(result['n']))
        self.k_combo.setCurrentText(str(result['k']))
        self.j_combo.setCurrentText(str(result['j']))
        self.s_combo.setCurrentText(str(result['s']))
        self.current_samples = result['samples']
        self._pool_selected = set(result['samples'])
        self._rebuild_pool()
        self.samples_display.setText(", ".join(map(str, result['samples'])))
        self.current_results = result['groups']
        self.last_solve_time = result['solve_time']
        self.last_method = result['method']
        self.last_status = result.get('status', 'UNKNOWN')

        display_groups = result['groups'][:MAX_DISPLAYED_GROUPS]
        self.results_table.setRowCount(len(display_groups))
        for i, group in enumerate(display_groups):
            self.results_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.results_table.setItem(
                i, 1, QTableWidgetItem(", ".join(map(str, group))))
        self._results_placeholder.setVisible(False)
        self.results_table.setVisible(True)
        self._stat_groups.findChild(QLabel, "statVal").setText(str(result['num_groups']))
        self._stat_time.findChild(QLabel, "statVal").setText(f"{result['solve_time']:.1f}s")
        self._stat_status.findChild(QLabel, "statVal").setText(
            self.last_status[:8])
        self.save_btn.setEnabled(True)
        self.print_btn.setEnabled(True)
        self.status_bar.showMessage(f"Loaded {filename} into Computation tab")

    def delete_from_db(self):
=======

        row = selected[0].row()
        filename = self.db_list.item(row, 0).text()

        result = self.db_manager.load_result(filename)
        if result:
            # Display in preview
            preview_text = f"File: {filename}\n"
            preview_text += f"Parameters: m={result['m']}, n={result['n']}, k={result['k']}, j={result['j']}, s={result['s']}\n"
            preview_text += f"Samples: {result['samples']}\n"
            preview_text += f"Method: {result['method']} | Status: {result.get('status', 'UNKNOWN')} | Time: {result['solve_time']:.3f}s\n"
            preview_text += f"Created: {result['created_at']}\n\n"
            preview_text += f"Groups ({result['num_groups']} total):\n"
            preview_groups = result['groups'][:MAX_DISPLAYED_GROUPS]
            for i, group in enumerate(preview_groups):
                preview_text += f"  {i+1}. {', '.join(map(str, group))}\n"
            if len(result['groups']) > MAX_DISPLAYED_GROUPS:
                preview_text += f"\nShowing first {MAX_DISPLAYED_GROUPS} groups only.\n"

            self.preview_text.setText(preview_text)

            # Also load into main tab
            self.m_spin.setValue(result['m'])
            self.n_spin.setValue(result['n'])
            self.k_spin.setValue(result['k'])
            self.j_spin.setValue(result['j'])
            self.s_spin.setValue(result['s'])
            self.current_samples = result['samples']
            self.samples_display.setText(", ".join(map(str, result['samples'])))
            self.current_results = result['groups']

            self.last_solve_time = result['solve_time']
            self.last_method = result['method']
            self.last_status = result.get('status', 'UNKNOWN')

            display_groups = result['groups'][:MAX_DISPLAYED_GROUPS]
            self.results_table.setRowCount(len(display_groups))
            for i, group in enumerate(display_groups):
                self.results_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                self.results_table.setItem(i, 1, QTableWidgetItem(", ".join(map(str, group))))

            display_note = (
                f" | Showing first {MAX_DISPLAYED_GROUPS}"
                if len(result['groups']) > MAX_DISPLAYED_GROUPS else ""
            )
            self.stats_label.setText(
                f"Loaded from DB | Status: {self.last_status} | Groups: {result['num_groups']}{display_note}"
            )
            self.save_btn.setEnabled(True)
            self.tab_widget.setCurrentIndex(0)

            self.status_bar.showMessage(f"Loaded {filename}")
        else:
            QMessageBox.critical(self, "Error", "Failed to load result.")

    def delete_from_db(self):
        """Delete selected result from database."""
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
        selected = self.db_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Error", "Please select a result to delete.")
            return
<<<<<<< HEAD
        row = selected[0].row()
        filename = self.db_list.item(row, 0).data(Qt.UserRole)
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete {filename}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.db_manager.delete_result(filename):
                self.refresh_db_list()
                self._clear_db_detail()
                self.status_bar.showMessage(f"Deleted {filename}")
            else:
                QMessageBox.critical(self, "Error", "Failed to delete file.")

    # ── DB detail panel ───────────────────────────────────────────────────────

    def _on_db_row_clicked(self, row: int, _column: int):
        self._display_selected_db()

    def _display_selected_db(self):
        selected = self.db_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Error", "Please select a record to display.")
            return
        row = selected[0].row()
        filename = self.db_list.item(row, 0).data(Qt.UserRole)
        result = self.db_manager.load_result(filename)
        if not result:
            QMessageBox.critical(self, "Error", "Failed to load the selected record.")
            return

        # Update header
        display_name = filename.replace('.db', '')
        self.detail_file_label.setText(
            f"{display_name}    "
            f"m={result['m']}  n={result['n']}  "
            f"k={result['k']}  j={result['j']}  s={result['s']}")

        # Update stat cards
        self._db_stat_groups.findChild(QLabel, "statVal").setText(
            str(result['num_groups']))
        self._db_stat_time.findChild(QLabel, "statVal").setText(
            f"{result['solve_time']:.1f}s")
        self._db_stat_status.findChild(QLabel, "statVal").setText(
            result.get('status', 'UNK')[:8])

        # Update pool chips
        while self._db_pool_chip_container.count():
            item = self._db_pool_chip_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for num in result['samples']:
            chip = QLabel(str(num))
            chip.setFixedSize(30, 22)
            chip.setAlignment(Qt.AlignCenter)
            chip.setStyleSheet(
                f"background:{C_SEL}; color:{C_ACCENT}; border-radius:4px;"
                f"font-size:10px; font-weight:bold;")
            self._db_pool_chip_container.addWidget(chip)

        # Clear old group cards
        while self._grp_card_layout.count():
            item = self._grp_card_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Build group cards (max 200 for performance)
        groups = result['groups'][:200]
        COLS = 3
        for idx, group in enumerate(groups):
            card = self._make_group_card(idx + 1, group)
            self._grp_card_layout.addWidget(card, idx // COLS, idx % COLS)

        if result['num_groups'] > 200:
            note = QLabel(
                f"Showing first 200 of {result['num_groups']} groups")
            note.setStyleSheet(
                f"color:{C_MUTED}; font-size:10px; font-style:italic;")
            note.setAlignment(Qt.AlignCenter)
            self._grp_card_layout.addWidget(
                note, len(groups) // COLS + 1, 0, 1, COLS)

        self._db_placeholder.setVisible(False)
        self.detail_group.setVisible(True)
        self.status_bar.showMessage(f"Displaying {filename}")

    def _make_group_card(self, idx: int, group: tuple) -> QWidget:
        card = QWidget()
        card.setStyleSheet(
            f"background:{C_CARD}; border:1px solid {C_BORDER};"
            f"border-radius:8px;")
        cv = QVBoxLayout(card)
        cv.setContentsMargins(10, 8, 10, 8)
        cv.setSpacing(6)

        hdr = QHBoxLayout()
        grp_lbl = QLabel("Group")
        grp_lbl.setStyleSheet(f"color:{C_MUTED}; font-size:10px;")
        num_lbl = QLabel(f"#{idx:02d}")
        num_lbl.setStyleSheet(
            f"color:{C_ACCENT}; font-size:10px; font-weight:bold;")
        hdr.addWidget(grp_lbl)
        hdr.addStretch()
        hdr.addWidget(num_lbl)
        cv.addLayout(hdr)

        chips_row = QHBoxLayout()
        chips_row.setSpacing(4)
        for num in group:
            chip = QLabel(str(num))
            chip.setFixedSize(28, 22)
            chip.setAlignment(Qt.AlignCenter)
            chip.setStyleSheet(
                f"background:{C_BG}; color:{C_TEXT}; border-radius:4px;"
                f"font-size:11px; border:1px solid {C_BORDER};")
            chips_row.addWidget(chip)
        chips_row.addStretch()
        cv.addLayout(chips_row)
        return card

    def _clear_db_detail(self):
        self.detail_group.setVisible(False)
        self._db_placeholder.setVisible(True)
        while self._grp_card_layout.count():
            item = self._grp_card_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        while self._db_pool_chip_container.count():
            item = self._db_pool_chip_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.detail_file_label.setText("")

    # ── Print / Export ────────────────────────────────────────────────────────

    def print_results(self):
        if not self.current_results:
            QMessageBox.warning(self, "Error", "No results to export.")
            return
        m = self._safe_int(self.m_combo, 45)
        n = self._safe_int(self.n_combo, 9)
        k = self._safe_int(self.k_combo, 6)
        j = self._safe_int(self.j_combo, 4)
        s = self._safe_int(self.s_combo, 4)
        default_name = f"{m}-{n}-{k}-{j}-{s}-results.txt"
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Export Results", default_name,
            "Text Files (*.txt);;All Files (*)")
        if not filepath:
            return
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("An Optimal Samples Selection System\n")
                f.write("=" * 44 + "\n")
                f.write(f"Parameters : m={m}, n={n}, k={k}, j={j}, s={s}\n")
                f.write(f"Samples ({n}): {', '.join(map(str, self.current_samples))}\n")
                f.write(f"Method     : {self.last_method}\n")
                f.write(f"Status     : {self.last_status}\n")
                f.write(f"Total Groups: {len(self.current_results)}\n")
                f.write("=" * 44 + "\n\n")
                for i, group in enumerate(self.current_results):
                    f.write(f"Group {i + 1:>4d}: {', '.join(map(str, group))}\n")
            QMessageBox.information(
                self, "Export Successful", f"Saved to:\n{filepath}")
            self.status_bar.showMessage(f"Exported to {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed:\n{e}")

    def print_db_result(self):
        selected = self.db_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Error", "Please select a record to export.")
            return
        row = selected[0].row()
        filename = self.db_list.item(row, 0).data(Qt.UserRole)
        result = self.db_manager.load_result(filename)
        if not result:
            QMessageBox.critical(self, "Error", "Failed to load the selected record.")
            return
        default_name = filename.replace('.db', '.txt')
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Export DB Record", default_name,
            "Text Files (*.txt);;All Files (*)")
        if not filepath:
            return
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("An Optimal Samples Selection System\n")
                f.write("=" * 44 + "\n")
                f.write(f"File       : {filename}\n")
                f.write(f"Parameters : m={result['m']}, n={result['n']}, "
                        f"k={result['k']}, j={result['j']}, s={result['s']}\n")
                f.write(f"Samples ({result['n']}): "
                        f"{', '.join(map(str, result['samples']))}\n")
                f.write(f"Method     : {result['method']}\n")
                f.write(f"Status     : {result.get('status', 'UNKNOWN')}\n")
                f.write(f"Created    : {result['created_at']}\n")
                f.write(f"Total Groups: {result['num_groups']}\n")
                f.write("=" * 44 + "\n\n")
                for i, group in enumerate(result['groups']):
                    f.write(f"Group {i + 1:>4d}: {', '.join(map(str, group))}\n")
            QMessageBox.information(
                self, "Export Successful", f"Saved to:\n{filepath}")
            self.status_bar.showMessage(f"Exported to {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed:\n{e}")
=======

        row = selected[0].row()
        filename = self.db_list.item(row, 0).text()

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete {filename}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.db_manager.delete_result(filename):
                self.refresh_db_list()
                self.preview_text.clear()
                self.status_bar.showMessage(f"Deleted {filename}")
            else:
                QMessageBox.critical(self, "Error", "Failed to delete file.")
>>>>>>> 311a0a2c5536d8f6c482ee28606985489c1947ba
