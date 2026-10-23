#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nile Smile — Final UI Fixes (Transparent Header + Clean Dock)
=============================================================
- إصلاح الهيدر ليكون شفافاً (بلوك أوت أسود خفيف)
- إزالة قائمة الموبايل المكررة نهائياً
- إصلاح زر البحث
- تغيير لون زر الواتساب إلى الذهبي
"""

import re
import shutil
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_final_ui.py <path-to-html>")
        sys.exit(1)

    html_path = Path(sys.argv[1])
    if not html_path.exists():
        print(f"[X] File not found: {html_path}")
        sys.exit(1)

    print("\n============================================")
    print("  Nile Smile - Final UI Fixes")
    print("============================================\n")

    # Backup
    backup_path = html_path.with_suffix(html_path.suffix + ".backup_final")
    shutil.copy2(html_path, backup_path)
    print(f"[OK] Backup created: {backup_path.name}\n")

    # Read
    with open(html_path, 'r', encoding='utf-8', newline='') as f:
        content = f.read()

    has_crlf = '\r\n' in content
    content = content.replace('\r\n', '\n')

    # 1. Remove old header CSS and replace with transparent version
    old_header_css = re.search(r'<style id="modernHeaderStyles">.*?</style>', content, flags=re.DOTALL)
    if old_header_css:
        content = content.replace(old_header_css.group(0), '')

    new_header_css = r'''
<style id="modernHeaderStyles">
:root {
  --header-bg: rgba(10, 13, 16, 0.35); /* Dark transparent overlay */
  --header-border: rgba(255, 255, 255, 0.15);
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
  -webkit-backdrop-filter: blur(8px) saturate(140%);
  backdrop-filter: blur(8px) saturate(140%);
  border: 1px solid var(--header-border);
  border-radius: 50px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}
.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 60px;
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
  color: #F6F3EE; /* Light color for dark background */
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
  color: #E8C88A; /* Gold */
  text-transform: uppercase;
}
.logo-tagline {
  font-family: 'Montserrat', sans-serif;
  font-size: 0.35rem;
  letter-spacing: 0.12em;
  color: #B8C5D1;
  text-transform: uppercase;
  margin-top: 1px;
  opacity: 0.8;
}
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
  color: #F6F3EE; /* Light icon */
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.icon-btn:hover { background: rgba(255, 255, 255, 0.15); color: #E8C88A; }
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
  .logo-script { font-size: 2.2rem; }
  .logo { margin-left: 0; }
  .header-cta { display: inline-flex; }
}
/* Adjust hero top padding */
.hero { padding-top: 8rem; }
@media (max-width: 768px) { .hero { padding-top: 7rem; } }
</style>
'''
    content = content.replace('</head>', new_header_css + '\n</head>')
    print("[OK] Injected transparent header CSS")

    # 2. Remove the mobile menu HTML (to avoid duplication with Dock)
    # Replace the entire header block with a version that has NO mobile menu and NO toggle button.
    old_header_html = re.search(r'<header class="site-header" id="header">.*?</header>', content, flags=re.DOTALL)
    if old_header_html:
        content = content.replace(old_header_html.group(0), '')

    new_header_html = r'''
<header class="site-header" id="header">
  <div class="header-inner">
    <a href="#main" class="logo" aria-label="Nile Smile Concierge — Home">
      <span class="logo-script">Nile Smile</span>
      <span class="logo-sub">
        <span class="logo-sans">Concierge</span>
        <span class="logo-tagline">World-Class Smile</span>
      </span>
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
    print("[OK] Injected clean header (no mobile menu)")

    # 3. Update Dock CSS to make WhatsApp button Gold
    old_dock_css = re.search(r'<style id="appleDockStyles">.*?</style>', content, flags=re.DOTALL)
    if old_dock_css:
        content = content.replace(old_dock_css.group(0), '')

    new_dock_css = r'''
<style id="appleDockStyles">
.apple-dock {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 92%;
  max-width: 400px;
  height: 64px;
  background: rgba(246, 243, 238, 0.85); /* Slightly more opaque for readability */
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

/* Gold WhatsApp Button */
.dock-item.wa-btn {
  background: linear-gradient(135deg, #AE9164, #E8C88A); /* Gold gradient */
  color: #1F2A36; /* Dark text for contrast */
  border-radius: 50%;
  box-shadow: 0 4px 10px rgba(174, 145, 100, 0.4);
}
.dock-item.wa-btn:hover {
  background: linear-gradient(135deg, #E8C88A, #AE9164);
  color: #1F2A36;
  transform: scale(1.05);
}

/* Ensure body has space for dock */
body {
  padding-bottom: 100px !important;
}
</style>
'''
    content = content.replace('</head>', new_dock_css + '\n</head>')
    print("[OK] Updated Dock CSS (Gold WhatsApp button)")

    # 4. Fix Search Logic (Ensure Search Trigger opens the modal)
    # Remove old search JS if any (conflicts)
    content = re.sub(r'<script id="searchScript">.*?</script>', '', content, flags=re.DOTALL)
    
    search_js = r'''
<script id="searchScript">
(function() {
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
    
    // Close logic (overlay, ESC)
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
})();
</script>
'''
    content = content.replace('</body>', search_js + '\n</body>')
    print("[OK] Fixed Search JS")

    # 5. Remove duplicate mobile menu / old JS leftovers
    content = re.sub(r'<script id="modernHeaderScript">.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div id="mobileMenu".*?</div>', '', content, flags=re.DOTALL)
    
    # 6. Write back
    if has_crlf:
        content = content.replace('\n', '\r\n')
    with open(html_path, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    print("\nSUCCESS. All fixes applied.")
    print("Refresh your browser (Ctrl+Shift+R) to see the changes.\n")

if __name__ == '__main__':
    main()