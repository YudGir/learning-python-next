# 1. Perintahkan Python untuk membaca file .env tersembunyi
import os
import streamlit as st
from dotenv import load_dotenv 
from google import genai

# 1. Baca file .env secara aman
load_dotenv()
apiKey = os.getenv("GEMINI_API_KEY")

# 2. Sambungkan pipa ke server Google
client = genai.Client(api_key=apiKey)

# 3. Tampilan Aplikasi Web Streamlit
st.title("AI Deteksi Kata Kasar Jogja 🤖")
st.write("Aplikasi pendeteksi teks otomatis berbasis Google Gemini.")

# Kotak input untuk user
kalimat_user = st.text_input("Masukkan kalimatmu di sini:")

# Tombol eksekusi
if st.button("Proses AI"):
    if kalimat_user:  # Memastikan user sudah mengetik sesuatu
        with st.spinner("AI sedang berpikir..."): # Animasi loading biar keren
            response_AI = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=kalimat_user,
            )
            
            # KUNCI UTAMA: Tambahkan '.text' di belakangnya agar keluar teks murni!
            st.success("Analisis Selesai!")
            st.write(f"**Hasil Analisis AI:** {response_AI.text}")
    else:
        st.warning("Ketik kalimatnya dulu dong, bro! 🗿")