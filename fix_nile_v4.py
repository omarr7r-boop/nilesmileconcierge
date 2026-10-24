#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nile Smile — Ultimate UI Makeover v6.0
======================================
Transforms the dated design into a modern, luxurious 
"Pharaonic Gold + Dental Teal" theme.
"""

import shutil
import sys
from datetime import datetime
from pathlib import Path

CSS_MAKEOVER = """
<!-- ═══════════════════ ULTIMATE UI MAKEOVER v6.0 ═══════════════════ -->
<style id="modern-makeover">
:root {
  --primary-gold: #D4AF37;
  --primary-gold-light: #FDE047;
  --dental-teal: #0D9488;
  --dental-teal-light: #14B8A6;
  --bg-clinical: #F8FAFC;
  --text-dark: #1E293B;
}

/* 1. إصلاح الخلفيات المسمطة (من بيج لـ Clinical White فخم) */
body, section.bg-nile-beige, section.bg-white, .bg-white {
  background: var(--bg-clinical) !important;
  color: var(--text-dark) !important;
}

/* خلط الفرعوني (ذهبي) مع طب الأسنان (تركواز) في الخلفية */
body {
  background-image: 
    radial-gradient(circle at 15% 50%, rgba(13, 148, 136, 0.04) 0%, transparent 50%),
    radial-gradient(circle at 85% 30%, rgba(212, 175, 55, 0.04) 0%, transparent 50%) !important;
  background-attachment: fixed !important;
}

/* تحويل الأقسام لكروت ضخمة ناعمة لتعطي شكل حديث */
section.section {
  max-width: 96% !important;
  margin: 2rem auto !important;
  border-radius: 24px !important;
  background: #ffffff !important;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.03) !important;
  border: 1px solid rgba(0, 0, 0, 0.02) !important;
  overflow: hidden !important;
}

/* 2. تطوير الأزرار (Pill Shape + 3D Glow) */
.btn, .btn-gold, .btn-outline, .btn-outline-dark, button {
  border-radius: 100px !important; /* كبسولة */
  padding: 0.9rem 2rem !important;
  font-weight: 700 !important;
  font-size: 0.85rem !important;
  letter-spacing: 0.05em !important;
  text-transform: uppercase !important;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
  border: none !important;
}

/* الزر الفرعوني الذهبي (للأزرار المهمة جداً) */
.btn-gold {
  background: linear-gradient(135deg, var(--primary-gold) 0%, var(--primary-gold-light) 100%) !important;
  color: #1a1a1a !important;
  box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
}

.btn-gold:hover {
  transform: translateY(-4px) scale(1.02) !important;
  box-shadow: 0 10px 25px rgba(212, 175, 55, 0.5) !important;
}

/* الزر الطبي التركواز (للأزرار الثانوية) */
.btn-outline, .btn-outline-dark {
  background: transparent !important;
  color: var(--dental-teal) !important;
  border: 2px solid var(--dental-teal) !important;
  box-shadow: none !important;
}

.btn-outline:hover, .btn-outline-dark:hover {
  background: var(--dental-teal) !important;
  color: #ffffff !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 20px rgba(13, 148, 136, 0.3) !important;
}

/* 3. إصلاح الزوايا الحادة في الصناديق والنماذج */
input, select, textarea, .card, .modal-content, .bg-white, .bg-nile-beige {
  border-radius: 16px !important;
}

/* صناديق الإدخال */
input, select, textarea {
  border: 2px solid #E2E8F0 !important;
  padding: 1rem 1.2rem !important;
  background: #F8FAFC !important;
  transition: all 0.3s ease !important;
}

input:focus, select:focus, textarea:focus {
  border-color: var(--dental-teal) !important;
  background: #ffffff !important;
  box-shadow: 0 0 0 4px rgba(13, 148, 136, 0.1) !important;
  outline: none !important;
}

/* 4. إخفاء الأزرار الزائدة والمكررة لترتيب الصفحة */
/* إخفاء زر الاتصال في الهيدر لأنه مكرر مع الواتساب */
.header-cta { display: none !important; }

/* تصغير أزرار الباقات عشان ميبقوش ضخمين */
#packages .btn-gold { 
  font-size: 0.75rem !important; 
  padding: 0.7rem 1.5rem !important; 
}

/* 5. لمسة فرعونية فخمة للعناوين الرئيسية */
h2, h3 {
  color: #0F172A !important;
  letter-spacing: -0.02em !important;
}

/* تحويل اللون الذهبي النصي ليكون أوضح */
.text-nile-gold, .gold-text {
  background: linear-gradient(135deg, #B45309, #F59E0B, #B45309) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  font-weight: 800 !important;
}

/* 6. الشريط العلوي (Header) - زجاجي حديث */
.site-header {
  border-radius: 100px !important;
  margin-top: 10px !important;
  background: rgba(255, 255, 255, 0.85) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(255,255,255,0.5) !important;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05) !important;
}
</style>
<!-- ═══════════════════ END MAKEOVER ═══════════════════ -->
"""

def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('index.html')
    if not path.exists():
        print(f"❌ File not found: {path}")
        return

    html = path.read_text(encoding='utf-8')
    
    if 'id="modern-makeover"' in html:
        print("⚠️ Makeover already applied. Skipping...")
        return

    print(f"\n🎨 Applying Ultimate UI Makeover v6.0...\n")

    # حقن الكود قبل إغلاق الـ head
    if '</head>' in html:
        html = html.replace('</head>', CSS_MAKEOVER + '\n</head>')
        print("   ✅ Injected Modern CSS Theme")
    else:
        print("   ❌ </head> tag not found!")
        return

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup = path.with_name(f'{path.stem}.backup_v6_{ts}{path.suffix}')
    shutil.copy2(path, backup)
    
    path.write_text(html, encoding='utf-8')
    print(f"\n💾 Backup: {backup.name}")
    print(f"💾 Saved: {path.name}")
    print("\n🚀 Done! Open the website and Hard Refresh (Ctrl+F5)\n")

if __name__ == '__main__':
    main()