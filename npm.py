import numpy as np

# data = [100,80,60,50,30]
# arr = np.array(data)
# print(f"ini array numpy: {arr}")

# A = np.array([[1, 2], [3, 4]])
# B = np.array([[5, 6], [7, 8]])

# hasil_dot = np.dot(A, B)
# print("Matriks A: ")
# print(A)
# print("\nMatriks B: ")
# print(B)
# print("\nHasil Dot:")
# print(hasil_dot)

#sintaks arange (START, STOP, STEP)
# arange itu membuat angka sesuai parameter
arange = np.arange(1,11) 
print(arange)

bikin = np.arange(2, 11, 2)
print(bikin)
print()

#sintaksnya : (baris, kolom)
kosong = np.zeros((2,2))
print("Matriks Nol (2 x 2)")
print(kosong)

satu = np.ones((2,2))
print("\nMatriks Tak Nol (2 x 2)")
print(satu)

# linspace = np.linspace(0, 100, 1000) #linspace (dari ..., ke ..., bagi dengan ...)
# print("\nHasil Linspace")
# print(linspace)

data_ganjil = np.arange(1, 16, 2)
print("\nIni brok data ganjil dari 1-15 pake numpy array:")
print(data_ganjil)

matriks_tak_nol = np.ones((2,2))
print("\nIni brok matriks order 2x2 yg isinya tak nol: ")
print(matriks_tak_nol)

matriks_baru = np.arange(1,17).reshape(4,4)
print("\nIni matriks 4x4:")
print(matriks_baru)

slicing_tengahAtas = matriks_baru[1, 1:3]
slicing_tengahBawah = matriks_baru[2, 1:3]
kotak_tengah = matriks_baru[1:3, 1:3]
print("\nHasil Slicing (utk 6 & 7 - 10 & 11): ")
# print(slicing_tengahAtas)
# print(slicing_tengahBawah)
print(kotak_tengah)