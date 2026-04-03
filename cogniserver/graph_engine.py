import ast
import os
import json
import networkx as nx
from pathlib import Path
from typing import List, Dict, Set, Optional

from .scanner import run_bandit_scan

class GraphEngine:
    """
    The brain of Cognicode. 
    Maintains a directed graph of the codebase dependencies.
    """
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir).resolve()
        self.graph = nx.DiGraph()
        self.file_map: Dict[str, str] = {} # module_name -> file_path
        self.architectural_violations: Dict[str, str] = {}
        self.vulnerabilities: Dict[str, List[Dict]] = {} # node_u -> List of vulnerabilities

        # Load architectural boundary rules
        rules_path = Path(__file__).parent / "architecture.json"
        if rules_path.exists():
            with open(rules_path, "r", encoding="utf-8") as f:
                rules_data = json.load(f)
                self._arch_rules = rules_data.get("rules", [])
                self._module_rules = rules_data.get("module_rules", [])
            total = len(self._arch_rules) + len(self._module_rules)
            print(f"Loaded {total} architectural rules ({len(self._arch_rules)} dir, {len(self._module_rules)} module).")
        else:
            self._arch_rules = []
            self._module_rules = []
            print("No architecture.json found – skipping boundary checks.")
        
    def build_graph(self):
        """Scans the codebase and builds the dependency graph."""
        self.graph.clear()
        self.file_map.clear()
        self.vulnerabilities.clear()
        
        print(f"Building graph for {self.root_dir}...")
        
        # 1. Index all files first
        py_files = list(self.root_dir.rglob("*.py"))
        print(f"Found {len(py_files)} Python files.")
        
        for file_path in py_files:
            # Ignore generated tests
            if "generated_tests" in file_path.parts:
                continue

            module_name = self._get_module_name(file_path)
            self.file_map[module_name] = str(file_path)
            self.graph.add_node(module_name, type="file", path=str(file_path))
            
        # 2. Parse each file for imports
        for file_path in py_files:
            if "generated_tests" in file_path.parts:
                continue
                
            try:
                self._analyze_imports(file_path)
            except Exception as e:
                print(f"Error analyzing {file_path.name}: {e}")
                
        print(f"Graph built: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges.")

        # 3. Security Scanning
        raw_vulns = run_bandit_scan(str(self.root_dir))
        for mod, path in self.file_map.items():
            path_obj = Path(path).resolve()
            if path_obj in raw_vulns:
                self.vulnerabilities[mod] = raw_vulns[path_obj]
        
        total_vulns = sum(len(v) for v in self.vulnerabilities.values())
        if total_vulns > 0:
            print(f"⚠️  Detected {total_vulns} vulnerabilities across {len(self.vulnerabilities)} modules.")

        # Pre-compute complexity scores after every build
        self.calculate_complexity_scores()

        # Validate architectural boundaries
        self.validate_architecture()

    # ------------------------------------------------------------------ #
    #  Architectural boundary validation                                   #
    # ------------------------------------------------------------------ #

    def validate_architecture(self):
        """
        Iterates every edge (u → v) in the graph and checks it against
        the loaded architectural rules from architecture.json.

        A rule  {"source_dir": "X", "cannot_import": "Y"}  means any
        module whose file path contains directory X must NOT import
        any module whose file path contains directory Y.

        Violations are stored in  self.architectural_violations  as
        {node_u: "Human-readable violation message"}.
        """
        self.architectural_violations = {}

        has_rules = self._arch_rules or self._module_rules
        if not has_rules:
            return

        for u, v in self.graph.edges:
            u_path = self.file_map.get(u, "").replace("\\", "/")
            v_path = self.file_map.get(v, "").replace("\\", "/")

            # Directory-level rules
            for rule in self._arch_rules:
                src_dir = rule.get("source_dir", "")
                banned_dir = rule.get("cannot_import", "")
                reason = rule.get("reason", f"{src_dir} must not import {banned_dir}")

                if (f"/{src_dir}/" in u_path or u_path.startswith(f"{src_dir}/")) and \
                   (f"/{banned_dir}/" in v_path or v_path.startswith(f"{banned_dir}/")):
                    self.architectural_violations[u] = (
                        f"'{u}' imports '{v}' — violates rule: {reason}"
                    )

            # Module-name-level rules  (substring match on node ids)
            for rule in self._module_rules:
                src_pat = rule.get("source_pattern", "")
                ban_pat = rule.get("cannot_import_pattern", "")
                reason = rule.get("reason", f"{src_pat} must not import {ban_pat}")

                if src_pat in u and ban_pat in v:
                    self.architectural_violations[u] = (
                        f"'{u}' imports '{v}' — violates rule: {reason}"
                    )

        if self.architectural_violations:
            print(f"[WARN] {len(self.architectural_violations)} architectural violation(s) detected.")
        else:
            print("[OK] No architectural violations detected.")

    # ------------------------------------------------------------------ #
    #  Complexity scoring  (Contract A)                                   #
    # ------------------------------------------------------------------ #

    def calculate_complexity_scores(self) -> Dict[str, int]:
        """
        For every node, compute its **Complexity Score** defined as the
        total number of its descendants in the dependency graph (all nodes
        reachable by following directed edges from this node).

        Stores the mapping in ``self.complexity_scores`` and also returns it.
        """
        self.complexity_scores: Dict[str, int] = {}

        for node in self.graph.nodes:
            self.complexity_scores[node] = len(nx.descendants(self.graph, node))

        print(f"Complexity scores computed for {len(self.complexity_scores)} nodes.")
        return self.complexity_scores

    def _get_module_name(self, file_path: Path) -> str:
        """Converts file path to python module name (dotted path)."""
        try:
            rel_path = file_path.relative_to(self.root_dir)
            return str(rel_path.with_suffix('')).replace(os.sep, '.')
        except ValueError:
            return file_path.stem

    def _analyze_imports(self, file_path: Path):
        """Parses a file and adds edges to the graph for imports."""
        current_module = self._get_module_name(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                tree = ast.parse(f.read())
            except SyntaxError:
                return # Skip broken files

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    target = alias.name
                    # Fix for absolute imports (test_repo.x -> x)
                    if target.startswith("test_repo."):
                        target = target.replace("test_repo.", "")
                    self._add_dependency(current_module, target)
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # from x.y import z
                    target = node.module
                    if target.startswith("test_repo."):
                        target = target.replace("test_repo.", "")
                    self._add_dependency(current_module, target)
                elif node.level > 0:
                    # from .xxxx import y (relative import)
                    # This is tricky without strict package structure logic
                    # Simplified: resolve relative to current package
                    parts = current_module.split('.')
                    base_parts = parts[:-node.level]
                    if node.module:
                        base_parts.append(node.module)
                    target = ".".join(base_parts)
                    self._add_dependency(current_module, target)

    def _add_dependency(self, source: str, target: str):
        """Adds an edge from source depends_on target."""
        # Clean target: "pandas.core" -> "pandas" if "pandas" is not in our repo? 
        # For now, we only care about internal deps.
        
        # Exact match check
        if target in self.file_map:
            self.graph.add_edge(source, target)
            return

        # Partial match (importing a function from a module)
        # If target is "utils.math_tools.add", but we only have "utils.math_tools"
        parts = target.split('.')
        for i in range(len(parts), 0, -1):
            sub_target = ".".join(parts[:i])
            if sub_target in self.file_map:
                if sub_target != source: # No self loops
                    self.graph.add_edge(source, sub_target)
                return

    def get_dependents(self, file_path: str) -> List[str]:
        """
        Returns a list of file paths that depend on the given file.
        (Reverse dependency lookup)
        """
        # Convert path to module
        path_obj = Path(file_path).resolve()
        target_module = None
        
        # Search map (inefficient but safe)
        for mod, path in self.file_map.items():
            if Path(path).resolve() == path_obj:
                target_module = mod
                break
                
        if not target_module: 
            # Try fuzzy match if absolute path fails due to casing etc
            try:
                target_module = self._get_module_name(path_obj)
            except:
                return []

        if target_module not in self.graph:
            return []
            
        # Find all nodes that have an edge TO this node
        # In NetworkX: predecessors are nodes that point TO the target
        # Our graph: Source --imports--> Target
        # So Source depends on Target.
        # If Target changes, Source needs testing.
        # So we want predecessors.
        
        dependents = list(self.graph.predecessors(target_module))
        
        # Convert back to paths
        return [self.file_map[d] for d in dependents if d in self.file_map]

    def get_impact_subgraph(self, changed_files: List[str]) -> Dict:
        """Returns JSON structure of the affected subgraph for visualization."""
        affected_nodes = set()
        
        # 1. Start with changed files
        for f in changed_files:
            mod = self._get_module_name(Path(f))
            if mod in self.graph:
                affected_nodes.add(mod)
                
        # 2. Add immediate dependents (first layer of impact)
        #    Recursive implementation could be added here for transitive impact
        dependents = set()
        for node in affected_nodes:
            dependents.update(self.graph.predecessors(node))
            
        all_nodes = affected_nodes.union(dependents)
        
        # Build subgraph JSON
        nodes_json = []
        edges_json = []
        
        for node in all_nodes:
            nodes_json.append({
                "id": node, 
                "file": self.file_map.get(node, ""),
                "status": "changed" if node in affected_nodes else "affected"
            })
            
        for u, v in self.graph.out_edges(list(all_nodes)):
            if u in all_nodes and v in all_nodes:
                edges_json.append({"source": u, "target": v})
                
        return {"nodes": nodes_json, "links": edges_json}
