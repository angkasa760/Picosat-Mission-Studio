# 🛰️ PIN-UHF | ELITE MISSION STUDIO V1

![Mission Hero Banner](docs/banner.png)

**Author:** Mohammad Fadlurahman Saeran  
**College:** Telkom University  
**Major:** S1 Teknik Telekomunikasi  

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)
![Status](https://img.shields.io/badge/Status-Operational-brightgreen.svg)
![Telemetry](https://img.shields.io/badge/Telemetry-Real--Time-orange.svg)

**High-Fidelity Orbital Simulation + Real-Time Telemetry Tracking System**

Sistem simulasi dan pelacakan satelit picosatellite (UHF 437.2 MHz) berbasis Python & Three.js. Proyek ini menggabungkan mekanika orbital tingkat lanjut dengan optimasi RF berbasis AI.

**Developer:** angkasa760 | **Status:** 🟢 OPERATIONAL & READY FOR MISSION | **Version:** 1.0 (Stable)

---

## 🖼️ Technical Simulation Gallery

Lihat hasil analisis mendalam dari mesin simulasi ELITE kami:

| **Link Budget Analysis** | **Orbital Thermal Analysis** |
|:---:|:---:|
| ![Link Budget](plots/academic_link_budget.png) | ![Thermal](plots/academic_thermal_analysis.png) |
| *Analisis margin sinyal LEO ke Jakarta* | *Simulasi pergeseran resonansi akibat suhu* |

| **AI Antenna Optimizer** | **RF Propagation Pattern** |
|:---:|:---:|
| ![AI Plot](plots/ai_antenna_optimizer.png) | ![RF GIF](plots/rf_propagation.gif) |
| *Optimasi S11 menggunakan Neural Network* | *Visualisasi radiasi medan UHF* |

---

## 📚 Research Methodology & Physics

Proyek ini menggunakan model matematika tingkat lanjut untuk menjamin akurasi data misi:

### 1. Link Budget Engineering
Menggunakan persamaan **Free Space Path Loss (FSPL)** yang dimodifikasi dengan kerugian atmosfer menurut standar **ITU-R**:
$$L_{FSPL} = 20 \log_{10}(d) + 20 \log_{10}(f) - 147.55$$
*Dimana $d$ adalah slant range real-time dan $f$ adalah frekuensi operasional 437.2 MHz.*

### 2. Thermal Resonance Modeling
Mekanisme pergeseran frekuensi antena akibat pemuaian termal dihitung menggunakan model **2-Node Lumped Parameter**:
- **Internal Node**: Panas dari batere & CPU picosat.
- **External Node**: Paparan radiasi matahari (Solar Irradiance).

### 3. AI-Powered S11 Optimization
Menggunakan **MLP Regressor (Multi-Layer Perceptron)** untuk memprediksi panjang lengan antena yang optimal demi mencapai VSWR < 1.5 secara dinamis berdasarkan dataset simulasi CST Microwave Studio.

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
