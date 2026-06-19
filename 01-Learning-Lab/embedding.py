from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

# 1. Kita buat database denah tiruan berbentuk List
database_denah = [
    "The Artificial Intelligence laboratory is located on the second floor of building B",
    "The campus cafeteria sells various food and beverages",
    "The administration office for student affairs is on the first floor",
    "The main library with thousands of books is next to the rectorate building"
]

# 2. Simulasi input/dropdown dari user
pertanyaan_user = "where is the main library located?"

# 3. Encode pertanyaan user
emb_pertanyaan = model.encode(pertanyaan_user)

print("--- MEMULAI PENCARIAN RUTE ---")

# 4. Lakukan perulangan (looping) untuk mengecek semua data di database
for i, denah in enumerate(database_denah):
    emb_denah = model.encode(denah)
    skor_kemiripan = util.cos_sim(emb_pertanyaan, emb_denah).item()
    
    print(f"Opsi {i+1}: Skor = {skor_kemiripan:.4f} -> {denah}")