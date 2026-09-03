(() => {
  document.documentElement.classList.add('js');

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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
    }, { threshold: 0.12 });
    revealNodes.forEach((node) => observer.observe(node));
  }

  const copyButton = document.querySelector('[data-copy-result]');
  const toast = document.querySelector('[data-toast]');

  copyButton?.addEventListener('click', async () => {
    const result = copyButton.dataset.result;
    const copy = `My Fourfold result is ${result}. Take the test: ${window.location.origin}`;

    try {
      await navigator.clipboard.writeText(copy);
    } catch {
      const field = document.createElement('textarea');
      field.value = copy;
      field.setAttribute('readonly', '');
      field.style.position = 'fixed';
      field.style.opacity = '0';
      document.body.appendChild(field);
      field.select();
      document.execCommand('copy');
      field.remove();
    }

    copyButton.firstChild.textContent = 'Copied ';
    toast?.classList.add('is-visible');
    window.setTimeout(() => {
      copyButton.firstChild.textContent = 'Copy result ';
      toast?.classList.remove('is-visible');
    }, 2200);
  });

  const form = document.querySelector('[data-quiz-form]');
  if (!form) return;

  const questions = [...form.querySelectorAll('.quiz-question')];
  const total = questions.length;
  const progressFill = document.querySelector('[data-progress-fill]');
  const currentLabel = document.querySelector('[data-current-question]');
  const previousButton = document.querySelector('[data-prev-question]');
  const submitButton = document.querySelector('[data-submit-quiz]');
  const exitButton = document.querySelector('[data-exit-test]');
  const exitDialog = document.querySelector('[data-exit-dialog]');
  const closeDialogButtons = [...document.querySelectorAll('[data-close-dialog]')];
  const exitAnyway = exitDialog?.querySelector('a');
  const storageKey = 'fourfold-quiz-progress';
  const tones = ['#a79ee8', '#ee977f', '#91c8ad', '#8eb8d2'];
  let current = 0;
  let advanceTimer;

  try {
    const saved = JSON.parse(sessionStorage.getItem(storageKey) || '{}');
    Object.entries(saved.answers || {}).forEach(([name, value]) => {
      const input = form.querySelector(`input[name="${CSS.escape(name)}"][value="${CSS.escape(value)}"]`);
      if (input) input.checked = true;
    });
    current = Math.min(Math.max(Number(saved.current) || 0, 0), total - 1);
  } catch {
    sessionStorage.removeItem(storageKey);
  }

  const saveProgress = () => {
    const answers = {};
    new FormData(form).forEach((value, key) => { answers[key] = value; });
    sessionStorage.setItem(storageKey, JSON.stringify({ current, answers }));
  };

  const syncChoices = (question) => {
    question.querySelectorAll('.choice').forEach((choice) => {
      const input = choice.querySelector('input');
      choice.classList.toggle('is-selected', Boolean(input?.checked));
    });
  };

  const renderQuestion = ({ focus = false } = {}) => {
    document.documentElement.style.setProperty('--quiz-accent', tones[current % tones.length]);
    questions.forEach((question, index) => {
      const isActive = index === current;
      question.hidden = !isActive;
      question.setAttribute('aria-hidden', String(!isActive));
      question.classList.toggle('is-active', isActive);
      if (isActive) syncChoices(question);
    });

    const shown = current + 1;
    if (currentLabel) currentLabel.textContent = String(shown).padStart(2, '0');
    if (progressFill) progressFill.style.width = `${(shown / total) * 100}%`;
    if (previousButton) previousButton.disabled = current === 0;

    const currentAnswered = Boolean(questions[current]?.querySelector('input:checked'));
    submitButton?.classList.toggle('is-visible', current === total - 1 && currentAnswered);

    saveProgress();
    if (focus) questions[current]?.querySelector('h1')?.focus({ preventScroll: true });
  };

  const goTo = (index, options = {}) => {
    window.clearTimeout(advanceTimer);
    current = Math.min(Math.max(index, 0), total - 1);
    renderQuestion(options);
  };

  questions.forEach((question, index) => {
    question.querySelectorAll('input[type="radio"]').forEach((input) => {
      input.addEventListener('change', () => {
        syncChoices(question);
        saveProgress();

        if (index === total - 1) {
          submitButton?.classList.add('is-visible');
          advanceTimer = window.setTimeout(() => {
            if (typeof form.requestSubmit === 'function') form.requestSubmit();
            else form.submit();
          }, reducedMotion ? 0 : 360);
          return;
        }

        advanceTimer = window.setTimeout(
          () => goTo(index + 1, { focus: true }),
          reducedMotion ? 0 : 360,
        );
      });
    });
  });

  previousButton?.addEventListener('click', () => goTo(current - 1, { focus: true }));
  form.addEventListener('submit', () => sessionStorage.removeItem(storageKey));

  window.addEventListener('keydown', (event) => {
    if (exitDialog?.open || event.metaKey || event.ctrlKey || event.altKey) return;
    const key = event.key.toLowerCase();

    if ((key === 'backspace' || key === 'arrowup') && current > 0) {
      event.preventDefault();
      goTo(current - 1, { focus: true });
      return;
    }

    const options = [...questions[current].querySelectorAll('input[type="radio"]')];
    let target;
    if (key === 'a' || key === '1' || key === 'arrowleft') target = options[0];
    if (key === 'b' || key === '2' || key === 'arrowright') target = options[1];
    if (!target) return;

    event.preventDefault();
    target.checked = true;
    target.dispatchEvent(new Event('change', { bubbles: true }));
  });

  exitButton?.addEventListener('click', () => exitDialog?.showModal());
  closeDialogButtons.forEach((button) => button.addEventListener('click', () => exitDialog?.close()));
  exitDialog?.addEventListener('click', (event) => {
    if (event.target === exitDialog) exitDialog.close();
  });
  exitAnyway?.addEventListener('click', () => sessionStorage.removeItem(storageKey));

  renderQuestion();
})();
