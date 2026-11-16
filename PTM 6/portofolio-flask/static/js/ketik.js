(function () {
  const kurangGerak = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function mesinKetik(el, daftar) {
    if (kurangGerak || daftar.length === 0) { el.textContent = daftar[0] || ''; return; }
    let kata = 0, huruf = 0, menghapus = false;

    function langkah() {
      const teks = daftar[kata];
      huruf += menghapus ? -1 : 1;
      el.textContent = teks.slice(0, huruf);

      let jeda = menghapus ? 45 : 85;
      if (!menghapus && huruf === teks.length) { menghapus = true; jeda = 1400; }
      else if (menghapus && huruf === 0) { menghapus = false; kata = (kata + 1) % daftar.length; jeda = 350; }
      setTimeout(langkah, jeda);
    }
    langkah();
  }

  document.querySelectorAll('[data-ketik]').forEach((el) => {
    mesinKetik(el, JSON.parse(el.dataset.ketik));
  });
})();
