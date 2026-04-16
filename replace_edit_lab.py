import re

# Read the file
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# Find Tab 3: Edit Lab
start_idx = None
for i, line in enumerate(lines):
    if '# Tab 3: Edit Lab' in line and i > 330 and i < 370:
        start_idx = i
        break

if start_idx:
    # Find the end of this section (next major section)
    end_idx = None
    for i in range(start_idx + 1, len(lines)):
        if '# =============' in lines[i]:
            end_idx = i
            break
    
    if end_idx is None:
        end_idx = start_idx + 40
    
    print(f"Found Tab 3: Edit Lab at line {start_idx + 1}")
    print(f"Replacing lines {start_idx + 1} to {end_idx}")
    
    # New code with button approach
    new_code = """    # Tab 3: Edit Lab
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
            st.info("ℹ️ Belum ada lab yang terdaftar.")"""
    
    # Replace the section
    new_lines = lines[:start_idx] + new_code.split('\n') + lines[end_idx:]
    
    # Write back
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print("\n" + "="*60)
    print("✅ File successfully modified!")
    print("="*60)
    print("\nModified section:")
    new_section = new_code.split('\n')
    for i, line in enumerate(new_section):
        print(f"{start_idx + i + 1:4d}: {line}")
else:
    print("❌ Could not find Tab 3: Edit Lab section")
