"""
Validation Module
Handles data validation for inventory system
"""
from datetime import datetime
import re
from typing import Tuple, List, Dict

class ValidationFramework:
    """Validates inventory data"""
    
    @staticmethod
    def validate_equipment(equipment_data: Dict) -> Tuple[bool, str]:
        """
        Validate equipment data
        
        Args:
            equipment_data: Equipment data dictionary
        
        Returns:
            (is_valid, error_message)
        """
        errors = []
        
        # Validate nama (required)
        nama = equipment_data.get('nama', '').strip()
        if not nama:
            errors.append("Nama equipment wajib diisi")
        elif len(nama) < 3:
            errors.append("Nama equipment minimal 3 karakter")
        elif len(nama) > 100:
            errors.append("Nama equipment maksimal 100 karakter")
        
        # Validate jumlah (required)
        try:
            jumlah = float(equipment_data.get('jumlah', 0))
            if jumlah < 0:
                errors.append("Jumlah tidak boleh negatif")
        except (ValueError, TypeError):
            errors.append("Jumlah harus berupa angka")
        
        # Validate harga_satuan (required)
        try:
            harga = float(equipment_data.get('harga_satuan', 0))
            if harga < 0:
                errors.append("Harga satuan tidak boleh negatif")
        except (ValueError, TypeError):
            errors.append("Harga satuan harus berupa angka")
        
        # Validate status
        status = equipment_data.get('status', '').lower()
        valid_status = ['active', 'maintenance', 'depleted', 'archived']
        if status and status not in valid_status:
            errors.append(f"Status harus salah satu dari: {', '.join(valid_status)}")
        
        # Validate type
        eq_type = equipment_data.get('type', '').strip()
        if eq_type and len(eq_type) > 50:
            errors.append("Type maksimal 50 karakter")
        
        if errors:
            return False, "; ".join(errors)
        
        return True, ""
    
    @staticmethod
    def validate_lab(lab_data: Dict) -> Tuple[bool, str]:
        """
        Validate lab data
        
        Args:
            lab_data: Lab data dictionary
        
        Returns:
            (is_valid, error_message)
        """
        errors = []
        
        # Validate name (required)
        name = lab_data.get('name', '').strip()
        if not name:
            errors.append("Nama lab wajib diisi")
        elif len(name) < 3:
            errors.append("Nama lab minimal 3 karakter")
        elif len(name) > 100:
            errors.append("Nama lab maksimal 100 karakter")
        
        # Validate description
        description = lab_data.get('description', '').strip()
        if description and len(description) > 500:
            errors.append("Deskripsi maksimal 500 karakter")
        
        if errors:
            return False, "; ".join(errors)
        
        return True, ""
    
    @staticmethod
    def validate_lab_id(lab_id: str) -> Tuple[bool, str]:
        """
        Validate lab ID format
        
        Args:
            lab_id: Lab ID to validate
        
        Returns:
            (is_valid, error_message)
        """
        if not lab_id:
            return False, "Lab ID wajib diisi"
        
        lab_id = lab_id.strip()
        
        # Check pattern: lowercase with underscores
        if not re.match(r'^[a-z_]+$', lab_id):
            return False, "Lab ID hanya boleh berisi huruf kecil dan underscore"
        
        if len(lab_id) < 3:
            return False, "Lab ID minimal 3 karakter"
        
        if len(lab_id) > 50:
            return False, "Lab ID maksimal 50 karakter"
        
        return True, ""
    
    @staticmethod
    def validate_quantity_movement(equipment_id: str, current_qty: float, 
                                   qty_change: float) -> Tuple[bool, str]:
        """
        Validate inventory movement
        
        Args:
            equipment_id: Equipment ID
            current_qty: Current quantity
            qty_change: Quantity change (can be negative)
        
        Returns:
            (is_valid, error_message)
        """
        errors = []
        
        if not equipment_id:
            errors.append("Equipment ID wajib diisi")
        
        if qty_change == 0:
            errors.append("Jumlah perubahan harus tidak nol")
        
        new_qty = current_qty + qty_change
        
        if new_qty < 0:
            errors.append(f"Operasi akan membuat stok negatif ({new_qty})")
        
        if errors:
            return False, "; ".join(errors)
        
        return True, ""
    
    @staticmethod
    def validate_import_data(dataframe, required_columns: List[str]) -> Tuple[bool, str]:
        """
        Validate imported Excel data
        
        Args:
            dataframe: Pandas dataframe
            required_columns: List of required columns
        
        Returns:
            (is_valid, error_message)
        """
        errors = []
        
        if dataframe.empty:
            return False, "File Excel kosong"
        
        # Check required columns
        for col in required_columns:
            if col not in dataframe.columns:
                errors.append(f"Kolom '{col}' tidak ditemukan dalam file")
        
        if errors:
            return False, "; ".join(errors)
        
        return True, ""
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
        """
        Validate date range
        
        Args:
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
        
        Returns:
            (is_valid, error_message)
        """
        try:
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
            
            if start > end:
                return False, "Tanggal mulai harus sebelum tanggal akhir"
            
            return True, ""
        except (ValueError, TypeError) as e:
            return False, f"Format tanggal tidak valid: {str(e)}"
    
    @staticmethod
    def sanitize_equipment_name(name: str) -> str:
        """
        Sanitize equipment name
        
        Args:
            name: Equipment name
        
        Returns:
            Sanitized name
        """
        # Remove extra whitespace
        name = ' '.join(name.split())
        
        # Keep only alphanumeric, spaces, and common symbols
        name = re.sub(r'[^a-zA-Z0-9\s\-_()./:&]', '', name)
        
        return name.strip()
    
    @staticmethod
    def sanitize_lab_id(lab_id: str) -> str:
        """
        Sanitize lab ID
        
        Args:
            lab_id: Lab ID
        
        Returns:
            Sanitized lab ID
        """
        # Convert to lowercase
        lab_id = lab_id.lower()
        
        # Replace spaces with underscores
        lab_id = lab_id.replace(' ', '_')
        
        # Remove special characters
        lab_id = re.sub(r'[^a-z_0-9]', '', lab_id)
        
        return lab_id.strip('_')
