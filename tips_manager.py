# modules/tips_manager.py
import streamlit as st
import random

# Variabel berisi tips dan trik
TIPS_DATA = [
    {
        "kategori": "Manajemen Waktu",
        "tips": [
            "Gunakan teknik Pomodoro: 25 menit fokus, 5 menit istirahat",
            "Buat jadwal mingguan dan patuhi deadline",
            "Prioritaskan tugas berdasarkan deadline dan tingkat kesulitan",
            "Alokasikan waktu untuk review dan revisi"
        ]
    },
    {
        "kategori": "Produktivitas",
        "tips": [
            "Minimalisir gangguan dengan mematikan notifikasi saat belajar",
            "Gunakan aplikasi to-do list untuk tracking progres",
            "Break down proyek besar menjadi tugas-tugas kecil",
            "Review pencapaian harian sebelum tidur"
        ]
    },
    {
        "kategori": "Keseimbangan Hidup",
        "tips": [
            "Jaga pola tidur 7-8 jam per hari",
            "Sisihkan waktu untuk hobi dan relaksasi",
            "Olahraga rutin untuk meningkatkan fokus",
            "Jangan lupa istirahat dan quality time dengan teman"
        ]
    },
    {
        "kategori": "Studi Efektif",
        "tips": [
            "Buat catatan dengan metode Cornell",
            "Ajarkan materi kepada orang lain untuk memperkuat pemahaman",
            "Gunakan teknik spaced repetition untuk mengingat",
            "Gabungkan berbagai sumber belajar"
        ]
    }
]

# Fungsi untuk mendapatkan tips acak
def get_random_tip():
    """Mengembalikan tips acak dari semua kategori"""
    all_tips = []
    for category in TIPS_DATA:
        all_tips.extend(category["tips"])
    return random.choice(all_tips)

# Fungsi untuk menampilkan halaman tips
def display_tips_page():
    """Menampilkan halaman tips dan trik"""
    
    st.markdown("""
    ### 💪 Tips Efektif untuk Mahasiswa
    
    Berikut adalah kumpulan tips dan trik yang bisa membantu Anda 
    mengelola aktivitas dengan lebih efektif:
    """)
    
    # Tampilkan semua tips dengan looping
    for category in TIPS_DATA:
        with st.expander(f"📌 {category['kategori']}", expanded=False):
            for i, tip in enumerate(category['tips'], 1):
                st.markdown(f"{i}. {tip}")
    
    st.markdown("---")
    
   