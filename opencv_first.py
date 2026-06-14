import cv2

# 1. Panggil Otak AI Detektor Wajah bawaan OpenCV (Haar Cascade)
otak_ai_wajah = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 2. Nyalakan kamera laptop
kamera = cv2.VideoCapture(0)

print("AI Scan Wajah Aktif! Dekatkan wajahmu ke kamera. Tekan 'q' untuk keluar.")

while True:
    ret, frame = kamera.read()
    if not ret:
        break
        
    # AI membutuhkan gambar hitam-putih agar proses deteksi angkanya lebih cepat
    frame_abu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 3. SURUH AI MENCARI KOORDINAT WAJAH KAMU!
    # scaleFactor dan minNeighbors itu setingan sensitivitas AI-nya
    daftar_wajah = otak_ai_wajah.detectMultiScale(frame_abu, scaleFactor=1.3, minNeighbors=5)
    
    # 4. Jika AI menemukan wajah, dia akan memberikan koordinat (X, Y, Lebar, Tinggi)
    for (x, y, lebar, tinggi) in daftar_wajah:
        
        # Gambar kotak hijau tepat di koordinat wajah yang dikasih sama AI!
        titik_atas_kiri = (x, y)
        titik_bawah_kanan = (x + lebar, y + tinggi)
        warna_hijau = (0, 255, 0)
        tebal_garis = 2
        
        cv2.rectangle(frame, titik_atas_kiri, titik_bawah_kanan, warna_hijau, tebal_garis)
        
        # Tambahan efek fiksi ilmiah: Kasih teks "USER DETECTED" di atas kotaknya!
        cv2.putText(frame, 'USER DETECTED', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, warna_hijau, 2)
        
    # Tampilkan hasilnya secara live!
    cv2.imshow('Real-Time AI Face Scanner', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

kamera.release()
cv2.destroyAllWindows()
