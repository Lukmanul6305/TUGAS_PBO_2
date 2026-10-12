
class ProgramStudi:
    """Merepresentasikan satu program studi."""

    def __init__(self, kode: str, nama: str):
        self.kode = kode
        self.nama = nama
        self.mahasiswa = []

    def tambah_mahasiswa(self, mahasiswa):
        """Hubungkan mahasiswa ke program studi; cegah NIM ganda."""
        if any(m.nim == mahasiswa.nim for m in self.mahasiswa):
            raise ValueError(
                f"NIM {mahasiswa.nim} sudah terdaftar di prodi ini."
            )
        self.mahasiswa.append(mahasiswa)


class MataKuliah:
    """Merepresentasikan mata kuliah dan daftar KRS yang mengambilnya."""

    def __init__(self, kode: str, nama: str, sks: int):
        if sks < 1 or sks > 6:
            raise ValueError("SKS harus berada pada rentang 1 sampai 6.")

        self.kode = kode
        self.nama = nama
        self.sks = sks
        self.peserta_krs = []

    def ringkasan(self):
        return f"{self.kode} - {self.nama} ({self.sks} SKS)"


class KRS:
    """Relasi/transaksi pengambilan mata kuliah oleh seorang mahasiswa."""

    def __init__(self, mahasiswa, matakuliah, semester: int):
        if semester < 1 or semester > 14:
            raise ValueError(
                "Semester harus berada pada rentang 1 sampai 14."
            )

        self.mahasiswa = mahasiswa
        self.matakuliah = matakuliah
        self.semester = semester
        self.nilai = None

    def ringkasan(self):
        return {
            "nim": self.mahasiswa.nim,
            "mahasiswa": self.mahasiswa.nama,
            "kode_mk": self.matakuliah.kode,
            "mata_kuliah": self.matakuliah.nama,
            "sks": self.matakuliah.sks,
            "semester": self.semester,
            "nilai": self.nilai or "Belum ada",
        }


class Mahasiswa:
    """Merepresentasikan mahasiswa dan daftar pengambilan mata kuliah."""

    def __init__(self, nim: str, nama: str, prodi: ProgramStudi):
        if not nim.strip():
            raise ValueError("NIM tidak boleh kosong.")
        if not nama.strip():
            raise ValueError("Nama tidak boleh kosong.")

        self.nim = nim.strip()
        self.nama = nama.strip()
        self.prodi = prodi
        self.krs = []

        self.prodi.tambah_mahasiswa(self)

    def ambil_mata_kuliah(self, matakuliah: MataKuliah, semester: int):
        """Membuat object KRS yang menghubungkan Mahasiswa dan MataKuliah."""
        duplikat = any(
            item.matakuliah.kode == matakuliah.kode
            and item.semester == semester
            for item in self.krs
        )

        if duplikat:
            raise ValueError(
                "Mata kuliah yang sama sudah ada di KRS semester ini."
            )

        item_krs = KRS(self, matakuliah, semester)
        self.krs.append(item_krs)
        matakuliah.peserta_krs.append(item_krs)

        return item_krs

    def jumlah_sks(self, semester: int):
        return sum(
            item.matakuliah.sks
            for item in self.krs
            if item.semester == semester
        )



def buat_data_demo():
    """Menghasilkan objek demo agar alur relasi dapat ditampilkan di browser."""
    ti = ProgramStudi("TI", "Teknik Informatika")
    si = ProgramStudi("SI", "Sistem Informasi")

    # Membuat object mata kuliah
    mk_oop = MataKuliah("TI350", "Pemrograman Berorientasi Objek", 3)
    mk_web = MataKuliah("TI364", "Pemrograman Web", 3)
    mk_basisdata = MataKuliah("TI322", "Sistem Basis Data", 3)
    mk_python = MataKuliah("TI370", "Pemrograman Python Lanjut", 3)

    # Membuat object mahasiswa
    mhs1 = Mahasiswa("20260001", "Alya Putri", ti)
    mhs2 = Mahasiswa("20260002", "Bagas Pratama", ti)
    mhs3 = Mahasiswa("20260003", "Citra Lestari", si)
    mhs4 = Mahasiswa("20260004", "Dewi Anggraini", ti)

    # Membuat relasi KRS mahasiswa dengan mata kuliah
    mhs1.ambil_mata_kuliah(mk_oop, 6)
    mhs1.ambil_mata_kuliah(mk_web, 6)

    mhs2.ambil_mata_kuliah(mk_oop, 6)
    mhs2.ambil_mata_kuliah(mk_basisdata, 6)

    mhs3.ambil_mata_kuliah(mk_basisdata, 4)

    mhs4.ambil_mata_kuliah(mk_oop, 6)
    mhs4.ambil_mata_kuliah(mk_python, 7)

    # Mengumpulkan seluruh object
    semua_mahasiswa = [mhs1, mhs2, mhs3, mhs4]
    semua_mk = [mk_oop, mk_web, mk_basisdata, mk_python]

    semua_krs = [
        item
        for mhs in semua_mahasiswa
        for item in mhs.krs
    ]

    semua_prodi = [ti, si]

    return semua_prodi, semua_mahasiswa, semua_mk, semua_krs

