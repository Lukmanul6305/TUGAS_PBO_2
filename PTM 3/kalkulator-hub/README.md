# Kalkulator Hub

Aplikasi web multi-halaman untuk mempraktikkan operator Python menggunakan Flask, Jinja2, HTML, dan CSS.

## Fitur

- **Kalkulator:** operator `+`, `-`, `*`, `/`, `//`, `%`, dan `**`, validasi input, serta riwayat 10 perhitungan terakhir.
- **Cicilan:** simulasi bunga flat dan anuitas, ringkasan pokok/bunga/total pembayaran, dan jadwal angsuran bulanan.
- **BMI:** menghitung indeks massa tubuh, kategori, dan rentang berat untuk BMI 18,5 sampai 24,9.
- **Konversi suhu:** konversi Celsius, Fahrenheit, dan Kelvin dengan validasi nol mutlak.
- **Navigasi bersama:** semua halaman memakai template dasar dan kartu fitur tersedia di beranda.

## Menjalankan aplikasi

```powershell
cd kalkulator-hub
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Buka `http://127.0.0.1:5000` di browser.

## Rute

- `/` - beranda
- `/kalkulator` - operasi hitung dan riwayat
- `/cicilan` - simulasi cicilan
- `/bmi` - kalkulator BMI
- `/suhu` - konversi suhu

Nilai pinjaman pada simulasi cicilan dimasukkan dalam rupiah bulat, tenor dalam bulan, dan bunga sebagai persentase tahunan. Rumus anuitas menggunakan bunga bulanan dan pembayaran akhir disesuaikan agar saldo pinjaman menjadi nol.
