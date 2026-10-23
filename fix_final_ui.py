#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nile Smile — Dynamic Adaptive UI (Header + Dock)
=================================================
- حجم هيدر أصغر وأكثر احترافية (52px)
- ألوان ديناميكية تتغير حسب لون الخلفية (Dark/Light Glass)
- تعديل هيكل اللوجو (السلوجان تحت CONCIERGE)
"""

import re
import shutil
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python dynamic_ui.py <path-to-html>")
        sys.exit(1)

    html_path = Path(sys.argv[1])
    if not html_path.exists():
        print(f"[X] File not found: {html_path}")
        sys.exit(1)

    print("\n============================================")
    print("  Nile Smile - Dynamic Adaptive UI")
    print("============================================\n")

    # Backup
    backup_path = html_path.with_suffix(html_path.suffix + ".backup_dynamic")
    shutil.copy2(html_path, backup_path)
    print(f"[OK] Backup created: {backup_path.name}\n")

    # Read
    with open(html_path, 'r', encoding='utf-8', newline='') as f:
        content = f.read()

    has_crlf = '\r\n' in content
    content = content.replace('\r\n', '\n')

    # ============================================================
    # 1. CLEANUP OLD BLOCKS
    # ============================================================
    content = re.sub(r'<style id="ultimateUIStyles">.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style id="modernHeaderStyles">.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style id="appleDockStyles">.*?</style>', '', content, flags=re.DOTALL)
    
    # Remove old header/dock HTML
    content = re.sub(r'<header class="site-header" id="header">.*?</header>', '', content, flags=re.DOTALL)
    content = re.sub(r'<nav class="apple-dock" id="appleDock">.*?</nav>', '', content, flags=re.DOTALL)
    
    # Remove old scripts
    content = re.sub(r'<script id="ultimateUIScript">.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script id="modernHeaderScript">.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script id="appleDockScript">.*?</script>', '', content, flags=re.DOTALL)

    # ============================================================
    # 2. INJECT NEW DYNAMIC CSS
    # ============================================================
    new_css = r'''
<style id="dynamicUIStyles">
/* --- HERO OVERLAY (Black transparent on Pyramids) --- */
.hero::before {
  content: '' !important;
  position: absolute !important;
  inset: 0 !important;
  background: linear-gradient(180deg, rgba(10,13,16,0.4) 0%, rgba(10,13,16,0.7) 100%) !important;
  z-index: 1 !important;
  pointer-events: none !important;
}
.hero-content {
  background: transparent !important;
  box-shadow: none !important;
  border: none !important;
  position: relative !important;
  z-index: 2 !important; 
}

/* --- DYNAMIC HEADER (Glass Pill) --- */
:root {
  --header-light-bg: rgba(251, 250, 247, 0.85);
  --header-dark-bg: rgba(10, 13, 16, 0.65);
  --header-light-text: #4F6070;
  --header-dark-text: #F6F3EE;
}
.site-header {
  position: fixed;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  width: 94%;
  max-width: 800px;
  z-index: 9999;
  border-radius: 50px;
  transition: background-color 0.4s ease, border-color 0.4s ease;
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid transparent;
}
/* Light Theme (Default) */
.site-header.theme-light {
  background: var(--header-light-bg);
  border-color: rgba(255, 255, 255, 0.9);
  box-shadow: 0 4px 20px rgba(31, 42, 54, 0.08);
}
.site-header.theme-light .logo-script { color: var(--header-light-text); }
.site-header.theme-light .logo-tagline { color: #6B7D8E; }
.site-header.theme-light .icon-btn { color: var(--header-light-text); }
.site-header.theme-light .icon-btn:hover { background: rgba(174, 145, 100, 0.12); color: #AE9164; }

/* Dark Theme */
.site-header.theme-dark {
  background: var(--header-dark-bg);
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}
.site-header.theme-dark .logo-script { color: var(--header-dark-text); }
.site-header.theme-dark .logo-tagline { color: #B8C5D1; }
.site-header.theme-dark .icon-btn { color: var(--header-dark-text); }
.site-header.theme-dark .icon-btn:hover { background: rgba(255, 255, 255, 0.15); color: #E8C88A; }

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 52px;
  padding: 0 1rem;
}

/* --- LOGO LAYOUT (Slogan under Concierge) --- */
.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  margin-left: 0.5rem;
  gap: 8px;
}
.logo-script {
  font-family: 'Italianno', cursive;
  font-size: 1.9rem;
  line-height: 0.8;
  background: linear-gradient(90deg, currentColor 0%, currentColor 40%, #AE9164 50%, #E8C88A 60%, currentColor 70%, currentColor 100%);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: logoGoldSweep 15s linear infinite;
}
@keyframes logoGoldSweep {
  0% { background-position: 200% center; }
  100% { background-position: -200% center; }
}
.logo-text-group {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.logo-concierge {
  font-family: 'Montserrat', sans-serif;
  font-size: 0.55rem;
  font-weight: 800;
  letter-spacing: 0.15em;
  color: #AE9164;
}
.logo-tagline {
  font-family: 'Montserrat', sans-serif;
  font-size: 0.35rem;
  letter-spacing: 0.15em;
  margin-top: 1px;
}

/* --- ACTIONS --- */
.header-actions {
  display: flex;
  align-items: center;
  gap: 0.2rem;
}
.icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border: none;
  background: transparent;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s;
}
.header-cta {
  display: none;
  font-size: 0.65rem;
  padding: 0.5rem 1rem;
  white-space: nowrap;
  border-radius: 50px;
  font-weight: 700;
  color: #1F2A36;
}

@media (min-width: 768px) {
  .header-inner { padding: 0 1.25rem; }
  .logo-script { font-size: 2.2rem; }
  .logo { margin-left: 0; gap: 12px; }
  .logo-concierge { font-size: 0.65rem; }
  .logo-tagline { font-size: 0.4rem; }
  .header-cta { display: inline-flex; }
}
.hero { padding-top: 7rem; }
@media (max-width: 768px) { .hero { padding-top: 6rem; } }

/* --- DYNAMIC APPLE DOCK --- */
.apple-dock {
  position: fixed;
  bottom: 15px;
  left: 50%;
  transform: translateX(-50%);
  width: 92%;
  max-width: 400px;
  height: 60px;
  border-radius: 30px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  z-index: 9990;
  transition: background-color 0.4s ease, border-color 0.4s ease;
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid transparent;
  padding: 0 8px;
}
/* Dock Light */
.apple-dock.theme-light {
  background: var(--header-light-bg);
  border-color: rgba(255, 255, 255, 0.9);
  box-shadow: 0 8px 30px rgba(31, 42, 54, 0.15), inset 0 1px 0 rgba(255,255,255,0.6);
}
.apple-dock.theme-light .dock-item { color: #6B7D8E; }
.apple-dock.theme-light .dock-item.active { background: rgba(174, 145, 100, 0.15); color: #AE9164; }

/* Dock Dark */
.apple-dock.theme-dark {
  background: var(--header-dark-bg);
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.1);
}
.apple-dock.theme-dark .dock-item { color: #B8C5D1; }
.apple-dock.theme-dark .dock-item.active { background: rgba(232, 200, 138, 0.2); color: #E8C88A; }

.dock-item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  text-decoration: none;
  position: relative;
}
.dock-item svg {
  width: 20px;
  height: 20px;
  stroke-width: 1.8;
  fill: none;
  stroke: currentColor;
}
.dock-item.active::after {
  content: '';
  position: absolute;
  bottom: 3px;
  left: 50%;
  transform: translateX(-50%);
  width: 4px;
  height: 4px;
  background: currentColor;
  border-radius: 50%;
}

/* Gold WhatsApp Button */
.dock-item.wa-btn {
  background: linear-gradient(135deg, #AE9164, #E8C88A);
  color: #1F2A36;
  border-radius: 50%;
  box-shadow: 0 4px 10px rgba(174, 145, 100, 0.4);
  padding: 0;
}
.dock-item.wa-btn:hover {
  background: linear-gradient(135deg, #E8C88A, #AE9164);
  transform: scale(1.05);
}
.dock-item.wa-btn svg {
  width: 22px;
  height: 22px;
  fill: #1F2A36;
  stroke: none;
}
body { padding-bottom: 90px !important; }
</style>
'''

    content = content.replace('</head>', new_css + '\n</head>')
    print("[OK] Injected Dynamic CSS")

    # ============================================================
    # 3. INJECT NEW HEADER HTML
    # ============================================================
    new_header_html = r'''
<header class="site-header theme-light" id="header">
  <div class="header-inner">
    <a href="#main" class="logo" aria-label="Nile Smile Concierge">
      <span class="logo-script">Nile Smile</span>
      <div class="logo-text-group">
        <span class="logo-concierge">CONCIERGE</span>
        <span class="logo-tagline">WORLD-CLASS SMILE</span>
      </div>
    </a>

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
      <a href="#consult" class="btn btn-gold header-cta">Consult</a>
    </div>
  </div>
</header>
'''
    content = content.replace('<body>', '<body>\n' + new_header_html)
    print("[OK] Injected Header HTML")

    # ============================================================
    # 4. INJECT NEW DOCK HTML
    # ============================================================
    new_dock_html = r'''
<nav class="apple-dock theme-light" id="appleDock">
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
    <svg viewBox="0 0 24 24">
      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.82 9.82 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/>
    </svg>
  </a>
</nav>
'''
    content = content.replace('</body>', new_dock_html + '\n</body>')
    print("[OK] Injected Dock HTML")

    # ============================================================
    # 5. INJECT DYNAMIC JS (Theme Switcher & Search)
    # ============================================================
    new_js = r'''
<script id="dynamicUIScript">
(function() {
  'use strict';

  // 1. Search Modal Logic
  var trigger = document.getElementById('searchTrigger');
  var modal = document.getElementById('searchModal');
  if (trigger && modal) {
    trigger.addEventListener('click', function(e) {
      e.preventDefault();
      modal.classList.add('open');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      var input = document.getElementById('searchModalInput');
      if (input) setTimeout(function() { input.focus(); }, 100);
    });
    modal.addEventListener('click', function(e) {
      if (e.target === modal || e.target.hasAttribute('data-search-close')) {
        modal.classList.remove('open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      }
    });
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && modal.classList.contains('open')) {
        modal.classList.remove('open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      }
    });
  }

  // 2. Dynamic Header & Dock Theming
  var header = document.getElementById('header');
  var dock = document.getElementById('appleDock');
  
  // Sections that have dark backgrounds
  var darkSections = document.querySelectorAll('.hero, .bg-nile-blue, .bg-nile-blue-dark, #science, #consult, #turkey-rescue, #top-tier, #guarantees, #legal');
  var darkRanges = [];

  function calculateRanges() {
    darkRanges = Array.from(darkSections).map(function(sec) {
      var rect = sec.getBoundingClientRect();
      var top = rect.top + window.scrollY;
      return { top: top, bottom: top + rect.height };
    });
  }

  function updateTheme() {
    var scrollY = window.scrollY;
    
    // Check Header Theme (Top 52px + 10px offset)
    var headerCenter = scrollY + 40; 
    var isHeaderDark = darkRanges.some(function(range) {
      return headerCenter >= range.top && headerCenter <= range.bottom;
    });

    if (isHeaderDark) {
      header.classList.remove('theme-light');
      header.classList.add('theme-dark');
    } else {
      header.classList.remove('theme-dark');
      header.classList.add('theme-light');
    }

    // Check Dock Theme (Bottom 60px + 15px offset)
    var dockCenter = scrollY + window.innerHeight - 45;
    var isDockDark = darkRanges.some(function(range) {
      return dockCenter >= range.top && dockCenter <= range.bottom;
    });

    if (isDockDark) {
      dock.classList.remove('theme-light');
      dock.classList.add('theme-dark');
    } else {
      dock.classList.remove('theme-dark');
      dock.classList.add('theme-light');
    }
  }

  // Recalculate ranges on load and resize
  window.addEventListener('load', calculateRanges);
  window.addEventListener('resize', function() {
    calculateRanges();
    updateTheme();
  });

  // Throttled scroll listener
  var ticking = false;
  window.addEventListener('scroll', function() {
    if (!ticking) {
      window.requestAnimationFrame(function() {
        updateTheme();
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

  // Initial run
  setTimeout(calculateRanges, 100);
  setTimeout(updateTheme, 200);

  // 3. Dock Active State Logic
  var dockItems = document.querySelectorAll('.dock-item[data-target]');
  if (dockItems.length) {
    var navSections = Array.from(dockItems).map(function(item) {
      return { el: document.getElementById(item.getAttribute('data-target')), link: item };
    }).filter(function(s) { return s.el !== null; });

    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          dockItems.forEach(function(item) { item.classList.remove('active'); });
          var activeItem = navSections.find(function(s) { return s.el === entry.target; });
          if (activeItem) activeItem.link.classList.add('active');
        }
      });
    }, { rootMargin: '-20% 0px -50% 0px', threshold: 0 });

    navSections.forEach(function(s) { observer.observe(s.el); });
  }
})();
</script>
'''
    content = content.replace('</body>', new_js + '\n</body>')
    print("[OK] Injected Dynamic JS")

    # ============================================================
    # 6. WRITE BACK
    # ============================================================
    if has_crlf:
        content = content.replace('\n', '\r\n')
    with open(html_path, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    print("\nSUCCESS! Dynamic UI applied.")
    print("Refresh your browser (Ctrl+Shift+R).\n")

if __name__ == '__main__':
    main()