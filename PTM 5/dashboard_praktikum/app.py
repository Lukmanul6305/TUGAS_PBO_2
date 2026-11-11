"""Dashboard aktivitas praktikum dengan Flask dan Matplotlib.

Data dalam contoh ini adalah simulasi untuk latihan, bukan data kampus.
"""

import base64
from io import BytesIO

from flask import Flask, render_template
from matplotlib.figure import Figure

app = Flask(__name__)

# Satu sumber data dipakai untuk semua kartu ringkasan dan grafik.
DATA = [
    {"bulan": "Jan", "hadir": 120, "tuntas": 82},
    {"bulan": "Feb", "hadir": 135, "tuntas": 96},
    {"bulan": "Mar", "hadir": 128, "tuntas": 94},
    {"bulan": "Apr", "hadir": 155, "tuntas": 121},
    {"bulan": "Mei", "hadir": 168, "tuntas": 138},
    {"bulan": "Jun", "hadir": 182, "tuntas": 157},
]


def gambar_base64(fig):
    """Ubah Figure menjadi teks PNG agar bisa ditampilkan di HTML."""
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=140, bbox_inches="tight")
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def siapkan_grafik():
    bulan = [item["bulan"] for item in DATA]
    hadir = [item["hadir"] for item in DATA]
    tingkat = [item["tuntas"] / item["hadir"] * 100 for item in DATA]
    terakhir = DATA[-1]

    # Grafik 1: batang untuk membandingkan jumlah kehadiran tiap bulan.
    fig1 = Figure(figsize=(7, 3.4), facecolor="white")
    ax1 = fig1.subplots()
    batang = ax1.bar(bulan, hadir, color="#4f46e5", width=0.58)
    ax1.bar_label(batang, padding=4, fontsize=9, color="#334155")
    ax1.set_ylim(0, max(hadir) * 1.2)
    ax1.set_ylabel("Kehadiran")
    ax1.spines[["top", "right", "left"]].set_visible(False)
    ax1.tick_params(axis="y", length=0)
    ax1.grid(axis="y", alpha=0.16)
    ax1.set_axisbelow(True)

    # Grafik 2: garis untuk melihat perubahan persentase ketuntasan.
    fig2 = Figure(figsize=(7, 3.4), facecolor="white")
    ax2 = fig2.subplots()
    ax2.plot(bulan, tingkat, color="#0f766e", marker="o", linewidth=2.7)
    ax2.fill_between(bulan, tingkat, 0, color="#ccfbf1", alpha=0.7)
    ax2.set_ylim(0, 100)
    ax2.set_ylabel("Tuntas (%)")
    ax2.spines[["top", "right", "left"]].set_visible(False)
    ax2.tick_params(axis="y", length=0)
    ax2.grid(axis="y", alpha=0.16)
    ax2.set_axisbelow(True)
    ax2.annotate(f"{tingkat[-1]:.1f}%", (bulan[-1], tingkat[-1]),
                 xytext=(-4, 12), textcoords="offset points", ha="right",
                 color="#0f766e", weight="bold")

    # Grafik 3: donat untuk komposisi bulan terakhir.
    fig3 = Figure(figsize=(5.5, 3.4), facecolor="white")
    ax3 = fig3.subplots()
    belum = terakhir["hadir"] - terakhir["tuntas"]
    ax3.pie([terakhir["tuntas"], belum], startangle=90,
            colors=["#4f46e5", "#e2e8f0"],
            wedgeprops={"width": 0.32, "edgecolor": "white"})
    ax3.text(0, 0, f"{tingkat[-1]:.1f}%\ntuntas", ha="center", va="center",
             fontsize=13, weight="bold", color="#1e293b")
    ax3.set_aspect("equal")

    return {
        "batang": gambar_base64(fig1),
        "garis": gambar_base64(fig2),
        "donat": gambar_base64(fig3),
    }


@app.route("/")
def dashboard():
    total_hadir = sum(item["hadir"] for item in DATA)
    total_tuntas = sum(item["tuntas"] for item in DATA)
    terakhir = DATA[-1]
    return render_template(
        "index.html",
        grafik=siapkan_grafik(),
        data=DATA,
        total_hadir=total_hadir,
        total_tuntas=total_tuntas,
        tingkat_total=total_tuntas / total_hadir * 100,
        terakhir=terakhir,
        belum=terakhir["hadir"] - terakhir["tuntas"],
    )


if __name__ == "__main__":
    app.run(debug=True)  # Hanya untuk pengembangan lokal.
