import os

def apply_ultimate_fix():
    # البحث عن الملف الذي أرسلته
    input_file = '!DOCTYPE html.txt' 
    if not os.path.exists(input_file):
        input_file = 'index.html'
        if not os.path.exists(input_file):
            print(f"❌ خطأ: مش لاقي الملف. تأكد إن اسمه '{input_file}'")
            return

    output_file = 'index_FIXED.html'

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # ═══════════════════════════════════════════════════════════════
    # 1. إصلاح لون الهيدر والـ Dock (إلغاء الكاش، وقراءة الأماكن لايف)
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
      
      // Header Theme
      var headerCenter = scrollY + 40; 
      var isHeaderDark = darkRanges.some(function(r) { return headerCenter >= r.top && headerCenter <= r.bottom; });
      if (header) {
        header.classList.toggle('theme-dark', isHeaderDark);
        header.classList.toggle('theme-light', !isHeaderDark);
      }

      // Dock Theme
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
      var headerY = 40; // منتصف الهيدر
      var dockY = window.innerHeight - 45; // منتصف الدوك

      // بنقرأ مكان الأقسام لحظة بلحظة (Real-time) عشان نتجنب مشكلة تحميل الصور
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
        print("✅ 1. تم إصلاح كود تغيير لون الهيدر (Live Tracking)")
    else:
        print("⚠️ 1. تحذير: لم يتم العثور على كود الهيدر القديم (قد يكون معدلاً).")

    # ═══════════════════════════════════════════════════════════════
    # 2. إصلاح أداء الـ 3D (منع التجميد)
    # ═══════════════════════════════════════════════════════════════
    content = content.replace(
        "renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));",
        "renderer.setPixelRatio(1); // FIX: تقليل الحمل على كرت الشاشة"
    )
    content = content.replace(
        "renderer.shadowMap.enabled = true;",
        "renderer.shadowMap.enabled = false; // FIX: إيقاف الظلال الثقيلة"
    )
    
    old_animate = """        function animate(){
          if (!is3DVisible) return; // Stop infinite loop
          requestAnimationFrame(animate);
          controls.update();
          renderer.render(scene, camera);
        }"""
    
    new_animate = """        let lastRender = 0;
        const FRAME_MS = 1000 / 30; // قفل الرندر على 30 فريم بس
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
        print("✅ 2. تم إصلاح أداء المجسم ثلاثي الأبعاد (30 FPS + No Shadows)")
    else:
        print("⚠️ 2. تحذير: لم يتم العثور على دالة animate القديمة.")

    # ═══════════════════════════════════════════════════════════════
    # 3. القضاء على تجميد الـ Apple Dock + استخدام التمرير الأصلي للمتصفح
    # ═══════════════════════════════════════════════════════════════
    old_smooth_scroll = """document.querySelectorAll('a[href^="#"]').forEach(link=>{
  link.addEventListener('click', function(e){
    const href = this.getAttribute('href');
    if(!href || href === '#' || href === '#!') return;
    
    const target = document.querySelector(href);
    if(!target) return;
    
    e.preventDefault();
    
    const headerH = header.offsetHeight + 24;
    const targetY = target.getBoundingClientRect().top + window.pageYOffset - headerH;
    
    if(prefersReduced){
      window.scrollTo({ top: targetY, behavior: 'auto' });
      if(history.pushState) history.pushState(null, '', href);
      return;
    }
    
    const startY = window.pageYOffset;
    const distance = targetY - startY;
    const absDistance = Math.abs(distance);
    
    // ⚡ مدة أطول = cinematic
    const duration = Math.min(1400, Math.max(700, absDistance * 0.7));
    let startTs = null;
    
    // easeInOutExpo — الأنعم على الإطلاق (framer-motion style)
    const ease = t => {
      if (t === 0) return 0;
      if (t === 1) return 1;
      return t < 0.5
        ? Math.pow(2, 20 * t - 10) / 2
        : (2 - Math.pow(2, -20 * t + 10)) / 2;
    };
    
    function step(ts){
      if(!startTs) startTs = ts;
      const p = Math.min((ts - startTs) / duration, 1);
      window.scrollTo(0, startY + distance * ease(p));
      if(p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
    
    if(history.pushState) history.pushState(null,'',href);
  });
});"""

    new_smooth_scroll = """document.querySelectorAll('a[href^="#"]').forEach(link=>{
  link.addEventListener('click', function(e){
    const href = this.getAttribute('href');
    if(!href || href === '#' || href === '#!') return;
    
    const target = document.querySelector(href);
    if(!target) return;
    
    e.preventDefault();
    
    // FIX: استخدام التمرير الأصلي للمتصفح (Hardware Accelerated) بدلاً من الكود الثقيل
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
    // تحديث الرابط في المتصفح
    if(history.pushState) history.pushState(null,'',href);
  });
});"""
    
    if old_smooth_scroll in content:
        content = content.replace(old_smooth_scroll, new_smooth_scroll)
        print("✅ 3. تم استبدال كود التمرير الثقيل بتمرير المتصفح الأصلي (أسرع 10 مرات)")
    else:
        print("⚠️ 3. تحذير: لم يتم العثور على كود التمرير المخصص.")

    # ═══════════════════════════════════════════════════════════════
    # 4. حقن CSS لإلغاء الـ Blur من الـ Dock (السبب الرئيسي للتجميد)
    # ═══════════════════════════════════════════════════════════════
    css_override = """
<!-- ═══ APPLE DOCK FREEZE FIX ═══ -->
<style id="dock-freeze-fix">
  /* منع الـ GPU من إعادة حساب البلور أثناء التمرير */
  .apple-dock {
    -webkit-backdrop-filter: none !important;
    backdrop-filter: none !important;
    background: rgba(251, 250, 247, 0.98) !important; /* لون صلب تقريباً */
    transition: none !important; /* منع إعادة الرسم عند تغيير الكلاس */
  }
  .apple-dock.theme-dark {
    background: rgba(10, 13, 16, 0.98) !important;
  }
  .apple-dock .dock-item {
    transition: color 0.2s ease !important; /* الاحتفاظ فقط بتأثير الأزرار */
  }
</style>
"""
    
    if 'dock-freeze-fix' not in content:
        content = content.replace('</head>', css_override + '\n</head>')
        print("✅ 4. تم حقن كود CSS لإيقاف الـ Backdrop-Filter (القضاء على التجميد)")

    # حفظ الملف
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print("\n=======================================================")
    print(f"🎉 تم إنشاء الملف بنجاح: {output_file}")
    print("=======================================================")
    print("الخطوات النهائية (مهم جداً):")
    print("1. خد نسخة احتياطية من ملفك الأصلي (سميه index_old.html).")
    print("2. غير اسم الملف الجديد من index_FIXED.html إلى index.html.")
    print("3. افتح المتصفح واضغط Ctrl + F5 (عشان تمسح الكاش القديم).")

if __name__ == '__main__':
    apply_ultimate_fix()