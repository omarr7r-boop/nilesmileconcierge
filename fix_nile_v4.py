import os

def fix_performance():
    input_file = 'index.html'
    output_file = 'index_fixed.html'

    if not os.path.exists(input_file):
        print(f"❌ خطأ: مش لاقي ملف اسمه {input_file}")
        print("تأكد إنك غيرت اسم الملف لـ index.html وحطيته في نفس الفولدر ده.")
        return

    # قراءة الملف
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. إصلاح الـ 3D (تقليل الجودة وإيقاف الظلال)
    content = content.replace(
        "renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));",
        "renderer.setPixelRatio(1);"
    )
    content = content.replace(
        "renderer.shadowMap.enabled = true;",
        "renderer.shadowMap.enabled = false;"
    )

    # 2. إصلاح أنيميشن الـ 3D (تحديده بـ 30 فريم/ثانية + إيقافه لو التاب مش مفتوح)
    old_animate = """        function animate(){
          if (!is3DVisible) return; // Stop infinite loop
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
        print("✅ تم إصلاح كود أنيميشن الـ 3D")
    else:
        print("⚠️ مش لاقي كود أنيميشن الـ 3D (ممكن يكون اتعدل قبل كده)")

    # 3. إصلاح كروت الموقع (شيل will-change و preserve-3d)
    old_card_css = """  .card{
    background: #fff;
    border: 1px solid rgba(174,145,100,.15);
    border-radius: 4px;
    transform-style: preserve-3d;
    perspective: 1000px;
    transition: transform 0.55s cubic-bezier(0.16, 1, 0.3, 1),
                box-shadow 0.55s cubic-bezier(0.16, 1, 0.3, 1),
                border-color 0.3s ease;
    will-change: transform;
  }
  .card:hover{
    transform: translateY(-8px) rotateX(1.2deg) rotateY(-1.2deg) scale(1.015);
    box-shadow: 0 30px 60px rgba(79, 96, 112, 0.18),
                0 0 0 1px rgba(174, 145, 100, 0.2) inset;
    border-color: rgba(174,145,100,.4);
  }"""
    
    new_card_css = """  .card{
    background: #fff;
    border: 1px solid rgba(174,145,100,.15);
    border-radius: 4px;
    will-change: auto !important;
    transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1),
                box-shadow 0.35s cubic-bezier(0.16, 1, 0.3, 1),
                border-color 0.3s ease;
  }
  .card:hover{
    transform: translateY(-5px) scale(1.004);
    box-shadow: 0 16px 36px rgba(79, 96, 112, 0.13),
                0 0 0 1px rgba(174, 145, 100, 0.2) inset;
    border-color: rgba(174,145,100,.4);
  }"""

    if old_card_css in content:
        content = content.replace(old_card_css, new_card_css)
        print("✅ تم إصلاح كود الـ CSS بتاع الكروت")
    else:
        print("⚠️ مش لاقي كود الـ CSS بتاع الكروت")

    # 4. إصلاح الساعة (زيادة المدة لـ 30 ثانية بدل 15)
    content = content.replace(
        "setInterval(updateClocks, 15000);",
        "setInterval(updateClocks, 30000);"
    )

    # 5. إصلاح شريط التقدم (استخدام transform بدل width عشان الأداء)
    content = content.replace(
        "#progress{position:fixed;top:0;left:0;height:3px;width:0;background:linear-gradient(90deg,#AE9164,#E8C88A,#AE9164);z-index:9998;box-shadow:0 0 12px rgba(174,145,100,.5);transition:width .1s linear}",
        "#progress{position:fixed;top:0;left:0;height:3px;width:100%;background:linear-gradient(90deg,#AE9164,#E8C88A,#AE9164);z-index:9998;box-shadow:0 0 12px rgba(174,145,100,.5);transform:scaleX(0);transform-origin:left center;transition:transform .1s linear;will-change:transform}"
    )
    content = content.replace(
        "progress.style.width = h > 0 ? (window.scrollY/h*100)+'%' : '0%';",
        "progress.style.transform = 'scaleX(' + (h > 0 ? Math.min(window.scrollY/h, 1) : 0) + ')';"
    )

    # حفظ الملف الجديد
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("\n====================================")
    print(f"🎉 تم إنشاء ملف جديد اسمه: {output_file}")
    print("كل الإصلاحات اتطبقت بنجاح!")
    print("====================================")
    print("الخطوة الجاية: غير اسم الملف القديم لـ index_old.html")
    print("وغير اسم الملف الجديد من index_fixed.html لـ index.html")

if __name__ == '__main__':
    fix_performance()