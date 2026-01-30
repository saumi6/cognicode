import sqlite3
import time
import os
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
