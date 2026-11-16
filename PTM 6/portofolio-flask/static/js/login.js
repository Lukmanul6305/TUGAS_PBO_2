// Tombol tampilkan/sembunyikan password.
(function () {
  const sandi = document.getElementById('sandi');
  const tombol = document.getElementById('tombol-sandi');

  tombol.addEventListener('click', () => {
    const tampil = sandi.type === 'password';
    sandi.type = tampil ? 'text' : 'password';
    tombol.textContent = tampil ? 'Sembunyikan' : 'Tampilkan';
    tombol.setAttribute('aria-pressed', String(tampil));
  });
})();
