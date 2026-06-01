import streamlit as st
import os
import psycopg2
import pandas as pd

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") or st.secrets.get("ADMIN_PASSWORD")

st.title("📊 Ruang Kendali Administrator Web DMIF")
st.markdown("> _PENTING: Submenu ini khusus bagi Administrator Resmi DMIF saja._")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password_input = st.text_input("Masukkan Password Admin Keamanan Jaringan:", type="password")
    if st.button("LOGIN ADMINISTRATOR 🖐️", use_container_width=True):
        if password_input == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Password salah! Akses ditolak.")
    st.stop()

def get_analytics_data():
    host = "db.bhpiouzuqkoeyfainakj.supabase.co"
    port = 6543
    database = "postgres"
    user = "postgres"
    password = "IFPASTIBISA"

    if "DB_HOST" in st.secrets:
        host = st.secrets["DB_HOST"]
        port = int(st.secrets["DB_PORT"])
        database = st.secrets["DB_NAME"]
        user = st.secrets["DB_USER"]
        password = st.secrets["DB_PASS"]

    else:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        conn_str = os.getenv("DB_CONN_STR", "")
        if conn_str:
            try:
                cleaned = conn_str.replace("postgresql://", "")
                user_pass, host_port_db = cleaned.split("@")
                user, password = user_pass.split(":")
                host_port, database = host_port_db.split("/")
                host, port = host_port.split(":")
                port = int(port)
            except Exception:
                pass 

    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    
    df_search = pd.read_sql_query("SELECT rute_pencarian, status_api, created_at FROM search_analytics;", conn)
    df_learn = pd.read_sql_query("SELECT dari, ke, koreksi FROM model_learnings;", conn)
    conn.close()
    return df_search, df_learn

df_search, df_learn = get_analytics_data()

st.markdown("### 📈 Ringkasan Performa Aplikasi")
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric("Total Pencarian Rute", value=len(df_search))
with kpi2:
    success_rate = (len(df_search[df_search['status_api']=='SUCCESS']) / len(df_search) * 100) if len(df_search) > 0 else 100
    st.metric("API Success Rate", value=f"{success_rate:.1f}%")
with kpi3:
    st.metric("Jumlah Aturan di Otak AI", value=len(df_learn))

st.markdown("---")

st.markdown("### 🏆 Top 5 Rute Paling Sering Dicari Pengguna")
if not df_search.empty:
    top_routes = df_search['rute_pencarian'].value_counts().head(5)
    st.bar_chart(top_routes)
else:
    st.info("Belum ada data pencarian yang masuk.")

st.markdown("---")
st.markdown("### 🧠 Daftar Memori Hasil Ajaran User (Supabase Row Data)")
if not df_learn.empty:
    st.dataframe(df_learn, use_container_width=True)
else:
    st.info("AI belum mempelajari koreksi rute apa pun dari user.")
    
if st.button("LOGOUT ADMIN 🚪"):
    st.session_state.authenticated = False
    st.rerun()