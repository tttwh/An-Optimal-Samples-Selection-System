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
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIntValidator

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.solver import OptimalSamplesSolver
from database.db_manager import DatabaseManager


class SolverThread(QThread):
    """Background thread for running the solver."""
    finished = pyqtSignal(list, float, str)
    error = pyqtSignal(str)
    progress = pyqtSignal(int, int, int)

    def __init__(self, solver):
        super().__init__()
        self.solver = solver

    def run(self):
        try:
            result, solve_time, method = self.solver.solve_ilp(
                progress_callback=lambda d, c, b: self.progress.emit(d, c, b)
            )
            self.finished.emit(result, solve_time, method)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.current_samples = []
        self.current_results = []
        self.solver_thread = None

        self.last_solve_time = 0.0
        self.last_method = ""

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

        # Add labels and spinboxes
        param_layout.addWidget(QLabel("m (Total samples, 45-54):"), 0, 0)
        param_layout.addWidget(self.m_spin, 0, 1)

        param_layout.addWidget(QLabel("n (Select samples, 7-25):"), 1, 0)
        param_layout.addWidget(self.n_spin, 1, 1)

        param_layout.addWidget(QLabel("k (Group size, 4-7):"), 2, 0)
        param_layout.addWidget(self.k_spin, 2, 1)

        param_layout.addWidget(QLabel("j (Subset size, s≤j≤k):"), 3, 0)
        param_layout.addWidget(self.j_spin, 3, 1)

        param_layout.addWidget(QLabel("s (Min overlap, 3-7):"), 4, 0)
        param_layout.addWidget(self.s_spin, 4, 1)

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

        # Results section
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout(results_group)

        # Statistics
        self.stats_label = QLabel("")
        results_layout.addWidget(self.stats_label)

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
            solver = OptimalSamplesSolver(n, k, j, s, self.current_samples)
            stats = solver.get_statistics()

            self.status_bar.showMessage(f"Solving... (j-subsets: {stats['num_j_subsets']}, k-groups: {stats['num_k_groups']})")
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate
            self.solve_btn.setEnabled(False)

            # Run solver in background thread
            self.solver_thread = SolverThread(solver)
            self.solver_thread.finished.connect(self.on_solve_finished)
            self.solver_thread.error.connect(self.on_solve_error)
            self.solver_thread.start()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def on_solve_finished(self, result, solve_time, method):
        """Handle solver completion."""
        self.progress_bar.setVisible(False)
        self.solve_btn.setEnabled(True)
        self.current_results = result

        self.last_solve_time = solve_time
        self.last_method = method

        # Update stats
        self.stats_label.setText(
            f"Method: {method} | Time: {solve_time:.3f}s | Groups found: {len(result)}"
        )

        # Update table
        self.results_table.setRowCount(len(result))
        for i, group in enumerate(result):
            self.results_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.results_table.setItem(i, 1, QTableWidgetItem(", ".join(map(str, group))))

        self.save_btn.setEnabled(True)
        self.status_bar.showMessage(f"Found {len(result)} optimal groups in {solve_time:.3f}s using {method}")

    def on_solve_error(self, error_msg):
        """Handle solver error."""
        self.progress_bar.setVisible(False)
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
                self.last_method or "ILP"  # method
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
            preview_text += f"Method: {result['method']} | Time: {result['solve_time']:.3f}s\n"
            preview_text += f"Created: {result['created_at']}\n\n"
            preview_text += f"Groups ({result['num_groups']} total):\n"
            for i, group in enumerate(result['groups']):
                preview_text += f"  {i+1}. {', '.join(map(str, group))}\n"

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

            self.results_table.setRowCount(len(result['groups']))
            for i, group in enumerate(result['groups']):
                self.results_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                self.results_table.setItem(i, 1, QTableWidgetItem(", ".join(map(str, group))))

            self.stats_label.setText(f"Loaded from DB | Groups: {result['num_groups']}")
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
