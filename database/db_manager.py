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
                    solve_time: float, method: str, status: str = "UNKNOWN") -> str:
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
                status TEXT,
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
            INSERT INTO metadata (m, n, k, j, s, samples, solve_time, method, status, created_at, num_groups)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (m, n, k, j, s, json.dumps(samples), solve_time, method, status,
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

            cursor.execute('PRAGMA table_info(metadata)')
            columns = [row[1] for row in cursor.fetchall()]
            meta = dict(zip(columns, meta_row))

            result = {
                'm': meta['m'],
                'n': meta['n'],
                'k': meta['k'],
                'j': meta['j'],
                's': meta['s'],
                'samples': json.loads(meta['samples']),
                'solve_time': meta['solve_time'],
                'method': meta['method'],
                'status': meta.get('status', 'UNKNOWN'),
                'created_at': meta['created_at'],
                'num_groups': meta['num_groups'],
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

    def _known_covers_path(self) -> str:
        return os.path.join(self.db_folder, 'known_covers.sqlite')

    def _connect_known_covers(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._known_covers_path())
        conn.execute('''
            CREATE TABLE IF NOT EXISTS standard_covers (
                v INTEGER NOT NULL,
                k INTEGER NOT NULL,
                t INTEGER NOT NULL,
                lower_bound INTEGER,
                upper_bound INTEGER NOT NULL,
                is_proven_optimal INTEGER NOT NULL DEFAULT 0,
                blocks TEXT NOT NULL,
                source_url TEXT,
                source_updated_at TEXT,
                construction_method TEXT,
                created_at TEXT NOT NULL,
                PRIMARY KEY (v, k, t)
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS project_results (
                n INTEGER NOT NULL,
                k INTEGER NOT NULL,
                j INTEGER NOT NULL,
                s INTEGER NOT NULL,
                num_groups INTEGER NOT NULL,
                status TEXT NOT NULL,
                method TEXT,
                groups TEXT NOT NULL,
                source TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (n, k, j, s)
            )
        ''')
        return conn

    def save_standard_cover(self, v: int, k: int, t: int, lower_bound: int,
                            upper_bound: int, blocks: List[Tuple],
                            is_proven_optimal: bool = False,
                            source_url: str = None,
                            source_updated_at: str = None,
                            construction_method: str = None) -> None:
        conn = self._connect_known_covers()
        try:
            conn.execute('''
                INSERT OR REPLACE INTO standard_covers
                (v, k, t, lower_bound, upper_bound, is_proven_optimal, blocks,
                 source_url, source_updated_at, construction_method, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                v, k, t, lower_bound, upper_bound, int(is_proven_optimal),
                json.dumps([list(block) for block in blocks]),
                source_url, source_updated_at, construction_method,
                datetime.now().isoformat(),
            ))
            conn.commit()
        finally:
            conn.close()

    def get_standard_cover(self, v: int, k: int, t: int) -> Optional[dict]:
        conn = self._connect_known_covers()
        try:
            cursor = conn.execute('''
                SELECT v, k, t, lower_bound, upper_bound, is_proven_optimal,
                       blocks, source_url, source_updated_at, construction_method
                FROM standard_covers
                WHERE v = ? AND k = ? AND t = ?
            ''', (v, k, t))
            row = cursor.fetchone()
            if not row:
                return None
            return {
                'v': row[0],
                'k': row[1],
                't': row[2],
                'lower_bound': row[3],
                'upper_bound': row[4],
                'is_proven_optimal': bool(row[5]),
                'blocks': [tuple(block) for block in json.loads(row[6])],
                'source_url': row[7],
                'source_updated_at': row[8],
                'construction_method': row[9],
            }
        finally:
            conn.close()

    def save_project_result(self, n: int, k: int, j: int, s: int,
                            groups: List[Tuple], status: str,
                            method: str = None, source: str = None) -> None:
        existing = self.get_project_result(n, k, j, s)
        if existing and not self._should_replace_project_result(existing, len(groups), status):
            return

        now = datetime.now().isoformat()
        created_at = existing['created_at'] if existing else now

        conn = self._connect_known_covers()
        try:
            conn.execute('''
                INSERT OR REPLACE INTO project_results
                (n, k, j, s, num_groups, status, method, groups, source, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                n, k, j, s, len(groups), status, method,
                json.dumps([list(group) for group in groups]),
                source, created_at, now,
            ))
            conn.commit()
        finally:
            conn.close()

    def get_project_result(self, n: int, k: int, j: int, s: int) -> Optional[dict]:
        conn = self._connect_known_covers()
        try:
            cursor = conn.execute('''
                SELECT n, k, j, s, num_groups, status, method, groups, source, created_at, updated_at
                FROM project_results
                WHERE n = ? AND k = ? AND j = ? AND s = ?
            ''', (n, k, j, s))
            row = cursor.fetchone()
            if not row:
                return None
            return {
                'n': row[0],
                'k': row[1],
                'j': row[2],
                's': row[3],
                'num_groups': row[4],
                'status': row[5],
                'method': row[6],
                'groups': [tuple(group) for group in json.loads(row[7])],
                'source': row[8],
                'created_at': row[9],
                'updated_at': row[10],
            }
        finally:
            conn.close()

    def _should_replace_project_result(self, existing: dict, new_size: int, new_status: str) -> bool:
        if existing['status'] == 'OPTIMAL':
            return new_status == 'OPTIMAL' and new_size < existing['num_groups']
        if new_status == 'OPTIMAL':
            return True
        return new_size < existing['num_groups']

    def seed_builtin_known_covers(self) -> None:
        """Seed small verified covers used by the assignment examples."""
        covers = [
            {
                'v': 7, 'k': 6, 't': 5, 'lower': 6, 'upper': 6,
                'blocks': [
                    (1, 2, 3, 4, 5, 7), (1, 2, 3, 4, 6, 7),
                    (1, 2, 3, 5, 6, 7), (1, 2, 4, 5, 6, 7),
                    (1, 3, 4, 5, 6, 7), (2, 3, 4, 5, 6, 7),
                ],
            },
            {
                'v': 8, 'k': 6, 't': 5, 'lower': 12, 'upper': 12,
                'blocks': [
                    (1, 2, 3, 4, 5, 8), (1, 2, 3, 4, 6, 7),
                    (1, 2, 3, 5, 6, 7), (1, 2, 3, 6, 7, 8),
                    (1, 2, 4, 5, 6, 8), (1, 2, 4, 5, 7, 8),
                    (1, 3, 4, 5, 6, 8), (1, 3, 4, 5, 7, 8),
                    (1, 3, 5, 6, 7, 8), (2, 3, 4, 5, 6, 7),
                    (2, 3, 4, 6, 7, 8), (2, 3, 5, 6, 7, 8),
                ],
            },
            {
                'v': 9, 'k': 6, 't': 4, 'lower': 12, 'upper': 12,
                'blocks': [
                    (1, 2, 3, 4, 5, 9), (1, 2, 3, 5, 7, 8),
                    (1, 2, 3, 6, 8, 9), (1, 2, 4, 5, 6, 7),
                    (1, 2, 4, 7, 8, 9), (1, 3, 4, 5, 6, 8),
                    (1, 3, 4, 6, 7, 9), (1, 5, 6, 7, 8, 9),
                    (2, 3, 4, 6, 7, 8), (2, 3, 5, 6, 7, 9),
                    (2, 4, 5, 6, 8, 9), (3, 4, 5, 7, 8, 9),
                ],
            },
        ]

        for cover in covers:
            self.save_standard_cover(
                cover['v'], cover['k'], cover['t'],
                cover['lower'], cover['upper'], cover['blocks'],
                is_proven_optimal=cover['lower'] == cover['upper'],
                source_url='https://ljcr.dmgordon.org/cover/table.html',
                source_updated_at='2026-04-21 19:09:46',
                construction_method='assignment example / La Jolla cover',
            )
