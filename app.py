# app.py - Aplikasi Utama
import streamlit as st
import json
import os
from datetime import datetime


# Import modul yang dibuat
from modules import activity_manager, tips_manager
# Tambahkan di app.py setelah import
# Konfigurasi halaman
st.set_page_config(
    page_title="Aktivitas Mahasiswa",
    page_icon="📚",
    layout="wide"
)

# Inisialisasi session state
if 'activities' not in st.session_state:
    st.session_state.activities = activity_manager.load_activities()

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Beranda"

# Inisialisasi session state untuk notifikasi
if 'notification' not in st.session_state:
    st.session_state.notification = None

# Inisialisasi session state untuk konfirmasi hapus
if 'confirm_delete_id' not in st.session_state:
    st.session_state.confirm_delete_id = None

# Variabel global
APP_TITLE = "Aktivitas Mahasiswa 📚"
APP_DESCRIPTION = "Kelola aktivitas akademik dan organisasi dengan efisien"

# Fungsi navigasi
def navigate_to(page):
    st.session_state.current_page = page

# Fungsi untuk menampilkan notifikasi
def show_notification(message, type="success"):
    """Menampilkan notifikasi di bagian atas halaman"""
    st.session_state.notification = {"message": message, "type": type}

# Sidebar untuk navigasi
with st.sidebar:
    st.title("📊 Menu Navigasi")
    st.markdown("---")
    
    # Menu navigasi menggunakan if statement
    if st.button("🏠 Beranda", use_container_width=True):
        navigate_to("Beranda")
    
    if st.button("➕ Tambah Aktivitas", use_container_width=True):
        navigate_to("Tambah Aktivitas")
    
    if st.button("📋 Daftar Aktivitas", use_container_width=True):
        navigate_to("Daftar Aktivitas")
    
    if st.button("💡 Tips & Trik", use_container_width=True):
        navigate_to("Tips & Trik")
    
    st.markdown("---")
    
    # Statistik
    total_activities = len(st.session_state.activities)
    completed = sum(1 for act in st.session_state.activities if act.get('status') == 'Selesai')
    
    st.metric("Total Aktivitas", total_activities)
    st.metric("Selesai", completed)
    
    st.markdown("---")
    st.caption(f"Versi 1.0 | {datetime.now().year}")

# Header aplikasi
st.title(APP_TITLE)
st.markdown(f"*{APP_DESCRIPTION}*")
st.markdown("---")

# Tampilkan notifikasi jika ada
if st.session_state.notification:
    notification = st.session_state.notification
    if notification["type"] == "success":
        st.success(notification["message"])
    elif notification["type"] == "info":
        st.info(notification["message"])
    elif notification["type"] == "warning":
        st.warning(notification["message"])
    elif notification["type"] == "error":
        st.error(notification["message"])
    
    # Hapus notifikasi setelah ditampilkan
    st.session_state.notification = None

# Routing berdasarkan halaman yang dipilih
current_page = st.session_state.current_page

# Logika if untuk routing halaman
if current_page == "Beranda":
    st.header("🏠 Dashboard Beranda")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📚 Aktivitas Akademik")
        academic_count = sum(1 for act in st.session_state.activities if act.get('kategori') == 'Akademik')
        st.metric("Jumlah", academic_count)
    
    with col2:
        st.success("🏃 Aktivitas Organisasi")
        org_count = sum(1 for act in st.session_state.activities if act.get('kategori') == 'Organisasi')
        st.metric("Jumlah", org_count)
    
    with col3:
        st.warning("⚡ Aktivitas Lainnya")
        other_count = sum(1 for act in st.session_state.activities if act.get('kategori') == 'Lainnya')
        st.metric("Jumlah", other_count)
    
    st.markdown("---")
    
    # Aktivitas mendatang
    st.subheader("⏰ Aktivitas Mendatang (7 hari ke depan)")
    upcoming = activity_manager.get_upcoming_activities(st.session_state.activities)
    
    if upcoming:
        for activity in upcoming[:5]:
            with st.expander(f"{activity['nama']} - {activity['deadline']}"):
                st.write(f"**Kategori:** {activity['kategori']}")
                st.write(f"**Prioritas:** {activity['prioritas']}")
                st.write(f"**Status:** {activity['status']}")
                st.write(f"**Deskripsi:** {activity['deskripsi']}")
    else:
        st.info("Tidak ada aktivitas mendatang dalam 7 hari ke depan")
    
    # Tips acak
    st.markdown("---")
    st.subheader("💡 Tips Hari Ini")
    random_tip = tips_manager.get_random_tip()
    st.success(random_tip)

elif current_page == "Tambah Aktivitas":
    st.header("➕ Tambah Aktivitas Baru")
    activity_manager.add_activity_form(show_notification)

elif current_page == "Daftar Aktivitas":
    st.header("📋 Daftar Semua Aktivitas")
    activity_manager.display_activities(st.session_state.activities, show_notification)

elif current_page == "Tips & Trik":
    st.header("💡 Tips & Trik Manajemen Aktivitas")
    tips_manager.display_tips_page()

else:
    st.error("Halaman tidak ditemukan!")