
"""Percabangan Hub: proyek akhir praktikum percabangan if-else (Python + Flask)."""
import math

# pyrefly: ignore[missing-import]
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'ganti-kunci-ini-saat-deploy'  # dibutuhkan Flask untuk session (riwayat)

TARIF_PPN = 0.11
TIER_DISKON = [
    (500_000, 0.15, 'Tier Platinum (>= Rp 500.000)'),
    (250_000, 0.10, 'Tier Gold (>= Rp 250.000)'),
    (100_000, 0.05, 'Tier Silver (>= Rp 100.000)'),
    (0, 0.00, 'Reguler (< Rp 100.000)'),
]


# ---------------------------------------------------------------- fungsi bantu
def format_id(nilai, desimal=0):
    """Format angka gaya Indonesia: titik untuk ribuan, koma untuk desimal."""
    teks = f'{nilai:,.{desimal}f}'
    return teks.replace(',', '#').replace('.', ',').replace('#', '.')


def ke_angka(teks):
    """Ubah teks input menjadi float. Koma desimal gaya Indonesia diterima."""
    try:
        angka = float(teks.strip().replace(',', '.'))
    except ValueError:
        raise ValueError('Masukkan angka yang valid.') from None
    if not math.isfinite(angka):
        raise ValueError('Masukkan angka yang valid.')
    return angka


def catat_riwayat(teks):
    riwayat = session.get('riwayat_akademik', [])
    session['riwayat_akademik'] = ([teks] + riwayat)[:8]  # simpan 8 evaluasi terakhir


@app.template_filter('rupiah')
def rupiah(nilai):
    return 'Rp ' + format_id(nilai, 0)


@app.template_filter('angka')
def angka(nilai, desimal=0):
    return format_id(nilai, desimal)


# --------------------------------------------------------- fungsi percabangan
def konversi_grade(nilai_akhir):
    """Konversi nilai numerik (0-100) ke huruf mutu dan predikat dengan if-elif-else."""
    if nilai_akhir >= 85:
        return 'A', 'Sangat Baik', 'normal'
    elif nilai_akhir >= 70:
        return 'B', 'Baik', 'normal'
    elif nilai_akhir >= 55:
        return 'C', 'Cukup', 'lebih'
    elif nilai_akhir >= 40:
        return 'D', 'Kurang', 'obesitas'
    else:
        return 'E', 'Sangat Kurang', 'obesitas'


def evaluasi_akademik(tugas, uts, uas, kehadiran):
    """Evaluasi nilai akhir dan diagnosis kelulusan dengan nested if."""
    akhir = tugas * 0.30 + uts * 0.30 + uas * 0.40
    grade, predikat, nada_grade = konversi_grade(akhir)

    # Percabangan bersarang (nested if) untuk menentukan kelulusan & alasan spesifik
    if kehadiran < 75:
        lulus = False
        alasan = 'Kehadiran di bawah batas minimum 75%.'
    else:
        if akhir >= 55:
            if uas >= 40:
                lulus = True
                alasan = 'Memenuhi seluruh syarat nilai akhir, UAS, dan kehadiran.'
            else:
                lulus = False
                alasan = 'Nilai akhir cukup, tetapi nilai UAS di bawah 40.'
        else:
            lulus = False
            alasan = 'Nilai akhir belum mencapai batas kelulusan 55.'

    # Ekspresi kondisional (ternary)
    status = 'LULUS' if lulus else 'TIDAK LULUS'
    nada = 'normal' if lulus else 'obesitas'

    return {
        'akhir': akhir,
        'akhir_teks': format_id(akhir, 2),
        'grade': grade,
        'predikat': predikat,
        'lulus': lulus,
        'status': status,
        'nada': nada if not lulus else nada_grade,
        'alasan': alasan,
    }


def hitung_kasir(harga, jumlah, status_member, bayar):
    """Hitung diskon bertingkat, bonus member, PPN 11%, dan kecukupan bayar."""
    subtotal = harga * jumlah

    # Percabangan if-elif-else untuk menentukan tier diskon utama
    if subtotal >= 500_000:
        persen_utama = 0.15
        nama_tier = 'Platinum (15%)'
    elif subtotal >= 250_000:
        persen_utama = 0.10
        nama_tier = 'Gold (10%)'
    elif subtotal >= 100_000:
        persen_utama = 0.05
        nama_tier = 'Silver (5%)'
    else:
        persen_utama = 0.0
        nama_tier = 'Reguler (0%)'

    # Percabangan tambahan untuk anggota (member)
    if status_member == 'member':
        persen_member = 0.05 if subtotal >= 50_000 else 0.02
    else:
        persen_member = 0.0

    diskon_utama = round(subtotal * persen_utama)
    diskon_member = round(subtotal * persen_member)
    total_diskon = diskon_utama + diskon_member
    dpp = subtotal - total_diskon
    ppn = round(dpp * TARIF_PPN)
    total_bayar = dpp + ppn
    selisih = bayar - total_bayar
    cukup = bayar >= total_bayar

    simulasi_tier = []
    for batas, persen, label in TIER_DISKON:
        potongan = round(subtotal * persen)
        simulasi_tier.append({
            'label': label,
            'batas': batas,
            'persen': int(persen * 100),
            'potongan': potongan,
            'aktif': persen == persen_utama,
        })

    return {
        'subtotal': subtotal,
        'nama_tier': nama_tier,
        'persen_utama': int(persen_utama * 100),
        'persen_member': int(persen_member * 100),
        'diskon_utama': diskon_utama,
        'diskon_member': diskon_member,
        'total_diskon': total_diskon,
        'dpp': dpp,
        'ppn': ppn,
        'total_bayar': total_bayar,
        'bayar': bayar,
        'selisih': abs(selisih),
        'cukup': cukup,
        'status_bayar': 'Transaksi Lunas' if cukup else 'Uang Bayar Kurang',
        'nada': 'normal' if cukup else 'obesitas',
        'simulasi_tier': simulasi_tier,
    }


def seleksi_beasiswa(ipk, penghasilan, semester, prestasi):
    """Seleksi kelayakan beasiswa menggunakan nested if dan kondisi majemuk."""
    syarat_semester = 2 <= semester <= 8
    syarat_ipk_dasar = ipk >= 3.00
    syarat_ekonomi = penghasilan <= 5_000_000
    punya_prestasi = prestasi in ('nasional', 'provinsi')

    # Hitung skor komposit (0-100) untuk visualisasi skala
    skor_ipk = (ipk / 4.0) * 60
    skor_ekonomi = 25 if penghasilan <= 3_000_000 else (15 if penghasilan <= 5_000_000 else 5)
    skor_prestasi = 15 if prestasi == 'nasional' else (10 if prestasi == 'provinsi' else 0)
    skor_total = min(round(skor_ipk + skor_ekonomi + skor_prestasi, 1), 100)

    if not syarat_semester:
        keputusan = 'Tidak Memenuhi Syarat'
        jalur = 'Di luar rentang semester aktif (2–8)'
        nominal = 0
        nada = 'obesitas'
    elif ipk < 3.00:
        keputusan = 'Belum Lolos Seleksi'
        jalur = 'IPK di bawah batas minimum 3,00'
        nominal = 0
        nada = 'obesitas'
    else:
        # Nested if ketika syarat dasar (semester & IPK >= 3.00) terpenuhi
        if ipk >= 3.75 and (syarat_ekonomi or punya_prestasi):
            keputusan = 'Beasiswa Penuh (Unggulan)'
            jalur = 'Jalur Prestasi & Akademik Unggul'
            nominal = 6_000_000
            nada = 'normal'
        elif ipk >= 3.50 and syarat_ekonomi:
            keputusan = 'Beasiswa Penuh (Afirmasi)'
            jalur = 'Jalur Afirmasi Ekonomi & Akademik'
            nominal = 5_000_000
            nada = 'normal'
        elif ipk >= 3.25 or (syarat_ipk_dasar and punya_prestasi):
            keputusan = 'Beasiswa Parsial'
            jalur = 'Bantuan UKT Semester'
            nominal = 3_000_000
            nada = 'kurang'
        elif syarat_ekonomi:
            keputusan = 'Prioritas Cadangan'
            jalur = 'Daftar Tunggu Bantuan Finansial'
            nominal = 1_500_000
            nada = 'lebih'
        else:
            keputusan = 'Belum Lolos Seleksi'
            jalur = 'Perlu peningkatan IPK atau capaian prestasi'
            nominal = 0
            nada = 'obesitas'

    daftar_syarat = [
        {'nama': 'Semester aktif antara 2 sampai 8', 'terpenuhi': syarat_semester},
        {'nama': 'IPK minimal 3,00', 'terpenuhi': syarat_ipk_dasar},
        {'nama': 'Penghasilan orang tua <= Rp 5.000.000', 'terpenuhi': syarat_ekonomi},
        {'nama': 'Memiliki prestasi tingkat provinsi/nasional', 'terpenuhi': punya_prestasi},
    ]

    return {
        'keputusan': keputusan,
        'jalur': jalur,
        'nominal': nominal,
        'nada': nada,
        'skor': format_id(skor_total, 1),
        'posisi': min(max(skor_total, 0), 100),
        'daftar_syarat': daftar_syarat,
    }


# --------------------------------------------------------------------- halaman
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/akademik', methods=['GET', 'POST'])
def akademik():
    form = {'tugas': '', 'uts': '', 'uas': '', 'kehadiran': '85'}
    hasil = error = None

    if request.method == 'POST':
        form = {kunci: request.form.get(kunci, awal) for kunci, awal in form.items()}
        try:
            tugas = ke_angka(form['tugas'])
            uts = ke_angka(form['uts'])
            uas = ke_angka(form['uas'])
            kehadiran = ke_angka(form['kehadiran'])

            if not (0 <= tugas <= 100 and 0 <= uts <= 100 and 0 <= uas <= 100):
                raise ValueError('Nilai tugas, UTS, dan UAS harus berada pada rentang 0 sampai 100.')
            if not 0 <= kehadiran <= 100:
                raise ValueError('Persentase kehadiran harus berada pada rentang 0 sampai 100.')

            hasil = evaluasi_akademik(tugas, uts, uas, kehadiran)
            catat_riwayat(
                f"Akhir {hasil['akhir_teks']} (Grade {hasil['grade']}) — {hasil['status']}"
            )
        except ValueError as e:
            error = str(e)

    return render_template(
        'akademik.html', form=form, hasil=hasil, error=error,
        riwayat=session.get('riwayat_akademik', []),
    )


@app.route('/riwayat/hapus', methods=['POST'])
def hapus_riwayat():
    session.pop('riwayat_akademik', None)
    return redirect(url_for('akademik'))


@app.route('/diskon', methods=['GET', 'POST'])
def diskon():
    form = {'harga': '125000', 'jumlah': '3', 'member': 'member', 'bayar': '400000'}
    hasil = error = None

    if request.method == 'POST':
        form = {kunci: request.form.get(kunci, awal) for kunci, awal in form.items()}
        try:
            harga = int(ke_angka(form['harga']))
            jumlah = int(ke_angka(form['jumlah']))
            bayar = int(ke_angka(form['bayar']))

            if harga <= 0:
                raise ValueError('Harga satuan harus lebih dari Rp 0.')
            if not 1 <= jumlah <= 10_000:
                raise ValueError('Jumlah barang harus di antara 1 sampai 10.000.')
            if bayar < 0:
                raise ValueError('Uang bayar tidak boleh bernilai negatif.')

            hasil = hitung_kasir(harga, jumlah, form['member'], bayar)
        except ValueError as e:
            error = str(e)

    return render_template('diskon.html', form=form, hasil=hasil, error=error)


@app.route('/beasiswa', methods=['GET', 'POST'])
def beasiswa():
    form = {'ipk': '', 'penghasilan': '', 'semester': '4', 'prestasi': 'tidak'}
    hasil = error = None

    if request.method == 'POST':
        form = {kunci: request.form.get(kunci, awal) for kunci, awal in form.items()}
        try:
            ipk = ke_angka(form['ipk'])
            penghasilan = ke_angka(form['penghasilan'])
            semester = int(ke_angka(form['semester']))

            if not 0.0 <= ipk <= 4.0:
                raise ValueError('IPK harus berada pada rentang 0,00 sampai 4,00.')
            if penghasilan < 0:
                raise ValueError('Penghasilan orang tua tidak boleh bernilai negatif.')
            if not 1 <= semester <= 14:
                raise ValueError('Semester harus berada pada rentang 1 sampai 14.')

            hasil = seleksi_beasiswa(ipk, penghasilan, semester, form['prestasi'])
        except ValueError as e:
            error = str(e)

    return render_template('beasiswa.html', form=form, hasil=hasil, error=error)


if __name__ == '__main__':
    app.run(debug=True)