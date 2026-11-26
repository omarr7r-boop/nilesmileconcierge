/* ==========================================================================
   Nile Smile IVF Concierge (Arabic) — Interactive Script
   Standalone for ivf.nilesmileconcierge.com/ar/
   Progressive enhancement only: every feature degrades gracefully.
   ========================================================================== */

(() => {
  'use strict';

  const CONCIERGE_WHATSAPP = '201503308333';
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // تلميحات أرقام الواتساب حسب بلد الإقامة
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
     1. ارتفاع الهيدر عند التمرير
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
     2. قائمة الموبايل (درج ثابت + خلفية معتمة + إعادة التركيز)
     ------------------------------------------------------------------------ */
  const menuToggle = document.getElementById('menuToggle');
  const mobileMenu = document.getElementById('mobileMenu');
  const navBackdrop = document.getElementById('navBackdrop');
  const desktopNav = window.matchMedia('(min-width: 1024px)');

  if (menuToggle && mobileMenu) {
    const setMenuState = (open, restoreFocus = false) => {
      menuToggle.setAttribute('aria-expanded', String(open));
      menuToggle.setAttribute('aria-label', open ? 'إغلاق قائمة التنقل' : 'فتح قائمة التنقل');
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
     3. ظهور تدريجي لطيف عند التمرير (يحترم تقليل الحركة)
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
     4. أكورديون الأسئلة الشائعة
        سؤال واحد مفتوح في كل مرة، مع مزامنة aria-expanded و hidden.
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

    // توحيد الحالة الابتدائية حتى لا تتعارض الترميزات مع ARIA
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
     5. نافذة ميثاق الخصوصية (aria-hidden + إدارة التركيز + حصر التبويب)
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
     6. تعبئة الباقة المختارة مسبقاً
     ------------------------------------------------------------------------ */
  const packageSelect = document.getElementById('packageInterest');

  document.querySelectorAll('.select-package-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const selectedPackage = btn.getAttribute('data-package');
      if (packageSelect && selectedPackage) {
        packageSelect.value = selectedPackage;
      }
    });
  });

  /* ------------------------------------------------------------------------
     7. نموذج الاستشارة السرية
        تحقق -> رسالة واتساب مشفّرة -> إخفاء النموذج -> شاشة النجاح
     ------------------------------------------------------------------------ */
  const leadForm = document.getElementById('ivfLeadForm');
  const nameInput = document.getElementById('patientName');
  const whatsappInput = document.getElementById('patientWhatsapp');
  const countrySelect = document.getElementById('patientCountry');
  const contactTimeSelect = document.getElementById('contactTime');
  const femaleCoordinatorCheck = document.getElementById('femaleCoordinator');
  const nameError = document.getElementById('name-error');
  const whatsappError = document.getElementById('whatsapp-error');
  const countryError = document.getElementById('country-error');
  const timeError = document.getElementById('time-error');
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
      setFieldError(whatsappInput, whatsappError, '');
      setFieldError(countrySelect, countryError, '');
      setFieldError(contactTimeSelect, timeError, '');
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
      const whatsapp = (whatsappInput?.value || '').trim();
      const country = countrySelect?.value || '';
      const contactTime = contactTimeSelect?.value || '';
      const packageChoice = packageSelect?.value || 'استشارة سرية عامة للحقن المجهري';
      const femalePref = femaleCoordinatorCheck?.checked
        ? 'نعم — يفضّل التواصل عبر منسقة نسائية'
        : 'لا يوجد تفضيل محدد';

      const digitsCount = whatsapp.replace(/\D/g, '').length;
      let firstInvalidField = null;

      if (name.length < 2) {
        setFieldError(nameInput, nameError, 'فضلاً أدخلي الاسم الأول أو الاسم المستعار الذي تفضلينه لنخاطبكِ بكل ود.');
        firstInvalidField = firstInvalidField || nameInput;
      }

      if (digitsCount < 8) {
        setFieldError(whatsappInput, whatsappError, 'يرجى إدخال رقم واتساب صحيح مع رمز الدولة (8 أرقام على الأقل).');
        firstInvalidField = firstInvalidField || whatsappInput;
      }

      if (!country) {
        setFieldError(countrySelect, countryError, 'فضلاً اختاري بلد الإقامة لنتمكن من تنسيق مواعيد السفر بدقة.');
        firstInvalidField = firstInvalidField || countrySelect;
      }

      if (!contactTime) {
        setFieldError(contactTimeSelect, timeError, 'يرجى اختيار الوقت الأنسب والأكثر خصوصية للتواصل معك.');
        firstInvalidField = firstInvalidField || contactTimeSelect;
      }

      if (firstInvalidField) {
        showFormError('يرجى مراجعة الحقول المحددة أعلاه قبل المتابعة.');
        firstInvalidField.focus();
        return;
      }

      // رقم مرجعي سري لا يحتوي على أي بيانات شخصية
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

      // encodeURIComponent يحمي البيانات داخل رابط واتساب
      const waUrl = `https://wa.me/${CONCIERGE_WHATSAPP}?text=${encodeURIComponent(messageLines.join('\n'))}`;

      if (whatsappLaunchBtn) {
        whatsappLaunchBtn.href = waUrl;
      }

      if (successSummaryText) {
        successSummaryText.textContent = `شكراً لثقتكِ الغالية، ${name}. تم تجهيز ملفكِ السري برقم مرجعي (${refCode}). اضغطي أدناه لبدء محادثة واتساب خاصة ومشفّرة مع ${femaleCoordinatorCheck?.checked ? 'منسقتكِ النسائية' : 'فريق الرعاية'} في الوقت الذي اخترتِه (${contactTime}).`;
      }

      leadForm.hidden = true;

      if (formSuccess) {
        formSuccess.classList.add('is-visible');
        formSuccess.setAttribute('tabindex', '-1');
        formSuccess.focus({ preventScroll: true });
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
        formSuccess.removeAttribute('tabindex');
        leadForm.hidden = false;
        clearErrors();
        nameInput?.focus();
      });
    }
  }
})();
