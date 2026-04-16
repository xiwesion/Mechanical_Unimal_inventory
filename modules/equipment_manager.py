"""
Equipment Manager Module
Handles equipment registry, storage, and retrieval
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import uuid

class EquipmentManager:
    """Manages equipment registry and storage"""
    
    DATA_DIR = Path(__file__).parent.parent / "data"
    EQUIPMENT_FILE = DATA_DIR / "equipment_registry.json"
    
    def __init__(self):
        """Initialize equipment manager"""
        self.equipment = self._load_equipment()
    
    def _ensure_dir(self):
        """Ensure data directory exists"""
        self.DATA_DIR.mkdir(exist_ok=True)
    
    def _load_equipment(self) -> Dict:
        """Load equipment from JSON file"""
        self._ensure_dir()
        
        if self.EQUIPMENT_FILE.exists():
            try:
                with open(self.EQUIPMENT_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading equipment: {e}")
                return {}
        return {}
    
    def _save_equipment(self):
        """Save equipment to JSON file"""
        self._ensure_dir()
        try:
            with open(self.EQUIPMENT_FILE, 'w') as f:
                json.dump(self.equipment, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving equipment: {e}")
    
    def add_equipment(self, lab_id: str, equipment_data: Dict) -> Optional[str]:
        """
        Add new equipment
        
        Args:
            lab_id: Lab ID where equipment belongs
            equipment_data: Dictionary with equipment information
        
        Returns:
            Equipment ID if successful, None otherwise
        """
        try:
            # Validate required fields
            required_fields = ['nama', 'jumlah', 'harga_satuan']
            for field in required_fields:
                if field not in equipment_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Generate unique ID
            equipment_id = str(uuid.uuid4())[:8]
            
            # Prepare equipment data
            equipment_data['equipment_id'] = equipment_id
            equipment_data['lab_id'] = lab_id
            equipment_data['created_date'] = datetime.now().isoformat()
            equipment_data['last_modified'] = datetime.now().isoformat()
            
            # Calculate harga_keseluruhan if not provided
            if 'harga_keseluruhan' not in equipment_data:
                jumlah = float(equipment_data.get('jumlah', 0))
                harga_satuan = float(equipment_data.get('harga_satuan', 0))
                equipment_data['harga_keseluruhan'] = jumlah * harga_satuan
            
            # Set default status
            if 'status' not in equipment_data:
                equipment_data['status'] = 'active'
            
            # Initialize quantity history
            equipment_data['quantity_history'] = [
                {
                    'date': datetime.now().isoformat(),
                    'quantity': float(equipment_data['jumlah']),
                    'type': 'initial',
                    'notes': 'Penambahan awal'
                }
            ]
            
            self.equipment[equipment_id] = equipment_data
            self._save_equipment()
            
            return equipment_id
        except Exception as e:
            print(f"Error adding equipment: {e}")
            return None
    
    def get_equipment(self, equipment_id: str) -> Optional[Dict]:
        """Get specific equipment by ID"""
        return self.equipment.get(equipment_id)
    
    def get_all_equipment(self) -> List[Dict]:
        """Get all equipment"""
        return list(self.equipment.values())
    
    def get_equipment_by_lab(self, lab_id: str) -> List[Dict]:
        """Get equipment by lab"""
        return [eq for eq in self.equipment.values() if eq.get('lab_id') == lab_id]
    
    def update_equipment(self, equipment_id: str, equipment_data: Dict) -> bool:
        """Update equipment information"""
        try:
            if equipment_id not in self.equipment:
                raise ValueError("Equipment not found")
            
            # Preserve original data and update
            existing = self.equipment[equipment_id]
            
            # Update data
            for key, value in equipment_data.items():
                if key not in ['equipment_id', 'created_date', 'quantity_history']:
                    existing[key] = value
            
            # Recalculate harga_keseluruhan
            if 'jumlah' in equipment_data or 'harga_satuan' in equipment_data:
                jumlah = float(existing.get('jumlah', 0))
                harga_satuan = float(existing.get('harga_satuan', 0))
                existing['harga_keseluruhan'] = jumlah * harga_satuan
            
            existing['last_modified'] = datetime.now().isoformat()
            
            self._save_equipment()
            return True
        except Exception as e:
            print(f"Error updating equipment: {e}")
            return False
    
    def delete_equipment(self, equipment_id: str) -> bool:
        """Delete equipment from registry"""
        try:
            if equipment_id not in self.equipment:
                raise ValueError("Equipment not found")
            
            del self.equipment[equipment_id]
            self._save_equipment()
            return True
        except Exception as e:
            print(f"Error deleting equipment: {e}")
            return False
    
    def adjust_quantity(self, equipment_id: str, qty_change: float, notes: str = "", movement_type: str = "adjustment") -> bool:
        """
        Adjust equipment quantity (for in/out tracking)
        
        Args:
            equipment_id: Equipment ID
            qty_change: Quantity change (positive for in, negative for out)
            notes: Additional notes for the movement
            movement_type: Type of movement (in, out, adjustment)
        
        Returns:
            True if successful
        """
        try:
            if equipment_id not in self.equipment:
                raise ValueError("Equipment not found")
            
            eq = self.equipment[equipment_id]
            current_qty = float(eq.get('jumlah', 0))
            new_qty = current_qty + qty_change
            
            if new_qty < 0:
                raise ValueError("Quantity cannot be negative")
            
            # Update quantity
            eq['jumlah'] = new_qty
            
            # Recalculate total price
            harga_satuan = float(eq.get('harga_satuan', 0))
            eq['harga_keseluruhan'] = new_qty * harga_satuan
            
            # Record in history
            if 'quantity_history' not in eq:
                eq['quantity_history'] = []
            
            eq['quantity_history'].append({
                'date': datetime.now().isoformat(),
                'quantity': new_qty,
                'change': qty_change,
                'type': movement_type,
                'notes': notes
            })
            
            # Update status if depleted
            if new_qty == 0:
                eq['status'] = 'depleted'
            elif eq.get('status') == 'depleted' and new_qty > 0:
                eq['status'] = 'active'
            
            eq['last_modified'] = datetime.now().isoformat()
            
            self._save_equipment()
            
            # Also record in inventory movements
            from modules.inventory_manager import InventoryManager
            im = InventoryManager()
            im.record_movement(equipment_id, eq['lab_id'], movement_type, qty_change, notes)
            
            return True
        except Exception as e:
            print(f"Error adjusting quantity: {e}")
            return False
    
    def search_equipment(self, query: str) -> List[Dict]:
        """Search equipment by name"""
        query = query.lower()
        return [
            eq for eq in self.equipment.values()
            if query in eq.get('nama', '').lower() or
               query in eq.get('merk', '').lower()
        ]
    
    def get_statistics(self) -> Dict:
        """Get equipment statistics"""
        all_eq = self.equipment.values()
        
        total_value = sum(float(eq.get('harga_keseluruhan', 0)) for eq in all_eq)
        total_items = sum(float(eq.get('jumlah', 0)) for eq in all_eq)
        
        by_type = {}
        by_status = {}
        
        for eq in all_eq:
            eq_type = eq.get('type', 'Lainnya')
            status = eq.get('status', 'active')
            
            if eq_type not in by_type:
                by_type[eq_type] = 0
            by_type[eq_type] += 1
            
            if status not in by_status:
                by_status[status] = 0
            by_status[status] += 1
        
        return {
            'total_equipment': len(all_eq),
            'total_value': total_value,
            'total_items': total_items,
            'by_type': by_type,
            'by_status': by_status
        }
