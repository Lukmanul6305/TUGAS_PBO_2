from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Komponen: Class (Minimal 1 class domain)
class Buku:
    """Merepresentasikan satu objek buku perpustakaan."""
    
    def __init__(self, kode_buku, judul, penulis, penerbit, tahun):
        # Komponen: Attribute (Minimal 4 attribute)
        self.kode_buku = kode_buku
        self.judul = judul
        self.penulis = penulis
        self.penerbit = penerbit
        self.tahun = tahun

    # Komponen: Method (Minimal 2 method)
    def tampilkan_info_utama(self):
        return f"{self.kode_buku} - {self.judul}"

    def detail_buku(self):
        return f"Ditulis oleh {self.penulis}, diterbitkan oleh {self.penerbit} ({self.tahun})"


# Data awal aplikasi
data_awal = [
    Buku("B001", "Clean Code", "Robert C. Martin", "Prentice Hall", 2008),
    Buku("B002", "The Pragmatic Programmer", "Andy Hunt", "Addison-Wesley", 1999),
]

# Penyimpanan sementara di memori
data_buku = data_awal.copy()

@app.route("/", methods=["GET", "POST"])
def index():
    pesan = None

    # Komponen: Aksi (Tambah data)
    if request.method == "POST":
        kode_buku = request.form.get("kode_buku", "").strip()
        judul = request.form.get("judul", "").strip()
        penulis = request.form.get("penulis", "").strip()
        penerbit = request.form.get("penerbit", "").strip()
        tahun = request.form.get("tahun", "").strip()

        # Komponen: Validasi (Minimal 2 validasi input)
        # Validasi 1: Mencegah input kosong
        if not kode_buku or not judul or not penulis or not penerbit or not tahun:
            pesan = "Semua field wajib diisi."

        # Validasi 2: Mencegah kode buku duplikat
        elif any(b.kode_buku == kode_buku for b in data_buku):
            pesan = "Kode Buku sudah terdaftar. Gunakan kode lain."

        else:
            # Komponen: Object (Object dibuat dari input pengguna)
            buku_baru = Buku(kode_buku, judul, penulis, penerbit, tahun)
            data_buku.append(buku_baru)
            return redirect(url_for("index"))

    return render_template(
        "index.html",
        koleksi_buku=data_buku,
        pesan=pesan
    )

# Komponen: Aksi (Hapus data)
@app.route("/hapus/<kode_buku>", methods=["POST"])
def hapus(kode_buku):
    global data_buku
    data_buku = [b for b in data_buku if b.kode_buku != kode_buku]
    return redirect(url_for("index"))


@app.route("/reset", methods=["POST"])
def reset():
    global data_buku
    data_buku = data_awal.copy()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)