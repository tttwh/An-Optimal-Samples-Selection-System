"""
Database manager for storing and retrieving results.

Uses SQLite for lightweight file-based storage.
File naming format: {m}-{n}-{k}-{j}-{s}-{x}-{y}.db
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Tuple, Optional
from pathlib import Path


class DatabaseManager:
    """Manager for storing and retrieving optimal samples selection results."""

    def __init__(self, db_folder: str = None):
        """
        Initialize database manager.

        Args:
            db_folder: Folder to store database files. Defaults to 'results' in current directory.
        """
        if db_folder is None:
            db_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')

        self.db_folder = db_folder
        os.makedirs(self.db_folder, exist_ok=True)

    def _get_db_filename(self, m: int, n: int, k: int, j: int, s: int, run_number: int, num_results: int) -> str:
        """Generate database filename according to format: m-n-k-j-s-x-y.db"""
        return f"{m}-{n}-{k}-{j}-{s}-{run_number}-{num_results}.db"

    def _get_next_run_number(self, m: int, n: int, k: int, j: int, s: int) -> int:
        """Get the next run number for given parameters."""
        prefix = f"{m}-{n}-{k}-{j}-{s}-"
        existing_files = [f for f in os.listdir(self.db_folder) if f.startswith(prefix) and f.endswith('.db')]

        if not existing_files:
            return 1

        max_run = 0
        for f in existing_files:
            try:
                parts = f.replace('.db', '').split('-')
                if len(parts) >= 6:
                    run_num = int(parts[5])
                    max_run = max(max_run, run_num)
            except (ValueError, IndexError):
                continue

        return max_run + 1

    def save_result(self, m: int, n: int, k: int, j: int, s: int,
                    samples: List[int], groups: List[Tuple],
                    solve_time: float, method: str) -> str:
        """
        Save a result to database.

        Args:
            m: Total sample pool size
            n: Number of selected samples
            k: Group size
            j: Subset size
            s: Minimum overlap
            samples: The n selected samples
            groups: The optimal k-groups
            solve_time: Time taken to solve
            method: Algorithm used

        Returns:
            The database filename created
        """
        num_results = len(groups)
        run_number = self._get_next_run_number(m, n, k, j, s)
        filename = self._get_db_filename(m, n, k, j, s, run_number, num_results)
        filepath = os.path.join(self.db_folder, filename)

        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                id INTEGER PRIMARY KEY,
                m INTEGER,
                n INTEGER,
                k INTEGER,
                j INTEGER,
                s INTEGER,
                samples TEXT,
                solve_time REAL,
                method TEXT,
                created_at TEXT,
                num_groups INTEGER
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY,
                group_index INTEGER,
                members TEXT
            )
        ''')

        # Insert metadata
        cursor.execute('''
            INSERT INTO metadata (m, n, k, j, s, samples, solve_time, method, created_at, num_groups)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (m, n, k, j, s, json.dumps(samples), solve_time, method,
              datetime.now().isoformat(), num_results))

        # Insert groups
        for idx, group in enumerate(groups):
            cursor.execute('''
                INSERT INTO groups (group_index, members)
                VALUES (?, ?)
            ''', (idx + 1, json.dumps(list(group))))

        conn.commit()
        conn.close()

        return filename

    def load_result(self, filename: str) -> Optional[dict]:
        """
        Load a result from database file.

        Args:
            filename: The database filename

        Returns:
            Dictionary with result data or None if not found
        """
        filepath = os.path.join(self.db_folder, filename)

        if not os.path.exists(filepath):
            return None

        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()

        try:
            # Get metadata
            cursor.execute('SELECT * FROM metadata LIMIT 1')
            meta_row = cursor.fetchone()

            if not meta_row:
                return None

            # Get groups
            cursor.execute('SELECT group_index, members FROM groups ORDER BY group_index')
            group_rows = cursor.fetchall()

            result = {
                'm': meta_row[1],
                'n': meta_row[2],
                'k': meta_row[3],
                'j': meta_row[4],
                's': meta_row[5],
                'samples': json.loads(meta_row[6]),
                'solve_time': meta_row[7],
                'method': meta_row[8],
                'created_at': meta_row[9],
                'num_groups': meta_row[10],
                'groups': [tuple(json.loads(row[1])) for row in group_rows]
            }

            return result

        except sqlite3.Error:
            return None
        finally:
            conn.close()

    def list_results(self) -> List[dict]:
        """
        List all saved results.

        Returns:
            List of dictionaries with result summaries
        """
        results = []

        for filename in os.listdir(self.db_folder):
            if not filename.endswith('.db'):
                continue

            try:
                parts = filename.replace('.db', '').split('-')
                if len(parts) >= 7:
                    results.append({
                        'filename': filename,
                        'm': int(parts[0]),
                        'n': int(parts[1]),
                        'k': int(parts[2]),
                        'j': int(parts[3]),
                        's': int(parts[4]),
                        'run': int(parts[5]),
                        'num_groups': int(parts[6])
                    })
            except (ValueError, IndexError):
                continue

        # Sort by creation time (newest first)
        results.sort(key=lambda x: (x['m'], x['n'], x['k'], x['j'], x['s'], -x['run']))

        return results

    def delete_result(self, filename: str) -> bool:
        """
        Delete a result file.

        Args:
            filename: The database filename to delete

        Returns:
            True if deleted, False otherwise
        """
        filepath = os.path.join(self.db_folder, filename)

        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False

    def get_db_folder(self) -> str:
        """Return the database folder path."""
        return self.db_folder
