/* ==========================================================================
   Nile Smile IVF Concierge — Interactive Script
   Standalone for ivf.nilesmileconcierge.com (English)
   Progressive enhancement only: every feature degrades gracefully.
   ========================================================================== */

(() => {
  'use strict';

  const CONCIERGE_WHATSAPP = '201503308333';
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------------------------------
     1. Fixed Header Elevation
     ------------------------------------------------------------------------ */
  const siteHeader = document.getElementById('siteHeader');

  if (siteHeader) {
    const updateHeaderShadow = () => {
      siteHeader.classList.toggle('is-scrolled', window.scrollY > 12);
    };
    window.addEventListener('scroll', updateHeaderShadow, { passive: true });
    updateHeaderShadow();
  }

  /* ------------------------------------------------------------------------
     2. Mobile Navigation (fixed drawer + backdrop + focus restore)
     ------------------------------------------------------------------------ */
  const menuToggle = document.getElementById('menuToggle');
  const mobileMenu = document.getElementById('mobileMenu');
  const navBackdrop = document.getElementById('navBackdrop');
  const desktopNav = window.matchMedia('(min-width: 1024px)');

  if (menuToggle && mobileMenu) {
    const setMenuState = (open, restoreFocus = false) => {
      menuToggle.setAttribute('aria-expanded', String(open));
      menuToggle.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');
      mobileMenu.hidden = !open;
      if (navBackdrop) navBackdrop.hidden = !open;
      document.body.classList.toggle('nav-open', open);

      if (open) {
        const firstItem = mobileMenu.querySelector('a, button');
        firstItem?.focus({ preventScroll: true });
      } else if (restoreFocus) {
        menuToggle.focus();
      }
    };

    menuToggle.addEventListener('click', () => {
      setMenuState(menuToggle.getAttribute('aria-expanded') !== 'true');
    });

    mobileMenu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => setMenuState(false));
    });

    navBackdrop?.addEventListener('click', () => setMenuState(false, true));

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
        setMenuState(false, true);
      }
    });

    desktopNav.addEventListener('change', (event) => {
      if (event.matches && menuToggle.getAttribute('aria-expanded') === 'true') {
        setMenuState(false);
      }
    });
  }

  /* ------------------------------------------------------------------------
     3. Gentle Scroll Reveal (respects reduced motion)
     ------------------------------------------------------------------------ */
  const revealItems = document.querySelectorAll('.reveal');

  if (revealItems.length) {
    if (prefersReducedMotion || !('IntersectionObserver' in window)) {
      revealItems.forEach((el) => el.classList.add('is-visible'));
    } else {
      const revealObserver = new IntersectionObserver(
        (entries, observer) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add('is-visible');
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.12, rootMargin: '0px 0px -30px 0px' }
      );

      revealItems.forEach((el) => revealObserver.observe(el));
    }
  }

  /* ------------------------------------------------------------------------
     4. Accessible FAQ Accordion
        One panel open at a time; aria-expanded and [hidden] stay in sync.
     ------------------------------------------------------------------------ */
  const faqItems = Array.from(document.querySelectorAll('.faq-item'));

  const setFaqState = (item, open) => {
    const trigger = item.querySelector('.faq-trigger');
    const panelId = trigger ? trigger.getAttribute('aria-controls') : null;
    const panel = panelId ? document.getElementById(panelId) : item.querySelector('.faq-panel');

    if (!trigger || !panel) return;

    trigger.setAttribute('aria-expanded', String(open));
    panel.hidden = !open;
  };

  faqItems.forEach((item) => {
    const trigger = item.querySelector('.faq-trigger');
    if (!trigger) return;

    // Normalise the initial state so markup and ARIA never disagree.
    setFaqState(item, trigger.getAttribute('aria-expanded') === 'true');

    trigger.addEventListener('click', () => {
      const willOpen = trigger.getAttribute('aria-expanded') !== 'true';

      faqItems.forEach((other) => {
        if (other !== item) setFaqState(other, false);
      });

      setFaqState(item, willOpen);
    });
  });

  /* ------------------------------------------------------------------------
     5. Privacy Charter Modal (aria-hidden + focus management + focus trap)
     ------------------------------------------------------------------------ */
  const privacyModal = document.getElementById('privacyModal');

  if (privacyModal) {
    const openTriggers = [
      document.getElementById('openPrivacyModal'),
      document.getElementById('footerPrivacyBtn'),
    ].filter(Boolean);

    const closeTriggers = [
      document.getElementById('closePrivacyModal'),
      document.getElementById('acceptPrivacyModal'),
    ].filter(Boolean);

    let lastFocusedElement = null;

    const getFocusable = () =>
      Array.from(
        privacyModal.querySelectorAll(
          'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
        )
      ).filter((el) => el.offsetParent !== null || el === document.activeElement);

    const openModal = (trigger) => {
      lastFocusedElement = trigger || document.activeElement;
      privacyModal.hidden = false;
      privacyModal.classList.add('is-open');
      privacyModal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';

      const firstFocusable = document.getElementById('closePrivacyModal') || getFocusable()[0] || privacyModal;
      firstFocusable.focus();
    };

    const closeModal = () => {
      privacyModal.classList.remove('is-open');
      privacyModal.setAttribute('aria-hidden', 'true');
      privacyModal.hidden = true;
      document.body.style.overflow = '';

      if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
        lastFocusedElement.focus();
      }
    };

    openTriggers.forEach((btn) => {
      btn.addEventListener('click', () => openModal(btn));
    });

    closeTriggers.forEach((btn) => {
      btn.addEventListener('click', closeModal);
    });

    privacyModal.addEventListener('click', (event) => {
      if (event.target === privacyModal) closeModal();
    });

    document.addEventListener('keydown', (event) => {
      if (privacyModal.hidden) return;

      if (event.key === 'Escape') {
        event.preventDefault();
        closeModal();
        return;
      }

      if (event.key === 'Tab') {
        const focusable = getFocusable();
        if (!focusable.length) return;

        const first = focusable[0];
        const last = focusable[focusable.length - 1];

        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
    });
  }

  /* ------------------------------------------------------------------------
     6. Package Selection Pre-Fill
     ------------------------------------------------------------------------ */
  const packageField = document.getElementById('patientPackage');

  document.querySelectorAll('[data-package]').forEach((trigger) => {
    trigger.addEventListener('click', () => {
      if (!packageField) return;
      packageField.value = trigger.getAttribute('data-package') || '';
    });
  });

  /* ------------------------------------------------------------------------
     7. Confidential Lead Form
        Validate -> build a discreet, URL-encoded WhatsApp message ->
        hide the form -> reveal the confirmation screen.
     ------------------------------------------------------------------------ */
  const leadForm = document.getElementById('consultForm');
  const nameInput = document.getElementById('patientName');
  const countrySelect = document.getElementById('patientCountry');
  const notesInput = document.getElementById('patientNotes');
  const nameError = document.getElementById('name-error');
  const countryError = document.getElementById('country-error');
  const formError = document.getElementById('formError');
  const formSuccess = document.getElementById('formSuccess');
  const successHeading = document.getElementById('successHeading');
  const successSummaryText = document.getElementById('successSummaryText');
  const whatsappLaunchBtn = document.getElementById('whatsappLaunchBtn');
  const resetFormBtn = document.getElementById('resetFormBtn');

  if (leadForm) {
    const setFieldError = (field, errorEl, message) => {
      if (!errorEl) return;
      if (message) {
        errorEl.textContent = message;
        errorEl.hidden = false;
        field?.setAttribute('aria-invalid', 'true');
      } else {
        errorEl.textContent = '';
        errorEl.hidden = true;
        field?.removeAttribute('aria-invalid');
      }
    };

    const clearErrors = () => {
      setFieldError(nameInput, nameError, '');
      setFieldError(countrySelect, countryError, '');
      if (formError) {
        formError.textContent = '';
        formError.classList.remove('is-visible');
      }
    };

    const showFormError = (message) => {
      if (!formError) return;
      formError.textContent = message;
      formError.classList.add('is-visible');
    };

    leadForm.addEventListener('submit', (event) => {
      event.preventDefault();
      clearErrors();

      const name = (nameInput?.value || '').trim();
      const country = countrySelect?.value || '';
      const packageChoice = (packageField?.value || '').trim() || 'General Confidential IVF Consultation';
      const notes = (notesInput?.value || '').trim();

      let firstInvalidField = null;

      if (name.length < 2) {
        setFieldError(nameInput, nameError, 'Please share a first name or alias of at least 2 characters.');
        firstInvalidField = firstInvalidField || nameInput;
      }

      if (!country) {
        setFieldError(countrySelect, countryError, 'Please select your country of residence.');
        firstInvalidField = firstInvalidField || countrySelect;
      }

      if (firstInvalidField) {
        showFormError('Please review the highlighted fields before continuing.');
        firstInvalidField.focus();
        return;
      }

      // Discreet reference code (no personal data).
      const refCode = `NS-IVF-${Math.floor(1000 + Math.random() * 9000)}`;

      const messageLines = [
        `Confidential IVF Concierge Inquiry (${refCode})`,
        `Name / Alias: ${name}`,
        `Country: ${country}`,
        `Interest: ${packageChoice}`,
      ];

      if (notes) {
        messageLines.push(`Notes: ${notes}`);
      }

      // encodeURIComponent keeps the payload safe inside the wa.me URL.
      const waUrl = `https://wa.me/${CONCIERGE_WHATSAPP}?text=${encodeURIComponent(messageLines.join('\n'))}`;

      if (whatsappLaunchBtn) {
        whatsappLaunchBtn.href = waUrl;
      }

      if (successSummaryText) {
        successSummaryText.textContent = `Thank you, ${name}. Your confidential reference code is ${refCode}. Tap below to open a private WhatsApp chat with our concierge team.`;
      }

      leadForm.hidden = true;
      if (formSuccess) {
        formSuccess.classList.add('is-visible');
        successHeading?.focus({ preventScroll: true });
        formSuccess.scrollIntoView({
          behavior: prefersReducedMotion ? 'auto' : 'smooth',
          block: 'center',
        });
      } else {
        window.open(waUrl, '_blank', 'noopener');
      }
    });

    if (resetFormBtn && formSuccess) {
      resetFormBtn.addEventListener('click', () => {
        formSuccess.classList.remove('is-visible');
        leadForm.hidden = false;
        clearErrors();
        nameInput?.focus();
      });
    }
  }
})();
