Bab 5. Proyek Akhir: Kalkulator Hub
Proyek ini menggabungkan seluruh materi menjadi aplikasi web multi-halaman dengan tampilan profesional (Flask, HTML, dan CSS). Berkas proyek dibagikan terpisah dalam folder kalkulator-hub.
Halaman	Operator yang dilatih	Fitur
Kalkulator	+ - * / // % **	tujuh operator, validasi input, riwayat perhitungan
Cicilan	* / **	bunga flat dan anuitas, ringkasan biaya, jadwal angsuran
BMI	/ ** dan perbandingan berantai	indeks massa tubuh, kategori, rentang berat ideal
Struktur proyek:
kalkulator-hub/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── kalkulator.html
│   ├── cicilan.html
│   └── bmi.html
└── static/css/style.css
Cara menjalankan:
cd kalkulator-hub
pip install -r requirements.txt
python app.py
Lalu buka http://127.0.0.1:5000.
Poin pembelajaran dari proyek:
1.	Pewarisan template Jinja2 (base.html) agar tampilan seragam di semua halaman.
2.	Pemisahan logika (fungsi perhitungan di Python) dari tampilan (HTML dan CSS).
3.	Validasi dan penanganan kesalahan yang ramah pengguna.
4.	Desain antarmuka responsif dengan CSS Grid dan Flexbox.
Tugas pengembangan: tambahkan halaman Konversi Suhu (Celsius, Fahrenheit, Kelvin) lengkap dengan menu navigasi dan kartu di beranda.
