from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
import os
from pathlib import Path
from .graph_engine import GraphEngine

app = FastAPI(title="CogniServer")

# Enable CORS for Dashboard
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the dashboard URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instance
# In a real app, this would be initialized with configurable root
ROOT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_repo") # go up from cogniserver/
engine = GraphEngine(ROOT_DIR)

class FileChangeRequest(BaseModel):
    file_path: str

class ImpactResponse(BaseModel):
    changed_file: str
    affected_files: List[str]
    graph_data: Dict

@app.on_event("startup")
async def startup_event():
    """Build graph on startup"""
    engine.build_graph()

@app.get("/")
def read_root():
    return {"status": "CogniServer is running", "nodes": engine.graph.number_of_nodes()}

@app.post("/refresh")
def refresh_graph():
    """Force rebuild the graph"""
    engine.build_graph()
    return {"status": "Graph rebuilt", "nodes": engine.graph.number_of_nodes()}

@app.post("/impact/file", response_model=ImpactResponse)
def analyze_file_impact(request: FileChangeRequest):
    """
    Analyze impact of a file change.
    Returns list of files that need to be re-tested.
    """
    file_path = request.file_path
    
    # Normalize path checking
    # If partial path provided, try to resolve it
    if not os.path.isabs(file_path):
        # Allow passing "test_repo/math_tools.py"
        potential_path = os.path.join(ROOT_DIR, file_path)
        if os.path.exists(potential_path):
            file_path = potential_path
            
    print(f"Analyzing impact for: {file_path}")
    
    dependents = engine.get_dependents(file_path)
    
    # Get visualization data
    graph_viz = engine.get_impact_subgraph([file_path])
    
    return {
        "changed_file": file_path,
        "affected_files": dependents,
        "graph_data": graph_viz
    }

@app.get("/graph")
def get_full_graph():
    """Return full graph for dashboard"""
    # Convert networkx graph to readable JSON
    nodes = []
    links = []
    
    for node in engine.graph.nodes:
        nodes.append({
            "id": node, 
            "path": engine.file_map.get(node, ""),
            "type": "file"
        })
        
    for u, v in engine.graph.edges:
        links.append({"source": u, "target": v})
        
    return {"nodes": nodes, "links": links}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
