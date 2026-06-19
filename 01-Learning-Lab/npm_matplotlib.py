import matplotlib.pyplot as plt
import numpy as np

# hari = [1, 2, 3, 4, 5]
# skill = [10, 20, 30, 40, 50]

# 1: plt.plot(sumbu_x, sumbu_y) - graph of showing straight line
# plt.title("Proggress of Learning AI")
# plt.xlabel("Day")
# plt.ylabel("Level of Skill")
# plt.plot(hari, skill)
# plt.grid(True)
# plt.show() # tampilkan

# 2: plt.bar (to compare its category), like diagram 'batang'
# kategori = ['Python', 'C++', 'PostgreSQL']
# skor = [90, 80, 75]

# plt.bar(kategori, skor, color='skyblue')
# plt.xlabel("Skill")
# plt.ylabel("Score")
# plt.show()

# 3: .scatter (most important for AIE), shows the coordinates through dots (if you'd like to see the correlation between variables)
# jam_belajar = [1, 2, 3, 4, 5, 6]
# nilai = [50, 55, 70, 75, 88, 95]

# plt.scatter(jam_belajar, nilai, color='red')
# plt.xlabel("Hour of Learning")
# plt.ylabel("Exam Grade")
# plt.show()

# 4: .hist (its form like .bar, but having another purpose -> to see in what range which found most)
# data_umur = [20, 22, 22, 25, 30, 35, 35, 35, 40]
# plt.hist(data_umur, bins=50)
# plt.show()

# 5: .pie (like its a circle form for many pieces to see the percentage or proportional of 100%)
# label = ['Deep Learning', 'Machine Learning', 'Data Science']
# porsi = [40, 35, 25]

# plt.pie(porsi, labels=label, autopct='%1.1f%%')
# plt.show()


# LEGEND: to give its label on visualization and to compare between two categorials data
# x = np.arange(5) #to create 0 to 4 (for 5 times)
# model_lama = [10, 20, 25, 30, 42]
# model_baru = [5, 15, 20, 35, 50]
# model_dikembangkan = [15, 20, 15, 40, 55]
# model_kuno = [5, 10, 15, 20, 25]

# plt.plot(x, model_lama, label='Model Lama', color='red')
# plt.plot(x, model_baru, label='Model Baru', color='green')

# plt.legend()  # GIVING THE LABEL TO SEE MORE CLEAR ON
# plt.show()


# plt.subplot(baris, kolom, nomor_gambar) - if wanna see two visualizations in a row
                # 1 -> first, in the left side
# plt.subplot(2, 3, 1)
# plt.plot(model_lama)
# plt.title("Accuracy of Old Model")

# plt.subplot(2, 3, 2)
# plt.plot(model_dikembangkan)
# plt.title("Accuracy of Growing Model")

# plt.subplot(2, 3, 3)
# plt.plot(model_baru)
# plt.title("Accuracy of New Model")

# plt.subplot(2, 3, 4)
# plt.plot(model_kuno)
# plt.title("Accuracy of Ancient Model")

# plt.tight_layout()
# plt.show()

# x = np.linspace(0, 10, 100)   # creating 100 numbers that starts from 0, ends with 10.
# y1 = np.sin(x)
# y2 = np.cos(x)

# plt.figure(figsize=(10,4))   # manage the size of paper (figure)
# plt.subplot(1, 2, 1)
# plt.plot(x, y1, color='purple')
# plt.title("Signal A")

# plt.subplot(1, 2, 2)
# plt.plot(x, y2, color='yellow')
# plt.title("Signal B")

# plt.tight_layout()
# plt.show()

# jam_di_aplikasi = np.random.rand(50) * 10   # Sumbu X
# total_belanja = np.random.rand(50) * 500    # Sumbu Y

# warna = np.random.rand(50)
# ukuran = np.random.rand(50) * 1000

# plt.scatter(jam_di_aplikasi, total_belanja,
#             c=warna,
#             s=ukuran,
#             alpha=0.5,
#             cmap='viridis')

# plt.colorbar(label='Tingkat Loyalitas')
# plt.xlabel('Jam di aplikasi')
# plt.ylabel('Total belanja (ribu)')
# plt.title('Analisis Pelanggan')

# plt.show()

usia_mobil = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
harga_mobil = [500, 450, 400, 320, 300, 250, 200, 180, 150, 120]

plt.scatter(usia_mobil, harga_mobil, label= 'Real Data', color='red')
plt.plot(usia_mobil, harga_mobil, label= 'Prediction Data', color='blue')

plt.xlabel('Age of Car (Year)')
plt.ylabel('Price of Car (Juta)')
plt.grid(True)
plt.legend()
plt.show()