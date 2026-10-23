#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nile Smile — Modern Hero Buttons & Cleanup
==========================================
- إخفاء كل الأزرار العائمة (Sticky/WhatsApp)
- تحديث أزرار الـ Hero لتكون Rounded وتتبع تسلسل هرمي حديث
"""

import re
import shutil
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python modern_hero.py <path-to-html>")
        sys.exit(1)

    html_path = Path(sys.argv[1])
    if not html_path.exists():
        print(f"[X] File not found: {html_path}")
        sys.exit(1)

    print("\n============================================")
    print("  Nile Smile - Modern Hero & Cleanup")
    print("============================================\n")

    # Backup
    backup_path = html_path.with_suffix(html_path.suffix + ".backup_hero")
    shutil.copy2(html_path, backup_path)
    print(f"[OK] Backup created: {backup_path.name}\n")

    # Read
    with open(html_path, 'r', encoding='utf-8', newline='') as f:
        content = f.read()

    has_crlf = '\r\n' in content
    content = content.replace('\r\n', '\n')

    # 1. Remove previous hero button styles if they exist
    content = re.sub(r'<style id="modernHeroButtons">.*?</style>', '', content, flags=re.DOTALL)

    # 2. Inject New Modern CSS
    new_css = r'''
<style id="modernHeroButtons">
/* ============================================================
   HIDE ALL STICKY / FLOATING BUTTONS
   (We use the Apple Dock at the bottom instead)
   ============================================================ */
.float-wa, 
.sticky-mobile, 
#stickyCta, 
#exitPopup {
  display: none !important;
}

/* ============================================================
   MODERN HERO BUTTONS (2026 UI/UX Standards)
   ============================================================ */
/* 1. Container Layout */
.hero-content > div.flex.flex-col.sm\:flex-row {
  display: flex !important;
  flex-direction: column !important;
  gap: 1rem !important;
  max-width: 30rem !important;
  margin: 2rem auto 0 !important;
  align-items: stretch !important;
  padding: 0 1rem !important;
}
@media (min-width: 640px) {
  .hero-content > div.flex.flex-col.sm\:flex-row {
    flex-direction: row !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 !important;
  }
}

/* 2. Base Button Styles */
.hero-content .btn {
  border-radius: 50px !important;
  min-height: 56px !important; /* Touch-friendly size */
  font-size: 0.75rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 2rem !important;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
  text-decoration: none !important;
}

/* 3. Primary Button (Get Free Treatment Plan) */
.hero-content #heroMainCta {
  background: linear-gradient(135deg, #AE9164 0%, #E8C88A 100%) !important;
  color: #1F2A36 !important;
  border: none !important;
  box-shadow: 0 8px 24px rgba(174, 145, 100, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
  flex: 1 !important; /* Takes up more space than secondary */
  position: relative !important;
  overflow: hidden !important;
}

/* Shimmer Effect for Primary Button */
.hero-content #heroMainCta::before {
  content: '' !important;
  position: absolute !important;
  top: 0; left: -100% !important;
  width: 100%; height: 100% !important;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent) !important;
  animation: btnShimmer 4s infinite !important;
}
@keyframes btnShimmer {
  0% { left: -100%; }
  20% { left: 100%; }
  100% { left: 100%; }
}

.hero-content #heroMainCta:hover {
  transform: translateY(-3px) scale(1.02) !important;
  box-shadow: 0 12px 32px rgba(174, 145, 100, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}

/* 4. Secondary Button (Turkey Rescue) */
.hero-content a[href="#turkey-rescue"] {
  background: rgba(255, 255, 255, 0.05) !important; /* Glassmorphism */
  color: #F6F3EE !important;
  border: 1.5px solid rgba(255, 255, 255, 0.3) !important;
  backdrop-filter: blur(8px) !important;
  -webkit-backdrop-filter: blur(8px) !important;
  flex: 0.8 !important; /* Slightly smaller */
}

.hero-content a[href="#turkey-rescue"]:hover {
  background: rgba(255, 255, 255, 0.15) !important;
  border-color: rgba(255, 255, 255, 0.7) !important;
  transform: translateY(-3px) !important;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3) !important;
}

/* 5. Clean up text below buttons */
.hero-content p.text-center.mt-4 {
  margin-top: 1.5rem !important;
  font-size: 0.65rem !important;
  letter-spacing: 0.15em !important;
  color: #E8C88A !important;
  opacity: 0.9 !important;
}
</style>
'''

    # Insert before </head>
    content = content.replace('</head>', new_css + '\n</head>')
    print("[OK] Injected Modern Hero CSS & Removed Sticky Buttons")

    # Write back
    if has_crlf:
        content = content.replace('\n', '\r\n')
    with open(html_path, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    print("\nSUCCESS! Modern buttons applied and sticky elements removed.")
    print("Refresh your browser (Ctrl+Shift+R).\n")

if __name__ == '__main__':
    main()