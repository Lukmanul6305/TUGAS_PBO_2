(function () {
  const splash = document.querySelector('.splash');
  const angka = document.getElementById('angka');
  const garis = document.getElementById('garis');
  const tujuan = splash.dataset.tujuan;
  const kurangGerak = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const DURASI = kurangGerak ? 500 : 3200; // milidetik

  function selesai() {
    document.body.classList.add('keluar');
    setTimeout(() => { window.location.href = tujuan; }, kurangGerak ? 0 : 850);
  }

  const mulai = performance.now();
  function frame(sekarang) {
    const t = Math.min((sekarang - mulai) / DURASI, 1);
    const halus = 1 - Math.pow(1 - t, 3); // easing: cepat di awal, melambat di akhir
    const persen = Math.round(halus * 100);
    angka.textContent = persen;
    garis.style.width = persen + '%';
    if (t < 1) { requestAnimationFrame(frame); } else { selesai(); }
  }
  requestAnimationFrame(frame);
})();
