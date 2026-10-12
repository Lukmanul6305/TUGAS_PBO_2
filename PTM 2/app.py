
"""Flask presentation layer untuk mendemonstrasikan relasi antarobjek."""

from flask import Flask, render_template
from models.academic import buat_data_demo

app = Flask(__name__)

# Data dibuat sebagai object Python setiap aplikasi dijalankan.
# Belum memakai database: fokus pertemuan ini adalah object modeling.
PROGRAM_STUDI, MAHASISWA, MATA_KULIAH, KRS = buat_data_demo()


@app.route("/")
def index():
    """Tampilkan object dan hubungan yang telah dimodelkan."""
    return render_template(
        "index.html",
        program_studi=PROGRAM_STUDI,
        mahasiswa=MAHASISWA,
        mata_kuliah=MATA_KULIAH,
        daftar_krs=[item.ringkasan() for item in KRS],
    )


if __name__ == "__main__":
    app.run(debug=True)
