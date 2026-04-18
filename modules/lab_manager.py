"""
Lab Manager Module
Handles lab registry, storage, and retrieval
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

class LabManager:
    """Manages lab registry and storage"""
    
    DATA_DIR = Path(__file__).parent.parent / "data"
    LABS_FILE = DATA_DIR / "labs_registry.json"
    
    def __init__(self):
        """Initialize lab manager"""
        self.labs = self._load_labs()
    
    def _ensure_dir(self):
        """Ensure data directory exists"""
        self.DATA_DIR.mkdir(exist_ok=True)
    
    def _load_labs(self) -> Dict:
        """Load labs from JSON file"""
        self._ensure_dir()
        
        if self.LABS_FILE.exists():
            try:
                with open(self.LABS_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading labs: {e}")
                return self._get_default_labs()
        return self._get_default_labs()
    
    def _save_labs(self):
        """Save labs to JSON file"""
        self._ensure_dir()
        try:
            with open(self.LABS_FILE, 'w') as f:
                json.dump(self.labs, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving labs: {e}")
    
    def _get_default_labs(self) -> Dict:
        """Get default labs"""
        from utils.constants import DEFAULT_LABS
        return {
            lab_id: {
                **lab_info,
                'lab_id': lab_id,
                'created_date': datetime.now().isoformat(),
                'equipment_count': 0
            }
            for lab_id, lab_info in DEFAULT_LABS.items()
        }
    
    def add_lab(self, lab_id: str, lab_data: Dict) -> bool:
        """
        Add new lab
        
        Args:
            lab_id: Unique lab identifier (slug format: lab_name)
            lab_data: Dictionary with lab information
        
        Returns:
            True if successful
        """
        try:
            lab_id = lab_id.strip().lower().replace(' ', '_')
            
            if not lab_id:
                raise ValueError("Lab ID cannot be empty")
            
            if lab_id in self.labs:
                raise ValueError("Lab already exists")
            
            # Add metadata
            lab_data['lab_id'] = lab_id
            lab_data['created_date'] = datetime.now().isoformat()
            lab_data['equipment_count'] = 0
            
            self.labs[lab_id] = lab_data
            self._save_labs()
            
            return True
        except Exception as e:
            print(f"Error adding lab: {e}")
            return False
    
    def get_lab(self, lab_id: str) -> Optional[Dict]:
        """Get specific lab"""
        lab_id = lab_id.strip().lower().replace(' ', '_')
        return self.labs.get(lab_id)
    
    def get_all_labs(self) -> List[Dict]:
        """Get all labs"""
        return list(self.labs.values())
    
    def list_lab_ids(self) -> List[str]:
        """Get list of all lab IDs"""
        return sorted(list(self.labs.keys()))
    
    def update_lab(self, lab_id: str, lab_data: Dict) -> bool:
        """Update lab information"""
        try:
            lab_id = lab_id.strip().lower().replace(' ', '_')
            
            if lab_id not in self.labs:
                raise ValueError("Lab not found")
            
            # Preserve original data and update
            existing = self.labs[lab_id]
            existing.update(lab_data)
            existing['last_modified'] = datetime.now().isoformat()
            
            self._save_labs()
            return True
        except Exception as e:
            print(f"Error updating lab: {e}")
            return False
    
    def delete_lab(self, lab_id: str) -> bool:
        """Delete lab from registry"""
        try:
            lab_id = lab_id.strip().lower().replace(' ', '_')
            
            if lab_id not in self.labs:
                raise ValueError("Lab not found")
            
            # Check if lab has equipment
            from modules.equipment_manager import EquipmentManager
            em = EquipmentManager()
            lab_equipment = em.get_equipment_by_lab(lab_id)
            
            if lab_equipment:
                raise ValueError(f"Cannot delete lab with {len(lab_equipment)} equipment. Please delete equipment first.")
            
            del self.labs[lab_id]
            self._save_labs()
            
            return True
        except Exception as e:
            print(f"Error deleting lab: {e}")
            return False
    
    def update_equipment_count(self, lab_id: str, count: int) -> bool:
        """Update equipment count for a lab"""
        try:
            lab_id = lab_id.strip().lower().replace(' ', '_')
            
            if lab_id not in self.labs:
                return False
            
            self.labs[lab_id]['equipment_count'] = count
            self._save_labs()
            return True
        except Exception as e:
            print(f"Error updating equipment count: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Get overall lab statistics"""
        from modules.equipment_manager import EquipmentManager
        em = EquipmentManager()
        
        stats = {
            'total_labs': len(self.labs),
            'total_equipment': len(em.get_all_equipment()),
            'labs': {}
        }
        
        for lab_id, lab in self.labs.items():
            lab_equipment = em.get_equipment_by_lab(lab_id)
            stats['labs'][lab_id] = {
                'name': lab.get('name'),
                'equipment_count': len(lab_equipment),
                'total_value': sum(eq.get('harga_keseluruhan', 0) for eq in lab_equipment)
            }
        
        return stats
    
    def reset_all_data(self) -> bool:
        """
        Reset all lab data (delete everything)
        
        Returns:
            True if successful
        """
        try:
            self.labs = {}
            self._save_labs()
            print("All labs data has been reset")
            return True
        except Exception as e:
            print(f"Error resetting labs data: {e}")
            return False
