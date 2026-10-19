from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from math import isfinite
import os

from flask import Flask, redirect, render_template, request, session, url_for


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'kalkulator-hub-local-demo-key')

OPERATORS = {
    '+': ('Tambah', lambda a, b: a + b),
    '-': ('Kurang', lambda a, b: a - b),
    '*': ('Kali', lambda a, b: a * b),
    '/': ('Bagi', lambda a, b: a / b),
    '//': ('Bagi bulat', lambda a, b: a // b),
    '%': ('Sisa bagi', lambda a, b: a % b),
    '**': ('Pangkat', lambda a, b: a ** b),
}

UNITS = {
    'C': 'Celsius',
    'F': 'Fahrenheit',
    'K': 'Kelvin',
}


def rupiah_bulat(nilai):
    return int(Decimal(str(nilai)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def hitung_cicilan_flat(pokok, bunga_tahunan, bulan):
    bunga_bulanan = bunga_tahunan / Decimal('1200')
    total_bunga = rupiah_bulat(Decimal(pokok) * bunga_bulanan * bulan)
    pokok_dasar, sisa_pokok = divmod(pokok, bulan)
    bunga_dasar, sisa_bunga = divmod(total_bunga, bulan)
    sisa_saldo = pokok
    jadwal = []

    for urutan in range(1, bulan + 1):
        bayar_pokok = pokok_dasar + (1 if urutan <= sisa_pokok else 0)
        bayar_bunga = bunga_dasar + (1 if urutan <= sisa_bunga else 0)
        sisa_saldo -= bayar_pokok
        jadwal.append({
            'bulan': urutan,
            'pokok': bayar_pokok,
            'bunga': bayar_bunga,
            'angsuran': bayar_pokok + bayar_bunga,
            'sisa': sisa_saldo,
        })

    return total_bunga, jadwal


def hitung_cicilan_anuitas(pokok, bunga_tahunan, bulan):
    bunga_bulanan = bunga_tahunan / Decimal('1200')
    if bunga_bulanan == 0:
        angsuran_teori = Decimal(pokok) / bulan
    else:
        faktor = (Decimal('1') + bunga_bulanan) ** bulan
        angsuran_teori = (
            Decimal(pokok) * bunga_bulanan * faktor / (faktor - Decimal('1'))
        )

    saldo = pokok
    total_bunga = 0
    jadwal = []

    for urutan in range(1, bulan + 1):
        bayar_bunga = rupiah_bulat(Decimal(saldo) * bunga_bulanan)
        if urutan == bulan:
            bayar_pokok = saldo
        else:
            bayar_pokok = rupiah_bulat(angsuran_teori - bayar_bunga)
            bayar_pokok = max(0, min(bayar_pokok, saldo))

        saldo -= bayar_pokok
        total_bunga += bayar_bunga
        jadwal.append({
            'bulan': urutan,
            'pokok': bayar_pokok,
            'bunga': bayar_bunga,
            'angsuran': bayar_pokok + bayar_bunga,
            'sisa': saldo,
        })

    return total_bunga, jadwal, rupiah_bulat(angsuran_teori)


@app.template_filter('rupiah')
def format_rupiah(nilai):
    return f'{int(nilai):,}'.replace(',', '.')


@app.template_filter('angka_id')
def format_angka_id(nilai):
    return f'{float(nilai):,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/kalkulator', methods=['GET', 'POST'])
def kalkulator():
    form = {'angka_a': '', 'angka_b': '', 'operator': '+'}
    hasil = None
    error = None
    riwayat = session.get('riwayat_kalkulator', [])

    if request.method == 'POST':
        if request.form.get('action') == 'clear_history':
            session.pop('riwayat_kalkulator', None)
            return redirect(url_for('kalkulator'))

        form = {
            'angka_a': request.form.get('angka_a', '').strip(),
            'angka_b': request.form.get('angka_b', '').strip(),
            'operator': request.form.get('operator', '+'),
        }
        try:
            angka_a = float(form['angka_a'])
            angka_b = float(form['angka_b'])
            operator = form['operator']
            if operator not in OPERATORS:
                raise ValueError('Pilih operator yang tersedia.')
            if not isfinite(angka_a) or not isfinite(angka_b):
                raise ValueError('Angka harus berupa nilai yang valid.')

            hasil_angka = OPERATORS[operator][1](angka_a, angka_b)
            if isinstance(hasil_angka, complex) or not isfinite(hasil_angka):
                raise ValueError('Hasil tidak dapat ditampilkan sebagai bilangan real.')

            hasil = f'{hasil_angka:,.8f}'.rstrip('0').rstrip('.')
            hasil = hasil.replace(',', '_').replace('.', ',').replace('_', '.')
            ekspresi = f'{angka_a:g} {operator} {angka_b:g}'
            riwayat = [{
                'ekspresi': ekspresi,
                'hasil': hasil,
            }] + riwayat[:9]
            session['riwayat_kalkulator'] = riwayat
        except (ValueError, ZeroDivisionError, OverflowError) as exc:
            error = str(exc) or 'Perhitungan tidak dapat dilakukan.'

    return render_template(
        'kalkulator.html', form=form, hasil=hasil, error=error,
        riwayat=riwayat, operators=OPERATORS
    )


@app.route('/cicilan', methods=['GET', 'POST'])
def cicilan():
    form = {
        'pokok': '',
        'bunga_tahunan': '',
        'bulan': '',
        'metode': 'flat',
    }
    hasil = None
    error = None

    if request.method == 'POST':
        form = {
            'pokok': request.form.get('pokok', '').strip(),
            'bunga_tahunan': request.form.get('bunga_tahunan', '').strip(),
            'bulan': request.form.get('bulan', '').strip(),
            'metode': request.form.get('metode', 'flat'),
        }
        try:
            pokok = int(form['pokok'])
            bunga_tahunan = Decimal(form['bunga_tahunan'])
            bulan = int(form['bulan'])

            if pokok <= 0:
                raise ValueError('Pokok pinjaman harus lebih besar dari nol.')
            if not bunga_tahunan.is_finite() or not Decimal('0') <= bunga_tahunan <= Decimal('100'):
                raise ValueError('Bunga tahunan harus berada pada rentang 0 sampai 100%.')
            if not 1 <= bulan <= 600:
                raise ValueError('Tenor harus antara 1 dan 600 bulan.')
            if form['metode'] not in ('flat', 'anuitas'):
                raise ValueError('Pilih metode cicilan yang tersedia.')

            if form['metode'] == 'flat':
                total_bunga, jadwal = hitung_cicilan_flat(pokok, bunga_tahunan, bulan)
                angsuran_per_bulan = rupiah_bulat(
                    Decimal(pokok + total_bunga) / bulan
                )
            else:
                total_bunga, jadwal, angsuran_per_bulan = hitung_cicilan_anuitas(
                    pokok, bunga_tahunan, bulan
                )

            total_bayar = sum(item['angsuran'] for item in jadwal)
            hasil = {
                'pokok': pokok,
                'bunga_tahunan': bunga_tahunan,
                'bulan': bulan,
                'metode': form['metode'],
                'nama_metode': 'Flat' if form['metode'] == 'flat' else 'Anuitas',
                'angsuran_per_bulan': angsuran_per_bulan,
                'total_bunga': total_bunga,
                'total_bayar': total_bayar,
                'jadwal': jadwal,
            }
        except (ValueError, InvalidOperation, OverflowError) as exc:
            error = str(exc) or 'Masukkan data pinjaman yang valid.'

    return render_template('cicilan.html', form=form, hasil=hasil, error=error)


@app.route('/bmi', methods=['GET', 'POST'])
def bmi():
    form = {'berat': '', 'tinggi': ''}
    hasil = None
    error = None

    if request.method == 'POST':
        form = {
            'berat': request.form.get('berat', '').strip(),
            'tinggi': request.form.get('tinggi', '').strip(),
        }
        try:
            berat = float(form['berat'])
            tinggi_cm = float(form['tinggi'])
            if not isfinite(berat) or not isfinite(tinggi_cm):
                raise ValueError('Berat dan tinggi harus berupa angka yang valid.')
            if berat <= 0 or tinggi_cm <= 0:
                raise ValueError('Berat dan tinggi harus lebih besar dari nol.')

            tinggi_meter = tinggi_cm / 100
            penyebut = tinggi_meter ** 2
            if penyebut == 0 or not isfinite(penyebut):
                raise ValueError('Tinggi tidak berada pada rentang yang dapat dihitung.')
            indeks = berat / penyebut
            berat_min = 18.5 * penyebut
            berat_max = 24.9 * penyebut
            if not all(isfinite(angka) for angka in (indeks, berat_min, berat_max)):
                raise ValueError('Rentang berat tidak dapat dihitung dari nilai tersebut.')
            if indeks < 18.5:
                kategori = 'Berat badan kurang'
            elif 18.5 <= indeks < 25:
                kategori = 'Berat badan normal'
            elif 25 <= indeks < 30:
                kategori = 'Berat badan berlebih'
            else:
                kategori = 'Obesitas'

            hasil = {
                'indeks': indeks,
                'kategori': kategori,
                'berat_min': berat_min,
                'berat_max': berat_max,
            }
        except (ValueError, OverflowError) as exc:
            error = str(exc) or 'Masukkan berat dan tinggi yang valid.'

    return render_template('bmi.html', form=form, hasil=hasil, error=error)


@app.route('/suhu', methods=['GET', 'POST'])
def suhu():
    form = {'nilai': '', 'dari': 'C', 'ke': 'F'}
    hasil = None
    error = None

    if request.method == 'POST':
        form = {
            'nilai': request.form.get('nilai', '').strip(),
            'dari': request.form.get('dari', 'C'),
            'ke': request.form.get('ke', 'F'),
        }
        try:
            nilai = float(form['nilai'])
            if not isfinite(nilai):
                raise ValueError('Suhu harus berupa angka yang valid.')
            if form['dari'] not in UNITS or form['ke'] not in UNITS:
                raise ValueError('Pilih satuan suhu yang tersedia.')
            batas_bawah = {'C': -273.15, 'F': -459.67, 'K': 0}[form['dari']]
            if nilai < batas_bawah:
                raise ValueError('Suhu tidak boleh lebih rendah dari nol mutlak.')

            if form['dari'] == 'C':
                celsius = nilai
            elif form['dari'] == 'F':
                celsius = (nilai - 32) * 5 / 9
            else:
                celsius = nilai - 273.15

            celsius = max(celsius, -273.15)

            semua_satuan = {
                'C': celsius,
                'F': celsius * 9 / 5 + 32,
                'K': celsius + 273.15,
            }
            if not all(isfinite(angka) for angka in semua_satuan.values()):
                raise ValueError('Nilai suhu terlalu besar untuk dikonversi.')

            hasil = {
                'nilai': semua_satuan[form['ke']],
                'nama_dari': UNITS[form['dari']],
                'nama_ke': UNITS[form['ke']],
                'semua': semua_satuan,
            }
        except ValueError as exc:
            error = str(exc) or 'Masukkan suhu yang valid.'

    return render_template('suhu.html', form=form, hasil=hasil, error=error, units=UNITS)


if __name__ == '__main__':
    app.run(debug=True)
