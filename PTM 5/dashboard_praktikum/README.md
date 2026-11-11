# Dashboard Aktivitas Praktikum

Contoh aplikasi Flask dengan tiga grafik Matplotlib. Seluruh data adalah **simulasi**.

## Menjalankan di Windows

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Jika PowerShell menolak aktivasi, gunakan Command Prompt dan jalankan `.venv\Scripts\activate.bat`.
Buka `http://127.0.0.1:5000` di browser.

## Menjalankan di macOS atau Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

`debug=True` dalam `app.py` hanya untuk praktikum lokal. Ubah daftar `DATA` di `app.py` untuk latihan. Pastikan `hadir` lebih dari nol dan `0 <= tuntas <= hadir`.
