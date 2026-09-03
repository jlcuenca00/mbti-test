(() => {
  document.documentElement.classList.add('js');

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  // Lightweight reveal system.
  const revealNodes = [...document.querySelectorAll('[data-reveal]')];
  if (reducedMotion || !('IntersectionObserver' in window)) {
    revealNodes.forEach((node) => node.classList.add('is-visible'));
  } else {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.16 });
    revealNodes.forEach((node) => observer.observe(node));
  }

  // Custom crosshair cursor for desktop only.
  if (finePointer && !reducedMotion) {
    const cursor = document.createElement('div');
    cursor.className = 'fx-cursor';
    cursor.setAttribute('aria-hidden', 'true');
    document.body.appendChild(cursor);

    let x = innerWidth / 2;
    let y = innerHeight / 2;
    let tx = x;
    let ty = y;

    const loop = () => {
      x += (tx - x) * 0.28;
      y += (ty - y) * 0.28;
      cursor.style.transform = `translate3d(${x}px, ${y}px, 0) translate(-50%, -50%)`;
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);

    addEventListener('pointermove', (event) => {
      tx = event.clientX;
      ty = event.clientY;
      cursor.style.opacity = '1';
      const interactive = event.target.closest('a, button, label, input, textarea');
      cursor.classList.toggle('is-active', Boolean(interactive));
    }, { passive: true });

    document.documentElement.addEventListener('mouseleave', () => {
      cursor.style.opacity = '0';
    });
  }

  // Progressive, single-question quiz experience. Backend POST contract stays unchanged.
  const form = document.querySelector('[data-quiz-form]');
  if (!form) return;

  const questions = [...form.querySelectorAll('.quiz-question')];
  const total = questions.length;
  const progress = document.querySelector('[data-progress-fill]');
  const counter = document.querySelector('[data-quiz-counter]');
  const currentLabel = document.querySelector('[data-current-question]');
  const previousButton = document.querySelector('[data-prev-question]');
  const submitButton = document.querySelector('[data-submit-quiz]');
  let current = 0;
  let advanceTimer = null;

  const update = () => {
    questions.forEach((question, index) => {
      const active = index === current;
      question.hidden = !active;
      question.setAttribute('aria-hidden', String(!active));
    });

    const shown = current + 1;
    if (counter) counter.textContent = `${String(shown).padStart(2, '0')} / ${String(total).padStart(2, '0')}`;
    if (currentLabel) currentLabel.textContent = `QUESTION ${String(shown).padStart(2, '0')}`;
    if (progress) progress.style.width = `${(shown / total) * 100}%`;
    if (previousButton) previousButton.style.visibility = current === 0 ? 'hidden' : 'visible';

    const selected = questions[current]?.querySelector('input[type="radio"]:checked');
    if (submitButton) {
      submitButton.classList.toggle('is-visible', current === total - 1 && Boolean(selected));
    }
  };

  const go = (index) => {
    current = Math.max(0, Math.min(total - 1, index));
    update();
    questions[current]?.querySelector('.question-copy')?.focus?.({ preventScroll: true });
  };

  questions.forEach((question, index) => {
    const options = [...question.querySelectorAll('.option-card')];
    options.forEach((option) => {
      const input = option.querySelector('input[type="radio"]');
      if (!input) return;

      const sync = () => {
        options.forEach((item) => item.classList.toggle('is-selected', item.querySelector('input')?.checked));
        if (submitButton) {
          submitButton.classList.toggle('is-visible', index === total - 1 && Boolean(question.querySelector('input:checked')));
        }
      };

      input.addEventListener('change', () => {
        sync();
        clearTimeout(advanceTimer);
        if (index < total - 1) {
          advanceTimer = setTimeout(() => go(index + 1), reducedMotion ? 0 : 240);
        }
      });
      sync();
    });
  });

  previousButton?.addEventListener('click', () => go(current - 1));

  addEventListener('keydown', (event) => {
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    const activeQuestion = questions[current];
    if (!activeQuestion) return;
    const inputs = [...activeQuestion.querySelectorAll('input[type="radio"]')];

    const key = event.key.toLowerCase();
    let target = null;
    if (key === 'a' || key === '1' || key === 'arrowleft') target = inputs[0];
    if (key === 'b' || key === '2' || key === 'arrowright') target = inputs[1];
    if (!target) return;

    event.preventDefault();
    target.checked = true;
    target.dispatchEvent(new Event('change', { bubbles: true }));
  });

  update();
})();
