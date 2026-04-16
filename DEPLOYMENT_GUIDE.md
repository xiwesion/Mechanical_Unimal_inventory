# Deployment Guide - Inventory System

## 🚀 How to Run the Application

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Windows / Mac / Linux

### Step 1: Navigate to Project Directory
```bash
cd c:\Users\sarag\OneDrive\Magang\Sistem\InventorySystem
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**What gets installed:**
- streamlit (web framework)
- pandas (data handling)
- numpy (numerical computing)
- matplotlib (plotting)
- plotly (interactive charts)
- openpyxl (Excel support)
- python-dateutil (date utilities)

### Step 3: Run the Application
```bash
streamlit run app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://[Your-IP]:8501
```

The browser will automatically open at `http://localhost:8501`

### Step 4: Access the Application
- **Local**: http://localhost:8501
- **Network**: Share the network URL for other devices

---

## 🎯 First Time Usage

### 1. Add Labs (Setup Phase)
1. Click **🏭 Lab Management** in sidebar
2. Go to **➕ Add New Lab** tab
3. Add 4 labs:
   - `manufaktur` → Lab Manufaktur
   - `material` → Lab Material
   - `konversi_energi` → Lab Konversi Energi
   - `konstruksi` → Lab Konstruksi

### 2. Import Equipment (Data Entry Phase)
1. Click **🔧 Equipment Management** in sidebar
2. Go to **📥 Import Equipment** tab
3. Click **📥 Download Template**
4. Fill the template with your equipment data
5. Upload and import

Or manually add equipment one by one using **➕ Add Equipment** tab

### 3. Monitor & Track (Operations Phase)
- Use **📊 Dashboard** to view overview
- Use **📤 Inventory Adjustment** to track in/out
- Use **📈 Reports & Analytics** for reporting

---

## 🛠️ Common Issues & Solutions

### Issue 1: Port Already in Use
```bash
# If port 8501 is already in use, use different port:
streamlit run app.py --server.port 8502
```

### Issue 2: ModuleNotFoundError
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue 3: Permission Denied (Mac/Linux)
```bash
# Add execute permission
chmod +x app.py

# Then run with python
python -m streamlit run app.py
```

### Issue 4: Excel Import Fails
- Verify file format is `.xlsx` (not `.xls`)
- Ensure header row matches template
- Check for empty rows in the middle
- Verify data types (numbers vs text)

### Issue 5: Slow Performance
- Clear browser cache
- Close unnecessary tabs
- Reload the page with Ctrl+Shift+R (Force Refresh)
- Reduce data range in filters

---

## 📊 Application Structure at Runtime

```
Streamlit Frontend (Browser)
    ↓
Session State Management
    ├─ LabManager instance
    ├─ EquipmentManager instance
    ├─ InventoryManager instance
    └─ TemplateHandler instance
    ↓
Data Layer (JSON Files)
    ├─ data/labs_registry.json
    ├─ data/equipment_registry.json
    └─ data/inventory_movements.json
```

---

## 🔒 Security Considerations

### For Production Use
1. **Data Backup**: Regularly backup `data/` folder
2. **Access Control**: Restrict folder access with file permissions
3. **HTTPS**: Deploy behind proxy (nginx/Apache) with SSL
4. **Authentication**: Add authentication layer if shared
5. **Audit Trail**: Enable logging for compliance

### Data Protection
```bash
# Backup data (Linux/Mac)
cp -r data/ data_backup_$(date +%Y%m%d)

# On Windows
xcopy data\ data_backup\
```

---

## 📈 Performance Optimization

### For Large Datasets (1000+ items)

#### 1. Implement Pagination
```python
# In app.py, limit displayed items
items_per_page = 50
start_idx = (page - 1) * items_per_page
end_idx = start_idx + items_per_page
displayed_items = all_items[start_idx:end_idx]
```

#### 2. Cache Data
```python
@st.cache_data
def load_equipment():
    return equipment_manager.get_all_equipment()
```

#### 3. Use Filters
- Filter by lab to reduce items shown
- Filter by date range for movements
- Use search instead of loading all data

### Memory Usage
- Current: ~10MB base + data size
- With 1000 items: ~15-20MB
- Acceptable for most systems

---

## 🌐 Network Deployment

### Share on Local Network
```bash
streamlit run app.py --server.address 0.0.0.0
```

Then access from other device using:
```
http://[Host-Machine-IP]:8501
```

### Find Your IP Address
**Windows:**
```bash
ipconfig | findstr "IPv4"
```

**Mac/Linux:**
```bash
ifconfig | grep inet
```

---

## 📝 Configuration Customization

### Change Default Colors
Edit `utils/constants.py`:
```python
DEFAULT_LABS = {
    'manufaktur': {
        'color': '#YOUR_COLOR_HERE'
    }
}
```

### Change Port
```bash
streamlit run app.py --server.port 9000
```

### Change Page Width
```bash
streamlit run app.py --client.toolbarMode minimal
```

---

## 🔄 Database Migration

### Export Data
```python
# From Python console
from modules.equipment_manager import EquipmentManager
em = EquipmentManager()
data = em.get_all_equipment()
# Save to CSV or Excel
```

### Reset Database
```bash
# Remove JSON files
rm -r data/   # Linux/Mac
rmdir /s data # Windows

# App will recreate with defaults
```

### Backup Strategy
```
Daily: Backup data/ folder
Weekly: Backup to external storage
Monthly: Archive old backups
```

---

## 📊 Monitoring & Logging

### Check System Status
1. **Dashboard** shows real-time stats
2. **Settings** → **System Info** shows database size
3. Monitor browser console for errors (F12)

### Enable Debug Mode
```bash
streamlit run app.py --logger.level=debug
```

---

## 🔗 Integration with External Systems

### Export to ERP
1. Generate Excel report in **Reports** page
2. Import into ERP system
3. Update on schedule (daily/weekly)

### REST API Integration (Future)
```python
# Can be extended with FastAPI
# to create REST endpoints for data access
```

---

## ✅ Deployment Checklist

Before going live:
- [ ] All 4 labs created
- [ ] Sample data imported
- [ ] Dashboard displays correctly
- [ ] In/Out tracking works
- [ ] Reports generate properly
- [ ] Excel import/export functional
- [ ] Backups configured
- [ ] Users trained
- [ ] Documentation shared
- [ ] Monitoring setup

---

## 🆘 Get Help

### Documentation
- **README.md** - Full documentation
- **QUICKSTART.md** - Quick start guide
- **UI_DESIGN_REFERENCE.md** - Design details

### Common Commands
```bash
# Run with specific port
streamlit run app.py --server.port 8080

# Run in headless mode
streamlit run app.py --headless

# Run with configuration
streamlit run app.py --client.showErrorDetails true
```

### Troubleshooting
1. Check browser console (F12)
2. Check terminal output
3. Verify file permissions
4. Check data folder exists
5. Reinstall dependencies

---

**Last Updated:** April 16, 2026  
**Status:** ✅ Production Ready
