import os
import sys

PROJECT_ROOT = r"c:\Users\gurav\prog\college\BE Proj\cognicode"
sys.path.insert(0, PROJECT_ROOT)

from cogniserver.database import Database

def inject_flakiness():
    db = Database(os.path.join(PROJECT_ROOT, "cognicode.db"))
    
    file1 = os.path.join(PROJECT_ROOT, "test_repo", "math_tools.py")
    file2 = os.path.join(PROJECT_ROOT, "test_repo", "auth_service.py")
    
    metrics1 = db.get_metrics(file1)
    metrics1["coverage_percent"] = 88.5
    metrics1["flakiness_rate"] = 25.0
    db.update_metrics(file1, metrics1)
    
    metrics2 = db.get_metrics(file2)
    metrics2["coverage_percent"] = 62.0
    metrics2["flakiness_rate"] = 50.0
    db.update_metrics(file2, metrics2)

    print("Flakiness set explicitly!")
    print(f"{os.path.basename(file1)} metrics:", db.get_metrics(file1))
    print(f"{os.path.basename(file2)} metrics:", db.get_metrics(file2))

if __name__ == "__main__":
    inject_flakiness()
