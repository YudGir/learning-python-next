import streamlit as st

st.set_page_config(page_title="Web Application for DMIF", page_icon="🚀", layout="wide")

pages = {
    "Menu Utama": [
        st.Page("map.app.py", title="IF Map Navigation", icon="🗺️"),
    ],
    "Sistem Admin": [
        st.Page("admin.py", title="Dashboard Analytics", icon="📊"),
    ]
}

pg = st.navigation(pages)
pg.run()
