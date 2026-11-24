/* ==========================================================================
   Nile Smile IVF Concierge (Arabic) — Interactive Script
   Self-contained for ivf.nilesmileconcierge.com/ar/
   ========================================================================== */

(() => {
  'use strict';

  const CONCIERGE_WHATSAPP = '201503308333';

  const COUNTRY_PHONE_HINTS = {
    'المملكة العربية السعودية': '+966 5X XXX XXXX',
    'الإمارات العربية المتحدة': '+971 5X XXX XXXX',
    'الكويت': '+965 XXXX XXXX',
    'قطر': '+974 XXXX XXXX',
    'البحرين': '+973 XXXX XXXX',
    'سلطنة عُمان': '+968 9XXX XXXX',
    'دولة أخرى': '+XX XXX XXX XXXX',
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
     2. Gentle Scroll Reveal Animations
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
      const packageChoice = packageSelect?.value || 'استشارة سرية عامة للحقن المجهري';
      const femalePref = femaleCoordinatorCheck?.checked
        ? 'نعم — يفضّل التواصل عبر منسقة نسائية'
        : 'لا يوجد تفضيل محدد';

      const digitsCount = whatsapp.replace(/\D/g, '').length;

      if (name.length < 2) {
        showError('فضلاً أدخلي الاسم الأول أو الاسم المستعار الذي تفضلينه لنخاطبكِ بكل ود.');
        nameInput?.focus();
        return;
      }

      if (digitsCount < 8) {
        showError('يرجى إدخال رقم واتساب صحيح مع رمز الدولة (8 أرقام على الأقل).');
        whatsappInput?.focus();
        return;
      }

      if (!country) {
        showError('فضلاً اختاري بلد الإقامة لنتمكن من تنسيق مواعيد السفر بدقة.');
        countrySelect?.focus();
        return;
      }

      if (!contactTime) {
        showError('يرجى اختيار الوقت الأنسب والأكثر خصوصية للتواصل معك.');
        contactTimeSelect?.focus();
        return;
      }

      const refCode = `NS-IVF-${Math.floor(1000 + Math.random() * 9000)}`;

      const messageLines = [
        `طلب استشارة طبية سرية — الحقن المجهري (${refCode})`,
        `الاسم / اللقب المفضّل: ${name}`,
        `رقم الواتساب: ${whatsapp}`,
        `بلد الإقامة: ${country}`,
        `الوقت المفضّل للتواصل: ${contactTime}`,
        `الباقة / الاستفسار: ${packageChoice}`,
        `تفضيل المنسقة النسائية: ${femalePref}`,
      ];

      const waUrl = `https://wa.me/${CONCIERGE_WHATSAPP}?text=${encodeURIComponent(messageLines.join('\n'))}`;

      if (whatsappLaunchBtn) {
        whatsappLaunchBtn.href = waUrl;
      }

      if (successSummaryText) {
        successSummaryText.textContent = `شكراً لثقتكِ الغالية، ${name}. تم تجهيز ملفكِ السري برقم مرجعي (${refCode}). اضغطي أدناه لبدء محادثة واتساب خاصة ومشفّرة مع ${femaleCoordinatorCheck?.checked ? 'منسقتكِ النسائية' : 'فريق الرعاية'} في الوقت الذي اخترتِه (${contactTime}).`;
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
