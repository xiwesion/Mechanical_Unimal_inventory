"""
Constants and Lookup Tables for Inventory Management System
Engineering Lab - Teknik Mesin
"""

# ============================================================================
# DEFAULT LABS
# ============================================================================
DEFAULT_LABS = {
    'manufaktur': {
        'name': 'Lab Manufaktur',
        'description': 'Laboratorium Manufaktur dan Proses Produksi',
        'color': '#E8F5E9'
    },
    'material': {
        'name': 'Lab Material',
        'description': 'Laboratorium Sifat dan Pengujian Material',
        'color': '#E3F2FD'
    },
    'konversi_energi': {
        'name': 'Lab Konversi Energi',
        'description': 'Laboratorium Konversi Energi dan Termodinamika',
        'color': '#FCE4EC'
    },
    'konstruksi': {
        'name': 'Lab Konstruksi',
        'description': 'Laboratorium Peralatan dan Konstruksi',
        'color': '#FFF3E0'
    }
}

# ============================================================================
# EQUIPMENT TYPES
# ============================================================================
EQUIPMENT_TYPES = [
    'Mesin',
    'Alat Ukur',
    'Peralatan Bengkel',
    'Peralatan Uji',
    'Peralatan Keselamatan',
    'Komponen Spare Part',
    'Konsumable',
    'Peralatan Peraga',
    'Software/Lisensi',
    'Lainnya'
]

# ============================================================================
# EQUIPMENT STATUS
# ============================================================================
EQUIPMENT_STATUS = {
    'active': {'label': 'Aktif', 'color': '#4CAF50'},
    'maintenance': {'label': 'Maintenance', 'color': '#FFC107'},
    'depleted': {'label': 'Habis Pakai', 'color': '#F44336'},
    'archived': {'label': 'Diarsipkan', 'color': '#9E9E9E'}
}

# ============================================================================
# INVENTORY MOVEMENT TYPES
# ============================================================================
MOVEMENT_TYPES = {
    'in': {'label': 'Barang Masuk', 'icon': '📥', 'color': '#4CAF50'},
    'out': {'label': 'Barang Keluar', 'icon': '📤', 'color': '#F44336'},
    'adjustment': {'label': 'Penyesuaian', 'icon': '⚙️', 'color': '#2196F3'},
    'transfer': {'label': 'Transfer Antar Lab', 'icon': '↔️', 'color': '#FF9800'}
}

# ============================================================================
# COLOR PALETTE - SOFT BRIGHT ELEGANT THEME
# ============================================================================
COLOR_PALETTE = {
    # Primary Colors - Soft & Elegant
    'primary_light': '#E8F5E9',      # Very soft green
    'primary': '#A5D6A7',             # Soft green
    'primary_dark': '#66BB6A',        # Medium green
    'primary_darker': '#43A047',      # Dark green
    
    # Secondary Colors - Soft blue
    'secondary_light': '#E3F2FD',     # Very soft blue
    'secondary': '#90CAF9',           # Soft blue
    'secondary_dark': '#42A5F5',      # Medium blue
    
    # Accent Colors
    'accent_pink': '#F8BBD0',         # Soft pink
    'accent_orange': '#FFE0B2',       # Soft orange
    'accent_purple': '#E1BEE7',       # Soft purple
    
    # Status Colors
    'success': '#66BB6A',             # Green
    'warning': '#FFA726',             # Orange
    'danger': '#EF5350',              # Red
    'info': '#42A5F5',                # Blue
    
    # Neutral Colors
    'text_dark': '#2C3E50',           # Dark gray-blue
    'text_light': '#7F8C8D',          # Light gray
    'border': '#E8EAED',              # Light border
    'background': '#FAFBFC'           # Off white
}

# ============================================================================
# SOFT THEME COLOR SCHEMES
# ============================================================================
THEME_COLORS = {
    'gradient_bg': 'linear-gradient(135deg, #E8F5E9 0%, #E3F2FD 100%)',
    'card_bg': '#FFFFFF',
    'card_border': '#E8EAED',
    'hover_bg': '#F5F5F5'
}

# ============================================================================
# THEME OPTIONS - SELECTABLE THEMES
# ============================================================================
THEME_OPTIONS = {
    'sage': {
        'name': '🌿 Hijau Sage',
        'primary_light': '#E8F5E9',
        'primary': '#A5D6A7',
        'primary_dark': '#66BB6A',
        'secondary_light': '#E3F2FD',
        'secondary': '#90CAF9',
        'nav_text': '#1B5E20',
        'gradient_bg': 'linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%)'
    },
    'sky': {
        'name': '🌤️ Biru Langit',
        'primary_light': '#E3F2FD',
        'primary': '#90CAF9',
        'primary_dark': '#42A5F5',
        'secondary_light': '#E0F2F1',
        'secondary': '#80DEEA',
        'nav_text': '#01579B',
        'gradient_bg': 'linear-gradient(135deg, #E3F2FD 0%, #E0F2F1 100%)'
    },
    'tecno': {
        'name': '⚡ Tecno',
        'primary_light': '#F3E5F5',
        'primary': '#CE93D8',
        'primary_dark': '#AB47BC',
        'secondary_light': '#E8EAF6',
        'secondary': '#9FA8DA',
        'nav_text': '#4A148C',
        'gradient_bg': 'linear-gradient(135deg, #F3E5F5 0%, #E8EAF6 100%)'
    },
    'abyss': {
        'name': '🌑 Abyss',
        'primary_light': '#1A1A2E',
        'primary': '#16213E',
        'primary_dark': '#0F3460',
        'secondary_light': '#2D3561',
        'secondary': '#533483',
        'nav_text': '#E0E0E0',
        'gradient_bg': 'linear-gradient(135deg, #1A1A2E 0%, #16213E 100%)'
    }
}

# ============================================================================
# FORM VALIDATION
# ============================================================================
MIN_EQUIPMENT_NAME_LENGTH = 3
MAX_EQUIPMENT_NAME_LENGTH = 100
MIN_QUANTITY = 0
MAX_QUANTITY = 999999

# ============================================================================
# DATE FORMATS
# ============================================================================
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DISPLAY_DATE_FORMAT = '%d %B %Y'
DISPLAY_DATETIME_FORMAT = '%d %b %Y, %H:%M'
