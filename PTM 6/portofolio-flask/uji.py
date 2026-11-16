import re
from app import app

c = app.test_client()
assert c.get('/portofolio').status_code == 302          # terkunci tanpa login

html = c.get('/login').get_data(as_text=True)
token = re.search(r'name=.csrf. value=.([0-9a-f]+)', html).group(1)

# tanpa token CSRF: ditolak, tetap di halaman login
r = c.post('/login', data={'username': 'mahasiswa', 'password': 'praktikum123'})
assert r.status_code == 200 and 'kedaluwarsa' in r.get_data(as_text=True)

# password salah: pesan generik
r = c.post('/login', data={'username': 'mahasiswa', 'password': 'salah', 'csrf': token})
assert r.status_code == 200 and 'Username atau password salah' in r.get_data(as_text=True)

# berhasil masuk
data = {'username': 'mahasiswa', 'password': 'praktikum123', 'csrf': token}
assert c.post('/login', data=data).status_code == 302   # berhasil masuk
assert c.get('/portofolio').status_code == 200          # kini terbuka

# open redirect lewat ?next= harus dinetralkan
c2 = app.test_client()
h = c2.get('/login').get_data(as_text=True)
t = re.search(r'name=.csrf. value=.([0-9a-f]+)', h).group(1)
r = c2.post('/login?next=//evil.com', data={**data, 'csrf': t})
assert r.headers['Location'].endswith('/portofolio')

# logout hanya POST
assert c.get('/logout').status_code == 405
h = c.get('/portofolio').get_data(as_text=True)
t = re.search(r'name=.csrf. value=.([0-9a-f]+)', h).group(1)
assert c.post('/logout', data={'csrf': t}).status_code == 302
assert c.get('/portofolio').status_code == 302

# halaman publik dan 404
for url in ('/', '/beranda', '/login'):
    assert c.get(url).status_code == 200
assert c.get('/tidak-ada').status_code == 404
print('Semua uji lulus')
