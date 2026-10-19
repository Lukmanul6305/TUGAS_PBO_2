while True:
    try:
        a = int(input('Masukkan bilangan pertama: '))
        b = int(input('Masukkan bilangan kedua   : '))
        bagi_int, sisa = divmod(a, b)

        print('Tambah   :', a + b)
        print('Kurang   :', a - b)
        print('Kali     :', a * b)
        print('Bagi     :', a / b)
        print('Bagi int :', bagi_int)
        print('Sisa     :', sisa)
        print('Pangkat  :', a ** b)
    except ValueError:
        print('Input harus berupa bilangan bulat.')
    except ZeroDivisionError:
        print('Pembagian dengan nol tidak diperbolehkan.')
