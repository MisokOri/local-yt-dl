# 🎬 Local YouTube to MP3/MP4 Converter

Aplikasi berbasis web lokal sederhana yang dibangun menggunakan **Python** dan **Flask** untuk mengunduh dan mengonversi video YouTube menjadi format **MP3** (audio) maupun **MP4** (video) dengan berbagai pilihan kualitas yang tersedia.

---

## ✨ Fitur Utama

- **Konversi Multi-Format:** Mengubah video YouTube menjadi file **MP3** atau **MP4** sesuai dengan resolusi/kualitas yang tersedia di sumber video.
- **Dukungan Playlist & Mix:** Mendukung pengunduhan satu video tunggal maupun banyak video sekaligus dalam format _Playlist_ atau _YouTube Mix_.
- **Antarmuka Lokal:** Berjalan langsung di browser melalui server lokal (`localhost`) tanpa perlu mengunggah data ke pihak ketiga.

---

## 🛠️ Spesifikasi & Prasyarat Sistem

Aplikasi ini dikembangkan dan diuji menggunakan lingkungan berikut:

- **Python:** `3.13.14`
- **Framework & Library Utama (`requirements.txt`):**
  - `Flask==3.1.3`
  - `Werkzeug==3.1.9`
  - `Jinja2==3.1.6`
  - `click==8.5.1`
  - `itsdangerous==2.2.0`
  - `MarkupSafe==3.0.4`
  - `blinker==1.9.0`

_(Catatan: Pastikan Anda juga telah memasang `yt-dlp` dan `FFmpeg` di sistem/environment Anda jika aplikasi menggunakannya di balik layar untuk proses ekstraksi dan konversi media)._

---

## 🚀 Cara Instalasi & Menjalankan Aplikasi

1. **Clone repositori ini:**

   ```bash
   git clone https://github.com/username-anda/nama-repo-anda.git
   cd nama-repo-anda
   ```

2. **Buat dan aktifkan Virtual Environment (Opsional namun disarankan):**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instal seluruh dependensi:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan aplikasi:**

   ```bash
   python app.py
   ```

   _(Sesuaikan `app.py` dengan nama file utama aplikasi Anda)._

5. **Buka di Browser:**
   Akses alamat lokal yang muncul di terminal (biasanya `http://127.0.0.1:5000`).

---

## ⚠️ Catatan & Batasan Penggunaan

Harap perhatikan beberapa hal berikut sebelum menggunakan aplikasi ini:

- **Privasi Video:** Aplikasi hanya dapat mengunduh video yang bersifat **Publik** atau **Tidak Publik (_Unlisted_)**. Video yang berstatus **Privat (_Private_)** tidak dapat diproses.
- **Durasi Video:** **Tidak direkomendasikan** untuk mengunduh atau mengonversi video dengan durasi yang terlalu panjang (misalnya siaran langsung berjam-jam atau kompilasi berdurasi sangat lama) karena dapat memakan memori berlebih atau menyebabkan _timeout_.
- **Performa:** Kecepatan proses pengunduhan (_downloading_) dan konversi (_converting_) sangat bergantung pada **kecepatan koneksi internet** serta **spesifikasi perangkat keras (CPU/RAM)** komputer masing-masing.

---

## 📄 Lisensi & Penafian (_Disclaimer_)

Proyek ini dibuat untuk tujuan edukasi dan penggunaan pribadi. Harap hormati hak cipta kreator dan patuhi Ketentuan Layanan (Terms of Service) YouTube saat menggunakan aplikasi ini.
