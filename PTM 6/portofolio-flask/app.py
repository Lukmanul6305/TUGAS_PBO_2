"""Portofolio Flask: splash screen, beranda, login, dan halaman portofolio terproteksi."""
import hmac
import os
import secrets
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from data import PROFIL

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'kunci-demo-ganti-saat-deploy')
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    # Aktifkan (set COOKIE_SECURE=1) hanya bila aplikasi dilayani lewat HTTPS.
    SESSION_COOKIE_SECURE=os.environ.get('COOKIE_SECURE') == '1',
)

# Akun demo. Pada aplikasi nyata, simpan HASH di database, bukan membuatnya dari teks di kode.
USERS = {
    'mahasiswa': {
        'nama': 'Mahasiswa Praktikum',
        'hash': generate_password_hash('praktikum123'),
    },
}


# ------------------------------------------------------------------- keamanan
def token_csrf():
    """Buat token acak sekali per sesi untuk melindungi form dari CSRF."""
    if 'csrf' not in session:
        session['csrf'] = secrets.token_hex(16)
    return session['csrf']


def csrf_valid():
    kiriman = request.form.get('csrf', '')
    asli = session.get('csrf', '')
    return bool(asli) and hmac.compare_digest(kiriman.encode(), asli.encode())


def tujuan_aman(url):
    """Hanya izinkan alamat internal seperti /portofolio. Tolak //situs-lain dan http://..."""
    return url.startswith('/') and not url.startswith('//') and '\\' not in url


def login_required(view):
    """Decorator: arahkan ke halaman login jika pengguna belum masuk."""
    @wraps(view)
    def pembungkus(*args, **kwargs):
        if 'user' not in session:
            flash('Silakan masuk untuk membuka portofolio.', 'info')
            return redirect(url_for('login', next=request.path))
        return view(*args, **kwargs)
    return pembungkus


@app.context_processor
def sisipkan_data():
    """Variabel yang otomatis tersedia di semua template."""
    return {'profil': PROFIL, 'csrf_token': token_csrf}


@app.after_request
def tanpa_cache(respons):
    """Halaman terproteksi tidak boleh disimpan browser (tombol Back setelah logout)."""
    if request.endpoint == 'portofolio':
        respons.headers['Cache-Control'] = 'no-store'
    return respons


# -------------------------------------------------------------------- halaman
@app.route('/')
def splash():
    return render_template('splash.html')


@app.route('/beranda')
def beranda():
    return render_template('beranda.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('portofolio'))

    username = ''
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '')

        if not csrf_valid():
            flash('Formulir kedaluwarsa. Muat ulang halaman lalu coba lagi.', 'error')
        else:
            akun = USERS.get(username)
            if akun and check_password_hash(akun['hash'], password):
                tujuan = request.args.get('next', '')  # dibaca sebelum session.clear()
                session.clear()  # sesi baru setelah login berhasil
                session['user'] = username
                session['nama'] = akun['nama']
                return redirect(tujuan if tujuan_aman(tujuan) else url_for('portofolio'))
            flash('Username atau password salah.', 'error')  # pesan sengaja tidak spesifik

    return render_template('login.html', username=username)


@app.route('/portofolio')
@login_required
def portofolio():
    return render_template('portofolio.html')


@app.route('/logout', methods=['POST'])
def logout():
    if csrf_valid():
        session.clear()
        flash('Anda sudah keluar.', 'info')
    return redirect(url_for('beranda'))


@app.errorhandler(404)
def tidak_ditemukan(galat):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)  # khusus praktikum; jangan dipakai di server publik
