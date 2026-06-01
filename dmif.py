import streamlit as st

# Setup konfigurasi halaman di paling atas file pengatur
st.set_page_config(page_title="Web Application for DMIF", page_icon="🚀", layout="wide")

# Definisikan halaman-halaman aplikasi menggunakan path absolut folder views
pages = {
    "Menu Utama": [
        st.Page("views/map.app.py", title="IF Map Navigation", icon="🗺️"),
    ],
    "Sistem Admin": [
        st.Page("views/admin.py", title="Dashboard Analytics", icon="📊"),
    ]
}

# Jalankan navigasi
pg = st.navigation(pages)
pg.run()
