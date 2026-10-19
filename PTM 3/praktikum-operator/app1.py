from flask import Flask, render_template, request

app = Flask(__name__)

TARIF_PPN = 0.11
BATAS_DISKON = 100_000
PERSEN_DISKON = 0.10
BATAS_DISKON_RINGAN = 50_000
PERSEN_DISKON_RINGAN = 0.05


@app.template_filter('rupiah')
def format_rupiah(nilai):
    return f'{nilai:,.0f}'.replace(',', '.')


def hitung(a, b, op):
    if op == 'tambah':
        return a + b
    elif op == 'kurang':
        return a - b
    elif op == 'kali':
        return a * b
    elif op == 'bagi':
        return a / b
    elif op == 'bagi_bulat':
        return a // b
    elif op == 'sisa':
        return a % b
    elif op == 'pangkat':
        return a ** b
    elif op == 'rata_rata':
        return (a + b) / 2
@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/kalkulator', methods=['GET', 'POST'])
def kalkulator():
    hasil = None
    error = None
    if request.method == 'POST':
        try:
            a = float(request.form['a'])
            b = float(request.form['b'])
            hasil = int(hitung(a, b, request.form['op']))
        except ValueError:
            error = 'Masukkan angka yang valid.'
        except ZeroDivisionError:
            error = 'Pembagian dengan nol tidak diperbolehkan.'
    return render_template('kalkulator.html', hasil=hasil, error=error)


@app.route('/kasir', methods=['GET', 'POST'])
def kasir():
    nota = None
    error = None
    form = {'harga': '', 'jumlah': '', 'bayar': ''}

    if request.method == 'POST':
        form = {nama: request.form.get(nama, '').strip()
                for nama in ('harga', 'jumlah', 'bayar')}
        try:
            harga = int(form['harga'])
            jumlah = int(form['jumlah'])
            bayar = int(form['bayar'])

            if harga <= 0:
                error = 'Harga harus lebih besar dari nol.'
            elif jumlah <= 0:
                error = 'Jumlah barang harus lebih besar dari nol.'
            elif bayar < 0:
                error = 'Uang bayar tidak boleh kurang dari nol.'
            else:
                subtotal = harga * jumlah
                if subtotal >= BATAS_DISKON:
                    diskon = subtotal * PERSEN_DISKON
                elif subtotal >= BATAS_DISKON_RINGAN:
                    diskon = subtotal * PERSEN_DISKON_RINGAN
                else:
                    diskon = 0

                dpp = subtotal - diskon
                ppn = dpp * TARIF_PPN
                total = round(dpp + ppn)
                kembalian = bayar - total

                nota = {
                    'subtotal': subtotal,
                    'diskon': round(diskon),
                    'ppn': round(ppn),
                    'total': total,
                    'kembalian': kembalian,
                    'cukup': bayar >= total,
                }
        except ValueError:
            error = 'Harga, jumlah, dan uang bayar harus berupa bilangan bulat.'

    return render_template('kasir.html', nota=nota, error=error, form=form)


def konversi_grade(nilai):
    if nilai >= 85:
        return 'A'
    elif nilai >= 70:
        return 'B'
    elif nilai >= 55:
        return 'C'
    elif nilai >= 40:
        return 'D'
    return 'E'


@app.route('/nilai', methods=['GET', 'POST'])
def nilai():
    form_rows = [{'nama': '', 'kehadiran': '', 'tugas': '', 'uts': '', 'uas': ''}]
    hasil = None
    rata_rata_kelas = None
    error = None

    if request.method == 'POST':
        field_names = ('nama', 'kehadiran', 'tugas', 'uts', 'uas')
        form_data = {field: request.form.getlist(field) for field in field_names}
        jumlah_baris = max((len(values) for values in form_data.values()), default=0)
        form_rows = [
            {field: form_data[field][i].strip() if i < len(form_data[field]) else ''
             for field in field_names}
            for i in range(jumlah_baris)
        ]

        # Jika kehadiran tidak dikirim, pertahankan bobot tiga komponen pada data uji awal.
        pakai_bobot_lama = 'kehadiran' not in request.form
        hasil = []
        nilai_mentah = []
        kesalahan = []

        if not form_rows:
            kesalahan.append('Masukkan setidaknya satu mahasiswa.')

        for i, row in enumerate(form_rows, start=1):
            try:
                tugas = float(row['tugas'])
                uts = float(row['uts'])
                uas = float(row['uas'])
                kehadiran = None if pakai_bobot_lama else float(row['kehadiran'])
            except ValueError:
                kesalahan.append(f'Lengkapi semua nilai mahasiswa ke-{i} dengan angka yang valid.')
                continue

            komponen = [tugas, uts, uas]
            if kehadiran is not None:
                komponen.append(kehadiran)
            if not all(0 <= komponen_nilai <= 100 for komponen_nilai in komponen):
                kesalahan.append(f'Setiap nilai mahasiswa ke-{i} harus berada pada rentang 0 sampai 100.')
                continue

            if pakai_bobot_lama:
                akhir = tugas * 0.3 + uts * 0.3 + uas * 0.4
            else:
                akhir = kehadiran * 0.1 + tugas * 0.3 + uts * 0.3 + uas * 0.3

            lulus = akhir >= 55 and uas >= 40
            if lulus:
                pesan = 'Mahasiswa dinyatakan lulus.'
            elif akhir >= 55 and uas < 40:
                pesan = 'Nilai akhir memenuhi batas, tetapi mahasiswa gagal karena nilai UAS di bawah 40.'
            elif akhir < 55 and uas < 40:
                pesan = 'Mahasiswa belum lulus: nilai akhir di bawah 55 dan nilai UAS di bawah 40.'
            else:
                pesan = 'Mahasiswa belum lulus karena nilai akhir di bawah 55.'

            nilai_mentah.append(akhir)
            hasil.append({
                'nama': row['nama'] or f'Mahasiswa {i}',
                'kehadiran': kehadiran,
                'tugas': tugas,
                'uts': uts,
                'uas': uas,
                'akhir': round(akhir, 2),
                'grade': konversi_grade(akhir),
                'lulus': lulus,
                'pesan': pesan,
            })

        if kesalahan:
            hasil = None
            error = ' '.join(kesalahan)
        elif hasil:
            rata_rata_kelas = round(sum(nilai_mentah) / len(nilai_mentah), 2)

    return render_template(
        'nilai.html', form_rows=form_rows, hasil=hasil,
        rata_rata_kelas=rata_rata_kelas, error=error
    )


@app.route('/lingkaran', methods=['GET', 'POST'])
def lingkaran():
    luas = None
    keliling = None
    error = None
    radius = ''

    if request.method == 'POST':
        radius = request.form.get('radius', '').strip()
        try:
            r = float(radius)
            if r < 0:
                error = 'Jari-jari tidak boleh kurang dari nol.'
            else:
                luas = 3.14159 * r ** 2
                keliling = 2 * 3.14159 * r
        except ValueError:
            error = 'Masukkan jari-jari yang valid.'

    return render_template(
        'lingkaran.html', radius=radius, luas=luas,
        keliling=keliling, error=error
    )


@app.route('/waktu', methods=['GET', 'POST'])
def konversi_waktu():
    total_detik = ''
    jam = menit = detik = None
    error = None

    if request.method == 'POST':
        total_detik = request.form.get('total_detik', '').strip()
        try:
            total = int(total_detik)
            if total < 0:
                error = 'Jumlah detik tidak boleh kurang dari nol.'
            else:
                jam = total // 3600
                sisa_detik = total % 3600
                menit = sisa_detik // 60
                detik = sisa_detik % 60
        except ValueError:
            error = 'Masukkan jumlah detik berupa bilangan bulat.'

    return render_template(
        'waktu.html', total_detik=total_detik,
        jam=jam, menit=menit, detik=detik, error=error
    )


@app.route('/pecahan', methods=['GET', 'POST'])
def pecahan_uang():
    nominal = ''
    pecahan = None
    sisa = None
    error = None

    if request.method == 'POST':
        nominal = request.form.get('nominal', '').strip()
        try:
            jumlah = int(nominal)
            if jumlah < 0:
                error = 'Nominal tidak boleh kurang dari nol.'
            else:
                sisa = jumlah
                pecahan = []
                for nilai in (100000, 50000, 20000, 10000):
                    lembar = sisa // nilai
                    sisa = sisa % nilai
                    pecahan.append((nilai, lembar))
        except ValueError:
            error = 'Masukkan nominal berupa bilangan bulat.'

    return render_template(
        'pecahan.html', nominal=nominal, pecahan=pecahan,
        sisa=sisa, error=error
    )



# Praktikum 4
@app.route('/cek/<int:angka>')
def cek(angka):
    jenis = 'genap' if angka % 2 == 0 else 'ganjil'
    kelipatan_15 = angka % 3 == 0 and angka % 5 == 0
    positif = angka > 0
    return (f'{angka} adalah bilangan {jenis}. '
            f'Kelipatan 3 dan 5: {kelipatan_15}. '
            f'Positif: {positif}.')

@app.route('/kabisat/<int:tahun>')
def kabisat(tahun):
    hasil = (tahun % 4 == 0 and tahun % 100 != 0) or tahun % 400 == 0
    if(hasil):
        hasil = "tahun kabisat"
    else:
        hasil = "Bukan tahun kabisat"
    return (f"hasil dari {tahun} adalah {hasil}")

@app.route('/rentang/<int:n>')
def rentang(n):
    hasil = 10 <= n <= 99
    return (f"hasil {n} adalah {hasil}")


if __name__ == '__main__':
    app.run(debug=True)
    
