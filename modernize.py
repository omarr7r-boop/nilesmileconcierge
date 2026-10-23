#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nile Smile — Header Modernizer
================================
يستبدل نظام الهيدر القديم (مع كل تعارضاته) بهيدر حديث نظيف.

الاستخدام:
    python modernize.py index.html

اللي بيعمله:
    1. يعمل نسخة احتياطية (index.html.backup)
    2. يشيل الهيدر القديم + كل أكواد ZK_* المتعارضة
    3. يشيل شاشة اللوجو القديمة (logoIntro)
    4. يزرع هيدر جديد (HTML + CSS + JS) قبل <main>
    5. يضبط scroll offsets عشان الـ anchors تظبط
    6. يتحقق من النتيجة
"""

import re
import shutil
import sys
from pathlib import Path


# ============================================================
# NEW HEADER BLOCK — HTML + CSS + JS
# ============================================================
NEW_HEADER_BLOCK = r'''
<!-- ═══════════════════ HEADER — MODERN 2026 ═══════════════════ -->
<style id="modernHeaderStyles">
:root {
  --header-height: 72px;
  --header-bg: rgba(246, 243, 238, 0.88);
  --header-bg-scrolled: rgba(246, 243, 238, 0.97);
  --header-border: rgba(174, 145, 100, 0.2);
  --header-blur: 12px;
}
.site-header {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 1000;
  background: var(--header-bg);
  -webkit-backdrop-filter: blur(var(--header-blur)) saturate(180%);
  backdrop-filter: blur(var(--header-blur)) saturate(180%);
  border-bottom: 1px solid var(--header-border);
}
@supports (animation-timeline: scroll()) {
  .site-header {
    animation: headerScroll linear both;
    animation-timeline: scroll();
    animation-range: 0px 120px;
  }
}
@keyframes headerScroll {
  to {
    background: var(--header-bg-scrolled);
    box-shadow: 0 8px 32px rgba(79, 96, 112, 0.10);
  }
}
@media (prefers-reduced-motion: reduce) {
  .site-header { animation: none !important; }
}
.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  min-height: var(--header-height);
  max-width: 80rem;
  margin: 0 auto;
  padding: 0 1.25rem;
}
.logo {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-decoration: none;
  line-height: 1;
  flex-shrink: 0;
  gap: 0;
}
.logo-script {
  font-family: 'Italianno', cursive;
  font-size: 2.2rem;
  color: #4F6070;
  line-height: 0.9;
  animation: none !important;
  text-shadow: none !important;
}
.logo-sub {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: -4px;
}
.logo-sans {
  font-family: 'Montserrat', sans-serif;
  font-size: 0.55rem;
  font-weight: 700;
  letter-spacing: 0.25em;
  color: #4F6070;
  text-transform: uppercase;
}
.logo-tagline {
  font-family: 'Montserrat', sans-serif;
  font-size: 0.4rem;
  letter-spacing: 0.12em;
  color: #6B7D8E;
  text-transform: uppercase;
  margin-top: 2px;
  opacity: 0.8;
}
.main-nav { display: none; }
.nav-list {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  list-style: none;
  margin: 0;
  padding: 0;
}
.nav-link {
  position: relative;
  font-family: 'Montserrat', sans-serif;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #4F6070;
  text-decoration: none;
  padding: 0.5rem 0;
  transition: color 0.3s ease;
}
.nav-link::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 0;
  height: 1.5px;
  background: #AE9164;
  transition: width 0.35s cubic-bezier(0.22, 1, 0.36, 1), left 0.35s ease;
  transform: translateX(-50%);
}
.nav-link:hover { color: #AE9164; }
.nav-link:hover::after { width: 100%; }
.header-actions {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-shrink: 0;
}
.icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border: none;
  background: transparent;
  color: #4F6070;
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.icon-btn:hover { background: rgba(174, 145, 100, 0.12); color: #AE9164; }
.icon-btn:focus-visible { outline: 2px solid #AE9164; outline-offset: 2px; }
.header-cta {
  display: none;
  font-size: 0.68rem;
  padding: 0.65rem 1.2rem;
  white-space: nowrap;
}
.menu-toggle {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 26px;
  height: 18px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
}
.menu-toggle span {
  display: block;
  width: 100%;
  height: 2px;
  background: #4F6070;
  border-radius: 2px;
  transition: transform 0.3s ease, opacity 0.3s ease;
}
.menu-toggle[aria-expanded="true"] span:nth-child(1) { transform: translateY(8px) rotate(45deg); }
.menu-toggle[aria-expanded="true"] span:nth-child(2) { opacity: 0; }
.menu-toggle[aria-expanded="true"] span:nth-child(3) { transform: translateY(-8px) rotate(-45deg); }
.mobile-menu {
  position: absolute;
  top: 100%; left: 0; right: 0;
  background: var(--header-bg-scrolled);
  -webkit-backdrop-filter: blur(16px);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--header-border);
  padding: 1.25rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  animation: menuSlide 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  max-height: calc(100vh - var(--header-height));
  overflow-y: auto;
}
.mobile-menu[hidden] { display: none !important; }
@keyframes menuSlide {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.mobile-nav-list { list-style: none; margin: 0 0 1rem; padding: 0; }
.mobile-nav-list .nav-link {
  display: block;
  padding: 0.85rem 0;
  border-bottom: 1px solid rgba(174, 145, 100, 0.12);
  font-size: 0.8rem;
}
.mobile-cta { width: 100%; justify-content: center; }
@media (min-width: 768px) {
  .main-nav { display: block; }
  .menu-toggle { display: none; }
  .header-cta { display: inline-flex; }
  .mobile-menu { display: none !important; }
}
@media (min-width: 1024px) {
  .nav-list { gap: 1.75rem; }
  .nav-link { font-size: 0.72rem; }
}
/* Neutralize legacy scroll-state styles (from old header CSS) */
.site-header nav,
.site-header.scrolled nav { min-height: unset !important; }
.site-header.scrolled { box-shadow: none; }
/* Fallback if backdrop-filter unsupported */
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .site-header { background: rgba(246, 243, 238, 0.98); }
}
/* Adjust hero top padding for smaller header */
.hero { padding-top: 8rem; }
@media (max-width: 768px) { .hero { padding-top: 7rem; } }
</style>

<header class="site-header" id="header">
  <div class="header-inner">
    <a href="#main" class="logo" aria-label="Nile Smile Concierge — Home">
      <span class="logo-script">Nile Smile</span>
      <span class="logo-sub">
        <span class="logo-sans">Concierge</span>
        <span class="logo-tagline">World-Class Smile &bull; Timeless Journey</span>
      </span>
    </a>

    <nav class="main-nav" aria-label="Primary">
      <ul class="nav-list">
        <li><a href="#packages" class="nav-link">Packages</a></li>
        <li><a href="#results" class="nav-link">Results</a></li>
        <li><a href="#founder" class="nav-link">Founder</a></li>
        <li><a href="#verify-us" class="nav-link">Verify Us</a></li>
        <li><a href="#guarantees" class="nav-link">Guarantees</a></li>
        <li><a href="#faq" class="nav-link">FAQ</a></li>
      </ul>
    </nav>

    <div class="header-actions">
      <button type="button" id="darkModeToggle" class="icon-btn" aria-label="Toggle dark mode">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
      </button>
      <button type="button" id="searchTrigger" class="icon-btn" aria-label="Search">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
      </button>
      <a href="#consult" class="btn btn-gold header-cta">Free Review</a>
      <button type="button" class="menu-toggle" id="menuToggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>

  <div id="mobileMenu" class="mobile-menu" hidden>
    <ul class="mobile-nav-list">
      <li><a href="#packages" class="nav-link">Packages</a></li>
      <li><a href="#results" class="nav-link">Results</a></li>
      <li><a href="#founder" class="nav-link">Founder</a></li>
      <li><a href="#verify-us" class="nav-link">Verify Us</a></li>
      <li><a href="#guarantees" class="nav-link">Guarantees</a></li>
      <li><a href="#faq" class="nav-link">FAQ</a></li>
    </ul>
    <a href="#consult" class="btn btn-gold mobile-cta">Get My Free Review</a>
  </div>
</header>

<script id="modernHeaderScript">
(function() {
  'use strict';
  var toggle = document.getElementById('menuToggle');
  var menu = document.getElementById('mobileMenu');
  if (!toggle || !menu) return;
  function openMenu() {
    toggle.setAttribute('aria-expanded', 'true');
    toggle.setAttribute('aria-label', 'Close menu');
    menu.hidden = false;
  }
  function closeMenu() {
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
    menu.hidden = true;
  }
  toggle.addEventListener('click', function() {
    toggle.getAttribute('aria-expanded') === 'true' ? closeMenu() : openMenu();
  });
  var links = menu.querySelectorAll('a');
  for (var i = 0; i < links.length; i++) links[i].addEventListener('click', closeMenu);
  document.addEventListener('click', function(e) {
    if (!menu.hidden && !menu.contains(e.target) && !toggle.contains(e.target)) closeMenu();
  });
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && !menu.hidden) { closeMenu(); toggle.focus(); }
  });
  if ('ResizeObserver' in window) {
    var ro = new ResizeObserver(function() {
      if (window.innerWidth >= 768 && !menu.hidden) closeMenu();
    });
    ro.observe(document.querySelector('.site-header'));
  }
})();
</script>
<!-- ═══════════════════ /HEADER ═══════════════════ -->
'''


# ============================================================
# PATTERNS — Old blocks to remove
# ============================================================
REMOVAL_PATTERNS = [
    ("Old header HTML",        r'<!--\s*═+\s*HEADER\s*═+\s*-->\s*<header\s+class="site-header"\s+id="header">.*?</header>\s*'),
    ("Logo Intro overlay",     r'<!--\s*═+\s*LOGO INTRO.*?(?=<!--\s*═+\s*PROGRESS\s*═+\s*-->)'),
    ("Logo intro styles",      r'<style\s+id="logoIntroStyles">.*?</style>\s*'),
    ("Logo intro fallback",    r'<style[^>]*>\s*/\*\s*Fallback:\s*لو\s*JS.*?</noscript>\s*'),
    ("ZK_NUCLEAR_V12 style",   r'<style\s+id="ZK_NUCLEAR_V12">.*?</style>\s*'),
    ("ZK_NUCLEAR_V12 script",  r'<script\s+id="ZK_NUCLEAR_V12_JS">.*?</script>\s*'),
    ("ZK_PERFECT_V14 style",   r'<style\s+id="ZK_PERFECT_V14">.*?</style>\s*'),
    ("ZK_PERFECT_V14 script",  r'<script\s+id="ZK_PERFECT_V14_JS">.*?</script>\s*'),
    ("Logo Intro JS section",  r'/\*\s*═+\s*1\.\s*LOGO INTRO.*?(?=/\*\s*═+\s*2\.\s*SCROLL PROGRESS)'),
]


# ============================================================
# HELPERS
# ============================================================
def remove_pattern(text, name, pattern):
    try:
        new_text, count = re.subn(pattern, '', text, flags=re.DOTALL)
    except re.error as e:
        print("  [X] Regex error in '{}': {}".format(name, e))
        return text, False
    if count > 0:
        print("  [OK] Removed: {} ({}x)".format(name, count))
        return new_text, True
    print("  [--] Not found: {}".format(name))
    return text, False


# ============================================================
# MAIN
# ============================================================
def main():
    if len(sys.argv) < 2:
        print("Usage: python modernize.py <path-to-html>")
        print("Example: python modernize.py index.html")
        sys.exit(1)

    html_path = Path(sys.argv[1])
    if not html_path.exists():
        print("[X] File not found: {}".format(html_path))
        sys.exit(1)

    print("\n===========================================")
    print("  Nile Smile - Header Modernizer")
    print("===========================================\n")

    # ---- Backup ----
    backup_path = html_path.with_suffix(html_path.suffix + ".backup")
    shutil.copy2(html_path, backup_path)
    print("[OK] Backup created: {}\n".format(backup_path.name))

    # ---- Read (UTF-8, preserving line endings) ----
    print("Reading file...")
    try:
        with open(html_path, 'r', encoding='utf-8', newline='') as f:
            raw = f.read()
    except UnicodeDecodeError:
        print("  [--] Not valid UTF-8. Trying utf-8-sig...")
        with open(html_path, 'r', encoding='utf-8-sig', newline='') as f:
            raw = f.read()

    has_crlf = '\r\n' in raw
    content = raw.replace('\r\n', '\n')
    original_len = len(content)
    print("  Size: {:,} chars | Line endings: {}\n".format(
        original_len, 'CRLF' if has_crlf else 'LF'
    ))

    # ---- Safety checks ----
    if 'id="modernHeaderStyles"' in content:
        print("[!] Modern header already installed. Aborting to prevent duplicates.")
        print("    To reinstall: restore from {} first.\n".format(backup_path.name))
        sys.exit(0)

    if 'class="site-header"' not in content and 'id="header"' not in content:
        print("[X] This doesn't look like the Nile Smile HTML file.")
        print("    Expected to find 'site-header' or 'id=\"header\"'.\n")
        sys.exit(1)

    # ---- Remove old header system ----
    print("Removing old header system...")
    removed = 0
    for name, pattern in REMOVAL_PATTERNS:
        content, ok = remove_pattern(content, name, pattern)
        if ok:
            removed += 1
    print("  Total blocks removed: {}\n".format(removed))

    # ---- Inject new header ----
    print("Injecting modern header...")
    anchor = '<main id="main">'
    if anchor not in content:
        print("[X] Anchor '{}' not found — aborting.".format(anchor))
        print("    Restore from {}\n".format(backup_path.name))
        sys.exit(1)
    content = content.replace(anchor, NEW_HEADER_BLOCK + '\n' + anchor, 1)
    print("  [OK] Injected before <main id=\"main\">\n")

    # ---- Adjust scroll offsets ----
    print("Adjusting scroll offsets...")
    replacements = [
        ('scroll-padding-top:130px;', 'scroll-padding-top:92px;'),
        ('section[id],header[id],main[id]{scroll-margin-top:130px}',
         'section[id],header[id],main[id]{scroll-margin-top:92px}'),
        ('html{scroll-padding-top:100px}section[id],header[id],main[id]{scroll-margin-top:100px}',
         'html{scroll-padding-top:88px}section[id],header[id],main[id]{scroll-margin-top:88px}'),
    ]
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print("  [OK] {}".format(new[:40]))
    print()

    # ---- Write back ----
    print("Writing file...")
    if has_crlf:
        content = content.replace('\n', '\r\n')
    with open(html_path, 'w', encoding='utf-8', newline='') as f:
        f.write(content)
    new_len = len(content)
    print("  New size: {:,} chars ({:+,})\n".format(new_len, new_len - original_len))

    # ---- Verify ----
    print("Verification:")
    checks = [
        ('New header present',    'id="modernHeaderStyles"' in content),
        ('Old ZK overrides gone', 'ZK_NUCLEAR_V12' not in content and 'ZK_PERFECT_V14' not in content),
        ('Logo intro gone',       'id="logoIntro"' not in content),
        ('Menu toggle present',   'id="menuToggle"' in content),
        ('Search trigger present','id="searchTrigger"' in content),
        ('Dark mode toggle',      'id="darkModeToggle"' in content),
        ('Only one header',       content.count('<header class="site-header"') == 1),
    ]
    all_ok = True
    for label, ok in checks:
        print("  {} {}".format("[OK]" if ok else "[X] ", label))
        if not ok:
            all_ok = False

    print()
    if all_ok:
        print("SUCCESS. Open {} in your browser.".format(html_path.name))
        print("If anything looks wrong, restore from {}.\n".format(backup_path.name))
    else:
        print("WARNING: Some checks failed.")
        print("Restore from {} if needed.\n".format(backup_path.name))


if __name__ == '__main__':
    main()