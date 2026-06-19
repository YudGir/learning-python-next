import pandas as pd

# cara paling umum: Baca file CSV
# df = pd.read_csv('nama_file.csv')

data = {
    'Nama' : ['Budi', 'Siti', 'Ayu', 'Siti', 'Edo', 'Candra', 'Badu', 'Dhayu', 'Ombe', 'Pasu'],
    'IPK'  : [   3.5,    3.7,   4.0,    3.7,   3.4,      3.6,    3.9,     3.8,    3.9,   3.5],
    'Jurusan' : ['IF',  'SI',  'TI',   'SI',  'TK',     'IF',   'TI',    'TK',    'SI',   'SI'],
    'Alamat' : ['Cirebon', 'Bandung', 'Yogyakarta', 'Bandung', 'Lampung', 'Cirebon', 'Yogyakarta', 'Lampung', 'Bandung', 'Bandung'],
    'UTS' : [10, 20, 30, 40, 50, 60, 70, 80, 90, 10],
    'UAS' : [90, 80, 70, 60, 50, 40, 30, 20, 10, 90]
}

df = pd.DataFrame(data) # 'DataFrame' utk mengubah isi dict jadi tabel
# print(df.head(1))       # df.head() -> ngambil nilai paling atas (defaultnya 5)
# print(df.info())        # df.info() -> liat "jeroan" tabel (tipe data, ada data kosong atau nggak)
# print(df.describe())    # df.describe() -> hitung rata-rata, nilai min, max, sampai standar deviasi

# print()
# print(df['IPK'])
# mahasiswa_IF = df[df['Jurusan'] == 'IF']
# print(mahasiswa_IF)

# df['Status'] = 'Tidak Aktif'  # utk menambahkan kolom baru di Pandas (secara keseluruhan)
# print(df)

# print()
# df.at[0, 'Status'] = 'Aktif'  # df.at[indeks ke ...., kolom mana ....] utk mengubah spesifik satu baris dengan indeks tertentu
# print(df)

# print()
# df.loc[0:1, 'Status'] = 'Aktif'  # .loc[start:end, kolom ...] utk mengubah banyak indeks spesifik sekaligus!
# print(df)                        # note: end di loc sifatnya 'inklusif', jadi indeks 1 pun diikutkan

# print()
# df.loc[df['Nama'] == 'Budi', 'Status'] = 'Reguler'  # AI ENGINEER SHOULD KNOW THIS (EFFICIENT)!
# df.loc[df['IPK'] > 3.5, 'Status'] = 'Unggulan'
# print(df)

# print()
# df_bersih = df.dropna()    # hapus semua baris yang ada data kosongnya
# print(df)

# df['IPK'] = df['IPK'].fillna(df['IPK'].mean())  # isi data yang kosong pake angka 0 atau rata-rata
# print(df)

# dF = df.drop('Alamat', axis = 1)  # hapus kolom 'Alamat'. axis=1 artinya kita mau hapus arah samping (kolom)
# print(dF)                         # note: axis = 1 utk KOLOM, axis = 0 utk BARIS
# print()

df = df.drop_duplicates()       # hapus data duplikat (harus SAMA PERSIS ya data di sana!)
# print(df)
# print()
# print(dF)

# print()
# pola_jurusan = df.groupby('Jurusan')['IPK'].mean()  # kelompokkan berdasarkan 'Jurusan', lalu ambil kolom 'IPK', terus cari mean-nya
# print(pola_jurusan)

# Pake inplace=True biar langsung ngerubah df tanpa perlu df = ... (langsung berubah permanen) (safer!)
# df.drop('Alamat', axis=1, inplace=True)
# print(df)

# print()
# DF = df.drop(3, axis = 0)
# print(DF)

# print()                 # subset -> cek duplikat HANYA utk kolom Nama
# df = df.drop_duplicates(subset =['Nama'], keep = 'first')  # AIE Way!
# print(df)                               # keep = first -> ambil yg PERTAMA KALI saja, sisanya buang

# print()
# INGET, KALO MENGHAPUS DATA, INDEKS ARRAY PASTI BERUBAH.
# KITA PERLU RESET LAGI PENG-INDEKS-ANNYA
df = df.reset_index(drop = True)  # drop = True -> indeks lama dibuang
# print(df)                         # reset_index -> mengganti indeks yg terbuang

# print()
# mabaIFKeren = df[(df['Jurusan'] == 'IF') & (df['IPK'] >= 3.5)]  # AIE Way!
# print(mabaIFKeren)

# print()
# df_baru = df.sort_values(by='IPK', ascending = False)  # .sort_values -> utk mengurutkan berdasarkan KONDISI
# print(df_baru)

# print()
# mahasiswa_Cirebon = df[df['Alamat'] == 'Cirebon']
# print(mahasiswa_Cirebon)

# print()
# urutMahasiswaCirebon = mahasiswa_Cirebon.sort_values(by='Nama', ascending = True)
# print(urutMahasiswaCirebon)

# print()
# urut = df[df['IPK'] < 3.5].sort_values(by='IPK', ascending = True)  # AIE Way!
# print(urut)                                    # ascending True itu default

# print()
# jumlah_per_jurusan = df['Jurusan'].value_counts()  # .value_counts() -> utk menghitung
# print(jumlah_per_jurusan)                          # banyak data 

# print()
# hasil = df.sort_values(by='IPK', ascending = False)['Nama'].iloc[0]     # .iloc[..] -> langsung ambil urutan ke ...
# print(f"Mahasiswa dengan IPK tertinggi: {hasil}")                       # .loc -> ambil berdasarkan labelnya (lihat di atas)

# print()
df['Nilai Akhir'] = (df['UTS'] + df['UAS']) / 2
# print(df)

# print()
def cek_prestasi(ipk):
    if ipk >= 3.5:
        return "Sangat Memuaskan"
    else: 
        return "Memuaskan"

df['Keterangan'] = df['IPK'].apply(cek_prestasi)
# print(df[['Nama', 'IPK', 'Keterangan']])


# daftar_jurusan = df['Jurusan'].unique()     # .unique -> daftar jurusan unik apa aja
# banyak_jurusan = df['Jurusan'].nunique()    # .nunique -> jumlah daftar jurusan unik

# print()
# print(daftar_jurusan)
# print(banyak_jurusan)

def pulau(alamat):
    daftar_kota = ['Cirebon', 'Bandung', 'Depok', 'Yogyakarta']
    if alamat in daftar_kota:
        return 'Jawa'
    else:
        return 'Luar Jawa'

df['Pulau'] = df['Alamat'].apply(pulau)
# print(df)

# print()
# rata_ipk_perPulau = df.groupby('Pulau')['IPK'].mean()
# print(rata_ipk_perPulau)

# print()
# # Soal 1: Filter & Modification
# df.loc[df['Jurusan'] == 'IF', 'IPK'] += 0.1 
# print(df)

# print()
# Soal 2: Multiple Conditions (The Elite Club)
# HASIL = df[(df['IPK'] > 3.6) & ((df['Alamat'] == 'Bandung') | (df['Alamat'] == 'Cirebon'))]
# print(HASIL)

# print()
# Cara "Pro" biar nggak pusing sama kurung:
# kota_pilihan = ['Bandung', 'Cirebon']
# HASIL = df[(df['IPK'] > 3.6) & (df['Alamat'].isin(kota_pilihan))]
# print(HASIL)

# print()
# # Soal 3: String Manipulation (The Searcher)
# Hasil = df[df['Nama'].str.startswith('A')]
# print(Hasil)

# Soal 4: Logika "Invert" (Kebalikan)
# print()
# kirim_email_ke = df[~(df['Jurusan'] == 'TK')]['Nama'] # or (df['Jurusan'] != 'TK') this works as well
# print(kirim_email_ke)

# Soal 5: Mencari Nilai Spesifik 
# print()
# ipktertinggiSI = df[df['Jurusan'] == 'SI'].sort_values(by='IPK', ascending = False)['Nama'].iloc[0]
# print(ipktertinggiSI)

# Soal 6: Deteksi Nama (String Contains)
# print()
# deteksiNama = df[df['Nama'].str.contains('ayu', case = False)]   # case = False -> mau itu 'Ayu' atau 'ayu', ambil aja
# print(deteksiNama)

# print()
# df_rapi = df.sort_values(by=['Jurusan', 'IPK'], ascending=[True, False])
# print(df_rapi)

# print()
df_siap_ai = pd.get_dummies(df, columns=['Jurusan'])
# print(df_siap_ai)

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

X = df_siap_ai.drop(['Nama', 'Alamat', 'Keterangan', 'Pulau',
                     'Jurusan_IF', 'Jurusan_SI', 'Jurusan_TI', 'Jurusan_TK'], axis = 1)
y = df_siap_ai['Jurusan_IF']
                                             # CATATAN: Data tabel gak boleh di-sort, biar AI-nya gak cuma hafal mati!
print(X)
print()
print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  
                                            # X_train -> data yg dipake buat data latihan                           (ibarat: soal tugas/latihan)
                                            # y_train -> jawaban data untuk data latihan di X_train                 (ibarat: jawaban dari soal tugas/latihan)
                                            # X_test -> banyak data yg dipake buat data test                        (ibarat: soal ujian)
                                            # y_test -> jawaban data yg seharusnya untuk data test dari X_test      (ibarat: jawaban soal ujian)

print(f"\nData latihan (X-train): {X_train.shape}")      # .shape -> utk melihat ukuran matriks    (sintaksnya: (baris, kolom))
print(f"Data ujian (x-test): {X_test.shape}")            # .reshape -> utk mengubah ukuran matriks   (sintaksnya sama kayak .shape)

model = KNeighborsClassifier(n_neighbors=3)             # inisialisasi model buatan menggunakan model AI KNN

model.fit(X_train, y_train)                             # .fit -> momen AI belajar dari data latihan kita (tugas harian)

y_pred = model.predict(X_test)                          # .predict -> momen AI 'predict' dari data tes kita (soal ujian)

print(f"\nHasil tebakan AI kamu yud: {y_pred}")
print(f"\nJawaban aslinya (harusnya) yud: {y_test.values}")
print(f"\nAkurasi model AI pertama kamu ini yud: {accuracy_score(y_test, y_pred) * 100}%")