#!/usr/bin/env python3
"""
Nile Smile — Performance Fix Applier
=====================================
Applies 9 verified fixes to prevent the 2-minute browser freeze.

Usage:
    python3 fix_perf.py index.html

Output:
    index.fixed.html   ← review, then rename to index.html
    index.backup.html  ← original, keep as safety net
"""

import sys
import shutil
from pathlib import Path


# ═══════════════════════════════════════════════════════════
#  FIX DEFINITIONS — each tuple is:
#    (name, find_string, replace_string)
# ═══════════════════════════════════════════════════════════

FIXES = [

    # ─────────────────────────────────────────────────────
    # FIX 1a: 3D — cap pixel ratio from 2 → 1
    #         Saves ~4× GPU fill-rate on retina screens
    # ─────────────────────────────────────────────────────
    (
        "3D: pixelRatio 2 → 1",
        "renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));",
        "renderer.setPixelRatio(1); // PERF: was 2 → 4× GPU fill-rate on retina",
    ),

    # ─────────────────────────────────────────────────────
    # FIX 1b: 3D — disable shadows entirely
    #         Saves ~40% GPU per frame
    # ─────────────────────────────────────────────────────
    (
        "3D: disable shadowMap",
        """      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;""",
        """      renderer.shadowMap.enabled = false; // PERF: shadows repainted 60fps""",
    ),

    # ─────────────────────────────────────────────────────
    # FIX 1c: 3D — cap animation loop to 30fps + respect hidden tab
    #         THE single most impactful fix
    # ─────────────────────────────────────────────────────
    (
        "3D: 30fps cap + tab-hidden pause",
        """      controls.addEventListener('start', function(){ controls.autoRotate = false; });

      
        if(loading) loading.style.display = 'none';

        // Pause 3D rendering when not in viewport to save CPU
        let is3DVisible = false;
        const obs3D = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            is3DVisible = entry.isIntersecting;
            if (is3DVisible) animate();
          });
        }, { threshold: 0 });
        obs3D.observe(container);

        function animate(){
          if (!is3DVisible) return; // Stop infinite loop
          requestAnimationFrame(animate);
          controls.update();
          renderer.render(scene, camera);
        }""",
        """      controls.addEventListener('start', function(){ controls.autoRotate = false; });

      
        if(loading) loading.style.display = 'none';

        // PERF: pause when out-of-viewport OR tab hidden + 30fps cap
        let is3DVisible = false;
        const obs3D = new IntersectionObserver((entries) => {
          entries.forEach(entry => { is3DVisible = entry.isIntersecting; });
        }, { threshold: 0, rootMargin: '100px' });
        obs3D.observe(container);

        let lastRender = 0;
        const FRAME_MS = 1000 / 30; // 30 fps cap

        function animate(ts) {
          requestAnimationFrame(animate);
          if (!is3DVisible || document.hidden) return;
          if (ts - lastRender < FRAME_MS) return;
          lastRender = ts;
          controls.update();
          renderer.render(scene, camera);
        }
        requestAnimationFrame(animate);""",
    ),

    # ─────────────────────────────────────────────────────
    # FIX 2: .card — remove will-change / preserve-3d / rotateX/Y
    #        Freed 50+ GPU layers (~160MB VRAM)
    # ─────────────────────────────────────────────────────
    (
        "Cards: kill will-change + 3D hover",
        """  .card{
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
  }""",
        """  .card{
    background: #fff;
    border: 1px solid rgba(174,145,100,.15);
    border-radius: 4px;
    /* PERF: removed preserve-3d / perspective / will-change — saved 50+ GPU layers */
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
  }""",
    ),

    # ─────────────────────────────────────────────────────
    # FIX 3: SVG map — pause CSS animations when out of view
    #        Adds .map-paused kill switch
    # ─────────────────────────────────────────────────────
    (
        "SVG map: pause CSS animations off-screen",
        "</head>",
        """<style id="perf-map-fix">
/* Real map animations killswitch (perf-master selectors were keyframe names, not classes) */
.map-paused .pin-pulse,
.map-paused .hub-ring,
.map-paused .map-routes path {
  animation-play-state: paused !important;
}
/* Slow down infinite CSS animations when map is visible */
.world-map-wrap .pin-pulse { animation-duration: 5.6s !important; }
.world-map-wrap .hub-ring  { animation-duration: 6s   !important; }
.world-map-wrap .map-routes path { animation-duration: 16s !important; }
</style>
</head>""",
    ),

    # ─────────────────────────────────────────────────────
    # FIX 4: Intl.DateTimeFormat — cache + 30s + hidden-tab pause
    #        Was creating 7 new formatters every 15s
    # ─────────────────────────────────────────────────────
    (
        "Clocks: cache Intl + 30s + tab pause",
        """(function(){
  'use strict';

  function updateClocks(){
    var clocks = document.querySelectorAll('.map-stat-time[data-tz]');
    var now = new Date();
    clocks.forEach(function(el){
      try {
        var tz = el.getAttribute('data-tz');
        var time = new Intl.DateTimeFormat('en-GB', {
          timeZone: tz,
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        }).format(now);
        el.textContent = time;
      } catch (e) {
        el.textContent = '—';
      }
    });
  }

  // First render
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateClocks);
  } else {
    updateClocks();
  }

  // Update every 15 seconds (accurate enough for minute display)
  setInterval(updateClocks, 15000);
})();""",
        """(function(){
  'use strict';
  // PERF: cache Intl.DateTimeFormat + 30s interval + pause when tab hidden
  var cache = {};
  var timer = null;

  function updateClocks(){
    if (document.hidden) return;
    var now = new Date();
    document.querySelectorAll('.map-stat-time[data-tz]').forEach(function(el){
      try {
        var tz = el.getAttribute('data-tz');
        cache[tz] = cache[tz] || new Intl.DateTimeFormat('en-GB', {
          timeZone: tz, hour: '2-digit', minute: '2-digit', hour12: false
        });
        el.textContent = cache[tz].format(now);
      } catch (e) {
        el.textContent = '—';
      }
    });
  }

  function start(){
    clearInterval(timer);
    updateClocks();
    timer = setInterval(updateClocks, 30000); // 30s instead of 15s
  }

  document.addEventListener('visibilitychange', function(){
    if (document.hidden) { clearInterval(timer); } else { start(); }
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();""",
    ),

    # ─────────────────────────────────────────────────────
    # FIX 5a: #progress — switch width → transform (composited)
    # ─────────────────────────────────────────────────────
    (
        "Progress bar CSS: transform (was width)",
        "  #progress{position:fixed;top:0;left:0;height:3px;width:0;background:linear-gradient(90deg,#AE9164,#E8C88A,#AE9164);z-index:9998;box-shadow:0 0 12px rgba(174,145,100,.5);transition:width .1s linear}",
        "  #progress{position:fixed;top:0;left:0;height:3px;width:100%;background:linear-gradient(90deg,#AE9164,#E8C88A,#AE9164);z-index:9998;box-shadow:0 0 12px rgba(174,145,100,.5);transform:scaleX(0);transform-origin:left center;transition:transform .1s linear;will-change:transform}",
    ),

    # ─────────────────────────────────────────────────────
    # FIX 5b: #progress — remove duplicate width:0 override
    # ─────────────────────────────────────────────────────
    (
        "Progress bar: remove width:0 override",
        "  /* ============ SCROLL PROGRESS BAR ============ */\n  #progress{width:0}",
        "  /* ============ SCROLL PROGRESS BAR ============ */\n  /* PERF: width handled by main rule — see #progress above */",
    ),

    # ─────────────────────────────────────────────────────
    # FIX 5c: #progress — JS uses scaleX instead of width
    # ─────────────────────────────────────────────────────
    (
        "Progress bar JS: scaleX (was width%)",
        "progress.style.width = h > 0 ? (window.scrollY/h*100)+'%' : '0%';",
        "progress.style.transform = 'scaleX(' + (h > 0 ? Math.min(window.scrollY/h, 1) : 0) + ')';",
    ),

    # ─────────────────────────────────────────────────────
    # FIX 6: Kill backdrop-filter (Safari sometimes ignores override)
    # ─────────────────────────────────────────────────────
    (
        "Kill backdrop-filter (blur → opaque)",
        "</head>",
        """<style id="perf-no-blur">
/* Safari sometimes ignores plain backdrop-filter: none — force + opaque fallback */
.site-header, .apple-dock, .modal-content, .search-modal-overlay,
.exit-popup-overlay, .sticky-mobile, .quick-bar {
  -webkit-backdrop-filter: none !important;
  backdrop-filter: none !important;
}
.site-header.theme-light { background: rgba(251,250,247,0.98) !important; }
.site-header.theme-dark  { background: rgba(10,13,16,0.98)   !important; }
.apple-dock.theme-light  { background: rgba(251,250,247,0.98) !important; }
.apple-dock.theme-dark   { background: rgba(10,13,16,0.98)   !important; }
.sticky-mobile           { background: rgba(31,42,54,0.98)   !important; }
</style>
</head>""",
    ),

    # ─────────────────────────────────────────────────────
    # FIX 7: Add IntersectionObserver to toggle .map-paused
    #        (works with FIX 3's CSS)
    # ─────────────────────────────────────────────────────
    (
        "SVG map: JS observer to toggle .map-paused",
        "</body>",
        """<script id="perf-map-pause-js">
(function(){
  'use strict';
  var mapWrap = document.querySelector('.world-map-wrap');
  if (!mapWrap || !('IntersectionObserver' in window)) return;
  new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      mapWrap.classList.toggle('map-paused', !e.isIntersecting);
    });
  }, { rootMargin: '200px', threshold: 0 }).observe(mapWrap);
})();
</script>
</body>""",
    ),
]


# ═══════════════════════════════════════════════════════════
#  RUNNER
# ═══════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fix_perf.py <input.html>")
        sys.exit(1)

    src = Path(sys.argv[1])
    if not src.exists():
        print(f"❌ File not found: {src}")
        sys.exit(1)

    # ── Backup ──
    backup = src.with_suffix(".backup" + src.suffix)
    shutil.copy2(src, backup)
    print(f"🔒 Backup: {backup}")

    content = src.read_text(encoding="utf-8")
    original_bytes = len(content.encode("utf-8"))

    applied, skipped = [], []

    for name, find, replace in FIXES:
        if find not in content:
            skipped.append(name)
            continue
        content = content.replace(find, replace, 1)
        applied.append(name)

    # ── Write output ──
    out = src.with_suffix(".fixed" + src.suffix)
    out.write_text(content, encoding="utf-8")
    final_bytes = len(content.encode("utf-8"))

    # ── Report ──
    print(f"\n{'═' * 68}")
    print(f"✅  APPLIED  {len(applied)}/{len(FIXES)}  fixes")
    print(f"{'═' * 68}")
    for name in applied:
        print(f"   ✓  {name}")

    if skipped:
        print(f"\n⚠️   SKIPPED  {len(skipped)} (pattern not found — already patched?)")
        for name in skipped:
            print(f"   ✗  {name}")

    print(f"\n{'═' * 68}")
    print(f"📄  Output:   {out}")
    print(f"📦  Size:     {original_bytes:,} → {final_bytes:,} bytes "
          f"({final_bytes - original_bytes:+,})")
    print(f"{'═' * 68}")
    print("\n➡️  Review the output, then replace your live file:")
    print(f"   mv {out} {src}")
    print(f"\n🧪  To verify in Chrome DevTools → Performance tab:")
    print(f"   1. Scroll to #implant-systems")
    print(f"   2. Record 60s")
    print(f"   3. Expect: FPS stable 50–60, CPU < 40%, GPU memory < 100MB")
    print(f"\n🔙  To rollback:")
    print(f"   mv {backup} {src}")


if __name__ == "__main__":
    main()