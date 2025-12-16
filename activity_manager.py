# modules/activity_manager.py
import streamlit as st
import json
import os
from datetime import datetime
import time


# Variabel konstan
DATA_FILE = "data/activities.json"
CATEGORIES = ["Akademik", "Organisasi", "Lainnya"]
PRIORITIES = ["Tinggi", "Sedang", "Rendah"]
STATUS_OPTIONS = ["Belum Dimulai", "Dalam Proses", "Selesai"]

# Fungsi untuk memuat aktivitas
def load_activities():
    """Memuat data aktivitas dari file JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Pastikan setiap aktivitas memiliki ID yang valid
                for activity in data:
                    if 'id' not in activity:
                        activity['id'] = int(time.time() * 1000) + data.index(activity)
                return data
        except:
            return []
    return []

# Fungsi untuk menyimpan aktivitas
def save_activities(activities):
    """Menyimpan data aktivitas ke file JSON"""
    try:
        os.makedirs("data", exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(activities, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Gagal menyimpan data: {str(e)}")
        return False

# Fungsi untuk menampilkan form tambah aktivitas
def add_activity_form(show_notification_func=None):
    """Form untuk menambahkan aktivitas baru"""
    with st.form("add_activity_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nama = st.text_input("Nama Aktivitas*")
            kategori = st.selectbox("Kategori*", CATEGORIES)
        
        with col2:
            deadline = st.date_input("Deadline*")
            prioritas = st.selectbox("Prioritas*", PRIORITIES)
        
        deskripsi = st.text_area("Deskripsi Aktivitas")
        catatan = st.text_area("Catatan Tambahan")
        
        submitted = st.form_submit_button("💾 Simpan Aktivitas")
        
        if submitted:
            if not nama:
                if show_notification_func:
                    show_notification_func("Nama aktivitas harus diisi!", "error")
                else:
                    st.error("Nama aktivitas harus diisi!")
                return
            
            # Generate ID unik berdasarkan timestamp
            new_id = int(time.time() * 1000)
            
            new_activity = {
                "id": new_id,
                "nama": nama,
                "kategori": kategori,
                "deadline": deadline.strftime("%Y-%m-%d"),
                "prioritas": prioritas,
                "deskripsi": deskripsi,
                "catatan": catatan,
                "status": "Belum Dimulai",
                "tanggal_dibuat": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            st.session_state.activities.append(new_activity)
            if save_activities(st.session_state.activities):
                # Tampilkan notifikasi
                if show_notification_func:
                    show_notification_func(f"Aktivitas '{nama}' berhasil ditambahkan!", "success")
                else:
                    st.success(f"Aktivitas '{nama}' berhasil ditambahkan!")
                
                st.rerun()
            else:
                if show_notification_func:
                    show_notification_func("Gagal menyimpan aktivitas!", "error")

# Fungsi untuk menampilkan daftar aktivitas
def display_activities(activities, show_notification_func=None):
    """Menampilkan daftar aktivitas dalam format tabel sederhana"""
    if not activities:
        st.info("Belum ada aktivitas yang ditambahkan.")
        return
    
    # Filter berdasarkan kategori
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        filter_kategori = st.selectbox(
            "Filter Kategori",
            ["Semua"] + CATEGORIES,
            key="filter_kategori"
        )
    
    with filter_col2:
        filter_status = st.selectbox(
            "Filter Status",
            ["Semua"] + STATUS_OPTIONS,
            key="filter_status"
        )
    
    with filter_col3:
        filter_priority = st.selectbox(
            "Filter Prioritas",
            ["Semua"] + PRIORITIES,
            key="filter_priority"
        )
    
    # Filter data menggunakan looping
    filtered_activities = []
    for activity in activities:
        kategori_match = (filter_kategori == "Semua" or 
                         activity['kategori'] == filter_kategori)
        status_match = (filter_status == "Semua" or 
                       activity['status'] == filter_status)
        priority_match = (filter_priority == "Semua" or 
                         activity['prioritas'] == filter_priority)
        
        if kategori_match and status_match and priority_match:
            filtered_activities.append(activity)
    
    # Menampilkan statistik
    st.subheader(f"📊 Total: {len(filtered_activities)} aktivitas")
    
    # Tampilkan dalam bentuk tabel sederhana
    if filtered_activities:
        # Buat header tabel
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])
        with col1:
            st.markdown("**Nama Aktivitas**")
        with col2:
            st.markdown("**Kategori**")
        with col3:
            st.markdown("**Deadline**")
        with col4:
            st.markdown("**Prioritas**")
        with col5:
            st.markdown("**Status**")
        
        st.markdown("---")
        
        # Tampilkan setiap aktivitas
        for activity in filtered_activities:
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])
            
            with col1:
                st.write(activity['nama'])
            with col2:
                st.write(activity['kategori'])
            with col3:
                st.write(activity['deadline'])
            with col4:
                # Warna berdasarkan prioritas
                if activity['prioritas'] == 'Tinggi':
                    st.error(activity['prioritas'])
                elif activity['prioritas'] == 'Sedang':
                    st.warning(activity['prioritas'])
                else:
                    st.success(activity['prioritas'])
            with col5:
                # Warna berdasarkan status
                if activity['status'] == 'Selesai':
                    st.success(activity['status'])
                elif activity['status'] == 'Dalam Proses':
                    st.info(activity['status'])
                else:
                    st.warning(activity['status'])
            
            st.markdown("---")
        
        # Detail setiap aktivitas menggunakan expander
        st.subheader("📝 Detail dan Kelola Aktivitas")
        
        # Form untuk edit aktivitas
        with st.expander("✏️ Edit Aktivitas Cepat", expanded=False):
            st.write("Pilih aktivitas untuk diedit:")
            
            # Dropdown untuk memilih aktivitas
            activity_options = {f"{act['nama']} (ID: {act['id']})": act['id'] for act in filtered_activities}
            if activity_options:
                selected_activity_key = st.selectbox(
                    "Pilih Aktivitas:",
                    options=list(activity_options.keys()),
                    key="edit_select"
                )
                
                if selected_activity_key:
                    selected_id = activity_options[selected_activity_key]
                    selected_activity = next((act for act in activities if act['id'] == selected_id), None)
                    
                    if selected_activity:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            new_nama = st.text_input("Nama Aktivitas", value=selected_activity['nama'], key=f"edit_nama_{selected_id}")
                            new_kategori = st.selectbox("Kategori", CATEGORIES, 
                                                      index=CATEGORIES.index(selected_activity['kategori']),
                                                      key=f"edit_kategori_{selected_id}")
                            new_deadline = st.date_input("Deadline", 
                                                       value=datetime.strptime(selected_activity['deadline'], "%Y-%m-%d"),
                                                       key=f"edit_deadline_{selected_id}")
                        
                        with col2:
                            new_prioritas = st.selectbox("Prioritas", PRIORITIES, 
                                                       index=PRIORITIES.index(selected_activity['prioritas']),
                                                       key=f"edit_prioritas_{selected_id}")
                            new_status = st.selectbox("Status", STATUS_OPTIONS, 
                                                    index=STATUS_OPTIONS.index(selected_activity['status']),
                                                    key=f"edit_status_{selected_id}")
                            new_deskripsi = st.text_area("Deskripsi", value=selected_activity['deskripsi'], key=f"edit_deskripsi_{selected_id}")
                        
                        new_catatan = st.text_area("Catatan", value=selected_activity.get('catatan', ''), key=f"edit_catatan_{selected_id}")
                        
                        if st.button("💾 Simpan Perubahan", key=f"edit_save_{selected_id}"):
                            # Update data
                            selected_activity['nama'] = new_nama
                            selected_activity['kategori'] = new_kategori
                            selected_activity['deadline'] = new_deadline.strftime("%Y-%m-%d")
                            selected_activity['prioritas'] = new_prioritas
                            selected_activity['status'] = new_status
                            selected_activity['deskripsi'] = new_deskripsi
                            selected_activity['catatan'] = new_catatan
                            selected_activity['tanggal_diperbarui'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            if save_activities(st.session_state.activities):
                                # Tampilkan notifikasi
                                if show_notification_func:
                                    show_notification_func(f"Aktivitas '{new_nama}' berhasil diperbarui!", "success")
                                else:
                                    st.success(f"Aktivitas '{new_nama}' berhasil diperbarui!")
                                
                                st.rerun()
            else:
                st.info("Tidak ada aktivitas untuk diedit")
        
        st.markdown("---")
        
        # Detail individual setiap aktivitas
        for i, activity in enumerate(filtered_activities):
            with st.expander(f"{i+1}. {activity['nama']} - {activity['status']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**ID:** {activity['id']}")
                    st.write(f"**Kategori:** {activity['kategori']}")
                    st.write(f"**Prioritas:** {activity['prioritas']}")
                    st.write(f"**Deadline:** {activity['deadline']}")
                    st.write(f"**Tanggal Dibuat:** {activity.get('tanggal_dibuat', '-')}")
                    if 'tanggal_diperbarui' in activity:
                        st.write(f"**Terakhir Diperbarui:** {activity['tanggal_diperbarui']}")
                
                with col2:
                    # Update status langsung
                    current_status = activity['status']
                    new_status = st.selectbox(
                        f"Update Status",
                        STATUS_OPTIONS,
                        index=STATUS_OPTIONS.index(current_status),
                        key=f"status_{activity['id']}_{i}"
                    )
                    
                    if new_status != current_status:
                        if st.button("Update Status", key=f"update_{activity['id']}_{i}"):
                            activity['status'] = new_status
                            activity['tanggal_diperbarui'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            if save_activities(st.session_state.activities):
                                # Tampilkan notifikasi
                                if show_notification_func:
                                    show_notification_func(
                                        f"Status aktivitas '{activity['nama']}' berhasil diubah menjadi '{new_status}'!", 
                                        "info"
                                    )
                                else:
                                    st.success(f"Status berhasil diupdate!")
                                
                                st.rerun()
                
                st.write(f"**Deskripsi:** {activity.get('deskripsi', '-')}")
                st.write(f"**Catatan:** {activity.get('catatan', '-')}")
                
                # Tombol hapus - PERBAIKAN DI SINI
                st.markdown("---")
                col_del1, col_del2, col_del3 = st.columns([2, 1, 2])
                with col_del2:
                    # Gunakan session state untuk konfirmasi hapus
                    if st.button("🗑️ Hapus Aktivitas", key=f"delete_btn_{activity['id']}_{i}", type="secondary"):
                        # Set session state untuk konfirmasi
                        st.session_state.confirm_delete_id = activity['id']
                        st.rerun()
                
                # Tampilkan konfirmasi hapus jika ID sesuai
                if st.session_state.get('confirm_delete_id') == activity['id']:
                    st.warning("⚠️ **Konfirmasi Penghapusan**")
                    st.write(f"Apakah Anda yakin ingin menghapus aktivitas **'{activity['nama']}'**?")
                    
                    col_conf1, col_conf2, col_conf3 = st.columns([1, 1, 1])
                    with col_conf1:
                        if st.button("✅ Ya, Hapus", key=f"confirm_yes_{activity['id']}_{i}"):
                            activity_name = activity['nama']
                            
                            # Hapus aktivitas dari session state
                            st.session_state.activities = [
                                a for a in st.session_state.activities 
                                if a['id'] != activity['id']
                            ]
                            
                            # Simpan ke file
                            if save_activities(st.session_state.activities):
                                # Reset konfirmasi
                                st.session_state.confirm_delete_id = None
                                
                                # Tampilkan notifikasi
                                if show_notification_func:
                                    show_notification_func(
                                        f"Aktivitas '{activity_name}' berhasil dihapus!", 
                                        "warning"
                                    )
                                else:
                                    st.success("Aktivitas berhasil dihapus!")
                                
                                st.rerun()
                    
                    with col_conf2:
                        if st.button("❌ Batal", key=f"confirm_no_{activity['id']}_{i}"):
                            # Reset konfirmasi
                            st.session_state.confirm_delete_id = None
                            st.rerun()
    else:
        st.warning("Tidak ada aktivitas yang sesuai dengan filter.")

# Fungsi untuk mendapatkan aktivitas mendatang
def get_upcoming_activities(activities, days=7):
    """Mendapatkan aktivitas yang mendatang"""
    from datetime import datetime, timedelta
    
    upcoming = []
    today = datetime.now().date()
    
    for activity in activities:
        try:
            deadline = datetime.strptime(activity['deadline'], "%Y-%m-%d").date()
            days_diff = (deadline - today).days
            
            # Logika if untuk menentukan aktivitas mendatang
            if 0 <= days_diff <= days and activity['status'] != "Selesai":
                upcoming.append(activity)
        except:
            continue
    
    # Urutkan berdasarkan deadline terdekat
    upcoming.sort(key=lambda x: x['deadline'])
    return upcoming