"""
Inventory System for Engineering Lab - Main Application
Sistem Manajemen Inventory untuk Lab Teknik Mesin
Streamlit-based application following RBI Calculator architecture
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os
from io import BytesIO
import plotly.graph_objects as go
import plotly.express as px

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.lab_manager import LabManager
from modules.equipment_manager import EquipmentManager
from modules.inventory_manager import InventoryManager
from modules.template_handler import TemplateHandler
from utils.constants import (
    DEFAULT_LABS, EQUIPMENT_TYPES, EQUIPMENT_STATUS,
    MOVEMENT_TYPES, COLOR_PALETTE, THEME_COLORS, THEME_OPTIONS,
    DATE_FORMAT, DISPLAY_DATE_FORMAT, DISPLAY_DATETIME_FORMAT
)
from utils.helpers import inject_custom_css

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Inventory Lab Teknik Mesin",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme in session state
if 'selected_theme' not in st.session_state:
    st.session_state.selected_theme = 'sage'

# Inject custom CSS with selected theme
inject_custom_css(st.session_state.selected_theme)

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div style="text-align: center; margin-bottom: 30px; animation: fadeInUp 0.6s ease-out;">
    <h1 style="margin-bottom: 5px; font-size: 2.8rem;">📦 Inventory System</h1>
    <p style="font-size: 16px; margin: 2px 0; font-weight: 600;">Lab Teknik Mesin - Universitas Malikussaleh</p>
    <p style="font-size: 12px; margin-top: 5px; color: #7F8C8D;">Sistem Manajemen Inventory Equipment dan Asset</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'lab_manager' not in st.session_state:
    st.session_state.lab_manager = LabManager()
if 'equipment_manager' not in st.session_state:
    st.session_state.equipment_manager = EquipmentManager()
if 'inventory_manager' not in st.session_state:
    st.session_state.inventory_manager = InventoryManager()
if 'template_handler' not in st.session_state:
    st.session_state.template_handler = TemplateHandler()

# ============================================================================
# SIDEBAR NAVIGATION & THEME SELECTOR
# ============================================================================

with st.sidebar:
    # Theme Selector
    st.markdown("### 🎨 Pilih Tema")
    
    theme_choice = st.selectbox(
        "Tema Sistem:",
        options=list(THEME_OPTIONS.keys()),
        format_func=lambda x: THEME_OPTIONS[x]['name'],
        index=list(THEME_OPTIONS.keys()).index(st.session_state.selected_theme),
        key="theme_selector"
    )
    
    # Update theme if changed
    if theme_choice != st.session_state.selected_theme:
        st.session_state.selected_theme = theme_choice
        st.rerun()
    
    st.markdown("---")
    
    st.markdown('<div style="text-align: left; font-size: 16px; font-weight: 700; color: #000000; margin-bottom: 15px;">📋 Navigation Menu</div>', unsafe_allow_html=True)
    page = st.radio(
        "Select Page",
        [
            "📊 Dashboard",
            "🏭 Lab Management",
            "🔧 Equipment Management",
            "📤 Inventory Adjustment",
            "📈 Reports & Analytics",
            "⚙️ Settings"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; font-size: 11px; margin-top: 20px; animation: fadeInUp 0.8s ease-out;">
        <p style="font-weight: 700; color: #000000;"><strong>Inventory System v1.0</strong></p>
        <p style="color: #000000;">Lab Teknik Mesin</p>
        <p style="font-size: 10px; margin-top: 10px; color: #7F8C8D;">Dikembangakn FAH Group</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGE: DASHBOARD
# ============================================================================

if page == "📊 Dashboard":
    st.header("📊 Dashboard Inventory")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Get statistics
    labs = st.session_state.lab_manager.get_all_labs()
    equipment_list = st.session_state.equipment_manager.get_all_equipment()
    stats = st.session_state.equipment_manager.get_statistics()
    stock_summary = st.session_state.inventory_manager.get_stock_summary()
    
    with col1:
        st.metric(
            label="🏭 Total Lab",
            value=len(labs),
            delta="4 labs"
        )
    
    with col2:
        st.metric(
            label="🔧 Equipment",
            value=len(equipment_list),
            delta=f"Total {stats.get('total_equipment', 0)}"
        )
    
    with col3:
        st.metric(
            label="📦 Total Items",
            value=f"{int(stock_summary.get('total_items', 0))}",
            delta="Current Stock"
        )
    
    with col4:
        total_value = stock_summary.get('total_value', 0)
        st.metric(
            label="💰 Total Value",
            value=f"Rp {total_value:,.0f}",
            delta="Estimated"
        )
    
    st.markdown("---")
    
    # Lab Distribution
    st.subheader("📊 Equipment per Lab")
    
    lab_data = {}
    for lab_id in st.session_state.lab_manager.list_lab_ids():
        lab = st.session_state.lab_manager.get_lab(lab_id)
        eq_count = len(st.session_state.equipment_manager.get_equipment_by_lab(lab_id))
        lab_data[lab.get('name', lab_id)] = eq_count
    
    if lab_data:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure(data=[
                go.Bar(x=list(lab_data.keys()), y=list(lab_data.values()), 
                       marker=dict(color='#66BB6A'))
            ])
            fig.update_layout(
                template='plotly_white',
                height=400,
                paper_bgcolor='rgba(255,255,255,0)',
                plot_bgcolor='rgba(255,255,255,0)',
                font=dict(color='#2C3E50'),
                title=None,
                xaxis_title="Lab",
                yaxis_title="Jumlah Equipment"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Statistik per Lab:**")
            for lab_name, count in lab_data.items():
                st.write(f"- {lab_name}: {count} equipment")
    else:
        st.info("ℹ️ Belum ada lab yang terdaftar. Silakan tambahkan lab terlebih dahulu di halaman Lab Management.")
    
    st.markdown("---")
    
    # Equipment Status Distribution
    st.subheader("📈 Status Distribution")
    
    status_data = stats.get('by_status', {})
    if status_data:
        col1, col2 = st.columns(2)
        
        with col1:
            status_mapping = {
                'active': '🟢 Aktif',
                'maintenance': '🟡 Maintenance',
                'depleted': '🔴 Habis Pakai',
                'archived': '⚪ Diarsipkan'
            }
            
            status_labels = [status_mapping.get(k, k) for k in status_data.keys()]
            status_values = list(status_data.values())
            
            fig = go.Figure(data=[go.Pie(labels=status_labels, values=status_values, 
                                         marker=dict(colors=['#66BB6A', '#FFA726', '#EF5350', '#9E9E9E']))])
            fig.update_layout(
                template='plotly_white',
                height=400,
                paper_bgcolor='rgba(255,255,255,0)',
                plot_bgcolor='rgba(255,255,255,0)',
                font=dict(color='#2C3E50')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Status Breakdown:**")
            for status, count in status_data.items():
                status_name = {
                    'active': 'Aktif',
                    'maintenance': 'Maintenance',
                    'depleted': 'Habis Pakai',
                    'archived': 'Diarsipkan'
                }.get(status, status)
                st.write(f"- {status_name}: {count} equipment")

# ============================================================================
# PAGE: LAB MANAGEMENT
# ============================================================================

elif page == "🏭 Lab Management":
    st.header("🏭 Lab Management")
    
    tab1, tab2, tab3 = st.tabs(["📋 View Labs", "➕ Add New Lab", "✏️ Edit Lab"])
    
    # Tab 1: View Labs
    with tab1:
        st.subheader("Daftar Lab")
        
        labs = st.session_state.lab_manager.get_all_labs()
        
        if labs:
            for lab in labs:
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    with st.expander(f"🏭 {lab.get('name')} ({lab.get('lab_id')})"):
                        st.write(f"**Deskripsi:** {lab.get('description', '-')}")
                        st.write(f"**Tanggal Dibuat:** {lab.get('created_date', '-')}")
                        
                        # Get equipment for this lab
                        eq_list = st.session_state.equipment_manager.get_equipment_by_lab(lab.get('lab_id'))
                        st.write(f"**Equipment:** {len(eq_list)} items")
                        
                        # Show equipment summary
                        if eq_list:
                            eq_names = ", ".join([eq.get('nama', 'N/A') for eq in eq_list[:3]])
                            if len(eq_list) > 3:
                                eq_names += f", +{len(eq_list) - 3} more"
                            st.caption(f"Equipment: {eq_names}")
                
                with col2:
                    if st.button("✏️ Edit", key=f"edit_{lab.get('lab_id')}"):
                        st.session_state.edit_lab = lab.get('lab_id')
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_{lab.get('lab_id')}"):
                        try:
                            st.session_state.lab_manager.delete_lab(lab.get('lab_id'))
                            st.success(f"Lab {lab.get('name')} berhasil dihapus")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        else:
            st.info("ℹ️ Belum ada lab yang terdaftar. Silakan tambahkan lab baru.")
    
    # Tab 2: Add New Lab
    with tab2:
        st.subheader("Tambah Lab Baru")
        
        with st.form("add_lab_form", clear_on_submit=True):
            lab_id = st.text_input(
                "Lab ID (format: lab_name)",
                placeholder="manufaktur, material, etc.",
                help="Format: huruf kecil, gunakan underscore untuk spasi. Contoh: lab_manufaktur"
            )
            
            lab_name = st.text_input(
                "Nama Lab*",
                placeholder="Lab Manufaktur",
                help="Nama lengkap laboratorium yang akan ditampilkan di sistem"
            )
            
            description = st.text_area(
                "Deskripsi Lab",
                placeholder="Deskripsi singkat tentang lab ini...",
                height=100,
                help="Penjelasan singkat tentang fungsi dan kegiatan lab"
            )
            
            submitted = st.form_submit_button("➕ Tambah Lab", use_container_width=True)
            
            if submitted:
                if not lab_name:
                    st.error("❌ Nama Lab harus diisi!")
                elif not lab_id:
                    st.error("❌ Lab ID harus diisi!")
                else:
                    try:
                        lab_data = {
                            'name': lab_name,
                            'description': description,
                            'color': COLOR_PALETTE['primary_light']
                        }
                        
                        if st.session_state.lab_manager.add_lab(lab_id, lab_data):
                            st.success(f"✅ Lab '{lab_name}' berhasil ditambahkan!")
                        else:
                            st.error("❌ Gagal menambahkan lab. Lab mungkin sudah ada.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # Tab 3: Edit Lab
    with tab3:
        st.subheader("Edit Lab")
        
        labs = st.session_state.lab_manager.get_all_labs()
        if labs:
            selected_lab = st.selectbox(
                "Pilih Lab untuk diedit:",
                options=[lab.get('lab_id') for lab in labs],
                format_func=lambda x: next((lab.get('name') for lab in labs if lab.get('lab_id') == x), x)
            )
            
            lab = st.session_state.lab_manager.get_lab(selected_lab)
            
            if lab:
                lab_name = st.text_input("Nama Lab*", value=lab.get('name', ''))
                description = st.text_area("Deskripsi Lab", value=lab.get('description', ''), height=100)
                
                if st.button("💾 Simpan Perubahan", use_container_width=True, key=f"edit_lab_btn_{selected_lab}"):
                    try:
                        st.session_state.lab_manager.update_lab(
                            selected_lab,
                            {'name': lab_name, 'description': description}
                        )
                        st.success("✅ Lab berhasil diupdate!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        else:
            st.info("ℹ️ Belum ada lab yang terdaftar.")
# ============================================================================
# PAGE: EQUIPMENT MANAGEMENT
# ============================================================================

elif page == "🔧 Equipment Management":
    st.header("🔧 Equipment Management")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 View Equipment", 
        "➕ Add Equipment", 
        "📥 Import Equipment", 
        "📊 Search",
        "🗑️ Delete Equipment",
        "🔄 Edit Status"
    ])
    
    # Tab 1: View Equipment
    with tab1:
        st.subheader("Daftar Equipment")
        
        # Filter by lab
        labs = st.session_state.lab_manager.get_all_labs()
        lab_options = {lab.get('lab_id'): lab.get('name') for lab in labs}
        
        selected_lab = st.selectbox(
            "Filter by Lab:",
            options=['all'] + list(lab_options.keys()),
            format_func=lambda x: 'Semua Lab' if x == 'all' else lab_options.get(x, x)
        )
        
        # Get equipment
        if selected_lab == 'all':
            equipment_list = st.session_state.equipment_manager.get_all_equipment()
        else:
            equipment_list = st.session_state.equipment_manager.get_equipment_by_lab(selected_lab)
        
        if equipment_list:
            # Create dataframe for display
            df_data = []
            for eq in equipment_list:
                df_data.append({
                    'ID': eq.get('equipment_id', '')[:6],
                    'Nama': eq.get('nama', '-'),
                    'Qty': f"{int(eq.get('jumlah', 0))}",
                    'Merk': eq.get('merk', '-'),
                    'Type': eq.get('type', '-'),
                    'Harga Satuan': f"Rp {float(eq.get('harga_satuan', 0)):,.0f}",
                    'Total': f"Rp {float(eq.get('harga_keseluruhan', 0)):,.0f}",
                    'Status': eq.get('status', 'active')
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.caption(f"Total: {len(equipment_list)} equipment")
            
            # Export option
            if st.button("📥 Export to Excel", use_container_width=True):
                excel_bytes = st.session_state.template_handler.export_equipment(equipment_list)
                if excel_bytes:
                    st.download_button(
                        label="⬇️ Download Excel",
                        data=excel_bytes,
                        file_name=f"equipment_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        else:
            st.info("ℹ️ Belum ada equipment di lab ini.")
    
    # Tab 2: Add Equipment
    with tab2:
        st.subheader("Tambah Equipment Baru")
        
        labs = st.session_state.lab_manager.get_all_labs()
        if not labs:
            st.warning("⚠️ Belum ada lab yang terdaftar. Silakan tambahkan lab terlebih dahulu.")
        else:
            with st.form("add_equipment_form", clear_on_submit=True):
                selected_lab = st.selectbox(
                    "Pilih Lab*",
                    options=[lab.get('lab_id') for lab in labs],
                    format_func=lambda x: next((lab.get('name') for lab in labs if lab.get('lab_id') == x), x)
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    nama = st.text_input(
                        "Nama Equipment*", 
                        placeholder="Mesin Bubut CNC",
                        help="Masukkan nama/tipe equipment yang akan ditambahkan"
                    )
                    merk = st.text_input(
                        "Merk", 
                        placeholder="TOKOTA",
                        help="Merek/brand dari equipment (opsional)"
                    )
                    bom = st.text_input(
                        "BoM", 
                        placeholder="M01",
                        help="Bill of Materials atau kode internal (opsional)"
                    )
                
                with col2:
                    eq_type = st.selectbox(
                        "Type", 
                        options=EQUIPMENT_TYPES, 
                        index=0,
                        help="Pilih kategori/tipe equipment"
                    )
                    jumlah = st.number_input(
                        "Jumlah/Quantity*", 
                        min_value=0.0, 
                        step=1.0,
                        help="Jumlah unit equipment yang akan ditambahkan"
                    )
                    kategori = st.selectbox(
                        "Kategori", 
                        options=["Mesin", "Alat Ukur", "Peralatan Bengkel", "Lainnya"],
                        help="Kategori equipment untuk klasifikasi"
                    )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    harga_satuan = st.number_input(
                        "Harga Satuan*", 
                        min_value=0.0, 
                        step=1000.0,
                        help="Harga satuan per unit dalam Rupiah"
                    )
                
                with col2:
                    harga_keseluruhan = jumlah * harga_satuan
                    st.metric(label="Harga Keseluruhan", value=f"Rp {harga_keseluruhan:,.0f}")
                
                keterangan = st.text_area(
                    "Keterangan/Notes", 
                    height=80,
                    help="Informasi tambahan tentang equipment (kondisi, spesifikasi, dll)"
                )
                
                submitted = st.form_submit_button("➕ Tambah Equipment", use_container_width=True)
                
                if submitted:
                    if not nama or jumlah < 0 or harga_satuan < 0:
                        st.error("❌ Silakan isi semua field yang diperlukan dengan benar!")
                    else:
                        try:
                            equipment_data = {
                                'nama': nama,
                                'jumlah': jumlah,
                                'merk': merk,
                                'type': eq_type,
                                'bom': bom,
                                'harga_satuan': harga_satuan,
                                'harga_keseluruhan': harga_keseluruhan,
                                'kategori': kategori,
                                'keterangan': keterangan,
                                'status': 'active'
                            }
                            
                            eq_id = st.session_state.equipment_manager.add_equipment(selected_lab, equipment_data)
                            
                            if eq_id:
                                st.success(f"✅ Equipment '{nama}' berhasil ditambahkan!")
                            else:
                                st.error("❌ Gagal menambahkan equipment!")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
    
    # Tab 3: Import Equipment
    with tab3:
        st.subheader("Import Equipment dari Excel")
        
        labs = st.session_state.lab_manager.get_all_labs()
        if not labs:
            st.warning("⚠️ Belum ada lab yang terdaftar.")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                selected_lab = st.selectbox(
                    "Target Lab*",
                    options=[lab.get('lab_id') for lab in labs],
                    format_func=lambda x: next((lab.get('name') for lab in labs if lab.get('lab_id') == x), x)
                )
            
            with col2:
                st.write("")
                if st.button("📥 Download Template", use_container_width=True):
                    template_bytes = st.session_state.template_handler.get_template()
                    if template_bytes:
                        st.download_button(
                            label="⬇️ Download",
                            data=template_bytes,
                            file_name="equipment_template.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
            
            st.markdown("---")
            
            uploaded_file = st.file_uploader("Pilih file Excel untuk diimport", type=['xlsx', 'xls'])
            
            if uploaded_file:
                if st.button("📥 Import Data", use_container_width=True):
                    success, message, imported = st.session_state.template_handler.import_equipment(
                        uploaded_file, selected_lab, st.session_state.equipment_manager
                    )
                    
                    if success:
                        st.success(f"✅ {message}")
                        
                        if imported:
                            st.subheader("Data yang Diimport:")
                            import_df = pd.DataFrame(imported)
                            st.dataframe(import_df, use_container_width=True, hide_index=True)
                            st.rerun()
                    else:
                        st.error(f"❌ {message}")
    
    # Tab 4: Search
    with tab4:
        st.subheader("Cari Equipment")
        
        search_query = st.text_input("Cari berdasarkan nama atau merk:", placeholder="Cth: Mesin, TOKOTA")
        
        if search_query:
            results = st.session_state.equipment_manager.search_equipment(search_query)
            
            if results:
                st.success(f"✅ Ditemukan {len(results)} equipment")
                
                for eq in results:
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**{eq.get('nama')}**")
                        st.caption(f"Merk: {eq.get('merk', '-')} | Type: {eq.get('type', '-')}")
                    
                    with col2:
                        st.metric("Qty", int(eq.get('jumlah', 0)))
                    
                    with col3:
                        st.metric("Total", f"Rp {float(eq.get('harga_keseluruhan', 0)):,.0f}")
            else:
                st.info("ℹ️ Tidak ada equipment yang sesuai dengan pencarian.")
    
    # Tab 5: Delete Equipment
    with tab5:
        st.subheader("🗑️ Hapus Equipment")
        
        equipment_list = st.session_state.equipment_manager.get_all_equipment()
        if equipment_list:
            selected_equipment = st.selectbox(
                "Pilih Equipment untuk dihapus*",
                options=[eq.get('equipment_id') for eq in equipment_list],
                format_func=lambda x: next((f"{eq.get('nama')} (Qty: {int(eq.get('jumlah', 0))})" 
                                          for eq in equipment_list if eq.get('equipment_id') == x), x),
                key="delete_equipment"
            )
            
            eq = st.session_state.equipment_manager.get_equipment(selected_equipment)
            if eq:
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Nama:** {eq.get('nama')}")
                    st.write(f"**Qty Saat Ini:** {int(eq.get('jumlah', 0))}")
                with col2:
                    st.write(f"**Merk:** {eq.get('merk', '-')}")
                    st.write(f"**Total Harga:** Rp {float(eq.get('harga_keseluruhan', 0)):,.0f}")
                
                st.warning("⚠️ Aksi ini tidak dapat dibatalkan! Equipment akan dihapus selamanya.")
                
                if st.button("🗑️ Hapus Equipment Ini", use_container_width=True, type="secondary"):
                    try:
                        st.session_state.equipment_manager.delete_equipment(selected_equipment)
                        st.success(f"✅ Equipment '{eq.get('nama')}' berhasil dihapus!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        else:
            st.info("ℹ️ Belum ada equipment yang terdaftar.")
    
    # Tab 6: Edit Status Equipment
    with tab6:
        st.subheader("🔄 Ubah Status Equipment")
        
        equipment_list = st.session_state.equipment_manager.get_all_equipment()
        if equipment_list:
            selected_equipment = st.selectbox(
                "Pilih Equipment*",
                options=[eq.get('equipment_id') for eq in equipment_list],
                format_func=lambda x: next((f"{eq.get('nama')} - Status: {eq.get('status', 'active')}" 
                                          for eq in equipment_list if eq.get('equipment_id') == x), x),
                key="status_equipment"
            )
            
            eq = st.session_state.equipment_manager.get_equipment(selected_equipment)
            if eq:
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Nama:** {eq.get('nama')}")
                    st.write(f"**Status Saat Ini:** {eq.get('status', 'active').upper()}")
                with col2:
                    st.write(f"**Qty:** {int(eq.get('jumlah', 0))}")
                    st.write(f"**Merk:** {eq.get('merk', '-')}")
                
                # Normalize status value
                current_status = eq.get('status', 'active').lower().strip()
                status_mapping = {
                    'aktif': 'active',
                    'maintenance': 'maintenance',
                    'habis pakai': 'depleted',
                    'depleted': 'depleted',
                    'archived': 'archived',
                    'diarsipkan': 'archived'
                }
                normalized_status = status_mapping.get(current_status, 'active')
                
                # Ensure normalized status is in the allowed list
                allowed_statuses = ['active', 'maintenance', 'depleted', 'archived']
                if normalized_status not in allowed_statuses:
                    normalized_status = 'active'
                
                new_status = st.selectbox(
                    "Status Baru*",
                    options=['active', 'maintenance', 'depleted', 'archived'],
                    format_func=lambda x: {'active': '🟢 Aktif', 'maintenance': '🟡 Maintenance', 
                                          'depleted': '🔴 Habis Pakai', 'archived': '⚪ Diarsipkan'}.get(x, x),
                    index=allowed_statuses.index(normalized_status),
                    help="Pilih status baru untuk equipment ini"
                )
                
                keterangan = st.text_area(
                    "Catatan Perubahan Status",
                    placeholder="Contoh: Sedang dalam perbaikan di workshop",
                    height=80,
                    help="Berikan penjelasan alasan perubahan status"
                )
                
                if st.button("💾 Simpan Perubahan Status", use_container_width=True):
                    try:
                        eq.update({'status': new_status})
                        st.session_state.equipment_manager.update_equipment(selected_equipment, eq)
                        st.success(f"✅ Status equipment berhasil diubah menjadi: {new_status.upper()}")
                        if keterangan:
                            st.info(f"📝 Catatan: {keterangan}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        else:
            st.info("ℹ️ Belum ada equipment yang terdaftar.")

# ============================================================================
# PAGE: INVENTORY ADJUSTMENT
# ============================================================================

elif page == "📤 Inventory Adjustment":
    st.header("📤 Inventory Adjustment")
    
    tab1, tab2, tab3 = st.tabs(["➕ Barang Masuk", "➖ Barang Keluar", "📝 History"])
    
    # Tab 1: Barang Masuk
    with tab1:
        st.subheader("Barang Masuk (In)")
        
        labs = st.session_state.lab_manager.get_all_labs()
        if not labs:
            st.warning("⚠️ Belum ada lab yang terdaftar.")
        else:
            with st.form("in_movement_form", clear_on_submit=True):
                selected_lab = st.selectbox(
                    "Pilih Lab*",
                    options=[lab.get('lab_id') for lab in labs],
                    format_func=lambda x: next((lab.get('name') for lab in labs if lab.get('lab_id') == x), x),
                    key="in_lab"
                )
                
                # Get equipment for selected lab
                equipment_list = st.session_state.equipment_manager.get_equipment_by_lab(selected_lab)
                
                if equipment_list:
                    selected_equipment = st.selectbox(
                        "Pilih Equipment*",
                        options=[eq.get('equipment_id') for eq in equipment_list],
                        format_func=lambda x: next((eq.get('nama') for eq in equipment_list if eq.get('equipment_id') == x), x),
                        help="Equipment mana yang akan ditambahkan/masuk"
                    )
                    
                    quantity = st.number_input(
                        "Jumlah Masuk*", 
                        min_value=0.0, 
                        step=1.0, 
                        value=0.0,
                        help="Berapa jumlah unit yang masuk/ditambahkan"
                    )
                    notes = st.text_area(
                        "Catatan", 
                        height=80,
                        help="Catatan tambahan tentang barang yang masuk (opsional)"
                    )
                    
                    submitted = st.form_submit_button("✅ Catat Barang Masuk", use_container_width=True)
                    
                    if submitted:
                        if quantity > 0:
                            try:
                                st.session_state.equipment_manager.adjust_quantity(
                                    selected_equipment, quantity, notes, "in"
                                )
                                st.success(f"✅ Berhasil mencatat {quantity} barang masuk!")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                        else:
                            st.error("❌ Jumlah harus lebih dari 0!")
                else:
                    st.info("ℹ️ Belum ada equipment di lab ini.")
    
    # Tab 2: Barang Keluar
    with tab2:
        st.subheader("Barang Keluar (Out)")
        
        labs = st.session_state.lab_manager.get_all_labs()
        if not labs:
            st.warning("⚠️ Belum ada lab yang terdaftar.")
        else:
            with st.form("out_movement_form", clear_on_submit=True):
                selected_lab = st.selectbox(
                    "Pilih Lab*",
                    options=[lab.get('lab_id') for lab in labs],
                    format_func=lambda x: next((lab.get('name') for lab in labs if lab.get('lab_id') == x), x),
                    key="out_lab"
                )
                
                equipment_list = st.session_state.equipment_manager.get_equipment_by_lab(selected_lab)
                
                if equipment_list:
                    selected_equipment = st.selectbox(
                        "Pilih Equipment*",
                        options=[eq.get('equipment_id') for eq in equipment_list],
                        format_func=lambda x: next((eq.get('nama') for eq in equipment_list if eq.get('equipment_id') == x), x),
                        key="out_eq"
                    )
                    
                    # Get current quantity
                    eq = st.session_state.equipment_manager.get_equipment(selected_equipment)
                    current_qty = float(eq.get('jumlah', 0)) if eq else 0
                    
                    st.info(f"💾 Stok Saat Ini: {int(current_qty)} unit")
                    
                    quantity = st.number_input(
                        "Jumlah Keluar*",
                        min_value=0.0,
                        max_value=current_qty,
                        step=1.0,
                        value=0.0,
                        help="Berapa jumlah unit yang akan keluar (tidak boleh melebihi stok saat ini)"
                    )
                    
                    reason = st.selectbox(
                        "Alasan",
                        ["Penggunaan/Praktikum", "Hilang", "Rusak", "Perbaikan", "Lainnya"],
                        help="Pilih alasan barang keluar dari lab"
                    )
                    
                    notes = st.text_area(
                        "Catatan Detail", 
                        height=80,
                        help="Keterangan detail tentang penggunaan atau keadaan barang yang keluar"
                    )
                    
                    submitted = st.form_submit_button("✅ Catat Barang Keluar", use_container_width=True)
                    
                    if submitted:
                        if quantity > 0:
                            try:
                                full_notes = f"{reason}: {notes}" if notes else reason
                                st.session_state.equipment_manager.adjust_quantity(
                                    selected_equipment, -quantity, full_notes, "out"
                                )
                                st.success(f"✅ Berhasil mencatat {quantity} barang keluar!")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                        else:
                            st.error("❌ Jumlah harus lebih dari 0!")
                else:
                    st.info("ℹ️ Belum ada equipment di lab ini.")
    
    # Tab 3: History
    with tab3:
        st.subheader("History Pergerakan Inventory")
        
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Dari Tanggal:", key="movement_start")
        with col2:
            end_date = st.date_input("Sampai Tanggal:", key="movement_end")
        
        movements = st.session_state.inventory_manager.get_movements(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        if movements:
            # Create dataframe
            df_data = []
            for m in movements:
                eq = st.session_state.equipment_manager.get_equipment(m.get('equipment_id'))
                df_data.append({
                    'Tanggal': m.get('date', '')[:10],
                    'Equipment': eq.get('nama', 'N/A') if eq else 'N/A',
                    'Tipe': m.get('movement_type', '-').upper(),
                    'Qty': int(m.get('quantity', 0)),
                    'Catatan': m.get('notes', '')[:50]
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ Tidak ada pergerakan inventory dalam periode ini.")

# ============================================================================
# PAGE: REPORTS & ANALYTICS
# ============================================================================

elif page == "📈 Reports & Analytics":
    st.header("📈 Reports & Analytics")
    
    tab1, tab2, tab3 = st.tabs(["📊 Stock Summary", "🗑️ Consumption Report", "📥 Export Report"])
    
    # Tab 1: Stock Summary
    with tab1:
        st.subheader("Ringkasan Stok Saat Ini")
        
        labs = st.session_state.lab_manager.get_all_labs()
        selected_lab = st.selectbox(
            "Pilih Lab (atau Semua):",
            options=['all'] + [lab.get('lab_id') for lab in labs],
            format_func=lambda x: 'Semua Lab' if x == 'all' else next((lab.get('name') for lab in labs if lab.get('lab_id') == x), x),
            help="Pilih lab untuk melihat ringkasan stok lab tersebut atau semua lab"
        )
        
        stock_summary = st.session_state.inventory_manager.get_stock_summary(
            lab_id=None if selected_lab == 'all' else selected_lab
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Items", int(stock_summary.get('total_items', 0)))
        
        with col2:
            st.metric("Total Value", f"Rp {stock_summary.get('total_value', 0):,.0f}")
        
        with col3:
            total_eq = len(stock_summary.get('details', []))
            st.metric("Total Equipment", total_eq)
        
        st.markdown("---")
        
        # Status breakdown
        by_status = stock_summary.get('by_status', {})
        if by_status:
            col1, col2 = st.columns(2)
            
            with col1:
                status_display = {}
                for status, data in by_status.items():
                    status_name = {
                        'active': '🟢 Aktif',
                        'maintenance': '🟡 Maintenance',
                        'depleted': '🔴 Habis Pakai',
                        'archived': '⚪ Diarsipkan'
                    }.get(status, status)
                    status_display[status_name] = data.get('count', 0)
                
                fig = go.Figure(data=[
                    go.Bar(x=list(status_display.keys()), y=list(status_display.values()),
                           marker=dict(color=['#66BB6A', '#FFA726', '#EF5350', '#9E9E9E']))
                ])
                fig.update_layout(
                    template='plotly_white',
                    height=400,
                    paper_bgcolor='rgba(255,255,255,0)',
                    plot_bgcolor='rgba(255,255,255,0)',
                    font=dict(color='#2C3E50'),
                    title=None,
                    xaxis_title="Status",
                    yaxis_title="Jumlah Equipment"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("**Detail per Status:**")
                for status, data in by_status.items():
                    status_name = {
                        'active': 'Aktif',
                        'maintenance': 'Maintenance',
                        'depleted': 'Habis Pakai',
                        'archived': 'Diarsipkan'
                    }.get(status, status)
                    
                    count = data.get('count', 0)
                    value = data.get('value', 0)
                    st.write(f"- **{status_name}**: {count} equipment (Rp {value:,.0f})")
    
    # Tab 2: Consumption Report
    with tab2:
        st.subheader("Laporan Konsumsi/Habis Pakai")
        
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Dari Tanggal:", key="consumption_start")
        
        with col2:
            end_date = st.date_input("Sampai Tanggal:", key="consumption_end")
        
        labs = st.session_state.lab_manager.get_all_labs()
        selected_lab = st.selectbox(
            "Pilih Lab (atau Semua):",
            options=['all'] + [lab.get('lab_id') for lab in labs],
            format_func=lambda x: 'Semua Lab' if x == 'all' else next((lab.get('name') for lab in labs if lab.get('lab_id') == x), x),
            key="consumption_lab"
        )
        
        if st.button("🔍 Generate Laporan", use_container_width=True):
            depletion_report = st.session_state.inventory_manager.get_depletion_report(
                lab_id=None if selected_lab == 'all' else selected_lab,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat()
            )
            
            if depletion_report:
                st.success(f"✅ Ditemukan {len(depletion_report)} item yang dikonsumsi")
                
                # Create dataframe
                df_data = []
                for eq_id, data in depletion_report.items():
                    eq = st.session_state.equipment_manager.get_equipment(eq_id)
                    df_data.append({
                        'Equipment': eq.get('nama', 'N/A') if eq else 'N/A',
                        'Lab': data.get('lab_id', '-'),
                        'Jumlah Dikonsumsi': int(abs(data.get('total_consumed', 0))),
                        'Terakhir': data.get('last_consumption', '')[:10],
                        'Movements': len(data.get('movements', []))
                    })
                
                if df_data:
                    df = pd.DataFrame(df_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Export button
                    excel_bytes = st.session_state.template_handler.export_consumption_report(
                        depletion_report,
                        lab_name=next((lab.get('name') for lab in labs if lab.get('lab_id') == selected_lab), 'All Labs') if selected_lab != 'all' else 'All Labs'
                    )
                    
                    if excel_bytes:
                        st.download_button(
                            label="📥 Download Laporan Excel",
                            data=excel_bytes,
                            file_name=f"consumption_report_{start_date}_{end_date}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
            else:
                st.info("ℹ️ Tidak ada konsumsi dalam periode ini.")
    
    # Tab 3: Export Report
    with tab3:
        st.subheader("Export Data Lengkap")
        
        col1, col2 = st.columns(2)
        
        with col1:
            export_type = st.radio(
                "Tipe Export:",
                ["Equipment Data", "Consumption Data", "All Data"]
            )
        
        with col2:
            st.write("")
        
        if st.button("📥 Prepare Export", use_container_width=True):
            if export_type == "Equipment Data":
                equipment_list = st.session_state.equipment_manager.get_all_equipment()
                excel_bytes = st.session_state.template_handler.export_equipment(equipment_list)
                
                if excel_bytes:
                    st.download_button(
                        label="⬇️ Download Equipment Data",
                        data=excel_bytes,
                        file_name=f"equipment_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    st.success("✅ File siap diunduh!")
            
            elif export_type == "Consumption Data":
                depletion_report = st.session_state.inventory_manager.get_depletion_report()
                excel_bytes = st.session_state.template_handler.export_consumption_report(
                    depletion_report,
                    lab_name="All Labs"
                )
                
                if excel_bytes:
                    st.download_button(
                        label="⬇️ Download Consumption Data",
                        data=excel_bytes,
                        file_name=f"consumption_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    st.success("✅ File siap diunduh!")

# ============================================================================
# PAGE: SETTINGS
# ============================================================================

elif page == "⚙️ Settings":
    st.header("⚙️ Settings & Configuration")
    
    tab1, tab2, tab3 = st.tabs(["System Info", "Data Management", "About"])
    
    # Tab 1: System Info
    with tab1:
        st.subheader("Informasi Sistem")
        
        stats = st.session_state.equipment_manager.get_statistics()
        lab_stats = st.session_state.lab_manager.get_stats()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Statistik Inventory:**")
            st.write(f"- Total Lab: {len(st.session_state.lab_manager.get_all_labs())}")
            st.write(f"- Total Equipment: {stats.get('total_equipment', 0)}")
            st.write(f"- Total Items: {int(stats.get('total_items', 0))}")
            st.write(f"- Total Value: Rp {stats.get('total_value', 0):,.0f}")
        
        with col2:
            st.write("**Equipment per Type:**")
            by_type = stats.get('by_type', {})
            for eq_type, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True)[:10]:
                st.write(f"- {eq_type}: {count}")
    
    # Tab 2: Data Management
    with tab2:
        st.subheader("Manajemen Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Export Data:**")
            if st.button("📥 Export All Data", use_container_width=True):
                st.info("Fitur export akan mengekspor semua data ke file Excel")
        
        with col2:
            st.write("**Database Reset:**")
            if st.button("🗑️ Reset Database (HATI-HATI!)", use_container_width=True):
                st.warning("⚠️ Fitur ini akan menghapus SEMUA data. Silakan backup terlebih dahulu!")
    
    # Tab 3: About
    with tab3:
        st.subheader("Tentang Aplikasi")
        
        st.markdown("""
        ### Inventory System for Engineering Lab
        **Sistem Manajemen Inventory untuk Lab Teknik Mesin**
        
        #### Versi
        - **Version**: 1.0
        - **Release Date**: 2026
        - **Powered by**: Streamlit + Python
        
        #### Fitur Utama
        - 📦 Manajemen Equipment & Inventory
        - 🏭 Manajemen Lab
        - 📤 Tracking In/Out Inventory
        - 📊 Report & Analytics
        - 📥 Import/Export Data
        
        #### Teknologi
        - **Framework**: Streamlit
        - **Language**: Python 3.8+
        - **Data Storage**: JSON
        - **Export**: Excel (XLSX)
        
        #### Pengembang
        - **Organization**: Lab Teknik Mesin
        - **University**: [Universitas Malikusaleh]
        
        ---
        
        © 2026 Lab Teknik Mesin | All Rights Reserved
        """)
