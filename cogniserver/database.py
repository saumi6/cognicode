import sqlite3
import time
import os
import json
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path="cognicode.db"):
        # Ensure db is in the same directory or project root
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn

    # Default metrics template for new or missing entries
    DEFAULT_METRICS = {"coverage_percent": 0.0, "flakiness_rate": 0.0}

    def init_db(self):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS test_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                function_name TEXT,
                status TEXT NOT NULL, -- 'PASSED', 'FAILED', 'ERROR'
                timestamp REAL NOT NULL,
                error_message TEXT
            )
        ''')

        # --- Safe migration: add 'metrics' column if it doesn't exist ---
        try:
            c.execute("ALTER TABLE test_runs ADD COLUMN metrics TEXT DEFAULT '{}'")
        except sqlite3.OperationalError:
            # Column already exists – nothing to do
            pass

        conn.commit()
        conn.close()

    def add_result(self, file_path: str, status: str, function_name: str = None, error: str = None):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO test_runs (file_path, function_name, status, timestamp, error_message) 
            VALUES (?, ?, ?, ?, ?)
        ''', (file_path, function_name, status, time.time(), error))
        conn.commit()
        conn.close()

    def get_latest_results(self) -> Dict[str, str]:
        """
        Get the latest status for each file.
        Returns: { 'path/to/file.py': 'PASSED' | 'FAILED' }
        Logic: If ANY function in the latest batch failed, the file is FAILED.
        But for simplicity, we'll just take the latest entry for the file if we batch file-level tests.
        """
        conn = self.get_connection()
        c = conn.cursor()
        
        # We want the latest status for each file
        # This query looks for the row with max timestamp for each file_path
        query = '''
            SELECT file_path, status, error_message
            FROM test_runs t1
            WHERE t1.timestamp = (
                SELECT MAX(timestamp)
                FROM test_runs t2
                WHERE t2.file_path = t1.file_path
            )
        '''
        c.execute(query)
        rows = c.fetchall()
        
        results = {}
        for row in rows:
            # key: full path, value: status
            results[row['file_path']] = row['status']
            
        conn.close()
        return results

    def get_history(self, limit=50):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM test_runs ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = [dict(row) for row in c.fetchall()]
        conn.close()
        return rows

    # ------------------------------------------------------------------ #
    #  Metrics helpers (Contract A)                                       #
    # ------------------------------------------------------------------ #

    def update_metrics(self, file_path: str, metrics: Dict) -> None:
        """
        Upsert the metrics JSON blob for the latest test_run of *file_path*.
        If no row exists yet a new UNKNOWN row is inserted.
        """
        merged = {**self.DEFAULT_METRICS, **metrics}
        payload = json.dumps(merged)

        conn = self.get_connection()
        c = conn.cursor()

        # Try to update the most recent row for this file
        c.execute('''
            UPDATE test_runs
            SET metrics = ?
            WHERE id = (
                SELECT id FROM test_runs
                WHERE file_path = ? COLLATE NOCASE
                ORDER BY timestamp DESC
                LIMIT 1
            )
        ''', (payload, file_path))

        if c.rowcount == 0:
            # No existing row – seed one so the metrics aren't lost
            import time as _t
            c.execute('''
                INSERT INTO test_runs (file_path, status, timestamp, metrics)
                VALUES (?, 'UNKNOWN', ?, ?)
            ''', (file_path, _t.time(), payload))

        conn.commit()
        conn.close()

    def get_metrics(self, file_path: str) -> Dict:
        """
        Return the metrics dict for *file_path* (from its latest row).
        Falls back to DEFAULT_METRICS when nothing is stored yet.
        """
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''
            SELECT metrics FROM test_runs
            WHERE file_path = ? COLLATE NOCASE
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (file_path,))
        row = c.fetchone()
        conn.close()

        if row and row['metrics']:
            try:
                stored = json.loads(row['metrics'])
                return {**self.DEFAULT_METRICS, **stored}
            except (json.JSONDecodeError, TypeError):
                pass

        return dict(self.DEFAULT_METRICS)
