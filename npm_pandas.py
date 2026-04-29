import pandas as pd

# cara paling umum: Baca file CSV
# df = pd.read_csv('nama_file.csv')

data = {
    'Nama' : ['Budi', 'Siti', 'Ayu', 'Siti', 'Edo', 'Candra', 'Badu', 'Dhayu'],
    'IPK'  : [   3.5,    3.7,   4.0,    3.7,   3.4,      3.6,    3.9,     3.3],
    'Jurusan' : ['IF',  'SI',  'TI',   'SI',  'TK',     'IF',   'TI',    'TK'],
    'Alamat' : ['Cirebon', 'Bandung', 'Yogyakarta', 'Bandung', 'Depok', 'Cirebon', 'Yogyakarta', 'Depok']
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
# df.loc[0:1, 'Status'] = 'Aktif'  # df.loc[start:end, kolom ...] utk mengubah banyak indeks spesifik sekaligus!
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

# dF = df.drop_duplicates()       # hapus data duplikat (harus SAMA PERSIS ya data di sana!)
# print(df)
# print()
# print(dF)

# print()
# pola_jurusan = df.groupby('Jurusan')['IPK'].mean()  # kelompokkan berdasarkan 'Jurusan', lalu ambil kolom 'IPK', terus cari mean-nya
# print(pola_jurusan)

# Pake inplace=True biar langsung ngerubah df tanpa perlu df = ... (langsung berubah permanen) (safer!)
df.drop('Alamat', axis=1, inplace=True)
print(df)

# print()
# DF = df.drop(3, axis = 0)
# print(DF)

print()                 # subset -> cek duplikat HANYA utk kolom Nama
df = df.drop_duplicates(subset =['Nama'], keep = 'first')  # AIE Way!
print(df)                               # keep -> ambil yg PERTAMA KALI saja, sisanya buang

print()
# INGET, KALO MENGHAPUS DATA, INDEKS ARRAY PASTI BERUBAH.
# KITA PERLU RESET LAGI PEN-INDEKS-ANNYA
df = df.reset_index(drop = True)  # drop = True -> indeks lama dibuang
print(df)                         # reset_index -> mengganti indeks yg terbuang