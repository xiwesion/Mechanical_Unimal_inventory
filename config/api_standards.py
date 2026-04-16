"""
API Standards and Configuration
Inventory System Standards
"""

# ============================================================================
# INVENTORY SYSTEM STANDARDS
# ============================================================================

INVENTORY_STANDARDS = {
    'version': '1.0',
    'organization': 'Lab Teknik Mesin',
    'standards': [
        'ISO 27001 - Data Security',
        'ISO 9001 - Quality Management',
        'Custom Inventory Best Practices'
    ]
}

# ============================================================================
# DATA VALIDATION STANDARDS
# ============================================================================

VALIDATION_STANDARDS = {
    'equipment_name': {
        'min_length': 3,
        'max_length': 100,
        'required': True,
        'pattern': '^[a-zA-Z0-9\s\-_()]+$'
    },
    'quantity': {
        'min': 0,
        'max': 999999,
        'required': True,
        'type': 'number'
    },
    'price': {
        'min': 0,
        'max': 999999999,
        'required': True,
        'type': 'number'
    },
    'lab_id': {
        'required': True,
        'pattern': '^[a-z_]+$'
    }
}

# ============================================================================
# RESPONSE FORMATS
# ============================================================================

RESPONSE_FORMATS = {
    'success': {
        'status': 'success',
        'code': 200,
        'message': 'Operation completed successfully'
    },
    'error': {
        'status': 'error',
        'code': 400,
        'message': 'Operation failed'
    },
    'not_found': {
        'status': 'error',
        'code': 404,
        'message': 'Resource not found'
    }
}

# ============================================================================
# DATABASE FIELD MAPPINGS
# ============================================================================

EQUIPMENT_FIELDS = {
    'equipment_id': {'type': 'string', 'required': False, 'auto_generate': True},
    'lab_id': {'type': 'string', 'required': True},
    'nama': {'type': 'string', 'required': True, 'min_length': 3},
    'jumlah': {'type': 'number', 'required': True, 'min': 0},
    'merk': {'type': 'string', 'required': False},
    'type': {'type': 'string', 'required': False},
    'bom': {'type': 'string', 'required': False},
    'harga_satuan': {'type': 'number', 'required': True, 'min': 0},
    'harga_keseluruhan': {'type': 'number', 'required': False, 'calculated': True},
    'kategori': {'type': 'string', 'required': False},
    'keterangan': {'type': 'string', 'required': False},
    'status': {'type': 'string', 'required': False, 'default': 'active'},
    'created_date': {'type': 'datetime', 'required': False, 'auto_generate': True},
    'last_modified': {'type': 'datetime', 'required': False, 'auto_generate': True},
    'quantity_history': {'type': 'array', 'required': False}
}

LAB_FIELDS = {
    'lab_id': {'type': 'string', 'required': True, 'pattern': '^[a-z_]+$'},
    'name': {'type': 'string', 'required': True},
    'description': {'type': 'string', 'required': False},
    'color': {'type': 'string', 'required': False},
    'created_date': {'type': 'datetime', 'required': False, 'auto_generate': True},
    'last_modified': {'type': 'datetime', 'required': False},
    'equipment_count': {'type': 'number', 'required': False, 'default': 0}
}

# ============================================================================
# ERROR MESSAGES
# ============================================================================

ERROR_MESSAGES = {
    'REQUIRED_FIELD': 'Kolom {field} wajib diisi',
    'INVALID_VALUE': 'Nilai {field} tidak valid',
    'DUPLICATE_ID': 'ID {id} sudah ada dalam sistem',
    'NOT_FOUND': '{entity} dengan ID {id} tidak ditemukan',
    'INVALID_QUANTITY': 'Jumlah tidak boleh negatif',
    'INVALID_PRICE': 'Harga tidak boleh negatif',
    'OPERATION_FAILED': 'Operasi gagal, silakan coba lagi'
}

# ============================================================================
# SUCCESS MESSAGES
# ============================================================================

SUCCESS_MESSAGES = {
    'CREATED': '{entity} berhasil ditambahkan',
    'UPDATED': '{entity} berhasil diupdate',
    'DELETED': '{entity} berhasil dihapus',
    'IMPORTED': '{count} {entity} berhasil diimport',
    'EXPORTED': 'Data berhasil diekspor'
}
