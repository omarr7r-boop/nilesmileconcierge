/* ==========================================================================
   Nile Smile IVF Concierge — Interactive Script
   Self-contained for ivf.nilesmileconcierge.com
   ========================================================================== */

(() => {
  'use strict';

  const CONCIERGE_WHATSAPP = '201503308333';

  // Country phone hint mapping for smoother Gulf UX
  const COUNTRY_PHONE_HINTS = {
    'Saudi Arabia': '+966 5X XXX XXXX',
    'United Arab Emirates': '+971 5X XXX XXXX',
    Kuwait: '+965 XXXX XXXX',
    Qatar: '+974 XXXX XXXX',
    Bahrain: '+973 XXXX XXXX',
    Oman: '+968 9XXX XXXX',
    Other: '+XX XXX XXX XXXX',
  };

  /* ------------------------------------------------------------------------
     1. Sticky Header Elevation & Mobile Navigation
     ------------------------------------------------------------------------ */
  const siteHeader = document.getElementById('siteHeader');
  const menuToggle = document.getElementById('menuToggle');
  const mobileMenu = document.getElementById('mobileMenu');

  if (siteHeader) {
    const updateHeaderShadow = () => {
      siteHeader.classList.toggle('is-scrolled', window.scrollY > 12);
    };
    window.addEventListener('scroll', updateHeaderShadow, { passive: true });
    updateHeaderShadow();
  }

  if (menuToggle && mobileMenu) {
    const closeMobileMenu = () => {
      mobileMenu.classList.remove('is-open');
      menuToggle.setAttribute('aria-expanded', 'false');
    };

    menuToggle.addEventListener('click', () => {
      const isOpen = mobileMenu.classList.toggle('is-open');
      menuToggle.setAttribute('aria-expanded', String(isOpen));
    });

    mobileMenu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', closeMobileMenu);
    });
  }

  /* ------------------------------------------------------------------------
     2. Gentle Scroll Reveal Animations (Respects Reduced Motion)
     ------------------------------------------------------------------------ */
  const revealItems = document.querySelectorAll('.reveal');
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (prefersReducedMotion || !('IntersectionObserver' in window)) {
    revealItems.forEach((el) => el.classList.add('is-visible'));
  } else {
    const observer = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -30px 0px' }
    );

    revealItems.forEach((el) => observer.observe(el));
  }

  /* ------------------------------------------------------------------------
     3. Privacy Charter Modal
     ------------------------------------------------------------------------ */
  const privacyModal = document.getElementById('privacyModal');
  const openPrivacyTriggers = [
    document.getElementById('openPrivacyModal'),
    document.getElementById('footerPrivacyBtn'),
  ].filter(Boolean);
  const closePrivacyTriggers = [
    document.getElementById('closePrivacyModal'),
    document.getElementById('acceptPrivacyModal'),
  ].filter(Boolean);

  const togglePrivacyModal = (open) => {
    if (!privacyModal) return;
    privacyModal.classList.toggle('is-open', open);
    privacyModal.setAttribute('aria-hidden', String(!open));
    if (open) {
      document.getElementById('closePrivacyModal')?.focus();
    }
  };

  openPrivacyTriggers.forEach((btn) => {
    btn.addEventListener('click', () => togglePrivacyModal(true));
  });

  closePrivacyTriggers.forEach((btn) => {
    btn.addEventListener('click', () => togglePrivacyModal(false));
  });

  if (privacyModal) {
    privacyModal.addEventListener('click', (event) => {
      if (event.target === privacyModal) {
        togglePrivacyModal(false);
      }
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && privacyModal.classList.contains('is-open')) {
        togglePrivacyModal(false);
      }
    });
  }

  /* ------------------------------------------------------------------------
     4. Accessible FAQ Accordion
     ------------------------------------------------------------------------ */
  document.querySelectorAll('.faq-item').forEach((item) => {
    const trigger = item.querySelector('.faq-trigger');
    if (!trigger) return;

    trigger.addEventListener('click', () => {
      const currentlyOpen = item.getAttribute('data-open') === 'true';
      item.setAttribute('data-open', String(!currentlyOpen));
      trigger.setAttribute('aria-expanded', String(!currentlyOpen));
    });
  });

  /* ------------------------------------------------------------------------
     5. Package Selection Pre-Fill
     ------------------------------------------------------------------------ */
  const packageSelect = document.getElementById('packageInterest');
  const formSection = document.getElementById('confidential-form');
  const nameInput = document.getElementById('patientName');

  document.querySelectorAll('.select-package-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const selectedPkg = btn.getAttribute('data-package');
      if (packageSelect && selectedPkg) {
        packageSelect.value = selectedPkg;
      }
      formSection?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setTimeout(() => nameInput?.focus({ preventScroll: true }), 550);
    });
  });

  /* ------------------------------------------------------------------------
     6. Confidential Lead Form Validation & Private WhatsApp Dispatch
     ------------------------------------------------------------------------ */
  const leadForm = document.getElementById('ivfLeadForm');
  const countrySelect = document.getElementById('patientCountry');
  const whatsappInput = document.getElementById('patientWhatsapp');
  const contactTimeSelect = document.getElementById('contactTime');
  const femaleCoordinatorCheck = document.getElementById('femaleCoordinator');
  const formError = document.getElementById('formError');
  const formSuccess = document.getElementById('formSuccess');
  const successSummaryText = document.getElementById('successSummaryText');
  const whatsappLaunchBtn = document.getElementById('whatsappLaunchBtn');
  const resetFormBtn = document.getElementById('resetFormBtn');

  if (countrySelect && whatsappInput) {
    countrySelect.addEventListener('change', () => {
      const hint = COUNTRY_PHONE_HINTS[countrySelect.value];
      if (hint) {
        whatsappInput.placeholder = hint;
      }
    });
  }

  const showError = (message) => {
    if (!formError) return;
    formError.textContent = message;
    formError.classList.add('is-visible');
  };

  const clearError = () => {
    if (!formError) return;
    formError.textContent = '';
    formError.classList.remove('is-visible');
  };

  if (leadForm) {
    leadForm.addEventListener('submit', (event) => {
      event.preventDefault();
      clearError();

      const name = nameInput?.value.trim() || '';
      const whatsapp = whatsappInput?.value.trim() || '';
      const country = countrySelect?.value || '';
      const contactTime = contactTimeSelect?.value || '';
      const packageChoice = packageSelect?.value || 'General Confidential IVF Consultation';
      const femalePref = femaleCoordinatorCheck?.checked
        ? 'Yes — Female Coordinator Requested'
        : 'No preference';

      const digitsCount = whatsapp.replace(/\D/g, '').length;

      if (name.length < 2) {
        showError('Please share your first name or preferred initials so we know how to address you warmly.');
        nameInput?.focus();
        return;
      }

      if (digitsCount < 8) {
        showError('Please enter a valid WhatsApp number including your country code (at least 8 digits).');
        whatsappInput?.focus();
        return;
      }

      if (!country) {
        showError('Please select your country of residence so we can tailor travel timing.');
        countrySelect?.focus();
        return;
      }

      if (!contactTime) {
        showError('Please choose your preferred private contact time.');
        contactTimeSelect?.focus();
        return;
      }

      // Generate discreet reference ID
      const refCode = `NS-IVF-${Math.floor(1000 + Math.random() * 9000)}`;

      const messageLines = [
        `Confidential IVF Concierge Inquiry (${refCode})`,
        `Name / Alias: ${name}`,
        `WhatsApp: ${whatsapp}`,
        `Country: ${country}`,
        `Preferred Contact Time: ${contactTime}`,
        `Interest: ${packageChoice}`,
        `Female Coordinator: ${femalePref}`,
      ];

      const waUrl = `https://wa.me/${CONCIERGE_WHATSAPP}?text=${encodeURIComponent(messageLines.join('\n'))}`;

      if (whatsappLaunchBtn) {
        whatsappLaunchBtn.href = waUrl;
      }

      if (successSummaryText) {
        successSummaryText.textContent = `Thank you, ${name}. Your confidential reference code is ${refCode}. Tap below to open a private WhatsApp chat with our concierge (${femaleCoordinatorCheck?.checked ? 'Female Coordinator requested' : 'Dedicated Care Team'}) at your preferred time (${contactTime}).`;
      }

      leadForm.style.display = 'none';
      formSuccess?.classList.add('is-visible');
    });
  }

  if (resetFormBtn && leadForm && formSuccess) {
    resetFormBtn.addEventListener('click', () => {
      formSuccess.classList.remove('is-visible');
      leadForm.style.display = 'flex';
      clearError();
    });
  }
})();
