// Interaksi halaman portofolio: progres scroll, kemunculan elemen, hitung naik,
// filter proyek, efek miring kartu, scrollspy, dan tombol salin email.
(function () {
  const kurangGerak = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 1. Bilah progres scroll dan garis bawah navigasi
  const bar = document.getElementById('bar-progres');
  const nav = document.getElementById('nav');
  function saatScroll() {
    const tinggi = document.documentElement.scrollHeight - window.innerHeight;
    const persen = tinggi > 0 ? (window.scrollY / tinggi) * 100 : 0;
    bar.style.width = persen + '%';
    nav.classList.toggle('berbayang', window.scrollY > 10);
  }
  window.addEventListener('scroll', saatScroll, { passive: true });
  saatScroll();

  // 2. Hitung naik untuk angka statistik
  function hitungNaik(el) {
    const target = Number(el.dataset.hitung);
    const durasi = 1600;
    const mulai = performance.now();
    function frame(sekarang) {
      const t = Math.min((sekarang - mulai) / durasi, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - t, 3)));
      if (t < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
  if (!kurangGerak) {
    document.querySelectorAll('.stat b').forEach((b) => { b.textContent = '0'; });
  }

  // 3. IntersectionObserver: beri kelas "terlihat" saat elemen masuk layar
  const pengamat = new IntersectionObserver((daftar) => {
    daftar.forEach((entri) => {
      if (!entri.isIntersecting) return;
      entri.target.classList.add('terlihat');
      if (entri.target.matches('.stat') && !kurangGerak) {
        hitungNaik(entri.target.querySelector('b'));
      }
      pengamat.unobserve(entri.target);
    });
  }, { threshold: 0.2 });
  document.querySelectorAll('.muncul, .stat').forEach((el) => pengamat.observe(el));

  // 4. Filter proyek berdasarkan kategori
  const tombolFilter = document.querySelectorAll('.filter');
  const kartu = document.querySelectorAll('.proyek');
  tombolFilter.forEach((tombol) => {
    tombol.addEventListener('click', () => {
      tombolFilter.forEach((t) => t.setAttribute('aria-pressed', String(t === tombol)));
      kartu.forEach((k) => {
        const cocok = tombol.dataset.filter === 'semua' || k.dataset.tag === tombol.dataset.filter;
        k.classList.toggle('sembunyi', !cocok);
      });
    });
  });

  // 5. Efek miring (tilt) pada kartu proyek, hanya untuk perangkat dengan mouse
  if (!kurangGerak && window.matchMedia('(hover: hover)').matches) {
    kartu.forEach((k) => {
      k.addEventListener('mousemove', (e) => {
        const r = k.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        k.style.transform =
          `perspective(900px) rotateX(${(-y * 8).toFixed(2)}deg) rotateY(${(x * 8).toFixed(2)}deg) translate(-3px, -3px)`;
      });
      k.addEventListener('mouseleave', () => { k.style.transform = ''; });
    });
  }

  // 6. Scrollspy: tandai menu sesuai bagian yang sedang dibaca
  const tautan = document.querySelectorAll('.nav__tautan a');
  const spy = new IntersectionObserver((daftar) => {
    daftar.forEach((entri) => {
      if (!entri.isIntersecting) return;
      tautan.forEach((a) => a.classList.toggle('aktif', a.getAttribute('href') === '#' + entri.target.id));
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  document.querySelectorAll('main section[id]').forEach((s) => spy.observe(s));

  // 7. Salin email ke clipboard
  const salin = document.getElementById('salin-email');
  if (salin) {
    salin.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(salin.dataset.email);
        salin.textContent = 'Email tersalin';
      } catch (galat) {
        salin.textContent = 'Salin dari tautan di atas';
      }
      setTimeout(() => { salin.textContent = 'Salin email'; }, 2200);
    });
  }
})();
