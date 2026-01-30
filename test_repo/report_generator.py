"""Report Generator.""" 
from  typing import List
from test_repo.inventory_manager import InventoryManager
from test_repo.date_utils import get_current_timestamp

def generate_inventory_report(inventory: InventoryManager) -> str:
    lines = [f"Inventory Report - {get_current_timestamp()}"]
    for sku, prod in inventory.products.items():
        lines.append(f"{sku}: {prod.name} - Stock: {prod.stock}")
    return "\n".join(lines)