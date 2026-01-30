"""Deeply complex logging system (fake)."""
from test_repo.date_utils import get_current_timestamp

class Logger:
    def __init__(self, name: str):
        self.name = name
    
    def info(self, message: str):
        ts = get_current_timestamp()
        print(f"[INFO] {ts} [{self.name}]: {message}")
        
    def error(self, message: str):
        ts = get_current_timestamp()
        print(f"[ERROR] {ts} [{self.name}]: {message}")

def get_logger(name: str) -> Logger:
    return Logger(name)