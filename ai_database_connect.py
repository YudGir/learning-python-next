import pandas as pd
from sqlalchemy import create_engine
from sklearn.neighbors import KNeighborsClassifier

# --- STEP 1: KONEKSI KE GUDANG (POSTGRESQL) ---
# Format: postgresql://user:password@host:port/database
# Ganti 'password_kamu' sesuai password yang kamu buat di Postgre tadi!
engine = create_engine('postgresql://postgres:admin123@localhost:5432/YUDHA_AI_MODEL')

# --- STEP 2: SEDOT DATA PAKE SQL ---
query = "SELECT * FROM Mahasiswa WHERE ipk > 3.6"
df = pd.read_sql(query, engine)

print("✅ Data dari Postgre berhasil ditarik!")
print(df.head())     # ngambil 5 teratas (secara default)

# --- STEP 3: PREPARASI AI (LOGIKA KITA TADI) ---
# Kita pake IPK, UTS, dan UAS buat fitur (X)
X = df[['ipk', 'uts', 'uas']]
y = df['jurusan'] # Targetnya mau nebak jurusan

# Panggil si KNN
knn = KNeighborsClassifier(n_neighbors=3)

# --- STEP 4: TRAINING ---
knn.fit(X, y) # AI belajar dari data yang barusan ditarik dari DB
print("\n✅ AI sudah selesai belajar dari data PostgreSQL!")

# --- STEP 5: PREDIKSI DATA BARU ---
# Misal ada mahasiswa baru: IPK 3.8, UTS 75, UAS 85. Dia jurusan apa?
# Masukin ke DataFrame biar ada nama kolomnya
data_baru = pd.DataFrame([[3.8, 75, 85]], columns=['ipk', 'uts', 'uas'])
prediksi = knn.predict(data_baru)


print(f"\nHasil Prediksi Mahasiswa Baru: Jurusan {prediksi[0]}")
