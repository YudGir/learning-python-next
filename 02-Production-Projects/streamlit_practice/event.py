import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. LOAD API KEY DARI .ENV
# Membaca file .env di folder yang sama
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="AI Project & Competition Idea Generator", page_icon="🚀", layout="wide")

# Judul Aplikasi
st.title("🚀 AI Generator Judul Proyek IT & Ide Lomba Otomatis")
nama_user = st.text_input("Masukkan namamu dulu bro:")
st.write(f"Halo, {nama_user}! Konfigurasi Gemini API & `.env` berhasil dideteksi.")

# Form Input User
col1, col2 = st.columns(2)

with col1:
    kategori = st.selectbox(
        "Kategori Proyek / Lomba:",
        ["Web Development", "Mobile Apps", "Machine Learning / AI", "Data Science", "IoT", "Cybersecurity"]
    )
    
    tingkat_kesulitan = st.select_slider(
        "Tingkat Kesulitan:",
        options=["Pemula (Semester 2)", "Menengah (Tugas Akhir)", "Mahir (Skala Lomba Nasional)"]
    )

with col2:
    topik_spesifik = st.text_input("Topik Spesifik (Contoh: Sampah, UMKM, Kesehatan):", placeholder="Misal: Pertanian")
    target_user = st.text_input("Target Pengguna / Instansi:", placeholder="Misal: Petani lokal, Dinas Kominfo")

# Tombol Generate
if st.button("🔥 Gas Generate Ide!"):
    if not gemini_api_key:
        st.error("Waduh, variabel `GEMINI_API_KEY` tidak ditemukan di file .env bro! Cek namanya lagi.")
    else:
        with st.spinner("Gemini lagi mikir keras nyari ide jenius..."):
            
            # --- ADVANCED PROMPT ENGINEERING ---
            system_prompt = """
            Anda adalah seorang Profesor IT senior, Mentor Inkubasi Bisnis Digital, dan Juri Kompetisi Pitching Startup Nasional.
            Tugas Anda adalah menciptakan judul proyek IT dan konsep aplikasi yang inovatif, menjual, bernilai komersial tinggi, dan relevan dengan tren teknologi terbaru.
            Jangan memberikan judul yang klise atau pasaran (seperti 'Sistem Informasi Absensi'). Gunakan penamaan unik (berupa akronim kreatif atau nama brand modern).
            """
            
            user_prompt = f"""
            Buatkan 3 rekomendasi judul proyek/lomba IT yang out-of-the-box berdasarkan parameter berikut:
            - Kategori: {kategori}
            - Tingkat Kesulitan: {tingkat_kesulitan}
            - Tema/Topik Spesifik: {topik_spesifik if topik_spesifik else 'Bebas / General'}
            - Target Pengguna: {target_user if target_user else 'Masyarakat Umum'}

            Berikan output dengan format Markdown terstruktur seperti contoh di bawah ini:

            ### 💡 Ide 1: [Nama Brand/Akronim] - [Judul Catchy & Menjual]
            * **Deskripsi Singkat:** [Jelaskan apa aplikasinya dan masalah apa yang diselesaikan dalam 2 kalimat]
            * **Fitur Utama:** [Sebutkan 3 fitur utama yang canggih]
            * **Teknologi Recommended:** [Sebutkan tech stack yang cocok untuk mahasiswa IF]
            * **Nilai Jual/Inovasi:** [Mengapa ide ini layak menang lomba atau mendapat nilai A]

            ---
            (Ulangi sampai Ide 3)
            """
            
            try:
                # Inisialisasi client Gemini menggunakan API Key dari .env
                client = genai.Client(api_key=gemini_api_key)
                
                # Menggunakan model gemini-2.5-flash (cepat, cerdas, dan efisien)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.7,
                    ),
                )
                
                # Menampilkan Hasil
                st.success("😎 Mantap! Ini 3 rekomendasi ide dari Gemini buat kamu:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Waduh ada error pas koneksi ke Gemini API: {e}")
