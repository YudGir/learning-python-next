import streamlit as st
import os
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
geminiAPI = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

# --- KUNCI PARAMETER INDIVIDUAL DI MAP_APP AGAR SINKRON DENGAN ADMIN ---
DB_HOST = "://supabase.com"
DB_PORT = 6543
DB_NAME = "postgres"
DB_USER = "postgres.bhpiouzuqkoeyfainakj"
DB_PASS = "IFPASTIBISA"

def fetch_learnings_from_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS, connect_timeout=5
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT dari, ke, koreksi FROM model_learnings;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception:
        return []

def log_search_to_db(rute, status):
    try:
        response = requests.get('http://ip-api.com', timeout=3).json()
        ip_anonim = response.get('query', 'Unknown IP')
        kota_asal = response.get('city', 'Unknown City')
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS, connect_timeout=5
        )
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO search_analytics (rute_pencarian, status_api, ip_user, lokasi) VALUES (%s, %s, %s, %s);", 
            (rute, status, ip_anonim, kota_asal)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception:
        try:
            conn = psycopg2.connect(
                host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS, connect_timeout=5
            )
            cur = conn.cursor()
            cur.execute("INSERT INTO search_analytics (rute_pencarian, status_api, ip_user, lokasi) VALUES (%s, %s, 'Unknown', 'Unknown');", (rute, status))
            conn.commit()
            cur.close()
            conn.close()
        except Exception:
            pass

def save_learning_to_db(dari, ke, koreksi):
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS, connect_timeout=5
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO model_learnings (dari, ke, koreksi) VALUES (%s, %s, %s);", (dari, ke, koreksi))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception:
        return False

db_learnings = fetch_learnings_from_db()

if "model_learnings" not in st.session_state:
    st.session_state.model_learnings = []
if "search_clicked" not in st.session_state:
    st.session_state.search_clicked = False
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

@st.fragment
def render_feedback_panel():
    st.markdown(
        """
        <div style="
            background-color: #262730; 
            padding: 12px; 
            border-radius: 8px; 
            border: 1px solid #464855;
            text-align: center; 
            margin-bottom: 15px;
        ">
            <h3 style="margin: 0; color: #FFFFFF; font-size: 1.15rem;">Mari, Bantu Gemini Belajar 🤖</h3>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.write("Apakah rute yang diberikan Gemini sebelumnya sudah akurat dan tepat?")
    
    if "feedback_status" not in st.session_state:
        st.session_state.feedback_status = None

    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        if st.button("👍 Ya, sudah akurat!", use_container_width=True):
            st.session_state.feedback_status = "akurat"
            st.toast("Mantap! Dukungan kamu begitu berarti.", icon="👏")
            
    with btn_col2:
        if st.button("👎 Belum akurat, nih.", use_container_width=True):
            st.session_state.feedback_status = "perlu_koreksi"

    if st.session_state.feedback_status == "perlu_koreksi":
        st.markdown("---")
        st.write("Bantu AI mempelajari rute yang benar versi kamu di bawah ini:")
        
        user_thought = st.text_area(
            "Tuliskan rute koreksi kamu di sini:", 
            placeholder="Misal: Harus lewat lift dulu lanjut deh naik ke lantai 3, jangan lewat tangga tengah.",
            key="sidebar_thought_input"
        )
        
        if st.button("KIRIM KOREKSI & LATIH MODEL LEBIH BAIK 🧠", use_container_width=True):
            cleaned_thought = user_thought.strip()
            
            if cleaned_thought: 
                success = save_learning_to_db(st.session_state.last_awal, st.session_state.last_tujuan, cleaned_thought)

                blacklist_words = ["anjing", "bangsat", "goblok", "tolol", "kontol", "bego", "ngentot", "jelek", "bodoh", "bodo", "bego", 
                                   "lemot", "dih", "pecundang", "lemah", "robot", "kaku", "pendiem", "cupu", "memek", "usil"
                                   "pusi", "pussy", "penis", "vagina", "dick", "jorok"]
                
                contains_bad_word = any(bad_word in cleaned_thought.lower() for bad_word in blacklist_words)

                if len(cleaned_thought) > 300:
                    st.error("Waduh, teks koreksi kamu kepanjangan! Maksimal 300 karakter saja.")
                elif contains_bad_word:
                    st.error("🚨 Deteksi Sistem: Mohon gunakan bahasa yang sopan di lingkungan UPNVY, ya!")
                elif cleaned_thought: 
                    success = save_learning_to_db(st.session_state.last_awal, st.session_state.last_tujuan, cleaned_thought)
                    if success:
                        st.toast("🧠 Terima kasih! Dukungan kamu begitu berarti.", icon="✅")
                        st.session_state.feedback_status = None
                        st.rerun()
                    else:
                        st.error("Gagal menyimpan ingatan. Coba lagi nanti.")
            else:
                st.warning("Tuliskan dulu perbaikan koreksi rute kamu sebelum mengirim, ya!")

with st.sidebar:
    user_key = ""

    with st.expander("🔑 Pengaturan API Key", expanded=False):
        st.write("Jika kuota harian developer habis, kamu bisa memasukkan API Key gratisan milikmu sendiri di bawah ini:")
        user_key = st.text_input("Gemini API Key kamu:", type="password", label_visibility="collapsed")

        if user_key.strip():
            with st.spinner("Memvalidasi API Key kamu..."):
                try:
                    test_client = genai.Client(api_key=user_key.strip())
                    test_client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents="ping",
                    )
                    
                    user_key = user_key.strip()
                    st.success("API Key kamu valid dan siap digunakan! 🚀")
                except Exception:
                    user_key = ""
                    st.error("Waduh, API Key yang kamu masukkan tidak valid atau salah! Periksa kembali.")
    
    if st.session_state.search_clicked and st.session_state.last_response:
        st.markdown("---")
        render_feedback_panel()

    if db_learnings:
        st.markdown("---")
        st.caption("🧠 **Otak Cloud AI (Pengetahuan Permanen):**")
        st.caption(f"Model memuat {len(db_learnings)} aturan kustom dari database Supabase.")
        
active_api_key = user_key if user_key else geminiAPI

if not active_api_key:
    st.error("Kuota utama developer habis. Punya API sendiri? Silakan buka menu 🔑 **Pengaturan API Key** di sidebar sebelah kiri.")

st.markdown("<h1 style='text-align: center;'>🗺️ IF Map Navigation</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Web Application for Departmental Map of Informatics UPNVY</p>", unsafe_allow_html=True)

st.image("assets/DMIF (Departmental Map Informatics).png", caption="@2026 All Rights Reserved To Yudha", use_container_width=True)

st.write("Rasain secara langsung bagaimana Gemini menentukan rute terbaik untuk kamu! 🤖")

def get_gemini_route_with_learning(lokasi_awal, lokasi_tujuan, user_prompt, system_prompt, learnings, _api_key):
    client = genai.Client(api_key=_api_key)
    img = Image.open("assets/DMIF (Departmental Map Informatics).png")
    
    custom_system_prompt = system_prompt
    if learnings:
        custom_system_prompt += "\n\nBerikut adalah aturan rute tambahan/koreksi khusus dari database cloud yang WAJIB dipatuhi:\n"
        for i, learn in enumerate(learnings, 1):
            custom_system_prompt += f"{i}. Jika rute dari '{learn['dari']}' ke '{learn['ke']}', rute BENAR: {learn['koreksi']}\n"

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[img, user_prompt],
        config=types.GenerateContentConfig(
            system_instruction=custom_system_prompt,
            temperature=0.3,
        ),
    )
    return response.text

st.markdown(
    """
    <style>
    [data-testid="stHorizontalBlock"] > div:first-child {
        border-right: 2px solid #464855 !important;
        padding-right: 25px !important;
    }

    [data-testid="stHorizontalBlock"] > div:last-child {
        padding-left: 25px !important;
    }

    @media (max-width: 768px) {
        [data-testid="stHorizontalBlock"] > div:first-child {
            border-right: none !important;
            padding-right: 0px !important;
            border-bottom: 2px solid #464855 !important;
            padding-bottom: 20px !important;
            margin-bottom: 20px !important;
        }
        [data-testid="stHorizontalBlock"] > div:last-child {
            padding-left: 0px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)
with col1: 
    position = st.selectbox(
        "Tempat Kamu Sekarang (Posisi):",
        ["Laboratorium", "Ruang Pattimura", "Toilet", "Lift", "Lapangan Basket", "Tempat Parkir", "Ruang Asisten Laboratorium", "Ruang Seminar Jurusan IF"], key="Position")
    
    sub_position = ""
    pos_pattRoom = ""

    if position == "Laboratorium":
        sub_position = st.selectbox(
            "Laboratorium:",
            ["Lab. Zettabyte", "Lab. Robotik", "Lab. Cloud Computing", "Lab. Internet of Things", "Lab. Jaringan",
             "Lab. Komputasi", "Lab. Geoinformatika", "Lab. Teknologi Mobile", "Lab. Basis Data",
             "Lab. Pengembangan dan Pengintegrasian Sistem Informasi",
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
        ["Laboratorium", "Ruang Pattimura", "Toilet", "Lift", "Lapangan Basket", "Tempat Parkir", "Ruang Asisten Laboratorium", "Ruang Seminar Jurusan IF"], key="Destination")

    sub_destination = ""
    des_pattRoom = ""

    if destination == "Laboratorium":
        sub_destination = st.selectbox(
            "Laboratorium:",
            ["Lab. Zettabyte", "Lab. Robotik", "Lab. Cloud Computing", "Lab. Internet of Things", "Lab. Jaringan",
             "Lab. Komputasi", "Lab. Geoinformatika", "Lab. Teknologi Mobile", "Lab. Basis Data",
             "Lab. Pengembangan dan Pengintegrasian Sistem Informasi",
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

lokasi_awal = f"{position} ({sub_position} {pos_pattRoom})".strip()
lokasi_tujuan = f"{destination} ({sub_destination} {des_pattRoom})".strip()

if st.button("GAS TEMUKAN RUTE TERBAIK UNTUK SAYA 😁", use_container_width=True):
    if not active_api_key:
        st.error("Waduh, variabel `GEMINI_API_KEY` tidak ditemukan di file .env! Cek namanya lagi.")
    else:
        if position and sub_position and destination and sub_destination:
            st.session_state.search_clicked = True
            with st.spinner("Gemini sedang melakukan yang terbaik, nih..."):
                
                system_prompt = """
                Tugas Anda adalah mencari rute terbaik dan menceritakannya kepada user secara presisi, tepat, profesional, dan berdaya teknologi.
                Jangan memberikan arah yang tidak tepat sesuai gambar yang diberikan. Gunakan pendekatan Algoritma Djikstra untuk mencari rute terdekat.
                
                JANGAN SEPERTI AI! yang memberikan respons yang kaku, AI-made, dan ambigu. Jelas, padat, singkat, tapi gacor abis (jangan sampaikan kata gacor di dalam respon kamu).
                Gambar DMIF itu sudah diberikan sebelumnya.
                Gambar tersebut adalah Departmental Map of Informatics. Di bagian tengahnya, anggap saja itu adalah lantai penghubung (area tengah) bagi para
                sivitas akademika melewat dari sisi bangunan kiri ke kanan (dan sebaliknya). Di area tengah gedung itu, di setiap lantainya (karena total ada 3 lantai),
                akan selalu ada kamar mandi laki-laki dan perempuan (persis seperti area tengah yang ada pada gambar ya!). Jangan pernah keluarkan kata 'presisi', cukup proses kamu mencari saja lakukan itu!

                Jika user DESTINASI-nya ingin ke Tempat Parkir atau Lapangan, jangan anggap ada Pintu Keluar ya! Yang ada itu jalan dari tengah gedung
                lantai kampus dan JALAN itu tuh sebenernya JALAN BENERAN (bukan lantai lagi) tapi di pinggirnya ada jalan lantai gitu (bukan jalanan parkir itu ya).
                Jalanan di sebelah kanan itu (yg persis gambarnya jalan) itu beneran jalanan, bahkan itu parkir motor juga!
                Deteksi semua letak ruangan dan objek semuanya secara presisi, akurat, dan berikan rute terbaik yang mantap sekali. 
                Tidak perlu ada diksi ilmiah atau yang menyulitkan orang awam.
                Jika user SEDANG BERADA DI POSISI DAN MENUJU DESTINASI 'toilet', karena kita tidak tau ada di lantai berapa toilet itu, maka:
                langsung saja arahkan user ke toilet yang berada di lantai yang sama dengan posisi user saat itu. Jadi user tidak perlu diajak naik-turun tangga cuma buat ke toilet!
                Ini juga berlaku buat posisi user dari 'Ruang Asisten Laboratorium' yang mau ke Toilet,
                langsung saja arahkan user ke toilet yang berada di lantai yang sama dengan posisi user saat itu. Jadi user tidak perlu diajak naik-turun tangga cuma buat ke toilet!
                Tunjukkan saja, LANGSUNG!

                JIKA posisi DAN destinasi ADALAH SAMA, jangan marahin user, kasih tau mereka bahwa posisi dan tujuan mereka itu masih sama dengan baik hati.
                Meski begitu, cukup pilih kata 'terbaik' saja tanpa memberitahu kata seperti 'efisien', dsb untuk prakatanya!
                Meskipun begitu, selalu lemparkan pilihan 'lift' atau 'tangga' ya!
                Lift atau tangga bukan 'atas' atau 'bawah' tengah gedung ya, tapi:
                - Kalo posisi sekarang berada di sebelah kiri dari tengah gedung, maka lift ada di sebelah kanan dan tangga di sebelah kiri di tengah gedung.
                - Kalo posisi sekarang berada di sebelah kanan dari tengah gedung, maka lift ada di sebelah kiri dan tangga di sebelah kanan di tengah gedung.

                Ada 4 lantai ya: Lantai Dasar (Ground), Lantai 1 (fleksibel aja ya: bisa dipanggil Pattimura 1), Lantai 2 (fleksibel aja ya: bisa dipanggil Pattimura 2), dan Lantai 3 (fleksibel aja ya: bisa dipanggil Pattimura 3).
                Ingat, lantai dasar (ground) bukan berarti lantai 1! Lantai dasar berarti lantai pertama dari gedung ini. Lantai 1 berarti satu lantai di atas lantai dasar (ground).
                
                PERHATIKAN WARNA NAMA RUANGAN INI:
                - WARNA MERAH RUANGANNYA: ruangan tersebut berada di LANTAI TIGA
                - WARNA HIJAU RUANGANNYA: ruangan tersebut berada di LANTAI DUA
                - WARNA BIRU RUANGANNYA: ruangan tersebut berada di LANTAI SATU
                - PERHATIKAN DAN DETEKSI WARNA DENGAN SUPER AKURAT + NO MISDETECTED + ABSOLUTE CINEMA + DETAIL PRESISI DENGAN GAMBARNYA! JANGAN SALAH ANALISIS WARNA NAMA RUANGAN!

                Di lantai dasar (Ground), ada Distrik Gedung IF. 
                CATATAN TAMBAHAN: 
                Khusus Ruang 'Toilet':
                - Kalo Toilet Laki-Laki, ada di sebelah kanan tengah gedung. 
                - Kalo Toilet Perempuan, ada di seberangnya toilet laki2, kiri tengah gedung. (jadi berseberangan dua toilet)
                - Dan ruangan Toilet selalu ada di setiap lantai.

                Khusus Ruang 'Lift':
                - Ada dua pintu lift di tengah gedung. 
                - Dan ruangan Lift selalu ada di setiap lantai.

                Khusus Ruang 'Tempat Parkir' dan 'Lapangan Basket':
                - Ini letaknya di ujung kampus dalam.
                - Mereka berdekatan, tinggal jalan aja bisa banget.
                - Kalo ada yang mau ke sini, pastikan mereka harus di LANTAI DASAR dulu baru jalan ke tempat ini.

                Khusus Ruang 'Ruang Asisten Laboratorium':
                - Karena kita tidak tau posisi tepatnya di lantai 1 atau 2, berikan masing2 arahan yang tepat untuk dua lantai sekaligus!
                - Kalo ada destinasinya mau ke sini, berikan juga masing2 arahan yang tepat untuk dua lantai sekaligus!
                - Misal: "Jika mencari rute ke Ruang Asisten Laboratorium di Lantai 1, (bla bla)".
                - Kalo ada dari posisi sini mau ke Toilet, tunjukkan arahnya ke KIRI bukan ke KANAN. Jika hendak ke toilet perempuan, toiletnya ada di sebelah kiri. Kalo laki2, toiletnya di seberang toilet perempuan!

                JANGAN PERNAH TAMPILKAN PESAN YANG TIDAK BERGUNA (BERPIKIR LAH SECARA LOGIS) KAYAK GINI:
                "Catatan: Di area Tengah Gedung, Anda akan menemukan fasilitas lift di sisi kanan dan tangga di sisi kiri, yang dapat digunakan untuk berpindah antar lantai jika diperlukan. Namun, untuk rute ke toilet di lantai yang sama, Anda tidak perlu menggunakannya."
                Seperti di atas ini jelas tidak perlu sekali! Jelas2 user dari posisi mereka di lantai tertentu dan hendak ke tempat tujuan yang MASIH SATU LANTAI (SELAGI ADA KAYAK LIFT DAN TOILET), ya JANGAN DISURUH TURUN ATAU NAIK LANTAI LAGI!

                Kalo user naik tangga atau lift, posisinya BUKAN di kiri atau kanan tengah gedung! Cukup bilang "Anda sudah di tengah gedung".

                Posisikan dirimu berada di posisi user ketika sudah menaiki tangga atau lift dari suatu posisi. 
                MISAL:
                Posisi user di Lab. Robotik (Lt. 1), mau pergi ke Lab. Zettabyte (Lt. 3). Misal user pilih naik tangga sampe ke Lt. 3.
                Karena di map posisi Lab. Zettabyte ini di sebelah kiri posisinya, tapi BUKAN BERARTI user KAMU ARAHIN "lab zettabyte ada di kiri", padahal di kiri yang ada malah Ruangan Pattimura III - 1A sampe III - 1D!
                HARUSNYA: "ketika sudah sampe naik tangga di lantai 3, lab zettabyte ada di sebelah kanan. Ruangan tujuan Anda ada di ujung kanan." NAH INI BARU AKURAT!
                Jadi gini intinya: 
                - kalo user naik tangga, posisi DESTINASI nya adalah ARAH BERLAWANAN DARI GAMBAR! Misal: kalo destinasi user adalah Lab. Zettabyte, karena di gambar itu posisi nya ada di kiri, MAKA KAMU HARUS ARAHIN USER ke kanan! bukan KE KIRI (begitu juga dengan semuanya)!
                - kalo user naik lift, posisi DESTINASI nya adalah SERUPA DENGAN POSISI DAN ARAH DI GAMBAR!

                APPLY KONSEP LOGIKA POSISI SUPER AKURAT INI BUAT SELURUH KEMUNGKINAN YA. PIKIRKAN BAIK2 DAN SE-AKURAT MUNGKIN!

                TIDAK ADA PATT. III - 2D YA!
                Jangan pernah generate warna di map kepada user! Misal: "ditandai warna biru/merah/hijau" INI JANGAN PERNAH!
                Koridor TIDAK SAMA DENGAN Area Tengah Gedung. Jangan pernah gunakan kata 'Koridor'.
                Jangan keluarkan kata "peta", "gambar", "sesuai", cukup kamu saja yang analisis di dalamnya!

                GINI PEMBAGIAN 4 SUB-RUANGAN (berupa LIST):
                Sub-Ruang A : 
                    - [Lab. Zettabyte, Patt. III - 2C, Patt. III - 2B, Patt. III - 2A] -> ini ada di Lantai 3 (sub ruang A), 
                    - [Patt. II - 2D, Patt. II - 2C, Patt. II - 2B, Patt. II - 2A] -> ini ada di Lantai 2 (sub ruang A), 
                    - [Ruang Seminar Jurusan IF, Lab. Robotik, Lab. Cloud Computing] -> ini ada di Lantai 1 (sub ruang A).

                Sub-Ruang B : 
                    - [Lab. Internet of Things, Lab. Jaringan, Lab. Komputasi, Ruang Asisten Laboratorium (di lantai 1)] -> ini ada di Lantai 1 (sub ruang B),
                    - [Lab. Geoinformatika, Lab. Teknologi Mobile, Lab. Basis Data, Ruang Asisten Laboratorium (di lantai 2)] -> ini ada di Lantai 2 (sub ruang B),
                    - [Lab. Pengembangan dan Pengintegrasian Sistem Informasi, Lab. Rancang Bangun Perangkat Lunak, Lab. Pemrograman] -> ini ada di Lantai 3 (sub ruang B).
                
                Sub-Ruang C : 
                    - [Patt. III - 1A, Patt. III - 1B, Patt. III - 1C, Patt. III - 1D] -> ini ada di Lantai 3 (sub ruang C), 
                    - [Patt. II - 1A, Patt. II - 1B, Patt. II - 1C, Patt. II - 1D] -> ini ada di Lantai 2 (sub ruang C), 
                    - [Patt. I - 1A, Patt. I - 1B, Patt. I - 1C, Patt. I - 1D] -> ini ada di Lantai 1 (sub ruang C).

                Sub-Ruang D : 
                    - [Patt. I - 3A, Patt. I - 3B, Patt. I - 3C, Patt. I - 3D] -> ini ada di Lantai 1 (sub ruang D), 
                    - [Patt. II - 3A, Patt. II - 3B, Patt. II - 3C, Patt. II - 3D] -> ini ada di Lantai 2 (sub ruang D),
                    - [Patt. III - 3A, Patt. III - 3B, Patt. III - 3C, Patt. III - 3D] -> ini ada di Lantai 3 (sub ruang D).

                (PERHATIKAN INI TEPAT + AKURAT + JELAS SEKALI DALAM MENGANALISIS POSISI USER SEKARANG!)
                Jika ada user yang berada di:
                - salah satu di Sub-Ruang A hendak pergi ke:
                  - lift: ada di kanan area gedung tengah di lantai itu!
                  - tangga: ada di kiri area gedung tengah di lantai itu!

                - salah satu di Sub-Ruang B hendak pergi ke:
                  - lift: ada di kanan area gedung tengah di lantai itu!
                  - tangga: ada di kiri area gedung tengah di lantai itu!

                - salah satu di Sub-Ruang C hendak pergi ke:
                  - lift: ada di kiri area gedung tengah di lantai itu!
                  - tangga: ada di kanan area gedung tengah di lantai itu!

                - salah satu di Sub-Ruang D hendak pergi ke:
                  - lift: ada di kiri area gedung tengah di lantai itu!
                  - tangga: ada di kanan area gedung tengah di lantai itu!

                Kalo ada yang mau pergi dari salah satu Sub Ruang A (cocokkan dari list sub ruang A di atas dengan posisi user sekarang!):
                - ingin menuju Toilet Perempuan: 
                  Arahnya adalah di sebelah kiri setelah menuju tengah gedung di dekat tangga tengah gedung di lantai itu!
                - ingin menuju Toilet Laki-laki:
                  Arahnya adalah di sebelah kiri setelah menuju tengah gedung di dekat tangga tengah gedung di lantai itu dan berseberangan dengan toilet Perempuan!
                
                Kalo ada yang mau pergi dari salah satu Sub Ruang B (cocokkan dari list sub ruang B di atas dengan posisi user sekarang!):
                - ingin menuju Toilet Perempuan: 
                  Arahnya adalah di sebelah kiri setelah menuju tengah gedung di dekat tangga tengah gedung di lantai itu!
                - ingin menuju Toilet Laki-laki:
                  Arahnya adalah di sebelah kiri setelah menuju tengah gedung di dekat tangga tengah gedung di lantai itu dan berseberangan dengan toilet Perempuan!
                
                Kalo ada yang mau pergi dari salah satu Sub Ruang C (cocokkan dari list sub ruang C di atas dengan posisi user sekarang!):
                - ingin menuju Toilet Laki-Laki: 
                  Arahnya adalah di sebelah kanan setelah menuju tengah gedung di dekat tangga tengah gedung di lantai itu!
                - ingin menuju Toilet Perempuan:
                  Arahnya adalah di sebelah kanan setelah menuju tengah gedung di dekat tangga tengah gedung di lantai itu dan berseberangan dengan toilet Laki-Laki!

                Kalo ada yang mau pergi dari salah satu Sub Ruang D (cocokkan dari list sub ruang D di atas dengan posisi user sekarang!):
                - ingin menuju Toilet Laki-Laki: 
                  Arahnya adalah di sebelah kanan setelah menuju tengah gedung di dekat tangga tengah gedung di lantai itu!
                - ingin menuju Toilet Perempuan:
                  Arahnya adalah di sebelah kanan setelah menuju tengah gedung di dekat tangga tengah gedung di lantai itu dan berseberangan dengan toilet Laki-Laki!

                Jangan ikutkan diksi "sayap", tapi berikan respon yang tepat dan awam sangat pun tahu itu!
                Jangan pernah sebut Sub-Ruang ini menuju output!
                Jangan pernah ikutkan arah dari posisi gambar lagi (kecuali untuk Tempat Parkir dan Lapangan Basket)! Ikuti saja arah di atas yang telah diberitahu kepadamu!
                """
                
                user_prompt = f"""
                Temukan rute terbaik untuk saya berdasarkan gambar yang saya lampirkan dengan parameter berikut:
                Dari, posisi {position} dan sub posisi {sub_position} (jika berada di Patt: {pos_pattRoom}).
                Menuju, destinasi: {destination} dan sub destinasi {sub_destination} (jika ada tujuan Patt {des_pattRoom}).

                Berikan output dengan format bernomor runtutan terstruktur dengan rutenya yang tepat, presisi, singkat, to the point, dan efektif seperti ini:
                "Rute terbaik dari {position} menuju {destination} adalah:
                1. Silakan Anda keluar dari ruangan {position} dahulu.
                2. Kemudian jalan lurus menuju tengah gedung di lantai (lantai posisi user) (kalo ada di dalam gedung ini apply ya!)
                3. Lanjut....
                4. {destination} ada di ( .... )."
                """
                
                try:
                    response_text = get_gemini_route_with_learning(
                        lokasi_awal, lokasi_tujuan, user_prompt, system_prompt, 
                        st.session_state.model_learnings, active_api_key
                    )
                    st.session_state.last_response = response_text
                    st.session_state.last_awal = lokasi_awal
                    st.session_state.last_tujuan = lokasi_tujuan
                    
                    log_search_to_db(f"{lokasi_awal} -> {lokasi_tujuan}", "SUCCESS")
                except Exception as e:
                    log_search_to_db(f"{lokasi_awal} -> {lokasi_tujuan}", "FAILED")
                    st.error(f"Waduh ada error pas koneksi ke Gemini API: {e}")
        
        else:
            st.warning("Pilih dulu dong posisi dan destinasinya.")


if st.session_state.search_clicked and st.session_state.last_response:
    st.success("😎 YEAYY! Mantap! Begini respons Gemini buat kamu:")
    st.markdown(st.session_state.last_response)
    st.markdown("---")

st.caption("**Catatan:** Mohon menunggu loading beberapa saat hingga selesai")
st.markdown("> _Informasi Tambahan: Aplikasi ini terintegrasi langsung dengan Gemini API._")
