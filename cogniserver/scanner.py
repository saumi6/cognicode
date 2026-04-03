import subprocess
import json
from pathlib import Path
from typing import Dict, List

def run_bandit_scan(root_dir: str) -> Dict[str, List[Dict]]:
    """
    Runs bandit sequentially on the project root and maps vulnerabilities
    to their constituent files.
    
    Returns:
        Dict mapping file paths (or module names) to a list of vulnerabilities.
    """
    try:
        # Run bandit across the root directory
        process = subprocess.run(
            ["bandit", "-r", str(root_dir), "-f", "json", "--quiet"],
            capture_output=True,
            text=True
        )
        
        # Bandit returns non-zero exit code if issues are found, 
        # so we rely on the JSON stdout rather than process.returncode
        output = process.stdout
        if not output:
            return {}
            
        data = json.loads(output)
        results = data.get("results", [])
        
        vulnerabilities = {}
        for issue in results:
            filepath = issue.get("filename")
            if not filepath:
                continue
                
            # Normalize path
            norm_path = Path(filepath).resolve()
            
            if norm_path not in vulnerabilities:
                vulnerabilities[norm_path] = []
                
            vulnerabilities[norm_path].append({
                "issue_text": issue.get("issue_text", ""),
                "issue_severity": issue.get("issue_severity", "LOW"),
                "issue_confidence": issue.get("issue_confidence", ""),
                "line_number": issue.get("line_number", 0),
                "test_name": issue.get("test_name", "")
            })
            
        return vulnerabilities
    except Exception as e:
        print(f"[Scanner] Bandit execution failed: {e}")
        return {}
