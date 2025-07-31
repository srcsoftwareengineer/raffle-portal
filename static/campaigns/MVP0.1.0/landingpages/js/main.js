document.addEventListener('DOMContentLoaded', () => {
  /* ========= CARROSSEL ========= */
  const images = document.querySelectorAll('.carousel img');
  let current = 0;
  if (images.length) {
    setInterval(() => {
      images[current].classList.remove('active');
      current = (current + 1) % images.length;
      images[current].classList.add('active');
    }, 4000); // troca a cada 4s
  }

  /* ========= CONTADOR ========= */
  const cdEl = document.getElementById('countdown');
  const cdDays = document.getElementById('cd-days');
  const cdHours = document.getElementById('cd-hours');
  const cdMins = document.getElementById('cd-mins');
  const cdSecs = document.getElementById('cd-secs');

  if (cdEl && cdDays && cdHours && cdMins && cdSecs) {
    // Data-alvo no atributo data-target (ISO com offset -03:00)
    const targetIso = cdEl.getAttribute('data-target') || '2025-08-16T20:00:00-03:00';
    const targetTime = new Date(targetIso).getTime();

    const pad2 = (n) => String(n).padStart(2, '0');

    const tick = () => {
      const now = Date.now();
      let delta = Math.max(0, targetTime - now);

      const days = Math.floor(delta / (1000 * 60 * 60 * 24));
      delta -= days * (1000 * 60 * 60 * 24);
      const hours = Math.floor(delta / (1000 * 60 * 60));
      delta -= hours * (1000 * 60 * 60);
      const mins = Math.floor(delta / (1000 * 60));
      delta -= mins * (1000 * 60);
      const secs = Math.floor(delta / 1000);

      cdDays.textContent = pad2(days);
      cdHours.textContent = pad2(hours);
      cdMins.textContent = pad2(mins);
      cdSecs.textContent = pad2(secs);

      // Quando chegar, muda a mensagem do CTA automaticamente
      if (targetTime - now <= 0) {
        cdEl.title = 'Sorteio hoje!';
        const cta = document.querySelector('.btn-primary');
        if (cta) cta.textContent = '🎟️ Participar agora (Sorteio hoje!)';
        clearInterval(timer);
      }
    };

    tick();
    const timer = setInterval(tick, 1000);
  }
});

