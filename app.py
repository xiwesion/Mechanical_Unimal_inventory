"""
Inventory System for Engineering Lab - Main Application
Sistem Manajemen Inventory untuk Lab Teknik Mesin
Streamlit-based application following RBI Calculator architecture
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
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
    DEFAULT_LABS, EQUIPMENT_TYPES, EQUIPMENT_CATEGORIES, EQUIPMENT_STATUS,
    MOVEMENT_TYPES, COLOR_PALETTE, THEME_COLORS, THEME_OPTIONS,
    DATE_FORMAT, DISPLAY_DATE_FORMAT, DISPLAY_DATETIME_FORMAT
)
from utils.helpers import inject_custom_css, init_stats_cache, calculate_realtime_stats, get_cached_stats, mark_stats_stale, refresh_stats_immediately

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

# Initialize realtime stats cache
init_stats_cache()
realtime_stats = calculate_realtime_stats()

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
    
    # Auto-refresh stats every render
    cached_stats = get_cached_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Get labs for count
    labs = st.session_state.lab_manager.get_all_labs()
    
    with col1:
        st.metric(
            label="🏭 Total Lab",
            value=len(labs),
            delta="Active Labs"
        )
    
    with col2:
        st.metric(
            label="🔧 Total Equipment",
            value=cached_stats['total_equipment'],
            delta="Registered"
        )
    
    with col3:
        st.metric(
            label="📦 Total Items",
            value=f"{cached_stats['total_items']}",
            delta="Units in Stock"
        )
    
    with col4:
        st.metric(
            label="💰 Total Value",
            value=f"Rp {cached_stats['total_value']:,.0f}",
            delta="Estimated Value"
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
    
    stats = st.session_state.equipment_manager.get_statistics()
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
        "✏️ Edit Equipment"
    ])
    
    # Tab 1: View Equipment
    with tab1:
        st.subheader("📋 Daftar Semua Equipment")
        
        # Filter by lab
        labs = st.session_state.lab_manager.get_all_labs()
        lab_options = {lab.get('lab_id'): lab.get('name') for lab in labs}
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_lab = st.selectbox(
                "Filter by Lab:",
                options=['all'] + list(lab_options.keys()),
                format_func=lambda x: 'Semua Lab' if x == 'all' else lab_options.get(x, x),
                key="view_lab_filter"
            )
        
        with col2:
            selected_type = st.selectbox(
                "Filter by Type:",
                options=['Semua'] + EQUIPMENT_TYPES,
                key="view_type_filter"
            )
        
        with col3:
            selected_status = st.selectbox(
                "Filter by Status:",
                options=['Semua', 'active', 'maintenance', 'depleted', 'archived'],
                key="view_status_filter"
            )
        
        # Get equipment with filters
        if selected_lab == 'all':
            equipment_list = st.session_state.equipment_manager.get_all_equipment()
        else:
            equipment_list = st.session_state.equipment_manager.get_equipment_by_lab(selected_lab)
        
        # Apply type filter
        if selected_type != 'Semua':
            equipment_list = [eq for eq in equipment_list if eq.get('type') == selected_type]
        
        # Apply status filter
        if selected_status != 'Semua':
            equipment_list = [eq for eq in equipment_list if eq.get('status') == selected_status]
        
        if equipment_list:
            # Create comprehensive dataframe for display
            df_data = []
            for eq in equipment_list:
                df_data.append({
                    'ID': eq.get('equipment_id', ''),
                    'Nama': eq.get('nama', '-'),
                    'Lab': eq.get('lab_id', '-'),
                    'Type': eq.get('type', '-'),
                    'Kategori': eq.get('kategori', '-'),
                    'Qty': int(eq.get('jumlah', 0)),
                    'Merk': eq.get('merk', '-'),
                    'BoM': eq.get('bom', '-'),
                    'Harga Satuan': f"Rp {float(eq.get('harga_satuan', 0)):,.0f}",
                    'Total Harga': f"Rp {float(eq.get('harga_keseluruhan', 0)):,.0f}",
                    'Status': eq.get('status', 'active'),
                    'Keterangan': eq.get('keterangan', '-')[:40],
                    'Dibuat': eq.get('created_date', '')[:10]
                })
            
            df = pd.DataFrame(df_data)
            
            # Display with height and scrolling
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=500
            )
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"📊 Total: {len(equipment_list)} equipment")
            with col2:
                total_qty = sum([int(eq.get('jumlah', 0)) for eq in equipment_list])
                st.caption(f"📦 Total Qty: {total_qty} unit")
            with col3:
                total_value = sum([float(eq.get('harga_keseluruhan', 0)) for eq in equipment_list])
                st.caption(f"💰 Total Value: Rp {total_value:,.0f}")
            
            st.divider()
            
            # Export option
            if st.button("📥 Export ke Excel", use_container_width=True):
                excel_bytes = st.session_state.template_handler.export_equipment(equipment_list)
                if excel_bytes:
                    st.download_button(
                        label="⬇️ Download Excel",
                        data=excel_bytes,
                        file_name=f"equipment_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="export_view"
                    )
        else:
            st.info("ℹ️ Tidak ada equipment sesuai filter yang dipilih.")
    
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
                        options=EQUIPMENT_CATEGORIES,
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
                                # Refresh realtime stats after adding equipment
                                from utils.helpers import refresh_stats_immediately
                                refresh_stats_immediately()
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
                    success, message, imported, warnings = st.session_state.template_handler.import_equipment(
                        uploaded_file, selected_lab, st.session_state.equipment_manager
                    )
                    
                    if success:
                        st.success(f"✅ {message}")
                        
                        if imported:
                            st.subheader("Data yang Diimport:")
                            import_df = pd.DataFrame(imported)
                            st.dataframe(import_df, use_container_width=True, hide_index=True)
                            refresh_stats_immediately()
                            st.rerun()
                    else:
                        st.error(f"❌ {message}")
    
    # Tab 4: Search Equipment
    with tab4:
        st.subheader("🔍 Cari Equipment")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "Cari berdasarkan nama atau merk*",
                placeholder="Cth: Mesin Bubut, TOKOTA, Caliper",
                help="Ketik nama atau merk equipment untuk mencari"
            )
        
        with col2:
            search_type_filter = st.selectbox(
                "Filter Type",
                options=['Semua'] + EQUIPMENT_TYPES,
                help="Filter hasil pencarian berdasarkan type"
            )
        
        if search_query:
            results = st.session_state.equipment_manager.search_equipment(search_query)
            
            # Apply type filter
            if search_type_filter != 'Semua':
                results = [eq for eq in results if eq.get('type') == search_type_filter]
            
            if results:
                st.success(f"✅ Ditemukan {len(results)} equipment")
                
                # Create dataframe for better presentation
                search_data = []
                for eq in results:
                    lab_info = st.session_state.lab_manager.get_lab(eq.get('lab_id'))
                    lab_name = lab_info.get('name', eq.get('lab_id', '-')) if lab_info else eq.get('lab_id', '-')
                    
                    search_data.append({
                        'ID': eq.get('equipment_id', ''),
                        'Nama': eq.get('nama', '-'),
                        'Lab': lab_name,
                        'Type': eq.get('type', '-'),
                        'Qty': int(eq.get('jumlah', 0)),
                        'Merk': eq.get('merk', '-'),
                        'Kategori': eq.get('kategori', '-'),
                        'Status': eq.get('status', 'active'),
                        'Harga Satuan': f"Rp {float(eq.get('harga_satuan', 0)):,.0f}",
                        'Total': f"Rp {float(eq.get('harga_keseluruhan', 0)):,.0f}",
                        'Keterangan': eq.get('keterangan', '-')[:50]
                    })
                
                df_search = pd.DataFrame(search_data)
                
                # Display with horizontal scroll
                st.dataframe(
                    df_search,
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )
                
                # Export search results
                if st.button("📥 Export Hasil Pencarian ke Excel", use_container_width=True):
                    # Get full equipment data for export
                    export_list = [eq for eq in results]
                    excel_bytes = st.session_state.template_handler.export_equipment(export_list)
                    if excel_bytes:
                        st.download_button(
                            label="⬇️ Download Excel",
                            data=excel_bytes,
                            file_name=f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
            else:
                st.info("ℹ️ Tidak ada equipment yang sesuai dengan pencarian.")
    
    # Tab 5: Delete Equipment (Enhanced with Cluster & Bulk)
    with tab5:
        st.subheader("🗑️ Hapus Equipment")
        
        equipment_list = st.session_state.equipment_manager.get_all_equipment()
        
        if equipment_list:
            st.info("💡 Pilih lab dan/atau type untuk filter, kemudian pilih equipment yang ingin dihapus dari tabel")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                labs = st.session_state.lab_manager.get_all_labs()
                lab_options = {lab.get('lab_id'): lab.get('name') for lab in labs}
                selected_lab_delete = st.selectbox(
                    "Filter Lab*",
                    options=['all'] + list(lab_options.keys()),
                    format_func=lambda x: 'Semua Lab' if x == 'all' else lab_options.get(x, x),
                    key="delete_lab_filter"
                )
            
            with col2:
                selected_type_delete = st.selectbox(
                    "Filter Type",
                    options=['Semua'] + EQUIPMENT_TYPES,
                    key="delete_type_filter"
                )
            
            with col3:
                delete_mode = st.selectbox(
                    "Mode Hapus*",
                    options=['Pilih Equipment', 'Hapus Semua di Lab Ini'],
                    help="Pilih individual equipment atau hapus semua di lab yang dipilih",
                    key="delete_mode"
                )
            
            st.divider()
            
            # Apply filters
            if selected_lab_delete == 'all':
                filtered_list = equipment_list
            else:
                filtered_list = st.session_state.equipment_manager.get_equipment_by_lab(selected_lab_delete)
            
            if selected_type_delete != 'Semua':
                filtered_list = [eq for eq in filtered_list if eq.get('type') == selected_type_delete]
            
            if delete_mode == 'Pilih Equipment':
                # Show table with checkboxes
                st.subheader("Pilih Equipment untuk Dihapus")
                
                delete_data = []
                for eq in filtered_list:
                    delete_data.append({
                        'Hapus': False,  # Checkbox column
                        'ID': eq.get('equipment_id', ''),
                        'Nama': eq.get('nama', '-'),
                        'Lab': eq.get('lab_id', '-'),
                        'Qty': int(eq.get('jumlah', 0)),
                        'Type': eq.get('type', '-'),
                        'Merk': eq.get('merk', '-'),
                        'Status': eq.get('status', 'active'),
                        'Total': f"Rp {float(eq.get('harga_keseluruhan', 0)):,.0f}"
                    })
                
                df_delete = pd.DataFrame(delete_data)
                
                # Data editor untuk memilih
                edited_df = st.data_editor(
                    df_delete,
                    use_container_width=True,
                    hide_index=True,
                    height=400,
                    key="delete_selection_table"
                )
                
                # Get selected items
                selected_to_delete = [
                    filtered_list[idx].get('equipment_id')
                    for idx, row in edited_df.iterrows()
                    if row['Hapus'] == True
                ]
                
                if selected_to_delete:
                    st.warning(f"⚠️ Akan menghapus {len(selected_to_delete)} equipment - Aksi ini TIDAK DAPAT dibatalkan!")
                    
                    # Summary
                    summary_data = [eq for eq in filtered_list if eq.get('equipment_id') in selected_to_delete]
                    total_qty = sum([int(eq.get('jumlah', 0)) for eq in summary_data])
                    total_value = sum([float(eq.get('harga_keseluruhan', 0)) for eq in summary_data])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Equipment Dipilih", len(selected_to_delete))
                    with col2:
                        st.metric("Total Qty", total_qty)
                    with col3:
                        st.metric("Total Value", f"Rp {total_value:,.0f}")
                    
                    # Confirmation checkbox
                    confirm = st.checkbox("✅ Saya yakin ingin menghapus equipment ini", key="delete_confirm_checkbox")
                    
                    if st.button("🗑️ HAPUS EQUIPMENT TERPILIH", use_container_width=True, type="secondary") and confirm:
                        success_count = 0
                        error_count = 0
                        
                        with st.spinner("Menghapus equipment..."):
                            for eq_id in selected_to_delete:
                                try:
                                    st.session_state.equipment_manager.delete_equipment(eq_id)
                                    success_count += 1
                                except Exception as e:
                                    error_count += 1
                                    st.error(f"❌ Gagal menghapus {eq_id}: {str(e)}")
                        
                        refresh_stats_immediately()
                        st.success(f"✅ Berhasil menghapus {success_count} equipment")
                        if error_count > 0:
                            st.warning(f"⚠️ Gagal menghapus {error_count} equipment")
                        time.sleep(1)
                        st.rerun()
            
            else:  # Hapus Semua di Lab Ini
                st.subheader(f"Hapus Semua Equipment di {lab_options.get(selected_lab_delete, 'Lab')} (Type: {selected_type_delete})")
                
                if filtered_list:
                    total_qty_lab = sum([int(eq.get('jumlah', 0)) for eq in filtered_list])
                    total_value_lab = sum([float(eq.get('harga_keseluruhan', 0)) for eq in filtered_list])
                    
                    st.error(f"⚠️ PERHATIAN: Akan MENGHAPUS SEMUA {len(filtered_list)} equipment di lab ini!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Equipment", len(filtered_list))
                    with col2:
                        st.metric("Total Qty", total_qty_lab)
                    with col3:
                        st.metric("Total Value", f"Rp {total_value_lab:,.0f}")
                    
                    # List all equipment yang akan dihapus
                    with st.expander("📋 Lihat daftar equipment yang akan dihapus"):
                        for eq in filtered_list:
                            st.text(f"• {eq.get('equipment_id')} - {eq.get('nama')} (Qty: {int(eq.get('jumlah', 0))})")
                    
                    # Double confirmation
                    col1, col2 = st.columns(2)
                    with col1:
                        confirm1 = st.checkbox("✅ Saya memahami ini akan MENGHAPUS SEMUA DATA", key="bulk_confirm1")
                    with col2:
                        confirm2 = st.checkbox("✅ Saya YAKIN ingin melanjutkan", key="bulk_confirm2")
                    
                    if st.button("🗑️ HAPUS SEMUA EQUIPMENT DI LAB INI", use_container_width=True, type="secondary") and confirm1 and confirm2:
                        success_count = 0
                        
                        with st.spinner("Menghapus semua equipment..."):
                            for eq in filtered_list:
                                try:
                                    st.session_state.equipment_manager.delete_equipment(eq.get('equipment_id'))
                                    success_count += 1
                                except Exception as e:
                                    st.error(f"❌ Gagal menghapus: {str(e)}")
                        
                        refresh_stats_immediately()
                        st.success(f"✅ Berhasil menghapus {success_count} equipment")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("ℹ️ Tidak ada equipment di lab/type yang dipilih")
        else:
            st.info("ℹ️ Belum ada equipment yang terdaftar.")
    
    # Tab 6: Edit Equipment (Comprehensive)
    with tab6:
        st.subheader("✏️ Edit Equipment")
        
        equipment_list = st.session_state.equipment_manager.get_all_equipment()
        if equipment_list:
            selected_equipment = st.selectbox(
                "Pilih Equipment untuk diedit*",
                options=[eq.get('equipment_id') for eq in equipment_list],
                format_func=lambda x: next((f"{eq.get('nama')} (ID: {eq.get('equipment_id')})" 
                                          for eq in equipment_list if eq.get('equipment_id') == x), x),
                key="edit_equipment_select"
            )
            
            eq = st.session_state.equipment_manager.get_equipment(selected_equipment)
            if eq:
                st.info(f"📌 Equipment ID: {eq.get('equipment_id')} | Lab: {eq.get('lab_id')} | Dibuat: {eq.get('created_date', '')[:10]}")
                
                with st.form(f"edit_equipment_form_{selected_equipment}", clear_on_submit=False):
                    col1, col2 = st.columns(2)
                    
                    # Left column
                    with col1:
                        st.subheader("Informasi Dasar")
                        
                        new_nama = st.text_input(
                            "Nama Equipment*",
                            value=eq.get('nama', ''),
                            help="Nama atau deskripsi singkat equipment"
                        )
                        
                        new_type = st.selectbox(
                            "Type Equipment*",
                            options=EQUIPMENT_TYPES,
                            index=EQUIPMENT_TYPES.index(eq.get('type', 'Lainnya')) if eq.get('type') in EQUIPMENT_TYPES else 0,
                            help="Kategori/tipe equipment"
                        )
                        
                        new_kategori = st.selectbox(
                            "Kategori*",
                            options=EQUIPMENT_CATEGORIES,
                            index=EQUIPMENT_CATEGORIES.index(eq.get('kategori', 'Lainnya')) if eq.get('kategori') in EQUIPMENT_CATEGORIES else 0,
                            help="Klasifikasi equipment"
                        )
                        
                        new_merk = st.text_input(
                            "Merk/Brand",
                            value=eq.get('merk', ''),
                            help="Merek atau manufacturer equipment"
                        )
                    
                    # Right column
                    with col2:
                        st.subheader("Detail Teknis & Stok")
                        
                        new_qty = st.number_input(
                            "Jumlah (Qty)*",
                            min_value=0.0,
                            value=float(eq.get('jumlah', 0)),
                            step=1.0,
                            help="Jumlah unit saat ini di sistem"
                        )
                        
                        new_harga_satuan = st.number_input(
                            "Harga Satuan (Rp)*",
                            min_value=0.0,
                            value=float(eq.get('harga_satuan', 0)),
                            step=1000.0,
                            help="Harga per unit dalam Rupiah"
                        )
                        
                        new_bom = st.text_input(
                            "BoM / Kode Internal",
                            value=eq.get('bom', ''),
                            help="Bill of Materials atau kode internal (opsional)"
                        )
                        
                        # Calculate and show total
                        new_harga_total = new_qty * new_harga_satuan
                        st.metric("Harga Total", f"Rp {new_harga_total:,.0f}")
                    
                    st.divider()
                    
                    # Status and Keterangan
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Normalize status
                        current_status = eq.get('status', 'active').lower().strip()
                        status_mapping = {
                            'aktif': 'active', 'maintenance': 'maintenance',
                            'habis pakai': 'depleted', 'depleted': 'depleted',
                            'archived': 'archived', 'diarsipkan': 'archived'
                        }
                        normalized_status = status_mapping.get(current_status, 'active')
                        allowed_statuses = ['active', 'maintenance', 'depleted', 'archived']
                        if normalized_status not in allowed_statuses:
                            normalized_status = 'active'
                        
                        new_status = st.selectbox(
                            "Status Equipment*",
                            options=allowed_statuses,
                            format_func=lambda x: {
                                'active': '🟢 Aktif', 
                                'maintenance': '🟡 Maintenance', 
                                'depleted': '🔴 Habis Pakai', 
                                'archived': '⚪ Diarsipkan'
                            }.get(x, x),
                            index=allowed_statuses.index(normalized_status),
                            help="Status operasional equipment"
                        )
                    
                    with col2:
                        st.caption("📋 Info Tambahan")
                        st.caption(f"Lab: {eq.get('lab_id')}")
                        st.caption(f"Dibuat: {eq.get('created_date', '')[:10]}")
                        st.caption(f"Terakhir diupdate: {eq.get('last_modified', '')[:10]}")
                    
                    st.divider()
                    
                    new_keterangan = st.text_area(
                        "Keterangan / Catatan",
                        value=eq.get('keterangan', ''),
                        placeholder="Contoh: Kondisi baik, Rusak sebagian, Perlu perbaikan, dll",
                        height=100,
                        help="Informasi lengkap tentang kondisi, spesifikasi, atau catatan penting equipment"
                    )
                    
                    # Submit button
                    col1, col2 = st.columns(2)
                    with col1:
                        submitted = st.form_submit_button("💾 Simpan Perubahan", use_container_width=True)
                    with col2:
                        st.form_submit_button("❌ Batal", use_container_width=True, disabled=True)
                    
                    if submitted:
                        if not new_nama or new_qty < 0 or new_harga_satuan < 0:
                            st.error("❌ Nama, Qty, dan Harga Satuan harus diisi dengan nilai valid!")
                        else:
                            try:
                                # Update equipment data
                                eq_updated = eq.copy()
                                eq_updated.update({
                                    'nama': new_nama,
                                    'type': new_type,
                                    'kategori': new_kategori,
                                    'merk': new_merk,
                                    'jumlah': new_qty,
                                    'harga_satuan': new_harga_satuan,
                                    'harga_keseluruhan': new_harga_total,
                                    'bom': new_bom,
                                    'status': new_status,
                                    'keterangan': new_keterangan,
                                    'last_modified': datetime.now().isoformat()
                                })
                                
                                success = st.session_state.equipment_manager.update_equipment(selected_equipment, eq_updated)
                                
                                if success:
                                    refresh_stats_immediately()
                                    st.success("✅ Equipment berhasil diperbarui!")
                                    st.info(f"📝 Perubahan: Nama={new_nama}, Type={new_type}, Status={new_status}")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error("❌ Gagal menyimpan perubahan")
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
            # Initialize session state
            if 'in_selected_lab' not in st.session_state:
                st.session_state.in_selected_lab = labs[0].get('lab_id') if labs else None
            
            # Lab selectbox OUTSIDE form to ensure proper refresh
            selected_lab = st.selectbox(
                "Pilih Lab*",
                options=[lab.get('lab_id') for lab in labs],
                format_func=lambda x: next((lab.get('name') for lab in labs if lab.get('lab_id') == x), x),
                key="in_lab_select",
                help="Pilih lab tempat barang masuk"
            )
            
            # Update session state
            st.session_state.in_selected_lab = selected_lab
            
            # Get equipment for selected lab
            equipment_list = st.session_state.equipment_manager.get_equipment_by_lab(selected_lab)
            
            if equipment_list:
                # Equipment selectbox OUTSIDE form to ensure proper state management
                selected_equipment = st.selectbox(
                    "Pilih Equipment*",
                    options=[eq.get('equipment_id') for eq in equipment_list],
                    format_func=lambda x: next((eq.get('nama') for eq in equipment_list if eq.get('equipment_id') == x), x),
                    help="Equipment mana yang akan ditambahkan/masuk",
                    key=f"in_equipment_{selected_lab}"
                )
                
                with st.form("in_movement_form", clear_on_submit=True):
                    # Add date input
                    col1, col2 = st.columns(2)
                    with col1:
                        adjustment_date = st.date_input(
                            "Tanggal Masuk*",
                            value=pd.Timestamp.now().date(),
                            help="Tanggal barang masuk ke lab",
                            key=f"in_date_{selected_lab}"
                        )
                    
                    with col2:
                        quantity = st.number_input(
                            "Jumlah Masuk*", 
                            min_value=0.0, 
                            step=1.0, 
                            value=0.0,
                            help="Berapa jumlah unit yang masuk/ditambahkan",
                            key=f"in_qty_{selected_lab}"
                        )
                    
                    notes = st.text_area(
                        "Catatan", 
                        height=80,
                        help="Catatan tambahan tentang barang yang masuk (opsional)",
                        key=f"in_notes_{selected_lab}"
                    )
                    
                    submitted = st.form_submit_button("✅ Catat Barang Masuk", use_container_width=True)
                    
                    if submitted:
                        if quantity > 0:
                            try:
                                st.session_state.equipment_manager.adjust_quantity(
                                    selected_equipment, quantity, notes, "in", adjustment_date=adjustment_date
                                )
                                refresh_stats_immediately()
                                st.success(f"✅ Berhasil mencatat {quantity} barang masuk pada {adjustment_date.strftime('%d-%m-%Y')}!")
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
            # Initialize session state
            if 'out_selected_lab' not in st.session_state:
                st.session_state.out_selected_lab = labs[0].get('lab_id') if labs else None
            
            # Lab selectbox OUTSIDE form to ensure proper refresh
            selected_lab = st.selectbox(
                "Pilih Lab*",
                options=[lab.get('lab_id') for lab in labs],
                format_func=lambda x: next((lab.get('name') for lab in labs if lab.get('lab_id') == x), x),
                key="out_lab_select",
                help="Pilih lab dari mana barang keluar"
            )
            
            # Update session state
            st.session_state.out_selected_lab = selected_lab
            
            equipment_list = st.session_state.equipment_manager.get_equipment_by_lab(selected_lab)
            
            if equipment_list:
                # Equipment selectbox OUTSIDE form to ensure proper refresh of stock info
                selected_equipment = st.selectbox(
                    "Pilih Equipment*",
                    options=[eq.get('equipment_id') for eq in equipment_list],
                    format_func=lambda x: next((eq.get('nama') for eq in equipment_list if eq.get('equipment_id') == x), x),
                    key=f"out_equipment_{selected_lab}",
                    help="Equipment mana yang akan keluar"
                )
                
                # Get current quantity - refresh automatically when equipment changes
                eq = st.session_state.equipment_manager.get_equipment(selected_equipment)
                current_qty = float(eq.get('jumlah', 0)) if eq else 0
                
                st.info(f"💾 Stok Saat Ini: {int(current_qty)} unit")
                
                with st.form("out_movement_form", clear_on_submit=True):
                    
                    # Add date input
                    col1, col2 = st.columns(2)
                    with col1:
                        adjustment_date = st.date_input(
                            "Tanggal Keluar*",
                            value=pd.Timestamp.now().date(),
                            help="Tanggal barang keluar dari lab",
                            key=f"out_date_{selected_lab}"
                        )
                    
                    with col2:
                        quantity = st.number_input(
                            "Jumlah Keluar*",
                            min_value=0.0,
                            max_value=current_qty,
                            step=1.0,
                            value=0.0,
                            help="Berapa jumlah unit yang akan keluar (tidak boleh melebihi stok saat ini)",
                            key=f"out_qty_{selected_lab}"
                        )
                    
                    reason = st.selectbox(
                        "Alasan",
                        ["Penggunaan/Praktikum", "Hilang", "Rusak", "Perbaikan", "Lainnya"],
                        help="Pilih alasan barang keluar dari lab",
                        key=f"out_reason_{selected_lab}"
                    )
                    
                    notes = st.text_area(
                        "Catatan Detail", 
                        height=80,
                        help="Keterangan detail tentang penggunaan atau keadaan barang yang keluar",
                        key=f"out_notes_{selected_lab}"
                    )
                    
                    submitted = st.form_submit_button("✅ Catat Barang Keluar", use_container_width=True)
                    
                    if submitted:
                        if quantity > 0:
                            try:
                                full_notes = f"{reason}: {notes}" if notes else reason
                                st.session_state.equipment_manager.adjust_quantity(
                                    selected_equipment, -quantity, full_notes, "out", adjustment_date=adjustment_date
                                )
                                refresh_stats_immediately()
                                st.success(f"✅ Berhasil mencatat {quantity} barang keluar pada {adjustment_date.strftime('%d-%m-%Y')}!")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                        else:
                            st.error("❌ Jumlah harus lebih dari 0!")
            else:
                st.info("ℹ️ Belum ada equipment di lab ini.")
    
    # Tab 3: History (Enhanced with Search)
    with tab3:
        st.subheader("📝 History Pergerakan Inventory")
        
        st.info("💡 Lihat semua pergerakan equipment (masuk, keluar, adjustment) dari semua lab")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            start_date = st.date_input(
                "Dari Tanggal*",
                value=(datetime.now() - timedelta(days=30)).date(),
                key="movement_start"
            )
        
        with col2:
            end_date = st.date_input(
                "Sampai Tanggal*",
                value=datetime.now().date(),
                key="movement_end"
            )
        
        with col3:
            # Get all labs for filter
            labs = st.session_state.lab_manager.get_all_labs()
            lab_options = {lab.get('lab_id'): lab.get('name') for lab in labs}
            selected_lab_history = st.selectbox(
                "Filter Lab",
                options=['all'] + list(lab_options.keys()),
                format_func=lambda x: 'Semua Lab' if x == 'all' else lab_options.get(x, x),
                key="history_lab_filter"
            )
        
        with col4:
            selected_movement_type = st.selectbox(
                "Filter Tipe Pergerakan",
                options=['Semua', 'in', 'out', 'adjustment'],
                format_func=lambda x: 'Semua' if x == 'Semua' else x.upper(),
                key="history_type_filter"
            )
        
        # Search button
        if st.button("🔍 Cari Pergerakan", use_container_width=True, key="search_history_btn"):
            movements = st.session_state.inventory_manager.get_movements(
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat()
            )
            
            # Apply lab filter
            if selected_lab_history != 'all':
                movements = [m for m in movements if m.get('lab_id') == selected_lab_history]
            
            # Apply movement type filter
            if selected_movement_type != 'Semua':
                movements = [m for m in movements if m.get('movement_type') == selected_movement_type]
            
            if movements:
                st.success(f"✅ Ditemukan {len(movements)} pergerakan inventory")
                
                # Create comprehensive dataframe
                df_data = []
                for m in movements:
                    # Get equipment name
                    equipment_name = m.get('equipment_name', '')
                    if not equipment_name:
                        eq = st.session_state.equipment_manager.get_equipment(m.get('equipment_id'))
                        equipment_name = eq.get('nama', 'N/A') if eq else 'N/A'
                    
                    # Get equipment type
                    equipment_type = 'N/A'
                    eq = st.session_state.equipment_manager.get_equipment(m.get('equipment_id'))
                    if eq:
                        equipment_type = eq.get('type', 'N/A')
                    
                    movement_type_display = {
                        'in': '📥 Masuk',
                        'out': '📤 Keluar',
                        'adjustment': '⚙️ Adjustment'
                    }.get(m.get('movement_type', '-'), m.get('movement_type', '-'))
                    
                    df_data.append({
                        'Tanggal': m.get('date', '')[:10],
                        'Jam': m.get('date', '')[11:19] if len(m.get('date', '')) > 10 else '-',
                        'Equipment ID': m.get('equipment_id', ''),
                        'Equipment Name': equipment_name,
                        'Type': equipment_type,
                        'Lab': m.get('lab_id', '-'),
                        'Tipe Pergerakan': movement_type_display,
                        'Qty': int(m.get('quantity', 0)),
                        'Catatan': m.get('notes', '')[:60]
                    })
                
                df = pd.DataFrame(df_data)
                
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    height=500
                )
                
                # Summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    in_count = len([m for m in movements if m.get('movement_type') == 'in'])
                    st.metric("📥 Masuk", in_count)
                with col2:
                    out_count = len([m for m in movements if m.get('movement_type') == 'out'])
                    st.metric("📤 Keluar", out_count)
                with col3:
                    adj_count = len([m for m in movements if m.get('movement_type') == 'adjustment'])
                    st.metric("⚙️ Adjustment", adj_count)
                
                # Export option
                if st.button("📥 Export History ke Excel", use_container_width=True):
                    # Create export file
                    excel_file = st.session_state.template_handler.export_consumption_report(movements)
                    if excel_file:
                        st.download_button(
                            label="⬇️ Download Excel",
                            data=excel_file,
                            file_name=f"history_{start_date}_{end_date}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
            else:
                st.info("ℹ️ Tidak ada pergerakan inventory dalam periode dan filter yang dipilih.")

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
                    # Try to get equipment name from multiple sources
                    equipment_name = data.get('equipment_name', '')  # From stored data
                    
                    if not equipment_name:
                        # Fallback: lookup from equipment_manager
                        eq = st.session_state.equipment_manager.get_equipment(eq_id)
                        equipment_name = eq.get('nama', 'N/A') if eq else 'N/A'
                    
                    # If still not found, try from stored movements
                    if equipment_name == 'N/A' and data.get('movements'):
                        first_movement = data.get('movements')[0]
                        equipment_name = first_movement.get('equipment_name', 'N/A')
                    
                    df_data.append({
                        'Equipment': equipment_name,
                        'Lab': data.get('lab_id', '-'),
                        'Jumlah Dikonsumsi': int(abs(data.get('total_consumed', 0))),
                        'Terakhir': data.get('last_consumption', '')[:10],
                        'Movements': len(data.get('movements', []))
                    })
                    # Add equipment_name to report for export (use the resolved name)
                    data['equipment_name'] = equipment_name
                
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
            try:
                if export_type == "Equipment Data":
                    equipment_list = st.session_state.equipment_manager.get_all_equipment()
                    if equipment_list:
                        excel_bytes = st.session_state.template_handler.export_equipment(equipment_list)
                        
                        if excel_bytes:
                            st.download_button(
                                label="⬇️ Download Equipment Data",
                                data=excel_bytes,
                                file_name=f"equipment_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                            st.success("✅ File siap diunduh!")
                    else:
                        st.info("ℹ️ Belum ada equipment data untuk diexport")
                
                elif export_type == "Consumption Data":
                    depletion_report = st.session_state.inventory_manager.get_depletion_report()
                    
                    if depletion_report:
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
                    else:
                        st.info("ℹ️ Belum ada data konsumsi untuk diexport")
                
                elif export_type == "All Data":
                    equipment_list = st.session_state.equipment_manager.get_all_equipment()
                    depletion_report = st.session_state.inventory_manager.get_depletion_report()
                    movements_data = st.session_state.inventory_manager.movements
                    
                    # Add equipment names to depletion report
                    for eq_id, data in depletion_report.items():
                        eq = st.session_state.equipment_manager.get_equipment(eq_id)
                        data['equipment_name'] = eq.get('nama', 'N/A') if eq else 'N/A'
                    
                    if equipment_list or depletion_report:
                        excel_bytes = st.session_state.template_handler.export_all_data(
                            equipment_list,
                            depletion_report,
                            movements_data
                        )
                        
                        if excel_bytes:
                            st.download_button(
                                label="⬇️ Download All Data",
                                data=excel_bytes,
                                file_name=f"all_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                            st.success("✅ File siap diunduh!")
                    else:
                        st.info("ℹ️ Belum ada data untuk diexport")
            except Exception as e:
                st.error(f"❌ Error saat menyiapkan export: {str(e)}")

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
            if st.button("📥 Export All Data", use_container_width=True, key="export_all_btn"):
                equipment_list = st.session_state.equipment_manager.get_all_equipment()
                depletion_report = st.session_state.inventory_manager.get_depletion_report()
                movements_data = st.session_state.inventory_manager.movements
                
                # Add equipment names to depletion report
                for eq_id, data in depletion_report.items():
                    eq = st.session_state.equipment_manager.get_equipment(eq_id)
                    data['equipment_name'] = eq.get('nama', 'N/A') if eq else 'N/A'
                
                if equipment_list or depletion_report:
                    excel_bytes = st.session_state.template_handler.export_all_data(
                        equipment_list,
                        depletion_report,
                        movements_data
                    )
                    
                    if excel_bytes:
                        st.download_button(
                            label="⬇️ Download All Data Excel",
                            data=excel_bytes,
                            file_name=f"inventory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        st.success("✅ File siap diunduh!")
                else:
                    st.info("ℹ️ Belum ada data untuk diexport")
        
        with col2:
            st.write("**Database Reset:**")
            
            # Initialize reset state if not exists
            if 'show_reset_dialog' not in st.session_state:
                st.session_state.show_reset_dialog = False
            
            if not st.session_state.show_reset_dialog:
                if st.button("🗑️ Reset Database (HATI-HATI!)", use_container_width=True, key="reset_btn"):
                    st.session_state.show_reset_dialog = True
                    st.rerun()
            else:
                st.warning("⚠️ Fitur ini akan menghapus SEMUA data. Silakan backup terlebih dahulu!")
                
                col_backup, col_reset = st.columns(2)
                
                with col_backup:
                    if st.button("📥 Backup Dulu (Export All Data)", use_container_width=True, key="backup_before_reset"):
                        equipment_list = st.session_state.equipment_manager.get_all_equipment()
                        depletion_report = st.session_state.inventory_manager.get_depletion_report()
                        movements_data = st.session_state.inventory_manager.movements
                        
                        # Add equipment names to depletion report
                        for eq_id, data in depletion_report.items():
                            eq = st.session_state.equipment_manager.get_equipment(eq_id)
                            data['equipment_name'] = eq.get('nama', 'N/A') if eq else 'N/A'
                        
                        if equipment_list or depletion_report:
                            excel_bytes = st.session_state.template_handler.export_all_data(
                                equipment_list,
                                depletion_report,
                                movements_data
                            )
                            
                            if excel_bytes:
                                st.download_button(
                                    label="⬇️ Download Backup",
                                    data=excel_bytes,
                                    file_name=f"inventory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                                st.info("✅ Silakan download backup terlebih dahulu sebelum reset")
                        
                        st.session_state.show_reset_dialog = False
                
                with col_reset:
                    if st.button("🔴 Hapus Semua Data (Tidak Bisa Dibatalkan!)", use_container_width=True, key="confirm_reset"):
                        try:
                            # Reset all data
                            st.session_state.lab_manager.reset_all_data()
                            st.session_state.equipment_manager.reset_all_data()
                            st.session_state.inventory_manager.reset_all_data()
                            
                            # Clear cache
                            refresh_stats_immediately()
                            
                            st.session_state.show_reset_dialog = False
                            st.success("✅ Database berhasil direset! Semua data telah dihapus.")
                            st.info("ℹ️ Halaman akan direload dalam 2 detik...")
                            time.sleep(2)
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error saat reset database: {str(e)}")
                            st.session_state.show_reset_dialog = False
                
                # Cancel button
                if st.button("❌ Batal", use_container_width=True, key="cancel_reset"):
                    st.session_state.show_reset_dialog = False
                    st.rerun()
    
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
