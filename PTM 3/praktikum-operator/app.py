from flask import Flask

app = Flask(__name__)

@app.route('/')
def beranda():
    return '<h1>Praktikum Operator Flask</h1>'

@app.route('/tambah/<int:a>/<int:b>')
def tambah(a, b):
    return f'{a} + {b} = {a + b}'

@app.route('/kurang/<int:a>/<int:b>')
def kurang(a, b):
    return f'{a} - {b} = {a - b}'

@app.route('/kali/<int:a>/<int:b>')
def kali(a, b):
    return f'{a} * {b} = {a * b}'

@app.route('/bagi/<int:a>/<int:b>')
def bagi(a, b):
    if b == 0:
        return 'Error: Pembagian dengan nol tidak diperbolehkan.', 400
    return f'{a} / {b} = {a / b}'

@app.route('/sisa/<int:a>/<int:b>')
def sisa(a, b):
    if b == 0:
        return 'Error: Pembagian dengan nol tidak diperbolehkan.', 400
    
    bagi_int, sisa_bagi = divmod(a, b)
    return f'Bagi int: {bagi_int}, Sisa: {sisa_bagi} (dari {a} dan {b})'

@app.route('/pangkat/<int:a>/<int:b>')
def pangkat(a, b):
    return f'{a} ** {b} = {a ** b}'

if __name__ == '__main__':
    app.run(debug=True)
