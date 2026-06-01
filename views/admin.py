def get_analytics_data():
    host = "://supabase.com"
    port = 6543
    database = "postgres"
    password = "IFPASTIBISA"
    
    # 1. Kunci username ke format default murni Supabase AWS
    user = "postgres" 

    try:
        # 2. SUNTIKKAN IDENTITAS TENANT LEWAT PARAMETER OPTIONS (ANTI-ENOTFOUND)
        # Trik ini memaksa driver psycopg2 untuk mengirimkan ID proyekmu langsung saat jabat tangan jaringan dilakukan
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            connect_timeout=5,
            options="-c synapse.tenant_id=bhpiouzuqkoeyfainakj"
        )
        df_search = pd.read_sql_query("SELECT rute_pencarian, status_api, created_at FROM search_analytics;", conn)
        df_learn = pd.read_sql_query("SELECT dari, ke, koreksi FROM model_learnings;", conn)
        conn.close()
        return df_search, df_learn
    except Exception as e:
        # Jalur Cadangan Otomatis Kedua jika kluster AWS meminta parameter gabungan string murni
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user="postgres.bhpiouzuqkoeyfainakj",
                password=password,
                connect_timeout=5
            )
            df_search = pd.read_sql_query("SELECT rute_pencarian, status_api, created_at FROM search_analytics;", conn)
            df_learn = pd.read_sql_query("SELECT dari, ke, koreksi FROM model_learnings;", conn)
            conn.close()
            return df_search, df_learn
        except Exception as err2:
            st.error(f"🚨 Jalur Koneksi Terbuka, Tapi Supabase Menolak Autentikasi: {err2}")
            return pd.DataFrame(), pd.DataFrame()
