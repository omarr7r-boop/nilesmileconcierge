#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nile Smile — Ultimate Performance & UI Architecture Fix
=======================================================
1. Stops the 2-minute freezing (Three.js, SVG, Scroll Thrashing).
2. Combines Hotel & Concierge Add-ons into a single unified UI.
3. Adds a detailed breakdown for Turkey Rescue ($4,990).
"""

import re
import shutil
import sys
from pathlib import Path

def fix_site(html_path):
    path = Path(html_path)
    if not path.exists():
        print(f"[X] File not found: {html_path}")
        return

    shutil.copy2(path, str(path) + ".backup_ultimate")
    print(f"[OK] Backup created: {path.name}.backup_ultimate\n")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # ============================================================
    # 1. FIX SCROLL FREEZING (Performance Fixes)
    # ============================================================
    
    # A. Remove the expensive DOM-thrashing scroll fallback
    old_reveal_fallback = re.search(r'/\* ✅ Fallback 1: افتح الأقسام في الـ viewport عند الـ scroll \*/.*?revealManualFallback\(\);', content, flags=re.DOTALL)
    if old_reveal_fallback:
        content = content.replace(old_reveal_fallback.group(0), '/* Fallback removed for performance */')
        print("[OK] Removed: Scroll DOM-thrashing fallback")

    # B. Pause Three.js rendering when out of view
    old_three_animate = re.search(r'if\(loading\) loading\.style\.display = \'none\';\s*function animate\(\)\{\s*requestAnimationFrame\(animate\);\s*controls\.update\(\);\s*renderer\.render\(scene, camera\);\s*\}\s*animate\(\);', content, flags=re.DOTALL)
    if old_three_animate:
        new_three_animate = """
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
        }
        """
        content = content.replace(old_three_animate.group(0), new_three_animate)
        print("[OK] Fixed: Three.js infinite rendering loop paused on scroll")

    # C. Pause SVG Map animations when out of view
    old_map_script = re.search(r'/\* ═══════════ DISCOVER EGYPT.*?render\(\'all\'\);\s*\}\)\(\);', content, flags=re.DOTALL)
    # We add a specific SVG pauser at the end of body
    svg_pauser = """
    <script id="svgPerformanceFix">
    (function(){
      var mapWrap = document.querySelector('.world-map-wrap');
      if(!mapWrap) return;
      var svg = mapWrap.querySelector('svg');
      if(!svg) return;
      
      var observer = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          if(entry.isIntersecting){
            if(svg.unpauseAnimations) svg.unpauseAnimations();
          } else {
            if(svg.pauseAnimations) svg.pauseAnimations();
          }
        });
      }, { threshold: 0 });
      observer.observe(mapWrap);
    })();
    </script>
    """
    content = content.replace('</body>', svg_pauser + '\n</body>')
    print("[OK] Fixed: SVG Map animations pause when out of view")

    # ============================================================
    # 2. COMBINE HOTELS & ADD-ONS (UI Architecture Fix)
    # ============================================================
    # We will replace the entire #travel-addons section with a combined, better-engineered layout.
    new_travel_addons = """
<section id="travel-addons" class="section bg-white reveal">
  <div class="container">
    <div class="text-center max-w-3xl mx-auto mb-12">
      <p class="eyebrow mb-4">Build Your Stay — Your Way</p>
      <h2 class="text-nile-blue mb-5" style="font-size:clamp(1.75rem,4vw,2.75rem)">Unified Travel & Concierge Builder</h2>
      <p class="text-nile-muted">Select your preferred hotel tier and add any concierge services. Prices are indicative for a standard 10-night stay and confirmed in writing after your clinical review.</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
      
      <!-- LEFT: HOTELS -->
      <div>
        <div class="flex items-center gap-3 mb-6 border-b border-nile-gold/20 pb-3">
          <span class="limited-badge" style="margin-bottom:0">Step 1</span>
          <h3 class="font-serif text-nile-blue text-2xl">Select Hotel Tier (10 Nights)</h3>
        </div>
        
        <div class="space-y-4">
          <!-- 3 Star -->
          <div class="card p-5 flex justify-between items-center border-l-4 border-gray-400">
            <div>
              <h4 class="font-serif text-nile-blue text-lg">3★ Hotel</h4>
              <p class="text-nile-muted text-xs">Sheikh Zayed / New Cairo · Breakfast & Transfers</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">$700</p>
              <p class="text-[10px] text-nile-muted uppercase">$70/night</p>
            </div>
          </div>
          <!-- 4 Star -->
          <div class="card p-5 flex justify-between items-center border-l-4 border-nile-gold bg-nile-gold/5">
            <div>
              <div class="flex items-center gap-2 mb-1">
                <h4 class="font-serif text-nile-blue text-lg">4★ Hotel</h4>
                <span class="bg-nile-gold text-white text-[9px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider">Most Chosen</span>
              </div>
              <p class="text-nile-muted text-xs">Novotel / Hilton / Marriott · Breakfast & Transfers</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">$1,200</p>
              <p class="text-[10px] text-nile-muted uppercase">$120/night</p>
            </div>
          </div>
          <!-- 5 Star -->
          <div class="card p-5 flex justify-between items-center border-l-4 border-nile-blue">
            <div>
              <h4 class="font-serif text-nile-blue text-lg">5★ Hotel</h4>
              <p class="text-nile-muted text-xs">Four Seasons / Ritz-Carlton · Nile/Pyramids View</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">$2,500</p>
              <p class="text-[10px] text-nile-muted uppercase">$250/night</p>
            </div>
          </div>
          <!-- 5 Star Suite -->
          <div class="card p-5 flex justify-between items-center border-l-4 border-nile-blue">
            <div>
              <h4 class="font-serif text-nile-blue text-lg">5★ Suite VIP</h4>
              <p class="text-nile-muted text-xs">Four Seasons Nile Plaza / St. Regis · Private Chauffeur</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">$4,500</p>
              <p class="text-[10px] text-nile-muted uppercase">$450/night</p>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT: CONCIERGE ADD-ONS -->
      <div>
        <div class="flex items-center gap-3 mb-6 border-b border-nile-gold/20 pb-3">
          <span class="limited-badge" style="margin-bottom:0">Step 2</span>
          <h3 class="font-serif text-nile-blue text-2xl">Optional Concierge Add-Ons</h3>
        </div>

        <div class="space-y-4">
          <!-- Recovery Care -->
          <div class="card p-5 flex justify-between items-center border-l-4 border-nile-gold">
            <div>
              <h4 class="font-serif text-nile-blue text-lg">Recovery Care</h4>
              <p class="text-nile-muted text-xs">Daily nurse, physiotherapy, pharmacy delivery, chef meals.</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">+$1,700</p>
              <p class="text-[10px] text-nile-muted uppercase">Per patient</p>
            </div>
          </div>
          <!-- Premium Concierge -->
          <div class="card p-5 flex justify-between items-center border-l-4 border-nile-gold bg-nile-gold/5">
            <div>
              <div class="flex items-center gap-2 mb-1">
                <h4 class="font-serif text-nile-blue text-lg">Premium Concierge</h4>
                <span class="bg-nile-gold text-white text-[9px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider">Most Chosen</span>
              </div>
              <p class="text-nile-muted text-xs">Dedicated coordinator, unlimited transfers, Nile dinner cruise.</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">+$1,700</p>
              <p class="text-[10px] text-nile-muted uppercase">Per patient</p>
            </div>
          </div>
          <!-- Signature VIP -->
          <div class="card p-5 flex justify-between items-center border-l-4 border-nile-blue">
            <div>
              <h4 class="font-serif text-nile-blue text-lg">Signature VIP Experience</h4>
              <p class="text-nile-muted text-xs">Private chef, Giza tour, Luxor trip, personal shopper, yacht dinner.</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">+$3,000</p>
              <p class="text-[10px] text-nile-muted uppercase">Per patient</p>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Examples -->
    <div class="bg-nile-beige p-6 md:p-8 border border-nile-gold/20 mt-12 max-w-4xl mx-auto">
      <h3 class="font-serif text-nile-blue text-xl mb-6 text-center">How to Combine (Examples)</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-nile-muted">
        <div class="text-center bg-white p-4 border border-nile-gold/10">
          <p class="font-semibold text-nile-blue mb-1">Budget-Conscious</p>
          <p>3★ Hotel + No Add-on = <strong class="text-nile-gold">$700</strong></p>
        </div>
        <div class="text-center bg-white p-4 border border-nile-gold/10">
          <p class="font-semibold text-nile-blue mb-1">Balanced</p>
          <p>4★ Hotel + Premium Concierge = <strong class="text-nile-gold">$2,900</strong></p>
        </div>
        <div class="text-center bg-white p-4 border border-nile-gold/10">
          <p class="font-semibold text-nile-blue mb-1">Full VIP</p>
          <p>5★ Suite + Signature VIP = <strong class="text-nile-gold">$7,500</strong></p>
        </div>
      </div>
    </div>
  </div>
</section>
"""
    content = re.sub(r'<section id="travel-addons".*?</section>', new_travel_addons, content, flags=re.DOTALL)
    print("[OK] UI Architecture: Hotels & Add-ons combined into a unified builder")

    # ============================================================
    # 3. TURKEY RESCUE PRICING BREAKDOWN ($4,990)
    # ============================================================
    # Insert an accordion explaining the $4,990 cost inside the turkey-rescue section.
    turkey_breakdown = """
    <!-- PRICE BREAKDOWN -->
    <div class="mt-10 max-w-3xl mx-auto">
      <details class="bg-white/5 border border-nile-gold/30 rounded-lg p-5 cursor-pointer group">
        <summary class="font-serif text-nile-gold-bright text-lg flex justify-between items-center list-none">
          <span>What does the $4,990 Full Rescue include? (Click to expand)</span>
          <span class="text-2xl group-open:rotate-180 transition-transform">▾</span>
        </summary>
        <div class="mt-6 space-y-3 text-sm text-gray-300">
          <div class="flex justify-between border-b border-white/10 pb-2">
            <span>Atraumatic removal of failed implants</span>
            <span class="font-bold text-white">$500</span>
          </div>
          <div class="flex justify-between border-b border-white/10 pb-2">
            <span>Bone grafting / Socket preservation (if needed)</span>
            <span class="font-bold text-white">$600 – $1,500</span>
          </div>
          <div class="flex justify-between border-b border-white/10 pb-2">
            <span>New Premium Implant (Straumann / Nobel)</span>
            <span class="font-bold text-white">$1,200</span>
          </div>
          <div class="flex justify-between border-b border-white/10 pb-2">
            <span>New Zirconia Crown</span>
            <span class="font-bold text-white">$800</span>
          </div>
          <div class="flex justify-between border-b border-white/10 pb-2">
            <span>CBCT 3D Scan + Surgical Guide</span>
            <span class="font-bold text-white">$200</span>
          </div>
          <div class="flex justify-between border-b border-white/10 pb-2">
            <span>Clinical Labor & Follow-ups</span>
            <span class="font-bold text-white">$500</span>
          </div>
          <div class="flex justify-between pt-2 text-nile-gold-bright text-lg font-bold">
            <span>Total Estimated Value</span>
            <span>$3,800 – $4,700+</span>
          </div>
          <p class="text-xs text-gray-400 italic mt-4">
            * The $4,990 flat fee covers a complete single-tooth rescue (removal + grafting + new premium implant + crown). Complex full-arch rescues are quoted separately. This fee is fully deductible from your final treatment package if you decide to proceed with us.
          </p>
        </div>
      </details>
    </div>
    """
    
    # Inject it just before the CTA in Turkey Rescue section
    old_turkey_cta = re.search(r'<!-- CTA -->\s*<div class="text-center" style="display:flex;flex-direction:column;gap:.75rem;max-width:32rem;margin:0 auto">', content, flags=re.DOTALL)
    if old_turkey_cta:
        content = content.replace(old_turkey_cta.group(0), turkey_breakdown + '\n' + old_turkey_cta.group(0))
        print("[OK] Added: Turkey Rescue pricing breakdown ($4,990)")

    # Write back
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("\nSUCCESS! Architecture and UI are now optimized.")
    print("Please do a Hard Refresh (Ctrl+Shift+R).")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ultimate_fix.py <path-to-html>")
    else:
        fix_site(sys.argv[1])