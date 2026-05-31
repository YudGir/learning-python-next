import streamlit as st
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
geminiAPI = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Web Application of DMIF", page_icon="🚀", layout="wide")

with st.sidebar:
    st.subheader("🔑 Pengaturan API Key")
    user_key = st.text_input("Gunakan API Key kamu sendiri (opsional jika kuota developer telah habis):", type="password")

active_api_key = user_key if user_key else geminiAPI

if not active_api_key:
    st.error("Kuota developer dan kamu sudah habis. Punya API lain? Silakan masukkan Gemini API kamu yang masih tersedia kuotanya di sidebar sebelah kiri.")

st.markdown("<h1 style='text-align: center;'>🗺️ IF Map Application</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Web Application for Departmental Informatics Map</p>", unsafe_allow_html=True)

st.image("assets/DMIF (Departmental Map Informatics).png", caption="@2026 All Rights Reserved To Yudha", use_container_width=True)

st.write("Rasain secara langsung bagaimana Gemini menentukan rute terbaik untuk kamu! 🤖")

col1, col2 = st.columns(2)

@st.cache_data(show_spinner=False)
def get_gemini_route(p_awal, d_tujuan, sub_awal, sub_tujuan, patt_awal, patt_tujuan, _api_key, user_prompt, system_prompt):
    client = genai.Client(api_key=_api_key)
    img = Image.open("assets/DMIF (Departmental Map Informatics).png")
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[img, user_prompt],
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
        ),
    )
    return response.text

with col1: 
    position = st.selectbox(
        "Tempat Kamu Sekarang (Posisi):",
        ["Laboratorium", "Ruang Pattimura", "Toilet", "Lift", "Lapangan Basket", "Tempat Parkir"], key="Position")
    
    sub_position = ""
    pos_pattRoom = ""

    if position == "Laboratorium":
        sub_position = st.selectbox(
            "Laboratorium:",
            ["Lab. Zettabyte", "Lab. Robotik", "Lab. Cloud Computing", "Lab. Internet of Things", "Lab. Jaringan",
             "Lab. Komputasi", "Lab. Geoinformatika", "Lab. Teknologi Mobile", "Lab. Basis Data",
             "Lab. Pengembangan dan Pengintegrasian Sistem Informasi", "Lab Pemrograman",
             "Lab. Pemrograman"], key="Position_A")

    elif position == "Ruang Pattimura":
        sub_position = st.selectbox(
            "Lantai:",
            ["III (Tiga)", "II (Dua)", "I (Satu)"], key="Position_B")
    
        if sub_position == "III (Tiga)":
            pos_pattRoom = st.selectbox(
                "Pilih Ruang:",
                ["III - 1A", "III - 1B", "III - 1C", "III - 1D", "III - 2A", "III - 2B", "III - 2C", 
                "III - 3A", "III - 3B", "III - 3C", "III - 3D"], key="Position_B3")
        
        elif sub_position == "II (Dua)":
            pos_pattRoom = st.selectbox(
                "Pilih Ruang:",
                ["II - 1A", "II - 1B", "II - 1C", "II - 1D", "II - 2A", "II - 2B", "II - 2C", "II - 2D", 
                "II - 3A", "II - 3B", "II - 3C", "II - 3D"], key="Position_B2")
        
        elif sub_position == "I (Satu)":
            pos_pattRoom = st.selectbox(
                "Pilih Ruang:",
                ["I - 1A", "I - 1B", "I - 1C", "I - 1D", "I - 3A", "I - 3B", "I - 3C", "I - 3D"], key="Position_B1")
    
    elif position == "Toilet":
        sub_position = st.selectbox(
            "Pilih Toilet:",
            ["Laki-laki", "Perempuan"], key="Position_C")

    else: 
        sub_position = position

with col2:
    destination = st.selectbox(
        "Tempat Destinasi (Tujuan):",
        ["Laboratorium", "Ruang Pattimura", "Toilet", "Lift", "Lapangan Basket", "Tempat Parkir"], key="Destination")

    sub_destination = ""
    des_pattRoom = ""

    if destination == "Laboratorium":
        sub_destination = st.selectbox(
            "Laboratorium:",
            ["Lab. Zettabyte", "Lab. Robotik", "Lab. Cloud Computing", "Lab. Internet of Things", "Lab. Jaringan",
             "Lab. Komputasi", "Lab. Geoinformatika", "Lab. Teknologi Mobile", "Lab. Basis Data",
             "Lab. Pengembangan dan Pengintegrasian Sistem Informasi", "Lab Pemrograman",
             "Lab. Pemrograman"], key="Destination_A")
        
    elif destination == "Ruang Pattimura":
        sub_destination = st.selectbox(
            "Lantai:",
            ["III (Tiga)", "II (Dua)", "I (Satu)"], key="Destination_B")
    
        if sub_destination == "III (Tiga)":
            des_pattRoom = st.selectbox(
                "Pilih Ruang:",
                ["III - 1A", "III - 1B", "III - 1C", "III - 1D", "III - 2A", "III - 2B", "III - 2C", 
                "III - 3A", "III - 3B", "III - 3C", "III - 3D"], key="Destination_B3")
        
        elif sub_destination == "II (Dua)":
            des_pattRoom = st.selectbox(
                "Pilih Ruang:",
                ["II - 1A", "II - 1B", "II - 1C", "II - 1D", "II - 2A", "II - 2B", "II - 2C", "II - 2D", 
                "II - 3A", "II - 3B", "II - 3C", "II - 3D"], key="Destination_B2")
        
        elif sub_destination == "I (Satu)":
            des_pattRoom = st.selectbox(
                "Pilih Ruang:",
                ["I - 1A", "I - 1B", "I - 1C", "I - 1D", "I - 3A", "I - 3B", "I - 3C", "I - 3D"], key="Destination_B1")
        
    elif destination == "Toilet":
        sub_destination = st.selectbox(
            "Pilih Toilet:",
            ["Laki-laki", "Perempuan"], key="Destination_C")

    else:
        sub_destination = destination

if st.button("GAS TEMUKAN RUTE TERBAIK UNTUK SAYA 😁", use_container_width=True):
    if not geminiAPI:
        st.error("Waduh, variabel `GEMINI_API_KEY` tidak ditemukan di file .env! Cek namanya lagi.")
    else:
        if position and sub_position and destination and sub_destination:
            with st.spinner("Gemini sedang melakukan yang terbaik, nih..."):
                
                # --- ADVANCED PROMPT ENGINEERING ---
                system_prompt = """
                Anda adalah seorang yang tahu segalanya dengan presisi maut, dan punya detail-efektif kepribadian.
                Tugas Anda adalah mencari rute terbaik dan menceritakannya kepada user secara presisi, tepat, profesional, dan berdaya teknologi.
                Jangan memberikan arah yang tidak tepat sesuai gambar yang diberikan. Gunakan pendekatan Algoritma Djikstra untuk mencari rute terdekat.
                
                JANGAN SEPERTI AI! yang memberikan respons yang kaku, AI-made, dan ambigu. Jelas, padat, singkat, tapi gacor abis (jangan sampaikan kata gacor di dalam respon kamu).
                Gambar DMIF itu sudah diberikan sebelumnya.
                Gambar tersebut adalah Departmental Map of Informatics. Di bagian tengahnya, anggap saja itu adalah lantai penghubung (area tengah) bagi para
                sivitas akademika melewat dari sisi bangunan kiri ke kanan (dan sebaliknya). Di area tengah gedung itu, di setiap lantainya (karena total ada 3 lantai),
                akan selalu ada kamar mandi laki-laki dan perempuan (persis seperti area tengah yang ada pada gambar ya!).

                Jika user DESTINASI-nya ingin ke Tempat Parkir atau Lapangan, jangan anggap ada Pintu Keluar ya! Yang ada itu jalan dari tengah gedung
                lantai kampus dan JALAN itu tuh sebenernya JALAN BENERAN (bukan lantai lagi) tapi di pinggirnya ada jalan lantai gitu (yg warna coklat ya, bukan jalanan itu).
                Jalanan di sebelah kanan itu (yg persis gambarnya jalan) itu beneran jalanan, bahkan itu parkir motor juga!
                Deteksi semua letak ruangan dan objek semuanya secara presisi, akurat, dan berikan rute terbaik yang mantap sekali. 
                Tidak perlu ada diksi ilmiah atau yang menyulitkan orang awam.
                Jika user SEDANG BERADA DI POSISI DAN MENUJU DESTINASI 'toilet', karena kita tidak tau ada di lantai berapa toilet itu, maka kasih arahan terbaik ya!
                Tunjukkan saja, LANGSUNG!

                JIKA posisi DAN destinasi ADALAH SAMA, jangan marahin user, kasih tau mereka bahwa posisi dan tujuan mereka itu masih sama dengan baik hati.
                Meski begitu, cukup pilih kata 'terbaik' saja tanpa memberitahu kata seperti 'efisien', dsb untuk prakatanya!
                """
                
                user_prompt = f"""
                Temukan rute terbaik untuk saya berdasarkan gambar yang saya lampirkan dengan parameter berikut:
                Dari, posisi {position} dan sub posisi {sub_position} (jika berada di Patt: {pos_pattRoom}).
                Menuju, destinasi: {destination} dan sub destinasi {sub_destination} (jika ada tujuan Patt {des_pattRoom}).

                Berikan output dengan format bernomor runtutan terstruktur dengan rutenya yang tepat, presisi, singkat, to the point, dan efektif.
                Jangan ikutkan diksi "sayap", tapi berikan konteks spesifik yang tepat dan awam sangat pun tahu itu!
                """
                
                try:
                    response_text = get_gemini_route(position, destination, sub_position, sub_destination, pos_pattRoom, des_pattRoom, active_api_key, user_prompt, system_prompt)

                    st.success("😎 YEAYY! Mantap! " \
                    "Begini respons Gemini buat kamu:")
                    st.markdown(response_text)
                    
                except Exception as e:
                    st.error(f"Waduh ada error pas koneksi ke Gemini API: {e}")
        
        else:
            st.warning("Pilih dulu dong posisi dan destinasinya.")

st.caption("**Catatan:** Mohon menunggu loading beberapa saat hingga selesai")
st.markdown("> _Informasi Tambahan: Aplikasi ini terintegrasi langsung dengan Gemini API._")