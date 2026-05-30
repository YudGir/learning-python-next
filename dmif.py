import streamlit as st
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
geminiAPI = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Web Application of DMIF", page_icon="🚀", layout="wide")
st.title("Web Application of DMIF")
st.image("assets/DMIF (Departmental Map Informatics).png", caption="@2026 All Rights Reserved", use_container_width=True, width='stretch')

st.write("Yuk, coba lihat Gemini menentukan rute terbaik untuk kamu di Gedung Jurusan Informatika!")

col1, col2 = st.columns(2)

with col1: 
    position = st.selectbox(
        "Tempat Kamu Sekarang (Posisi):",
        ["Laboratorium", "Ruang Pattimura", "Toilet", "Lift", "Lapangan Basket", "Tempat Parkir"], key="Position")
    
    if position == "Laboratorium":
        pos_pattRoom = ""
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
        pos_pattRoom = ""
        sub_position = st.selectbox(
            "Pilih Toilet:",
            ["Laki-laki", "Perempuan"], key="Position_C")

    elif position == "Lift":
        pos_pattRoom = ""
        sub_position = "Lift"

    elif position == "Lapangan Basket":
        pos_pattRoom = ""
        sub_position = "Lapangan Basket"
        
    elif position == "Tempat Parkir":
        pos_pattRoom = ""
        sub_position = "Tempat Parkir"

with col2:
    destination = st.selectbox(
        "Tempat Destinasi (Tujuan):",
        ["Laboratorium", "Ruang Pattimura", "Toilet", "Lift", "Lapangan Basket", "Tempat Parkir"], key="Destination")

    if destination == "Laboratorium":
        des_pattRoom = ""
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
        des_pattRoom = ""
        sub_destination = st.selectbox(
            "Pilih Toilet:",
            ["Laki-laki", "Perempuan"], key="Destination_C")

    elif destination == "Lift":
        des_pattRoom = ""
        sub_destination = "Lift"

    elif destination == "Lapangan Basket":
        des_pattRoom = ""
        sub_destination = "Lapangan Basket"
        
    elif destination == "Tempat Parkir":
        des_pattRoom = ""
        sub_destination = "Tempat Parkir"

if st.button("GAS TEMUKAN RUTE TERBAIK UNTUK SAYA 😁", width='stretch'):
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

                Berikan output dengan format Markdown terstruktur dengan tahap demi tahap yang tepat, presisi, dan efektif.
                """
                
                try:
                    client = genai.Client(api_key=geminiAPI)
                    
                    from PIL import Image
                    img = Image.open("assets/DMIF (Departmental Map Informatics).png")

                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            temperature=0.7,
                        ),
                    )
                    
                    st.success("😎 YEAYY! Mantap! " \
                    "Begini respons Gemini buat kamu:")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Waduh ada error pas koneksi ke Gemini API: {e}")
        
        else:
            st.warning("Pilih dulu dong posisi dan destinasinya, bro! 🗿")