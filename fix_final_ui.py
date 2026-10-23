#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nile Smile — Ultimate UI Fix (Header, Logo, Hero Overlay, Dock)
================================================================
"""

import re
import shutil
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python ultimate_fix.py <path-to-html>")
        sys.exit(1)

    html_path = Path(sys.argv[1])
    if not html_path.exists():
        print(f"[X] File not found: {html_path}")
        sys.exit(1)

    print("\n============================================")
    print("  Nile Smile - Ultimate UI Fix")
    print("============================================\n")

    # Backup
    backup_path = html_path.with_suffix(html_path.suffix + ".backup_ultimate")
    shutil.copy2(html_path, backup_path)
    print(f"[OK] Backup created: {backup_path.name}\n")

    # Read
    with open(html_path, 'r', encoding='utf-8', newline='') as f:
        content = f.read()

    has_crlf = '\r\n' in content
    content = content.replace('\r\n', '\n')

    # ============================================================
    # 1. REMOVE OLD STYLES & HTML
    # ============================================================
    content = re.sub(r'<style id="modernHeaderStyles">.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style id="appleDockStyles">.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<header class="site-header" id="header">.*?</header>', '', content, flags=re.DOTALL)
    content = re.sub(r'<nav class="apple-dock" id="appleDock">.*?</nav>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script id="modernHeaderScript">.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script id="appleDockScript">.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script id="searchScript">.*?</script>', '', content, flags=re.DOTALL)

    # ============================================================
    # 2. INJECT NEW CSS (Header, Hero Overlay, Dock)
    # ============================================================
    new_css = r'''
<style id="ultimateUIStyles">
/* --- HERO OVERLAY (Black transparent on Pyramids) --- */
.hero::before {
  content: '' !important;
  position: absolute !important;
  inset: 0 !important;
  background: linear-gradient(180deg, rgba(10,13,16,0.4) 0%, rgba(10,13,16,0.75) 100%) !important;
  z-index: 1 !important;
  pointer-events: none !important;
}
.hero-content {
  background: transparent !important;
  box-shadow: none !important;
  border: none !important;
  position: relative !important;
  z-index: 2 !important; /* Above overlay */
}

/* --- HEADER (White Milky Glass Pill) --- */
:root {
  --header-bg: rgba(251, 250, 247, 0.85);
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
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid var(--header-border);
  border-radius: 50px;
  box-shadow: 0 10px 30px rgba(31, 42, 54, 0.1);
}
.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 64px;
  padding: 0 1rem;
}

/* --- LOGO STRUCTURE & ANIMATION --- */
.logo {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  margin-left: 0.5rem;
}
.logo-top-row {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}
.logo-script {
  font-family: 'Italianno', cursive;
  font-size: 2.2rem;
  line-height: 0.8;
  background: linear-gradient(90deg, #4F6070 0%, #4F6070 40%, #AE9164 50%, #E8C88A 60%, #4F6070 70%, #4F6070 100%);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: logoGoldSweep 15s linear infinite;
}
@keyframes logoGoldSweep {
  0% { background-position: 200% center; }
  100% { background-position: -200% center; }
}
.logo-concierge {
  font-family: 'Montserrat', sans-serif;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: #AE9164;
}
.logo-tagline {
  font-family: 'Montserrat', sans-serif;
  font-size: 0.4rem;
  letter-spacing: 0.2em;
  color: #6B7D8E;
  margin-top: 2px;
}

/* --- ACTIONS & BUTTONS --- */
.header-actions {
  display: flex;
  align-items: center;
  gap: 0.4rem;
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
  transition: all 0.2s;
}
.icon-btn:hover { background: rgba(174, 145, 100, 0.12); color: #AE9164; }
.header-cta {
  display: none;
  font-size: 0.65rem;
  padding: 0.55rem 1.1rem;
  white-space: nowrap;
  border-radius: 50px;
  font-weight: 700;
  color: #1F2A36;
}

@media (min-width: 768px) {
  .header-inner { padding: 0 1.5rem; }
  .logo-script { font-size: 2.6rem; }
  .logo { margin-left: 0; }
  .header-cta { display: inline-flex; }
}
.hero { padding-top: 8rem; }
@media (max-width: 768px) { .hero { padding-top: 7rem; } }

/* --- APPLE DOCK (Bottom) --- */
.apple-dock {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 92%;
  max-width: 400px;
  height: 64px;
  background: rgba(251, 250, 247, 0.85);
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
@media(min-width: 768px) { .apple-dock { max-width: 450px; } }
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

/* Gold WhatsApp Button (Clean SVG) */
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
  width: 24px;
  height: 24px;
  fill: #1F2A36;
  stroke: none;
}
body { padding-bottom: 100px !important; }
</style>
'''

    content = content.replace('</head>', new_css + '\n</head>')
    print("[OK] Injected Ultimate CSS")

    # ============================================================
    # 3. INJECT NEW HEADER HTML
    # ============================================================
    new_header_html = r'''
<header class="site-header" id="header">
  <div class="header-inner">
    <a href="#main" class="logo" aria-label="Nile Smile Concierge">
      <div class="logo-top-row">
        <span class="logo-script">Nile Smile</span>
        <span class="logo-concierge">CONCIERGE</span>
      </div>
      <span class="logo-tagline">WORLD-CLASS SMILE</span>
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
    # 4. INJECT NEW DOCK HTML (Fixing SVG)
    # ============================================================
    new_dock_html = r'''
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
    <!-- Clean, precise WhatsApp SVG -->
    <svg viewBox="0 0 24 24">
      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.82 9.82 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/>
    </svg>
  </a>
</nav>
'''
    content = content.replace('</body>', new_dock_html + '\n</body>')
    print("[OK] Injected Dock HTML with clean SVG")

    # ============================================================
    # 5. INJECT JS (Search & Dock Active State)
    # ============================================================
    new_js = r'''
<script id="ultimateUIScript">
(function() {
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

  // 2. Dock Active State Logic
  var dockItems = document.querySelectorAll('.dock-item[data-target]');
  if (dockItems.length) {
    var sections = Array.from(dockItems).map(function(item) {
      return { el: document.getElementById(item.getAttribute('data-target')), link: item };
    }).filter(function(s) { return s.el !== null; });

    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          dockItems.forEach(function(item) { item.classList.remove('active'); });
          var activeItem = sections.find(function(s) { return s.el === entry.target; });
          if (activeItem) activeItem.link.classList.add('active');
        }
      });
    }, { rootMargin: '-20% 0px -50% 0px', threshold: 0 });

    sections.forEach(function(s) { observer.observe(s.el); });
  }
})();
</script>
'''
    content = content.replace('</body>', new_js + '\n</body>')
    print("[OK] Injected UI JavaScript")

    # ============================================================
    # 6. WRITE BACK
    # ============================================================
    if has_crlf:
        content = content.replace('\n', '\r\n')
    with open(html_path, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    print("\nSUCCESS! All fixes applied.")
    print("Please refresh your browser (Ctrl+Shift+R) and check the result.\n")

if __name__ == '__main__':
    main()