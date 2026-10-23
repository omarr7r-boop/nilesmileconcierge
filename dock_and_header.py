#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nile Smile — Header & Apple Dock Customization
================================================
يُطبق التصميم المطلوب بناءً على الصورة:
- هيدر عائم زجاجي (Glass Pill)
- إزالة كلمة Free Review
- إضافة Apple Dock سفلي
- إزالة الشريط السفلي القديم
"""

import re
import shutil
import sys
from pathlib import Path

# ============================================================
# NEW HEADER & DOCK BLOCK
# ============================================================
NEW_HEADER_CSS = r'''
<style id="modernHeaderStyles">
:root {
  --header-bg: rgba(255, 255, 255, 0.75);
  --header-border: rgba(255, 255, 255, 0.9);
}
.site-header {
  position: fixed;
  top: 12px;
  left: 50%;
  transform: translateX(-50%);
  width: 94%;
  max-width: 800px;
  z-index: 9999;
  background: var(--header-bg);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid var(--header-border);
  border-radius: 50px;
  box-shadow: 0 10px 30px rgba(31, 42, 54, 0.1);
  transition: all 0.3s ease;
}
.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 64px;
  padding: 0 1rem;
}
.logo {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-decoration: none;
  line-height: 1;
  flex-shrink: 0;
  gap: 0;
  margin-left: 0.5rem;
}
.logo-script {
  font-family: 'Italianno', cursive;
  font-size: 1.8rem;
  color: #4F6070;
  line-height: 0.9;
}
.logo-sub {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: -2px;
}
.logo-sans {
  font-family: 'Montserrat', sans-serif;
  font-size: 0.5rem;
  font-weight: 700;
  letter-spacing: 0.25em;
  color: #4F6070;
  text-transform: uppercase;
}
.logo-tagline {
  font-family: 'Montserrat', sans-serif;
  font-size: 0.35rem;
  letter-spacing: 0.12em;
  color: #6B7D8E;
  text-transform: uppercase;
  margin-top: 1px;
  opacity: 0.8;
}
.main-nav { display: none; }
.header-actions {
  display: flex;
  align-items: center;
  gap: 0.4rem;
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
.header-cta {
  display: none;
  font-size: 0.65rem;
  padding: 0.55rem 1.1rem;
  white-space: nowrap;
  border-radius: 50px; /* Pill shaped */
  font-weight: 700;
}
.menu-toggle {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 24px;
  height: 16px;
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
.menu-toggle[aria-expanded="true"] span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.menu-toggle[aria-expanded="true"] span:nth-child(2) { opacity: 0; }
.menu-toggle[aria-expanded="true"] span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
.mobile-menu {
  position: absolute;
  top: calc(100% + 10px);
  left: 0;
  right: 0;
  background: var(--header-bg);
  -webkit-backdrop-filter: blur(20px);
  backdrop-filter: blur(20px);
  border: 1px solid var(--header-border);
  border-radius: 20px;
  padding: 1.25rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  animation: menuSlide 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  max-height: calc(100vh - 100px);
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
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(174, 145, 100, 0.12);
  font-size: 0.8rem;
  color: #4F6070;
  text-decoration: none;
  font-weight: 600;
}
.mobile-cta { width: 100%; justify-content: center; }
@media (min-width: 768px) {
  .main-nav { display: block; }
  .menu-toggle { display: none; }
  .header-cta { display: inline-flex; }
  .mobile-menu { display: none !important; }
  .header-inner { padding: 0 1.5rem; }
  .logo-script { font-size: 2.2rem; }
  .logo { margin-left: 0; }
}
/* Adjust hero top padding for the floating header */
.hero { padding-top: 8rem; }
@media (max-width: 768px) { .hero { padding-top: 7rem; } }
</style>
'''

NEW_HEADER_HTML = r'''
<header class="site-header" id="header">
  <div class="header-inner">
    <a href="#main" class="logo" aria-label="Nile Smile Concierge — Home">
      <span class="logo-script">Nile Smile</span>
      <span class="logo-sub">
        <span class="logo-sans">Concierge</span>
        <span class="logo-tagline">World-Class Smile</span>
      </span>
    </a>

    <nav class="main-nav" aria-label="Primary">
      <ul class="nav-list" style="display:flex; gap:1.25rem; list-style:none; margin:0; padding:0;">
        <li><a href="#packages" class="nav-link" style="font-size:.7rem; font-weight:600; color:#4F6070; text-decoration:none;">Packages</a></li>
        <li><a href="#results" class="nav-link" style="font-size:.7rem; font-weight:600; color:#4F6070; text-decoration:none;">Results</a></li>
        <li><a href="#founder" class="nav-link" style="font-size:.7rem; font-weight:600; color:#4F6070; text-decoration:none;">Founder</a></li>
        <li><a href="#guarantees" class="nav-link" style="font-size:.7rem; font-weight:600; color:#4F6070; text-decoration:none;">Guarantees</a></li>
        <li><a href="#faq" class="nav-link" style="font-size:.7rem; font-weight:600; color:#4F6070; text-decoration:none;">FAQ</a></li>
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
      <!-- Changed from Free Review to Consult -->
      <a href="#consult" class="btn btn-gold header-cta">Consult</a>
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
    <a href="#consult" class="btn btn-gold mobile-cta">Get My Consultation</a>
  </div>
</header>
'''

DOCK_CSS = r'''
<style id="appleDockStyles">
.apple-dock {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 92%;
  max-width: 400px;
  height: 64px;
  background: rgba(255, 255, 255, 0.8);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  backdrop-filter: blur(20px) saturate(180%);
  border-radius: 35px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  box-shadow: 0 10px 30px rgba(0,0,0,0.15), inset 0 1px 0 rgba(255,255,255,0.6);
  z-index: 9990;
  border: 1px solid rgba(255,255,255,0.5);
  padding: 0 10px;
}
@media(min-width: 768px) {
  .apple-dock {
    max-width: 450px;
  }
}
.dock-item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 14px;
  color: #6B7D8E;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  text-decoration: none;
  position: relative;
}
.dock-item svg {
  width: 22px;
  height: 22px;
  stroke-width: 1.8;
  fill: none;
  stroke: currentColor;
}
.dock-item:hover, .dock-item.active {
  background: rgba(174, 145, 100, 0.15);
  color: #AE9164;
}
.dock-item.active::after {
  content: '';
  position: absolute;
  bottom: 4px;
  left: 50%;
  transform: translateX(-50%);
  width: 4px;
  height: 4px;
  background: #AE9164;
  border-radius: 50%;
}
.dock-item.wa-btn {
  background: #25D366;
  color: #fff;
  border-radius: 50%;
  box-shadow: 0 4px 10px rgba(37, 211, 102, 0.4);
}
.dock-item.wa-btn:hover {
  background: #1EBE5A;
  color: #fff;
}
body {
  padding-bottom: 100px !important; /* Space for the dock */
}
/* Hide old sticky mobile */
.sticky-mobile {
  display: none !important;
}
</style>
'''

DOCK_HTML = r'''
<nav class="apple-dock" id="appleDock">
  <a href="#main" class="dock-item active" aria-label="Home" data-target="main">
    <svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
      <polyline points="9 22 9 12 15 12 15 22"/>
    </svg>
  </a>
  <a href="#packages" class="dock-item" aria-label="Packages" data-target="packages">
    <svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
      <rect x="3" y="3" width="7" height="7"/>
      <rect x="14" y="3" width="7" height="7"/>
      <rect x="14" y="14" width="7" height="7"/>
      <rect x="3" y="14" width="7" height="7"/>
    </svg>
  </a>
  <a href="#results" class="dock-item" aria-label="Results" data-target="results">
    <svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
      <circle cx="8.5" cy="8.5" r="1.5"/>
      <polyline points="21 15 16 10 5 21"/>
    </svg>
  </a>
  <a href="#implant-systems" class="dock-item" aria-label="Implants" data-target="implant-systems">
    <svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 2v6.5a4.5 4.5 0 0 1-4.5 4.5H4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-5a2 2 0 0 0-2-2h-1.5A4.5 4.5 0 0 1 14 8.5V2"/>
      <path d="M8 2h8"/><path d="M12 14v4"/><path d="M10 18h4"/>
    </svg>
  </a>
  <a href="#guarantees" class="dock-item" aria-label="Guarantees" data-target="guarantees">
    <svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      <path d="M9 12l2 2 4-4"/>
    </svg>
  </a>
  <a href="#faq" class="dock-item" aria-label="FAQ" data-target="faq">
    <svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="10"/>
      <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
      <line x1="12" y1="17" x2="12.01" y2="17"/>
    </svg>
  </a>
  <a href="https://wa.me/201503308333" target="_blank" rel="noopener" class="dock-item wa-btn" aria-label="WhatsApp">
    <svg viewBox="0 0 24 24" stroke="none" fill="currentColor">
      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.82 9.82 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/>
    </svg>
  </a>
</nav>
'''

DOCK_JS = r'''
<script id="appleDockScript">
(function() {
  'use strict';
  var dockItems = document.querySelectorAll('.dock-item[data-target]');
  if(!dockItems.length) return;

  // Active state tracking on scroll
  var sections = Array.from(dockItems).map(function(item) {
    var targetId = item.getAttribute('data-target');
    return { el: document.getElementById(targetId), link: item };
  }).filter(function(s) { return s.el !== null; });

  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        dockItems.forEach(function(item) { item.classList.remove('active'); });
        var activeItem = sections.find(function(s) { return s.el === entry.target; });
        if(activeItem) {
          activeItem.link.classList.add('active');
        }
      }
    });
  }, { rootMargin: '-20% 0px -50% 0px', threshold: 0 });

  sections.forEach(function(s) {
    observer.observe(s.el);
  });
})();
</script>
'''

# ============================================================
# MAIN SCRIPT
# ============================================================
def main():
    if len(sys.argv) < 2:
        print("Usage: python dock_and_header.py <path-to-html>")
        sys.exit(1)

    html_path = Path(sys.argv[1])
    if not html_path.exists():
        print(f"[X] File not found: {html_path}")
        sys.exit(1)

    print("\n============================================")
    print("  Nile Smile - Header & Apple Dock")
    print("============================================\n")

    # Backup
    backup_path = html_path.with_suffix(html_path.suffix + ".backup_dock")
    shutil.copy2(html_path, backup_path)
    print(f"[OK] Backup created: {backup_path.name}\n")

    # Read
    with open(html_path, 'r', encoding='utf-8', newline='') as f:
        content = f.read()

    has_crlf = '\r\n' in content
    content = content.replace('\r\n', '\n')

    # 1. Remove old header styles (if any)
    content = re.sub(r'<style id="modernHeaderStyles">.*?</style>', '', content, flags=re.DOTALL)
    
    # 2. Remove old header HTML (between <body> and <main>)
    content = re.sub(r'<header class="site-header" id="header">.*?</header>', '', content, flags=re.DOTALL)
    
    # 3. Remove old header script
    content = re.sub(r'<script id="modernHeaderScript">.*?</script>', '', content, flags=re.DOTALL)

    # 4. Insert NEW Header CSS right before </head>
    if '</head>' in content:
        content = content.replace('</head>', NEW_HEADER_CSS + '\n</head>')
        print("[OK] Injected Header CSS")

    # 5. Insert NEW Header HTML & Script right after <body>
    body_match = re.search(r'(<body[^>]*>)', content)
    if body_match:
        insert_after_body = body_match.group(1) + '\n' + NEW_HEADER_HTML + '''
<script id="modernHeaderScript">
(function() {
  var toggle = document.getElementById('menuToggle');
  var menu = document.getElementById('mobileMenu');
  if (!toggle || !menu) return;
  function openMenu() { toggle.setAttribute('aria-expanded', 'true'); menu.hidden = false; }
  function closeMenu() { toggle.setAttribute('aria-expanded', 'false'); menu.hidden = true; }
  toggle.addEventListener('click', function() { toggle.getAttribute('aria-expanded') === 'true' ? closeMenu() : openMenu(); });
  var links = menu.querySelectorAll('a');
  for (var i = 0; i < links.length; i++) links[i].addEventListener('click', closeMenu);
  document.addEventListener('click', function(e) {
    if (!menu.hidden && !menu.contains(e.target) && !toggle.contains(e.target)) closeMenu();
  });
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && !menu.hidden) { closeMenu(); toggle.focus(); }
  });
})();
</script>
'''
        content = content.replace(body_match.group(1), insert_after_body)
        print("[OK] Injected Header HTML & JS")

    # 6. Insert Dock CSS, HTML, and JS right before </body>
    if '</body>' in content:
        dock_block = DOCK_CSS + '\n' + DOCK_HTML + '\n' + DOCK_JS
        content = content.replace('</body>', dock_block + '\n</body>')
        print("[OK] Injected Apple Dock")

    # Write back
    if has_crlf:
        content = content.replace('\n', '\r\n')
    with open(html_path, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    print("\nSUCCESS. Open the file and refresh (Ctrl+Shift+R).\n")


if __name__ == '__main__':
    main()