# Portofolio Flask

Aplikasi web portofolio dengan alur: **splash screen, beranda, login, lalu halaman portofolio** yang animatif.
Dibuat dengan Python + Flask, HTML, CSS, dan JavaScript murni (tanpa framework CSS atau JS).

## Menjalankan

```bash
python -m venv venv
# Windows (CMD): venv\Scripts\activate    |   Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Buka http://127.0.0.1:5000

Akun demo: **username** `mahasiswa`, **password** `praktikum123`

Pengujian otomatis: `python uji.py`

## Alur halaman

| URL | Metode | Fungsi | Perlu login |
|---|---|---|---|
| `/` | GET | splash screen, otomatis menuju beranda | tidak |
| `/beranda` | GET | halaman sambutan dengan tombol Masuk | tidak |
| `/login` | GET, POST | formulir masuk dan verifikasi akun | tidak |
| `/portofolio` | GET | portofolio lengkap | ya |
| `/logout` | POST | keluar (hanya metode POST bertoken CSRF) | tidak |

Alamat lain menampilkan halaman 404 bertema.

## Mengganti data dengan milik Anda

1. Ubah isi `PROFIL` di `data.py` (nama, peran, skill, proyek, pengalaman, kontak).
2. Ubah warna di `static/css/base.css` pada blok `:root` (`--biru`, `--jingga`, `--tinta`).
3. Ubah kecepatan splash lewat konstanta `DURASI` di `static/js/splash.js`.
4. Ubah akun di `USERS` pada `app.py`.
5. Untuk penggunaan nyata, isi variabel lingkungan `SECRET_KEY` dengan teks acak yang panjang,
   pasang HTTPS, lalu set `COOKIE_SECURE=1`. Jangan menjalankan `debug=True` di server publik.

## Struktur

```
app.py                 route, login, session, proteksi halaman
data.py                data profil (satu-satunya tempat mengedit isi)
uji.py                 pengujian otomatis dengan test_client
templates/             base.html, _flash.html, splash, beranda, login, portofolio, 404
static/css/            base.css, splash.css, publik.css, portofolio.css
static/js/             splash.js, ketik.js, login.js, portofolio.js
```
