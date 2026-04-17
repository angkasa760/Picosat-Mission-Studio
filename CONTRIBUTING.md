# Contributing to Picosat-Mission-Studio

Terima kasih telah tertarik untuk berkontribusi pada sistem *Picosatellite Mission Studio*! 🛰️
Proyek ini dipelopori oleh **Mohammad Fadlurahman Saeran (Telkom University)** untuk simulasi orbit tinggi dan analisis RF.

## Standar Kode (Elite Code Standards)
1. **Fisika Terutama**: Jika Anda memperbarui algoritma orbit (Skyfield) atau RF, pastikan menyertakan metrik pengujian (misal VSWR, Link Margin).
2. **Bahasa**: Gunakan bahasa Inggris/Indonesia yang profesional dalam *commit message*.
3. **Pemisahan Modul**: Modul RF (`sim/`) tidak boleh bercampur dengan kode Web Dashboard (`web/`).

## Cara Mengirim Pull Request (PR)
1. Fork repositori ini
2. Buat branch fitur (`git checkout -b feature/SatelitBaru`)
3. Commit perubahan (`git commit -m "Add new X-Band frequency analysis"`)
4. Push ke branch (`git push origin feature/SatelitBaru`)
5. Buka Pull Request dan isi formulir yang disediakan.

*Ad astra per aspera!*
