/* ==========================================================================
   Nile Smile IVF Concierge — MPA Shared Navigation Script
   Phase 1: Header scroll state, mobile slide-out drawer, footer year.
   Progressive enhancement only: all links and content remain usable without JS.
   ========================================================================== */

(() => {
  'use strict';

  const header = document.getElementById('siteHeader');
  const menuToggle = document.getElementById('menuToggle');
  const drawer = document.getElementById('mobileDrawer');
  const scrim = document.getElementById('navScrim');
  const closeButton = document.getElementById('drawerClose');
  const desktopQuery = window.matchMedia('(min-width: 1180px)');

  const FOCUSABLE =
    'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

  /* ------------------------------------------------------------------------
     1. Transparent → frosted-glass header on scroll
     ------------------------------------------------------------------------ */
  if (header) {
    const syncHeader = () => {
      header.classList.toggle('is-scrolled', window.scrollY > 16);
    };

    window.addEventListener('scroll', syncHeader, { passive: true });
    syncHeader();
  }

  /* ------------------------------------------------------------------------
     2. Mobile slide-out drawer
     ------------------------------------------------------------------------ */
  if (menuToggle && drawer && scrim) {
    let lastFocused = null;

    const setDrawerState = (open, restoreFocus = false) => {
      menuToggle.setAttribute('aria-expanded', String(open));
      menuToggle.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');

      drawer.classList.toggle('is-open', open);
      scrim.classList.toggle('is-open', open);
      drawer.setAttribute('aria-hidden', String(!open));
      document.body.classList.toggle('drawer-open', open);

      if (open) {
        lastFocused = document.activeElement;
        drawer.removeAttribute('inert');

        // Wait for the inert removal + visibility change to be applied,
        // then move focus in after the current click dispatch completes.
        requestAnimationFrame(() => {
          window.setTimeout(() => {
            const firstFocusable = drawer.querySelector(FOCUSABLE);
            firstFocusable?.focus({ preventScroll: true });
          }, 0);
        });
      } else {
        drawer.setAttribute('inert', '');

        if (restoreFocus) {
          const target = lastFocused && typeof lastFocused.focus === 'function' ? lastFocused : menuToggle;
          target.focus({ preventScroll: true });
        }
      }
    };

    menuToggle.addEventListener('click', () => {
      const isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
      setDrawerState(!isOpen);
    });

    closeButton?.addEventListener('click', () => setDrawerState(false, true));
    scrim.addEventListener('click', () => setDrawerState(false, true));

    drawer.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => setDrawerState(false));
    });

    document.addEventListener('keydown', (event) => {
      const isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
      if (!isOpen) return;

      if (event.key === 'Escape') {
        event.preventDefault();
        setDrawerState(false, true);
        return;
      }

      if (event.key !== 'Tab') return;

      const focusable = Array.from(drawer.querySelectorAll(FOCUSABLE)).filter(
        (element) => element.offsetParent !== null || element === document.activeElement
      );

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
    });

    desktopQuery.addEventListener('change', (event) => {
      if (event.matches && menuToggle.getAttribute('aria-expanded') === 'true') {
        setDrawerState(false);
      }
    });
  }

  /* ------------------------------------------------------------------------
     3. Consultation intake form
     Builds a private summary and hands it to WhatsApp. Nothing is stored
     on this website and no data leaves the browser until the user sends it.
     ------------------------------------------------------------------------ */
  const consultForm = document.getElementById('consultForm');

  if (consultForm) {
    const status = document.getElementById('formStatus');

    consultForm.addEventListener('submit', (event) => {
      event.preventDefault();

      if (!consultForm.reportValidity()) {
        return;
      }

      const data = new FormData(consultForm);
      const get = (key) => String(data.get(key) || '').trim();
      const isArabic = document.documentElement.lang === 'ar';
      const lines = isArabic
        ? [
            'السلام عليكم، نايل سمايل.',
            '',
            'أرغب في استشارة خاصة.',
            '',
            'الاسم: ' + get('firstName'),
            'واتساب: ' + get('whatsapp'),
            'البريد: ' + (get('email') || 'غير مذكور'),
            'بلد الإقامة: ' + get('country'),
            'الاهتمام: ' + get('interest'),
            'علاج سابق: ' + get('history'),
            'اللغة المفضلة: ' + get('language'),
            'وقت البدء: ' + get('timeline'),
          ]
        : [
            'Hello Nile Smile IVF Concierge,',
            '',
            'I would like a confidential consultation.',
            '',
            'Name: ' + get('firstName'),
            'WhatsApp: ' + get('whatsapp'),
            'Email: ' + (get('email') || 'Not provided'),
            'Country: ' + get('country'),
            'Interested in: ' + get('interest'),
            'Previous treatment: ' + get('history'),
            'Preferred language: ' + get('language'),
            'Timeline: ' + get('timeline'),
          ];

      const notes = get('message');
      if (notes) {
        lines.push('', (isArabic ? 'ملاحظات: ' : 'Notes: ') + notes);
      }

      lines.push('', isArabic ? 'أوافق على التواصل معي بخصوصية.' : 'I consent to being contacted privately.');

      const url = 'https://wa.me/201503308333?text=' + encodeURIComponent(lines.join('\n'));
      window.open(url, '_blank', 'noopener');

      if (status) {
        status.hidden = false;
        status.textContent = isArabic
          ? 'فتحت رسالتك الخاصة في واتساب. إذا لم تفتح، راسلينا مباشرة على ‎+20 150 330 8333. لم يُخزَّن شيء على هذا الموقع.'
          : 'Your private summary has opened in WhatsApp. If it did not open, message us directly on +20 150 330 8333. Nothing has been stored on this website.';
        status.focus({ preventScroll: true });
      }
    });
  }

  /* ------------------------------------------------------------------------
     4. Footer year
     ------------------------------------------------------------------------ */
  const year = document.getElementById('year');
  if (year) {
    year.textContent = String(new Date().getFullYear());
  }
})();
