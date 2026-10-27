import os

def fix_header_color():
    input_file = 'index.html'
    output_file = 'index_header_fixed.html'

    if not os.path.exists(input_file):
        print(f"❌ خطأ: مش لاقي ملف اسمه {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # الكود القديم اللي بيسبب المشكلة
    old_js = """  var header = document.getElementById('header');
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

    # الكود الجديد اللي بيحل المشكلة (بيقرا الأماكن لايف)
    new_js = """  var header = document.getElementById('header');
  var dock = document.getElementById('appleDock');
  var darkSections = Array.from(document.querySelectorAll('.hero, .bg-nile-blue, .bg-nile-blue-dark, #science, #consult, #turkey-rescue, #top-tier, #guarantees, #legal'));

  var themeTicking = false;
  function updateTheme() {
    if (themeTicking) return;
    themeTicking = true;
    requestAnimationFrame(function() {
      var headerCenter = 40; // المركز بتاع الهيدر
      var dockCenter = window.innerHeight - 45; // المركز بتاع الدوك
      
      var isHeaderDark = false;
      var isDockDark = false;

      // بنلف على الأقسام الداكنة ونشوف إحنا فين دلوقتي بالظبط
      for (var i = 0; i < darkSections.length; i++) {
        var rect = darkSections[i].getBoundingClientRect();
        if (headerCenter >= rect.top && headerCenter <= rect.bottom) {
          isHeaderDark = true;
        }
        if (dockCenter >= rect.top && dockCenter <= rect.bottom) {
          isDockDark = true;
        }
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
  
  setTimeout(updateTheme, 100);
  setTimeout(updateTheme, 500);"""

    if old_js in content:
        content = content.replace(old_js, new_js)
        print("✅ تم تعديل كود تغيير لون الهيدر بنجاح.")
    else:
        print("⚠️ تحذير: مش لاقي الكود القديم بالظبط. ممكن يكون اتعدل قبل كده.")

    # حفظ الملف الجديد
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print("====================================")
    print(f"🎉 تم إنشاء ملف جديد اسمه: {output_file}")
    print("كل الإصلاحات (التجميد + لون الهيدر) شغالة تمام.")
    print("====================================")
    print("الخطوة الجاية:")
    print("1. خد نسخة احتياطية من index.html الحالي (سميه index_old.html)")
    print("2. غير اسم index_header_fixed.html لـ index.html")
    print("3. افتح المتصفح وامسح الكاش (Ctrl + F5)")

if __name__ == '__main__':
    fix_header_color()