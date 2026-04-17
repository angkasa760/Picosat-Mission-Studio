# 🛰️ PIN-UHF | ELITE MISSION STUDIO V1

![Mission Hero Banner](docs/banner.png)

**Author:** Mohammad Fadlurahman Saeran  
**College:** Telkom University  
**Major:** S1 Teknik Telekomunikasi  

---

**High-Fidelity Orbital Simulation + Real-Time Telemetry Tracking System**

Sistem simulasi dan pelacakan satelit picosatellite (UHF 437.2 MHz) berbasis Python & Three.js. Proyek ini menggabungkan mekanika orbital tingkat lanjut dengan optimasi RF berbasis AI.

**Developer:** angkasa760 | **Status:** 🟢 OPERATIONAL & READY FOR MISSION | **Version:** 1.0 (Stable)

---

## 📋 Daftar Isi
1. [Informasi Dokumen](#informasi-dokumen)
2. [Arsitektur Sistem](#arsitektur-sistem)
3. [Fitur Utama](#fitur-utama)
4. [Cara Menjalankan Sistem](#cara-menjalankan-sistem)
5. [Analisis Teknis](#analisis-teknis)

---

## 📄 Informasi Dokumen
Sistem ini dirancang untuk mendukung operasional Ground Station picosatellite dengan akurasi tinggi. Menggunakan TLE riil dari Celestrak, model atmosfer ITU-R, dan visualisasi 3D real-time yang tersinkronisasi.

## 🏗️ Arsitektur Sistem
- **Backend (Python 3.12)**: Mesin perhitungan fisika, tracker posisi, dan pass predictor.
- **Frontend (Three.js/Vanilla JS)**: Dashboard visualisasi 3D dan HUD operasional.
- **AI Core (Scikit-Learn)**: Model prediksi optimasi antena CST.
- **Deployment**: Mendukung integrasi KML ke Google Earth secara live.

## ✨ Fitur Utama
- 🛰️ **Live Satellite Tracking**: Pelacakan posisi koordinat (Lat/Lon/Alt) secara riil setiap 10 detik.
- 📡 **High-Fidelity Link Budget**: Perhitungan Link Margin dinamis dengan kerugian FSPL & Gas Atmosferik.
- 🧊 **3D Orbiter HUD**: Visualisasi lintasan satelit di ruang angkasa menggunakan Three.js.
- 🧠 **Antenna AI Optimizer**: Prediksi pergeseran resonansi berdasarkan panjang lengan antena.
- 🌡️ **Orbital Thermal Analysis**: Simulasi suhu internal/eksternal satelit selama siklus orbit LEO.
- 📊 **Mission Reliability**: Simulasi Monte Carlo untuk probabilitas keberhasilan misi.

## 🚀 Cara Menjalankan Sistem
### 1. Persiapan Lingkungan
Pastikan Python sudah terinstal, lalu pasang dependensi:
```bash
pip install -r requirements.txt
```

### 2. Menjalankan Mesin Utama (Engine)
Gunakan skrip otomatis untuk memulai pelacakan dan prediksi lintasan:
- Klik ganda file **`GAS_REKAMAN.bat`**

### 3. Memantau Ground Station
Untuk tampilan visual, buka dashboard di browser:
- Buka **`web/orbit.html`** (Visualisasi 3D)
- Buka **`web/index.html`** (Data Telemetri 2D)

### 4. Ground Control GUI
Untuk menjalankan aplikasi Windows khusus Mission Control:
```bash
python sim/ground_control.py
```

## 📈 Analisis Teknis
Dokumentasi hasil simulasi tersedia dalam bentuk plot grafis:
- **RF Propagation**: Analisis pancaran gelombang.
- **Vibration Analysis**: Simulasi ketahanan struktur saat peluncuran.
- **Thermal Scan**: Prediksi pergeseran frekuensi akibat suhu ekstrem.

---
*Maintained with ❤️ by angkasa760*
