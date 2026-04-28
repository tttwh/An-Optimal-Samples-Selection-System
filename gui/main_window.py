"""
Main Window for the Optimal Samples Selection System.

Provides a user-friendly GUI for:
- Parameter input (m, n, k, j, s)
- Sample selection (random or manual)
- Result display
- Database operations
"""

import sys
import random
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QSpinBox, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem,
    QGroupBox, QRadioButton, QLineEdit, QMessageBox, QStatusBar,
    QTabWidget, QListWidget, QListWidgetItem, QSplitter, QProgressBar,
    QComboBox, QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal, QElapsedTimer
from PyQt5.QtGui import QFont, QIntValidator

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.solver import OptimalSamplesSolver, estimate_coverage_generation
from database.db_manager import DatabaseManager


MAX_GUI_COVER_RELATION_CHECKS = 20_000_000
MAX_DISPLAYED_GROUPS = 5000


class SolverThread(QThread):
    """Background thread for running the solver (supports multi-round training)."""
    finished = pyqtSignal(list, float, str, str)
    error = pyqtSignal(str)
    progress = pyqtSignal(int, int, int)
    round_progress = pyqtSignal(int, int, int)  # current_round, total_rounds, best_size

    TIME_LIMIT_PER_ROUND = 70.0

    def __init__(self, solver, initial_solution=None, initial_solution_status="FEASIBLE",
                 num_rounds=1):
        super().__init__()
        self.solver = solver
        self.initial_solution = initial_solution
        self.initial_solution_status = initial_solution_status
        self.num_rounds = max(1, num_rounds)

    def run(self):
        try:
            import time as _time
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
                    relative_gap_limit=0.10,
                )
                total_time += solve_time
                current_status = self.solver.last_status

                if best_result is None or len(result) < len(best_result):
                    best_result = result
                    best_status = current_status
                    best_method = f"{method} (round {rnd}/{self.num_rounds})"

                self.round_progress.emit(rnd, self.num_rounds,
                                         len(best_result) if best_result else -1)

                if current_status == "OPTIMAL":
                    break

            self.finished.emit(best_result, total_time, best_method, best_status)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.db_manager.seed_builtin_known_covers()
        self.current_samples = []
        self.current_results = []
        self.solver_thread = None

        self.last_solve_time = 0.0
        self.last_method = ""
        self.last_status = "NOT_SOLVED"

        self._progress_timer = QTimer(self)
        self._progress_timer.setInterval(8)
        self._progress_timer.timeout.connect(self._tick_progress)
        self._elapsed = QElapsedTimer()
        self._total_budget_ms = 0

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
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

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
                return

            estimate = self.estimate_problem_size(n, k, j, s)
            if estimate['relation_checks'] > MAX_GUI_COVER_RELATION_CHECKS:
                if cached_solution:
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
                return

            solver = OptimalSamplesSolver(n, k, j, s, self.current_samples)
            stats = solver.get_statistics()
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
            self.round_label.setText(f"Round 0 / {r}")
            self.round_label.setVisible(True)
            self.solve_btn.setEnabled(False)
            self._elapsed.start()
            self._progress_timer.start()

            # Run solver in background thread
            self.solver_thread = SolverThread(solver, initial_solution, initial_status,
                                              num_rounds=r)
            self.solver_thread.finished.connect(self.on_solve_finished)
            self.solver_thread.error.connect(self.on_solve_error)
            self.solver_thread.round_progress.connect(self.on_round_progress)
            self.solver_thread.start()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def on_round_progress(self, current_round, total_rounds, best_size):
        """Update round label after each training round completes."""
        size_str = f" | Best so far: {best_size}" if best_size >= 0 else ""
        self.round_label.setText(f"Round {current_round} / {total_rounds}{size_str}")
        self.status_bar.showMessage(f"Completed round {current_round} / {total_rounds}...")

    def _tick_progress(self):
        """Advance the progress bar based on elapsed wall-clock time."""
        if self._total_budget_ms <= 0:
            return
        elapsed = self._elapsed.elapsed()
        value = min(999, int(elapsed * 1000 / self._total_budget_ms))
        self.progress_bar.setValue(value)

    def estimate_problem_size(self, n, k, j, s):
        estimate = estimate_coverage_generation(n, k, j, s)
        estimate['relation_checks'] = estimate['optimized_coverage_entries']
        return estimate

    def get_precomputed_solution(self):
        """Return a trusted cached result before building the expensive solver object."""
        n = self.n_spin.value()
        k = self.k_spin.value()
        j = self.j_spin.value()
        s = self.s_spin.value()

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
                    source=standard['source_url'],
                )
                return groups, "OPTIMAL", "La Jolla exact cover cache"

            if best_groups is None or len(groups) < len(best_groups):
                best_groups = groups
                best_status = "FEASIBLE_CACHED"
                best_message = "La Jolla upper-bound cache"

        return best_groups, best_status, best_message

    def get_cached_solution_hint(self, solver):
        """Return a cached exact result or a feasible hint for OR-Tools."""
        n = self.n_spin.value()
        k = self.k_spin.value()
        j = self.j_spin.value()
        s = self.s_spin.value()

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
                        source=standard['source_url'],
                    )
                    return groups, "OPTIMAL", "La Jolla exact cover cache"

                if best_groups is None or len(groups) < len(best_groups):
                    best_groups = groups
                    best_status = "FEASIBLE_CACHED"

        return best_groups, best_status, "Cached upper bound"

    def map_canonical_groups_to_samples(self, groups):
        samples = sorted(self.current_samples)
        return [tuple(samples[index - 1] for index in group) for group in groups]

    def map_sample_groups_to_canonical(self, groups):
        index_by_sample = {sample: i + 1 for i, sample in enumerate(sorted(self.current_samples))}
        return [tuple(sorted(index_by_sample[value] for value in group)) for group in groups]

    def on_solve_finished(self, result, solve_time, method, status):
        """Handle solver completion."""
        self._progress_timer.stop()
        self.progress_bar.setValue(1000)
        self.progress_bar.setVisible(False)
        self.round_label.setVisible(False)
        self.solve_btn.setEnabled(True)
        self.current_results = result

        self.last_solve_time = solve_time
        self.last_method = method
        self.last_status = status

        canonical_groups = self.map_sample_groups_to_canonical(result)
        self.db_manager.save_project_result(
            self.n_spin.value(), self.k_spin.value(), self.j_spin.value(), self.s_spin.value(),
            canonical_groups, status, method=method, source="local solve/cache",
        )

        # Update stats
        solver = getattr(self.solver_thread, 'solver', None) if self.solver_thread else None
        best_bound = getattr(solver, 'last_best_bound', None) if solver else None
        gap_str = ""
        if best_bound and best_bound > 0 and len(result) > 0:
            gap = (len(result) - best_bound) / best_bound * 100
            gap_str = f" | Gap: {gap:.1f}%"

        self.stats_label.setText(
            f"Method: {method} | Status: {status} | Time: {solve_time:.3f}s | "
            f"Groups found: {len(result)}{gap_str}"
        )

        # Update table
        display_rows = min(len(result), MAX_DISPLAYED_GROUPS)
        self.results_table.setRowCount(display_rows)
        for i, group in enumerate(result[:display_rows]):
            self.results_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
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
        self._progress_timer.stop()
        self.progress_bar.setVisible(False)
        self.round_label.setVisible(False)
        self.solve_btn.setEnabled(True)
        QMessageBox.critical(self, "Solver Error", error_msg)
        self.status_bar.showMessage("Solver failed")

    def save_results(self):
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
        selected = self.db_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Error", "Please select a result to load.")
            return

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
        selected = self.db_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Error", "Please select a result to delete.")
            return

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
