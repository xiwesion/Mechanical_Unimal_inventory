"""
Inventory Manager Module
Handles inventory movements and tracking
"""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dateutil import parser as date_parser

class InventoryManager:
    """Manages inventory movements and tracking"""
    
    DATA_DIR = Path(__file__).parent.parent / "data"
    MOVEMENTS_FILE = DATA_DIR / "inventory_movements.json"
    
    def __init__(self):
        """Initialize inventory manager"""
        self.movements = self._load_movements()
    
    def _ensure_dir(self):
        """Ensure data directory exists"""
        self.DATA_DIR.mkdir(exist_ok=True)
    
    def _load_movements(self) -> List:
        """Load movements from JSON file"""
        self._ensure_dir()
        
        if self.MOVEMENTS_FILE.exists():
            try:
                with open(self.MOVEMENTS_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading movements: {e}")
                return []
        return []
    
    def _save_movements(self):
        """Save movements to JSON file"""
        self._ensure_dir()
        try:
            with open(self.MOVEMENTS_FILE, 'w') as f:
                json.dump(self.movements, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving movements: {e}")
    
    def record_movement(self, equipment_id: str, lab_id: str, movement_type: str, 
                       quantity: float, notes: str = "") -> bool:
        """
        Record inventory movement
        
        Args:
            equipment_id: Equipment ID
            lab_id: Lab ID
            movement_type: Type of movement (in, out, adjustment, transfer)
            quantity: Quantity moved (positive or negative)
            notes: Additional notes
        
        Returns:
            True if successful
        """
        try:
            movement = {
                'movement_id': f"{equipment_id}_{datetime.now().timestamp()}",
                'equipment_id': equipment_id,
                'lab_id': lab_id,
                'movement_type': movement_type,
                'quantity': quantity,
                'date': datetime.now().isoformat(),
                'notes': notes
            }
            
            self.movements.append(movement)
            self._save_movements()
            
            return True
        except Exception as e:
            print(f"Error recording movement: {e}")
            return False
    
    def get_movements(self, lab_id: Optional[str] = None, 
                     start_date: Optional[str] = None,
                     end_date: Optional[str] = None,
                     movement_type: Optional[str] = None) -> List[Dict]:
        """
        Get movements with optional filtering
        
        Args:
            lab_id: Filter by lab
            start_date: Filter from date (ISO format or string)
            end_date: Filter to date (ISO format or string)
            movement_type: Filter by movement type
        
        Returns:
            List of movements
        """
        results = self.movements
        
        # Filter by lab
        if lab_id:
            results = [m for m in results if m.get('lab_id') == lab_id]
        
        # Filter by movement type
        if movement_type:
            results = [m for m in results if m.get('movement_type') == movement_type]
        
        # Filter by date range
        if start_date or end_date:
            results = self._filter_by_date_range(results, start_date, end_date)
        
        return sorted(results, key=lambda x: x.get('date', ''), reverse=True)
    
    def _filter_by_date_range(self, movements: List[Dict], 
                             start_date: Optional[str],
                             end_date: Optional[str]) -> List[Dict]:
        """Filter movements by date range"""
        try:
            if start_date:
                start = date_parser.parse(start_date)
            else:
                start = datetime.min
            
            if end_date:
                end = date_parser.parse(end_date)
            else:
                end = datetime.max
            
            filtered = []
            for m in movements:
                try:
                    m_date = date_parser.parse(m.get('date', ''))
                    if start <= m_date <= end:
                        filtered.append(m)
                except:
                    pass
            
            return filtered
        except Exception as e:
            print(f"Error filtering by date: {e}")
            return movements
    
    def get_equipment_movements(self, equipment_id: str) -> List[Dict]:
        """Get all movements for specific equipment"""
        return [m for m in self.movements if m.get('equipment_id') == equipment_id]
    
    def get_depletion_report(self, lab_id: Optional[str] = None,
                            start_date: Optional[str] = None,
                            end_date: Optional[str] = None) -> Dict:
        """
        Get depletion report (equipment used/consumed)
        
        Args:
            lab_id: Filter by lab (None for all labs)
            start_date: Report period start
            end_date: Report period end
        
        Returns:
            Depletion report grouped by equipment
        """
        # Get out movements (consumption)
        out_movements = [m for m in self.movements if m.get('movement_type') in ['out', 'adjustment'] 
                        and m.get('quantity', 0) < 0]
        
        # Filter by lab if specified
        if lab_id:
            out_movements = [m for m in out_movements if m.get('lab_id') == lab_id]
        
        # Filter by date range
        if start_date or end_date:
            out_movements = self._filter_by_date_range(out_movements, start_date, end_date)
        
        # Group by equipment
        report = {}
        for m in out_movements:
            eq_id = m.get('equipment_id')
            if eq_id not in report:
                report[eq_id] = {
                    'equipment_id': eq_id,
                    'lab_id': m.get('lab_id'),
                    'total_consumed': 0,
                    'last_consumption': None,
                    'movements': []
                }
            
            qty = m.get('quantity', 0)
            report[eq_id]['total_consumed'] += abs(qty)
            report[eq_id]['last_consumption'] = m.get('date')
            report[eq_id]['movements'].append(m)
        
        return report
    
    def get_stock_summary(self, lab_id: Optional[str] = None) -> Dict:
        """
        Get current stock summary
        
        Args:
            lab_id: Filter by lab
        
        Returns:
            Stock summary
        """
        from modules.equipment_manager import EquipmentManager
        em = EquipmentManager()
        
        if lab_id:
            equipment = em.get_equipment_by_lab(lab_id)
        else:
            equipment = em.get_all_equipment()
        
        summary = {
            'total_items': 0,
            'total_value': 0,
            'by_status': {},
            'details': []
        }
        
        for eq in equipment:
            qty = float(eq.get('jumlah', 0))
            value = float(eq.get('harga_keseluruhan', 0))
            status = eq.get('status', 'active')
            
            summary['total_items'] += qty
            summary['total_value'] += value
            
            if status not in summary['by_status']:
                summary['by_status'][status] = {'count': 0, 'value': 0}
            
            summary['by_status'][status]['count'] += 1
            summary['by_status'][status]['value'] += value
            
            summary['details'].append({
                'equipment_id': eq.get('equipment_id'),
                'nama': eq.get('nama'),
                'quantity': qty,
                'value': value,
                'status': status
            })
        
        return summary
