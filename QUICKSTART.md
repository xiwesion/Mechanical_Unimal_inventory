# QUICKSTART - Inventory System

## ⚡ 5 Menit Setup & Run

### Step 1: Install Dependencies (2 menit)
```bash
cd c:\Users\sarag\OneDrive\Magang\Sistem\InventorySystem
pip install -r requirements.txt
```

### Step 2: Run Application (1 menit)
```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser otomatis di `http://localhost:8501`

---

## 🎮 First Time Setup

### 1. Tambah Lab (1 menit)
Setelah aplikasi terbuka:

1. **Sidebar** → 🏭 **Lab Management**
2. Tab **➕ Add New Lab**
3. Isi form:
   - **Lab ID**: `manufaktur` (format: lowercase, underscore)
   - **Nama Lab**: `Lab Manufaktur`
   - **Deskripsi**: `Laboratorium Manufaktur dan Proses Produksi`
4. Klik **➕ Tambah Lab**
5. ✅ Lab berhasil ditambahkan!

**Ulangi untuk 3 lab lainnya:**
- `material` → Lab Material
- `konversi_energi` → Lab Konversi Energi
- `konstruksi` → Lab Konstruksi

### 2. Import Equipment (2 menit) - RECOMMENDED

#### A. Download Template
1. **Sidebar** → 🔧 **Equipment Management**
2. Tab **📥 Import Equipment**
3. Pilih lab target (e.g., `Lab Manufaktur`)
4. Klik **📥 Download Template** → `equipment_template.xlsx`

#### B. Fill Template
Buka Excel file, isi baris 3+ dengan data equipment:

| Nama Equipment | Qty | Merk | Type | BoM | Harga Satuan | Kategori | Status |
|---|---|---|---|---|---|---|---|
| Mesin Bubut CNC | 2 | TOKOTA | CNC | M01 | 50000000 | Mesin | Aktif |
| Alat Ukur Digital | 5 | Mitutoyo | Caliper | M02 | 250000 | Alat Ukur | Aktif |
| Kompressor Udara | 1 | Atlas Copco | 15 HP | M03 | 75000000 | Mesin | Aktif |

**Minimal 3 kolom yang wajib:**
- ⭐ **Nama Equipment**
- ⭐ **Jumlah/Quantity**
- ⭐ **Harga Satuan**

#### C. Upload & Import
1. Back to app → Tab **📥 Import Equipment**
2. Klik **Choose File** → Select Excel file
3. Klik **📥 Import Data**
4. ✅ Data berhasil diimport!

### 3. View Dashboard (instant)
1. **Sidebar** → 📊 **Dashboard**
2. Lihat statistik real-time:
   - Total Lab
   - Total Equipment
   - Total Items
   - Total Value

---

## 📤 Basic Operations

### ➕ Barang Masuk
```
Sidebar → 📤 Inventory Adjustment → ➕ Barang Masuk
├─ Pilih Lab
├─ Pilih Equipment
├─ Input Jumlah Masuk
├─ Input Catatan
└─ Klik ✅ Catat Barang Masuk
```

### ➖ Barang Keluar
```
Sidebar → 📤 Inventory Adjustment → ➖ Barang Keluar
├─ Pilih Lab
├─ Pilih Equipment
├─ Input Jumlah Keluar (max: stok saat ini)
├─ Pilih Alasan (Penggunaan/Hilang/Rusak/dll)
├─ Input Catatan
└─ Klik ✅ Catat Barang Keluar
```

### 📊 Generate Report
```
Sidebar → 📈 Reports & Analytics → 📊 Stock Summary
├─ Filter Lab (optional)
├─ Lihat statistik per lab
├─ Lihat breakdown per status
└─ Download Excel (optional)
```

---

## 🔍 Tips & Tricks

### Tip 1: Search Equipment
Gunakan fitur Search untuk cari equipment dengan cepat:
```
Sidebar → 🔧 Equipment Management → 📊 Search
├─ Type nama atau merk
├─ Lihat hasil search
└─ View detail equipment
```

### Tip 2: Export Data
Export semua data untuk backup atau analisis:
```
Sidebar → 📈 Reports & Analytics → 📥 Export Report
├─ Pilih tipe export
├─ Klik 📥 Prepare Export
└─ Download file Excel
```

### Tip 3: Edit Equipment
Edit equipment langsung dari form:
```
Sidebar → 🔧 Equipment Management → 📋 View Equipment
├─ Klik equipment yang ingin diedit
├─ Ubah data
└─ Simpan
```

### Tip 4: Monitor History
Pantau semua pergerakan inventory:
```
Sidebar → 📤 Inventory Adjustment → 📝 History
├─ Filter tanggal
├─ Lihat semua movement
└─ Export ke Excel
```

---

## 🎯 Common Workflows

### Workflow 1: Inventory Awal Setup
```
1. Tambah 4 Lab
2. Download Template
3. Isi Equipment Data (100+ items)
4. Import ke sistem
5. Verifikasi di Dashboard
6. Export untuk backup
```

### Workflow 2: Daily Operations
```
Pagi:
  ├─ Cek Dashboard
  ├─ Catat barang masuk (pembelian baru)
  └─ Update stock status

Siang:
  ├─ Catat barang keluar (praktikum)
  └─ Monitor inventory

Akhir Hari:
  ├─ Generate consumption report
  └─ Backup data
```

### Workflow 3: Bulanan Reporting
```
1. Generate consumption report (1 bulan)
2. Export consumption data
3. Analyze in Excel
4. Send to management
5. Archive data
```

---

## 📱 Navigation Guide

### Pages Available
- 📊 **Dashboard** - Real-time overview
- 🏭 **Lab Management** - CRUD labs
- 🔧 **Equipment Management** - CRUD equipment + import/export
- 📤 **Inventory Adjustment** - Track in/out movements
- 📈 **Reports & Analytics** - Generate reports
- ⚙️ **Settings** - System info & data management

### Quick Keys
| Key | Action |
|---|---|
| `r` | Refresh page |
| `s` | Sidebar toggle |
| `?` | Help |

---

## ✅ Verification Checklist

Setelah setup, verifikasi:

- [ ] 4 Lab sudah ditambahkan
- [ ] Equipment sudah diimport (min 10 items)
- [ ] Dashboard menampilkan statistik
- [ ] Bisa catat barang masuk
- [ ] Bisa catat barang keluar
- [ ] Bisa generate report
- [ ] Bisa export ke Excel
- [ ] Excel template bisa didownload

---

## 🆘 If Something Goes Wrong

### Error: ModuleNotFoundError
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Error: Port 8501 Already in Use
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Error: Excel Import Failed
- ✅ File format: `.xlsx` (not `.xls`)
- ✅ Header row matches template
- ✅ No empty rows in middle
- ✅ Data types correct (number vs text)

### Error: Data Not Saved
```bash
# Check data folder permissions
cd data
ls -la  # On Mac/Linux
dir     # On Windows
```

---

## 📚 Next Steps

### Learn More
1. Read `README.md` for full documentation
2. Check `API_DOCUMENTATION.md` for details
3. Review `config/api_standards.py` for standards

### Customize
1. Edit `utils/constants.py` for custom colors
2. Modify `utils/helpers.py` for CSS styling
3. Add new modules in `modules/` folder

### Deploy
1. Follow `DEPLOYMENT_GUIDE.md`
2. Setup production environment
3. Configure security settings

---

## 🎉 You're Ready!

Aplikasi sudah siap digunakan. Mulai dengan:

1. ✅ Setup 4 lab
2. ✅ Import 20-30 equipment
3. ✅ Catat beberapa in/out movements
4. ✅ Generate pertama kali report
5. ✅ Explore semua fitur

Selamat menggunakan **Inventory System**! 🚀

---

**Questions?** Refer to README.md atau hubungi technical support.
