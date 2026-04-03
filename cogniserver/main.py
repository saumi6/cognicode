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
    coverage_percent: Optional[float] = None

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
    """Return full graph with test status and metrics (Contract A)"""
    # 1. Get Graph Data
    nodes = []
    links = []
    
    # 2. Get Test Status
    test_results = db.get_latest_results() # {abs_path: STATUS}
    
    # 3. Ensure complexity scores are current
    complexity_scores = engine.complexity_scores if hasattr(engine, 'complexity_scores') else {}

    # 4. Get architectural violations
    arch_violations = engine.architectural_violations if hasattr(engine, 'architectural_violations') else {}
    
    for node in engine.graph.nodes:
        # node is module name (e.g., 'math_tools')
        # engine.file_map[node] gives absolute path
        abs_path = engine.file_map.get(node, "")
        status = "UNKNOWN"
        
        if abs_path and abs_path in test_results:
             status = test_results[abs_path]
        
        # Pull per-file metrics from DB (defaults to 0.0 for both)
        db_metrics = db.get_metrics(abs_path) if abs_path else dict(db.DEFAULT_METRICS)

        metrics = {
            "coverage_percent": db_metrics.get("coverage_percent", 0.0),
            "flakiness_rate": db_metrics.get("flakiness_rate", 0.0),
            "complexity_score": complexity_scores.get(node, 0),
            "vulnerabilities": engine.vulnerabilities.get(node, []) if hasattr(engine, 'vulnerabilities') else []
        }

        # Override status if this node violates an architectural boundary
        if node in arch_violations:
            status = "VIOLATION"
            metrics["violation_reason"] = arch_violations[node]
        
        nodes.append({
            "id": node, 
            "path": abs_path,
            "type": "file",
            "status": status,
            "metrics": metrics
        })
        
    for u, v in engine.graph.edges:
        links.append({"source": u, "target": v})
        
    return {"nodes": nodes, "links": links}

# --- Semantic Clone Detection ---
import cogniserver.clone_detector as clone_detector

@app.get("/clone/scan")
def scan_clones():
    """Trigger FAISS semantic clone generation."""
    try:
        from .clone_detector import scan_for_clones
        res = scan_for_clones(engine.file_map)
        if isinstance(res, dict) and "error" in res:
            raise HTTPException(status_code=500, detail=res["error"])
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/knowledge/search")
def search_knowledge_base(q: str):
    """Trigger FAISS knowledge base semantic search."""
    try:
        from .clone_detector import search_code
        res = search_code(q, engine.file_map)
        if isinstance(res, dict) and "error" in res:
            raise HTTPException(status_code=500, detail=res["error"])
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ====================================================================== #
# --- Test Integration ---

@app.post("/tests/result")
def record_test_result(result: TestResult):
    """Save test result from test runner"""
    print(f"Payload received from runner: {result.file_path} -> {result.status}")
    db.add_result(result.file_path, result.status, error=result.error)

    # If coverage data was included, persist it into the metrics column
    if result.coverage_percent is not None:
        current_metrics = db.get_metrics(result.file_path)
        current_metrics["coverage_percent"] = result.coverage_percent
        db.update_metrics(result.file_path, current_metrics)
        print(f"[Coverage] Saved {result.coverage_percent}% for {result.file_path}")

    return {"status": "saved"}

@app.get("/tests/history")
def get_test_history():
    """Get history of tests"""
    return db.get_history()

# --- AI Summaries ---

# Lazy singleton so we don't pay the Groq-client init cost on every import
_groq_generator = None

def _get_groq_generator():
    global _groq_generator
    if _groq_generator is None:
        # Import here to keep the server bootable even if groq deps are missing
        sys.path.insert(0, PROJECT_ROOT)
        from test_generator_groq import TestGeneratorGroq
        _groq_generator = TestGeneratorGroq(verbose=False)
    return _groq_generator

@app.get("/summary/{node_id}")
def get_node_summary(node_id: str):
    """Return an AI-generated 3-sentence summary of a file's role."""
    # Resolve node_id (e.g. "math_tools") to absolute path
    abs_path = engine.file_map.get(node_id)

    if not abs_path or not os.path.exists(abs_path):
        # Try as a direct / partial path fallback
        if os.path.exists(node_id):
            abs_path = node_id
        else:
            raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found in graph.")

    # Build graph-context payload from dependency topology
    context_payload = ""
    try:
        if node_id in engine.graph:
            in_deg = engine.graph.in_degree(node_id)
            out_deg = engine.graph.out_degree(node_id)

            if in_deg == 0 and out_deg == 0:
                role = "an Isolated module (no graph connections)"
            elif out_deg == 0:
                role = f"a Leaf utility (0 dependencies, {in_deg} dependent{'s' if in_deg != 1 else ''})"
            elif in_deg == 0:
                role = f"an Entry Point (0 dependents, depends on {out_deg} module{'s' if out_deg != 1 else ''})"
            else:
                role = f"an Internal module ({in_deg} incoming, {out_deg} outgoing edges)"

            context_payload = f"This file is {role}."
    except Exception:
        pass  # graph inspection is best-effort

    try:
        gen = _get_groq_generator()
        summary = gen.generate_node_summary(abs_path, graph_context=context_payload)
    except Exception as e:
        summary = f"Summary unavailable: {e}"

    return {"summary": summary}

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
