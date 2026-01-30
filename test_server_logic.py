import sys
import os
from pathlib import Path

# Add current dir to path to import cogniserver
sys.path.append(os.getcwd())

from cogniserver.graph_engine import GraphEngine

def test_graph_logic():
    print("Initializing Graph Engine...")
    root = os.path.join(os.getcwd(), "test_repo")
    engine = GraphEngine(root)
    engine.build_graph()
    
    # Test Case 1: Math Tools
    # math_tools.py is a base utility.
    # It should have NO internal dependencies (constants maybe)
    # But many things depend ON it.
    
    math_tools = os.path.join(root, "math_tools.py")
    params = engine.get_dependents(math_tools)
    
    print(f"\n[Test 1] Dependents of math_tools.py:")
    for p in params:
        print(f" - {Path(p).name}")
        
    # Expected: product.py, price_calculator.py, cart_item.py (based on my memory of creation)
    
    # Test Case 2: Cart Manager
    # cart_manager.py depends on cart_item, product, user.
    # checkout_controller depends on cart_manager.
    
    cart_mgr = os.path.join(root, "cart_manager.py")
    dependents = engine.get_dependents(cart_mgr)
    print(f"\n[Test 2] Dependents of cart_manager.py:")
    for p in dependents:
        print(f" - {Path(p).name}")
        
    # Expected: price_calculator.py, checkout_controller.py, order_processor.py
    
    # Test Case 3: Verify Graph Nodes
    print(f"\n[Test 3] Total Nodes: {engine.graph.number_of_nodes()}")
    print(f"Total Edges: {engine.graph.number_of_edges()}")

if __name__ == "__main__":
    test_graph_logic()
