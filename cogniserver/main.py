from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import os
import subprocess
import asyncio
import sys
from pathlib import Path
from .graph_engine import GraphEngine
from .database import Database

app = FastAPI(title="CogniServer")

# Enable CORS for Dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
ROOT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_repo")
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASHBOARD_PATH = os.path.join(PROJECT_ROOT, "dashboard", "index.html")

# Initialize Engine and Database
engine = GraphEngine(ROOT_DIR)
db = Database(os.path.join(PROJECT_ROOT, "cognicode.db"))

# Models
class FileChangeRequest(BaseModel):
    file_path: str

class ImpactResponse(BaseModel):
    changed_file: str
    affected_files: List[str]
    graph_data: Dict

class TestResult(BaseModel):
    file_path: str
    status: str # PASSED, FAILED
    error: Optional[str] = None

class TestRunRequest(BaseModel):
    file_path: str

@app.on_event("startup")
async def startup_event():
    """Build graph on startup"""
    engine.build_graph()
    print(f"Server started. Root: {PROJECT_ROOT}")

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Serve the dashboard"""
    if os.path.exists(DASHBOARD_PATH):
        with open(DASHBOARD_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Dashboard not found</h1>"

@app.post("/refresh")
def refresh_graph():
    """Force rebuild the graph"""
    engine.build_graph()
    return {"status": "Graph rebuilt", "nodes": engine.graph.number_of_nodes()}

@app.post("/impact/file", response_model=ImpactResponse)
def analyze_file_impact(request: FileChangeRequest):
    """Analyze impact of a file change."""
    file_path = request.file_path
    
    # Normalize path checking - Handle partial paths
    if not os.path.isabs(file_path):
        potential_path = os.path.join(ROOT_DIR, file_path)
        if os.path.exists(potential_path):
            file_path = potential_path
            
    print(f"Analyzing impact for: {file_path}")
    
    dependents = engine.get_dependents(file_path)
    graph_viz = engine.get_impact_subgraph([file_path])
    
    return {
        "changed_file": file_path,
        "affected_files": dependents,
        "graph_data": graph_viz
    }

@app.get("/graph")
def get_full_graph():
    """Return full graph with test status"""
    # 1. Get Graph Data
    nodes = []
    links = []
    
    # 2. Get Test Status
    test_results = db.get_latest_results() # {abs_path: STATUS}
    
    for node in engine.graph.nodes:
        # node is module name (e.g., 'math_tools')
        # engine.file_map[node] gives absolute path
        abs_path = engine.file_map.get(node)
        status = "UNKNOWN"
        
        if abs_path and abs_path in test_results:
             status = test_results[abs_path]
        
        nodes.append({
            "id": node, 
            "path": engine.file_map.get(node, ""),
            "type": "file",
            "status": status # PASSED, FAILED, UNKNOWN
        })
        
    for u, v in engine.graph.edges:
        links.append({"source": u, "target": v})
        
    return {"nodes": nodes, "links": links}

# --- Test Integration ---

@app.post("/tests/result")
def record_test_result(result: TestResult):
    """Save test result from test runner"""
    print(f"Payload received from runner: {result.file_path} -> {result.status}")
    db.add_result(result.file_path, result.status, error=result.error)
    return {"status": "saved"}

@app.get("/tests/history")
def get_test_history():
    """Get history of tests"""
    return db.get_history()

def resolve_file_path(node_id: str) -> str:
    """Helper to resolve node_ID or partial path to absolute path"""
    if node_id in engine.file_map:
        return engine.file_map[node_id]
    
    # Try as direct path
    if os.path.exists(node_id):
        return node_id
        
    return node_id # Fallback

@app.post("/run_test")
async def manual_run_test_http(request: TestRunRequest):
    """Legacy endpoint (fallback)"""
    file_path = resolve_file_path(request.file_path)
    print(f"Manual trigger (via HTTP) for: {file_path}")
    
    python_exe = os.path.join(PROJECT_ROOT, "myenv", "Scripts", "python.exe")
    if not os.path.exists(python_exe):
        python_exe = "python"
    
    test_script = os.path.join(PROJECT_ROOT, "test.py")
    subprocess.Popen([python_exe, test_script, file_path], cwd=PROJECT_ROOT)
    return {"status": "started"}

@app.websocket("/ws/run/{node_id}")
async def websocket_test_runner(websocket: WebSocket, node_id: str):
    """
    WebSocket endpoint to run tests and stream output live.
    Supports Cascade Testing: Runs tests for the target, then its dependents.
    """
    await websocket.accept()
    
    try:
        # 1. Identify Target
        target_path = resolve_file_path(node_id)
        
        # 2. Identify Dependents (Cascade)
        # engine.get_dependents returns list of absolute paths
        dependents = engine.get_dependents(target_path)
        
        test_queue = [target_path] + dependents
        unique_queue = []
        [unique_queue.append(x) for x in test_queue if x not in unique_queue]
        
        await websocket.send_text(f"🎯 <b>Target:</b> {os.path.basename(target_path)}")
        if dependents:
            await websocket.send_text(f"🔗 <b>Cascade:</b> {len(dependents)} dependent(s) queued.")
        else:
            await websocket.send_text(f"🔗 <b>Cascade:</b> No dependents found.")
        await websocket.send_text("\n" + "="*40 + "\n")

        python_exe = os.path.join(PROJECT_ROOT, "myenv", "Scripts", "python.exe")
        if not os.path.exists(python_exe):
            python_exe = "python"
        
        test_script = os.path.join(PROJECT_ROOT, "test.py")

        for i, file_to_test in enumerate(unique_queue):
            filename = os.path.basename(file_to_test)
            await websocket.send_text(f"\n🚀 <b>Running [{i+1}/{len(unique_queue)}]:</b> {filename}...\n")
            
            # Use threading for Windows-safe blocking I/O reading
            import threading
            import queue
            
            # Queue to pass lines from thread to async loop
            line_queue = queue.Queue()
            
            def read_output(process, q):
                # Merged stdout and stderr
                for line in iter(process.stdout.readline, ''):
                    q.put(line)
                process.stdout.close()
                process.wait()

            # Start subprocess with Popen (Windows compatible)
            process = subprocess.Popen(
                [python_exe, test_script, file_to_test],
                cwd=PROJECT_ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, # Merge stderr into stdout
                text=True,
                bufsize=1, # Line buffered
                encoding='utf-8',
                errors='replace' # Handle encoding errors gracefully
            )
            
            # Background thread to read stdout
            t = threading.Thread(target=read_output, args=(process, line_queue))
            t.daemon = True
            t.start()
            
            # Async loop to consume queue and send to WS
            while t.is_alive() or not line_queue.empty():
                try:
                    # Non-blocking get
                    line = line_queue.get_nowait()
                    await websocket.send_text(line)
                except queue.Empty:
                    await asyncio.sleep(0.1) # Yield to event loop
            
            # Final status for this file
            if process.returncode == 0:
                await websocket.send_text(f"✅ <b>{filename}: PASSED</b>\n")
            else:
                await websocket.send_text(f"❌ <b>{filename}: FAILED</b>\n")

        await websocket.send_text("\n" + "="*40)
        await websocket.send_text("\n🏁 <b>ALL TASKS COMPLETED</b>")
        await websocket.close()
        
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        # Only try to send if still connected
        try:
             await websocket.send_text(f"Error: {str(e)}")
             await websocket.close()
        except:
            pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
