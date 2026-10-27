import os
import re

def apply_final_fix():
    input_file = '!DOCTYPE html.txt' 
    if not os.path.exists(input_file):
        input_file = 'index.html'
        if not os.path.exists(input_file):
            print(f"❌ خطأ: مش لاقي الملف. تأكد إن اسمه '{input_file}'")
            return

    output_file = 'index_FINAL.html'

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # ═══════════════════════════════════════════════════════════════
    # 1. القضاء على سبب الكراش (إلغاء view-transition والـ JS المخصص للتمرير)
    # ═══════════════════════════════════════════════════════════════
    # إزالة view-transition
    content = re.sub(r'@view-transition\s*\{[^}]*\}', '', content)
    
    # إزالة كود التمرير القديم (الذي كان يسبب الكراش)
    old_scroll_pattern = r"document\.querySelectorAll\('a\[href\^=\"#\"\]'\)\.forEach\(link=>\{.*?\}\);"
    content = re.sub(old_scroll_pattern, "", content, flags=re.DOTALL)
    
    # التأكد من وجود التمرير السلس الأصلي في CSS
    if 'scroll-behavior: smooth' not in content:
        content = content.replace('html{', 'html{ scroll-behavior: smooth; scroll-padding-top: 92px;')

    # ═══════════════════════════════════════════════════════════════
    # 2. إصلاح لون الهيدر (قراءة لايف لمنع مشكلة تحميل الصور)
    # ═══════════════════════════════════════════════════════════════
    old_header_logic = """  var header = document.getElementById('header');
  var dock = document.getElementById('appleDock');
  var darkSections = document.querySelectorAll('.hero, .bg-nile-blue, .bg-nile-blue-dark, #science, #consult, #turkey-rescue, #top-tier, #guarantees, #legal');
  var darkRanges = [];

  function calculateRanges() {
    darkRanges = Array.from(darkSections).map(function(sec) {
      var rect = sec.getBoundingClientRect();
      var top = rect.top + window.scrollY;
      return { top: top, bottom: top + rect.height };
    });
  }

  var themeTicking = false;
  function updateTheme() {
    if (themeTicking) return;
    themeTicking = true;
    requestAnimationFrame(function() {
      var scrollY = window.scrollY;
      
      var headerCenter = scrollY + 40; 
      var isHeaderDark = darkRanges.some(function(r) { return headerCenter >= r.top && headerCenter <= r.bottom; });
      if (header) {
        header.classList.toggle('theme-dark', isHeaderDark);
        header.classList.toggle('theme-light', !isHeaderDark);
      }

      var dockCenter = scrollY + window.innerHeight - 45;
      var isDockDark = darkRanges.some(function(r) { return dockCenter >= r.top && dockCenter <= r.bottom; });
      if (dock) {
        dock.classList.toggle('theme-dark', isDockDark);
        dock.classList.toggle('theme-light', !isDockDark);
      }
      
      themeTicking = false;
    });
  }

  window.addEventListener('load', calculateRanges);
  window.addEventListener('resize', function() { calculateRanges(); updateTheme(); });
  window.addEventListener('scroll', updateTheme, { passive: true });
  
  setTimeout(calculateRanges, 100);
  setTimeout(updateTheme, 200);"""

    new_header_logic = """  var header = document.getElementById('header');
  var dock = document.getElementById('appleDock');
  var darkSections = Array.from(document.querySelectorAll('.hero, .bg-nile-blue, .bg-nile-blue-dark, #science, #consult, #turkey-rescue, #top-tier, #guarantees, #legal'));

  var themeTicking = false;
  function updateTheme() {
    if (themeTicking) return;
    themeTicking = true;
    requestAnimationFrame(function() {
      var isHeaderDark = false;
      var isDockDark = false;
      var headerY = 40;
      var dockY = window.innerHeight - 45;

      for (var i = 0; i < darkSections.length; i++) {
        var rect = darkSections[i].getBoundingClientRect();
        if (headerY >= rect.top && headerY <= rect.bottom) isHeaderDark = true;
        if (dockY >= rect.top && dockY <= rect.bottom) isDockDark = true;
      }

      if (header) {
        header.classList.toggle('theme-dark', isHeaderDark);
        header.classList.toggle('theme-light', !isHeaderDark);
      }

      if (dock) {
        dock.classList.toggle('theme-dark', isDockDark);
        dock.classList.toggle('theme-light', !isDockDark);
      }
      
      themeTicking = false;
    });
  }

  window.addEventListener('scroll', updateTheme, { passive: true });
  window.addEventListener('resize', updateTheme, { passive: true });
  setTimeout(updateTheme, 200);"""
    
    if old_header_logic in content:
        content = content.replace(old_header_logic, new_header_logic)
        print("✅ 1. تم إصلاح كود لون الهيدر (Live Tracking)")
    else:
        print("⚠️ تحذير: لم يتم العثور على كود الهيدر القديم.")

    # ═══════════════════════════════════════════════════════════════
    # 3. إصلاح أداء الـ 3D (منع التجميد)
    # ═══════════════════════════════════════════════════════════════
    content = content.replace(
        "renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));",
        "renderer.setPixelRatio(1);"
    )
    content = content.replace(
        "renderer.shadowMap.enabled = true;",
        "renderer.shadowMap.enabled = false;"
    )
    
    old_animate = """        function animate(){
          if (!is3DVisible) return;
          requestAnimationFrame(animate);
          controls.update();
          renderer.render(scene, camera);
        }"""
    
    new_animate = """        let lastRender = 0;
        const FRAME_MS = 1000 / 30;
        function animate(ts) {
          requestAnimationFrame(animate);
          if (!is3DVisible || document.hidden) return;
          if (ts - lastRender < FRAME_MS) return;
          lastRender = ts;
          controls.update();
          renderer.render(scene, camera);
        }
        requestAnimationFrame(animate);"""
    
    if old_animate in content:
        content = content.replace(old_animate, new_animate)
        print("✅ 2. تم إصلاح أداء المجسم ثلاثي الأبعاد")
    else:
        print("⚠️ تحذير: لم يتم العثور على دالة animate القديمة.")

    # ═══════════════════════════════════════════════════════════════
    # 4. إيقاف تجميد الـ Apple Dock (إلغاء الـ Blur)
    # ═══════════════════════════════════════════════════════════════
    css_override = """
<!-- ═══ APPLE DOCK FREEZE FIX (NO JS CLONING) ═══ -->
<style id="dock-freeze-fix">
  .apple-dock {
    -webkit-backdrop-filter: none !important;
    backdrop-filter: none !important;
    background: rgba(251, 250, 247, 0.98) !important;
    transition: background-color 0.2s ease !important;
  }
  .apple-dock.theme-dark {
    background: rgba(10, 13, 16, 0.98) !important;
  }
</style>
"""
    
    if 'dock-freeze-fix' not in content:
        content = content.replace('</head>', css_override + '\n</head>')
        print("✅ 3. تم حقن كود CSS لإيقاف الـ Backdrop-Filter (القضاء على التجميد)")

    # حفظ الملف
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print("\n=======================================================")
    print(f"🎉 تم إنشاء الملف بنجاح: {output_file}")
    print("=======================================================")
    print("الخطوات النهائية:")
    print("1. خد نسخة احتياطية من ملفك الأصلي.")
    print("2. غير اسم الملف الجديد من index_FINAL.html إلى index.html.")
    print("3. افتح المتصفح واضغط Ctrl + F5 (عشان تمسح الكاش).")

if __name__ == '__main__':
    apply_final_fix()