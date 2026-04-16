# Inventory System for Engineering Lab
## Sistem Manajemen Inventory Lab Teknik Mesin

> **Modern Inventory Management System** dengan UI yang user-friendly dan fitur lengkap untuk mengelola equipment dan aset di laboratorium teknik mesin.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Database Structure](#database-structure)
- [API Documentation](#api-documentation)
- [UI/UX Design](#uiux-design)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

Sistem Inventory Lab Teknik Mesin adalah aplikasi berbasis **Streamlit** yang dirancang untuk mengelola equipment dan aset di 4 laboratorium teknik mesin:
- **Lab Manufaktur** - Manufaktur dan Proses Produksi
- **Lab Material** - Sifat dan Pengujian Material
- **Lab Konversi Energi** - Konversi Energi dan Termodinamika
- **Lab Konstruksi** - Peralatan dan Konstruksi

Sistem ini mengikuti arsitektur yang sama dengan **RBI Calculator** yang sudah dikembangkan sebelumnya, memastikan konsistensi dan kemudahan maintenance.

---

## ✨ Features

### 1. 📊 Dashboard
- **Real-time Statistics**: Total lab, equipment, items, dan nilai aset
- **Visual Analytics**: Grafik distribusi equipment per lab dan per status
- **Quick Overview**: Ringkasan inventory pada halaman utama

### 2. 🏭 Lab Management
- **Add New Lab**: Tambahkan lab baru dengan mudah
- **Edit Lab**: Update informasi lab yang sudah ada
- **Delete Lab**: Hapus lab (dengan validasi equipment)
- **Lab Statistics**: Lihat statistik per lab

### 3. 🔧 Equipment Management
- **Add Equipment**: Tambahkan equipment dengan data lengkap
- **View Equipment**: Lihat semua equipment dengan filter per lab
- **Search Equipment**: Cari equipment berdasarkan nama atau merk
- **Edit Equipment**: Update informasi equipment
- **Delete Equipment**: Hapus equipment dari sistem

**Data Fields per Equipment:**
- Nama Equipment
- Jumlah/Volume
- Merk
- Type
- BoM (Bill of Materials)
- Harga Satuan
- Harga Keseluruhan (otomatis: qty × harga satuan)
- Kategori
- Keterangan/Notes
- Status (Aktif, Maintenance, Habis Pakai, Diarsipkan)

### 4. 📤 Inventory Adjustment
- **Barang Masuk (In)**: Catat equipment yang masuk ke inventory
- **Barang Keluar (Out)**: Catat equipment yang digunakan/keluar
- **Movement History**: Lihat riwayat pergerakan inventory per periode
- **Auto Status Update**: Status otomatis berubah jadi "Habis Pakai" saat qty = 0

**Movement Types:**
- ➕ Barang Masuk (In)
- ➖ Barang Keluar (Out)
- ⚙️ Penyesuaian (Adjustment)
- ↔️ Transfer Antar Lab (Transfer)

### 5. 📥 Template System
- **Download Template**: Unduh Excel template yang sudah terformat
- **Import Data**: Import equipment secara bulk dari Excel
- **Validation**: Validasi data saat import dengan error handling yang jelas
- **Batch Processing**: Import hingga ratusan equipment sekaligus

### 6. 📈 Reports & Analytics
- **Stock Summary**: Ringkasan stok saat ini per lab atau semua lab
- **Consumption Report**: Laporan equipment yang dikonsumsi per periode
- **Status Breakdown**: Analisis equipment berdasarkan status
- **Export Reports**: Export ke Excel untuk analisis lanjutan

**Report Types:**
- 📊 Stock Summary (Real-time inventory status)
- 🗑️ Consumption Report (Equipment habis pakai)
- 📥 Export Report (Bulk export ke Excel)

### 7. ⚙️ Settings & Configuration
- **System Info**: Informasi sistem dan statistik
- **Data Management**: Backup dan export data
- **About**: Informasi aplikasi dan teknologi

---

## 🚀 Installation

### Prerequisites
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Step 1: Clone/Copy Project
```bash
cd c:\Users\sarag\OneDrive\Magang\Sistem\InventorySystem
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Requirements:**
- `streamlit>=1.28.0` - Web framework
- `pandas>=2.1.0` - Data manipulation
- `numpy>=1.26.0` - Numerical computing
- `matplotlib>=3.8.0` - Plotting
- `plotly>=5.17.0` - Interactive charts
- `openpyxl>=3.1.0` - Excel handling
- `python-dateutil>=2.8.2` - Date utilities

### Step 3: Run Application
```bash
streamlit run app.py
```

Aplikasi akan membuka di `http://localhost:8501`

---

## 📖 Usage

### Basic Workflow

#### 1️⃣ Setup: Tambah Lab
1. Buka sidebar → **🏭 Lab Management**
2. Klik tab **➕ Add New Lab**
3. Isi nama dan deskripsi lab
4. Klik **➕ Tambah Lab**

#### 2️⃣ Add Equipment Manually
1. Buka sidebar → **🔧 Equipment Management**
2. Klik tab **➕ Add Equipment**
3. Pilih lab target
4. Isi semua data equipment
5. Klik **➕ Tambah Equipment**

#### 3️⃣ Import Equipment Bulk (Recommended)
1. Buka sidebar → **🔧 Equipment Management**
2. Klik tab **📥 Import Equipment**
3. Klik **📥 Download Template**
4. Isi template Excel dengan data equipment
5. Upload file Excel
6. Klik **📥 Import Data**

#### 4️⃣ Monitor Inventory
1. Buka sidebar → **📊 Dashboard**
2. Lihat statistik real-time dan grafik

#### 5️⃣ Track In/Out
1. Buka sidebar → **📤 Inventory Adjustment**
2. Catat barang masuk atau keluar
3. Lihat history di tab **📝 History**

#### 6️⃣ Generate Reports
1. Buka sidebar → **📈 Reports & Analytics**
2. Pilih tipe report yang diinginkan
3. Filter berdasarkan lab dan periode
4. Export ke Excel jika diperlukan

---

## 🏗️ Architecture

### Project Structure
```
InventorySystem/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── config/
│   ├── __init__.py
│   └── api_standards.py           # API & validation standards
├── data/
│   ├── labs_registry.json         # Labs database
│   ├── equipment_registry.json    # Equipment database
│   └── inventory_movements.json   # Movements log
├── modules/
│   ├── __init__.py
│   ├── lab_manager.py             # Lab CRUD operations
│   ├── equipment_manager.py       # Equipment CRUD & tracking
│   ├── inventory_manager.py       # Inventory movements & reports
│   └── template_handler.py        # Excel import/export
├── utils/
│   ├── __init__.py
│   ├── constants.py               # System constants & colors
│   ├── helpers.py                 # CSS injection
│   └── validation.py              # Data validation
├── visualization/
│   ├── __init__.py
│   └── inventory_visualizer.py   # Charts & analytics
├── templates/
│   └── equipment_template.xlsx   # Excel template
└── README.md                      # This file
```

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Backend**: Pure Python (no database needed)
- **Data Storage**: JSON files (Simple, no SQL setup needed)
- **Data Processing**: Pandas & NumPy
- **Visualization**: Plotly & Matplotlib
- **Excel**: openpyxl
- **Styling**: Custom CSS (soft & elegant theme)

### Design Pattern
```
┌─────────────────────────────┐
│    Streamlit UI (app.py)    │
│   (Pages & Interactions)    │
└────────────┬────────────────┘
             │
┌────────────▼────────────────┐
│    Business Logic Modules   │
├─────────────────────────────┤
│ - LabManager                │
│ - EquipmentManager          │
│ - InventoryManager          │
│ - TemplateHandler           │
└────────────┬────────────────┘
             │
┌────────────▼────────────────┐
│   JSON Data Storage         │
├─────────────────────────────┤
│ - labs_registry.json        │
│ - equipment_registry.json   │
│ - inventory_movements.json  │
└─────────────────────────────┘
```

---

## 💾 Database Structure

### Labs Database (`labs_registry.json`)
```json
{
  "manufaktur": {
    "lab_id": "manufaktur",
    "name": "Lab Manufaktur",
    "description": "Laboratorium Manufaktur dan Proses Produksi",
    "color": "#E8F5E9",
    "created_date": "2026-04-16T10:30:00",
    "equipment_count": 5
  }
}
```

### Equipment Database (`equipment_registry.json`)
```json
{
  "a1b2c3d4": {
    "equipment_id": "a1b2c3d4",
    "lab_id": "manufaktur",
    "nama": "Mesin Bubut CNC",
    "jumlah": 2,
    "merk": "TOKOTA",
    "type": "CNC",
    "bom": "M01",
    "harga_satuan": 50000000,
    "harga_keseluruhan": 100000000,
    "kategori": "Mesin",
    "keterangan": "Kondisi baik",
    "status": "active",
    "created_date": "2026-04-16T10:30:00",
    "last_modified": "2026-04-16T10:30:00",
    "quantity_history": [
      {
        "date": "2026-04-16T10:30:00",
        "quantity": 2,
        "type": "initial",
        "notes": "Penambahan awal"
      }
    ]
  }
}
```

### Inventory Movements Database (`inventory_movements.json`)
```json
[
  {
    "movement_id": "a1b2c3d4_1681638600",
    "equipment_id": "a1b2c3d4",
    "lab_id": "manufaktur",
    "movement_type": "out",
    "quantity": -1,
    "date": "2026-04-16T14:30:00",
    "notes": "Penggunaan: Praktikum mahasiswa"
  }
]
```

---

## 📊 UI/UX Design

### Color Theme - Soft & Elegant
Menggunakan palet warna yang lembut, cerah, dan elegan tanpa kontras yang berlebihan:

**Primary Colors:**
- `#E8F5E9` - Very Soft Green (backgrounds)
- `#A5D6A7` - Soft Green (primary elements)
- `#66BB6A` - Medium Green (active states)

**Secondary Colors:**
- `#E3F2FD` - Very Soft Blue (accents)
- `#90CAF9` - Soft Blue (secondary elements)
- `#42A5F5` - Medium Blue (info)

**Accent Colors:**
- `#F8BBD0` - Soft Pink
- `#FFE0B2` - Soft Orange
- `#E1BEE7` - Soft Purple

**Status Colors:**
- `#66BB6A` - Success/Active (Green)
- `#FFA726` - Warning/Maintenance (Orange)
- `#EF5350` - Danger/Depleted (Red)
- `#42A5F5` - Info (Blue)

### Animations
- `fadeInUp` - Elemen muncul dari bawah (0.6s)
- `slideDown` - Elemen meluncur dari atas (0.4s)
- `scaleIn` - Elemen scale in (0.4s)
- `pulse` - Elemen berkedipan halus
- `glow` - Shadow effect glow
- `shimmer` - Shimmer effect

### Responsive Design
- Desktop: Full layout dengan sidebar
- Tablet: Adaptive layout
- Mobile: Optimized untuk layar kecil

---

## 🔌 API Documentation

### LabManager
```python
# Add new lab
lab_manager.add_lab(lab_id, lab_data)  # Returns: bool

# Get labs
lab_manager.get_all_labs()             # Returns: List[Dict]
lab_manager.get_lab(lab_id)            # Returns: Dict | None
lab_manager.list_lab_ids()             # Returns: List[str]

# Update/Delete
lab_manager.update_lab(lab_id, data)   # Returns: bool
lab_manager.delete_lab(lab_id)         # Returns: bool

# Stats
lab_manager.get_stats()                # Returns: Dict
```

### EquipmentManager
```python
# Add/Get
equipment_manager.add_equipment(lab_id, data)        # Returns: str (ID)
equipment_manager.get_equipment(equipment_id)        # Returns: Dict | None
equipment_manager.get_all_equipment()                # Returns: List[Dict]
equipment_manager.get_equipment_by_lab(lab_id)       # Returns: List[Dict]

# Search
equipment_manager.search_equipment(query)            # Returns: List[Dict]

# Update/Delete
equipment_manager.update_equipment(eq_id, data)      # Returns: bool
equipment_manager.delete_equipment(eq_id)            # Returns: bool

# Quantity
equipment_manager.adjust_quantity(eq_id, qty_change) # Returns: bool

# Stats
equipment_manager.get_statistics()                   # Returns: Dict
```

### InventoryManager
```python
# Record movement
inventory_manager.record_movement(eq_id, lab_id, type, qty, notes)  # Returns: bool

# Get movements
inventory_manager.get_movements(lab_id, start_date, end_date, type) # Returns: List[Dict]
inventory_manager.get_equipment_movements(eq_id)                    # Returns: List[Dict]

# Reports
inventory_manager.get_depletion_report(lab_id, start_date, end_date) # Returns: Dict
inventory_manager.get_stock_summary(lab_id)                         # Returns: Dict
```

### TemplateHandler
```python
# Template
template_handler.get_template()                      # Returns: bytes

# Import/Export
template_handler.import_equipment(file, lab_id)      # Returns: (bool, str, List)
template_handler.export_equipment(equipment_list)    # Returns: bytes
template_handler.export_consumption_report(data)     # Returns: bytes
```

---

## 🐛 Troubleshooting

### Issue: Streamlit tidak bisa di-run
**Solution:**
```bash
# Reinstall streamlit
pip uninstall streamlit
pip install streamlit>=1.28.0
```

### Issue: Excel import gagal
**Solution:**
- Pastikan format file: `.xlsx` (bukan `.xls`)
- Pastikan kolom header sesuai template
- Pastikan tidak ada baris kosong di tengah data

### Issue: Data tidak tersimpan
**Solution:**
- Cek folder `data/` apakah ada
- Cek permission folder write
- Cek file `.json` corruption

### Issue: Performa lambat
**Solution:**
- Kurangi jumlah data display (gunakan filter)
- Tutup tab yang tidak digunakan
- Restart aplikasi

---

## 📚 Additional Resources

### Related Systems
- **RBI Calculator**: Risk-Based Inspection system (main reference)
- **Lab Teknik Mesin**: University Engineering Lab

### Documentation Files
- `QUICKSTART.md` - Quick start guide
- `API_DOCUMENTATION.md` - Detailed API reference
- `DEPLOYMENT_GUIDE.md` - Deployment instructions
- `MAINTENANCE_GUIDE.md` - System maintenance

---

## 📝 License & Credits

**Developed for:** Lab Teknik Mesin  
**Based on:** RBI Calculator Architecture  
**Technology:** Streamlit + Python  
**Year:** 2026

---

## 📞 Support & Contact

Untuk pertanyaan atau bantuan, hubungi:
- **Lab Teknik Mesin**
- **Technical Support Team**

---

**Terakhir diupdate:** April 16, 2026  
**Versi:** 1.0  
**Status:** ✅ Production Ready
