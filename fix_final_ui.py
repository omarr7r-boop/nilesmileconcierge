#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nile Smile — Site Makeover & Performance Fix
=============================================
1. Fixes Scrolling Freeze (Removes custom JS smooth scroll)
2. Reorders sections logically (AIDA funnel)
3. Redesigns Travel Add-ons & Hotels (Combined UI)
"""

import re
import shutil
import sys
from pathlib import Path

def makeover_site(html_path):
    path = Path(html_path)
    if not path.exists():
        print(f"[X] File not found: {html_path}")
        return

    shutil.copy2(path, str(path) + ".backup_makeover")
    print(f"[OK] Backup created: {path.name}.backup_makeover\n")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # ============================================================
    # 1. REMOVE CUSTOM SMOOTH SCROLL (FIXES FREEZING)
    # ============================================================
    old_smooth_scroll = re.search(r'/\* ═════════ 6\. SMOOTH SCROLL — CINEMATIC ═════════ \*/.*?(?=/\* ═════════ 8\. HERO PARALLAX)', content, flags=re.DOTALL)
    if old_smooth_scroll:
        new_scroll = """
  /* ═════════ 6. NATIVE SMOOTH SCROLL (Performance Fix) ═════════ */
  // Custom JS smooth scroll removed to fix freezing with Dock buttons.
  // Native CSS scroll-behavior: smooth handles this much better.
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if(!href || href === '#' || href === '#!') return;
      const target = document.querySelector(href);
      if(!target) return;
      
      // Close mobile menu if open
      const menu = document.getElementById('mobileMenu');
      const btn = document.getElementById('menuBtn');
      if(menu && menu.classList.contains('open')){
        menu.classList.remove('open');
        if(btn) btn.classList.remove('open');
      }
      // Let the browser handle the scrolling naturally via CSS
    });
  });

  """
        content = content.replace(old_smooth_scroll.group(0), new_scroll)
        print("[OK] Fixed: Removed custom JS smooth scroll (Prevents Freezing)")

    # ============================================================
    # 2. REDESIGN TRAVEL ADD-ONS (Hotels & Concierge)
    # ============================================================
    new_travel_addons = """
<section id="travel-addons" class="section bg-white reveal">
  <div class="container">
    <div class="text-center max-w-3xl mx-auto mb-14">
      <p class="eyebrow mb-4">Build Your Stay — Your Way</p>
      <h2 class="text-nile-blue mb-5" style="font-size:clamp(1.75rem,4vw,2.75rem)">Hotels & Concierge Add-Ons</h2>
      <p class="text-nile-muted" style="font-size:1.05rem">
        <strong class="text-nile-blue">Clinical packages are treatment-only.</strong> Choose your preferred hotel and add any concierge services. Prices are indicative for a standard 10-night stay and confirmed in writing after your review.
      </p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 max-w-6xl mx-auto">
      
      <!-- LEFT: HOTELS -->
      <div class="bg-nile-beige p-6 md:p-8 rounded-lg border border-nile-gold/30 shadow-sm">
        <div class="flex items-center gap-3 mb-6 border-b border-nile-gold/20 pb-4">
          <span class="bg-nile-gold text-white w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm">1</span>
          <h3 class="font-serif text-nile-blue text-2xl">Select Hotel Tier</h3>
        </div>
        
        <div class="space-y-4">
          <!-- 3 Star -->
          <div class="bg-white p-5 rounded border-l-4 border-gray-400 shadow-sm flex justify-between items-center transition hover:shadow-md">
            <div>
              <h4 class="font-serif text-nile-blue text-lg">3★ Hotel</h4>
              <p class="text-nile-muted text-xs">Sheikh Zayed / New Cairo</p>
              <p class="text-[10px] text-gray-500 mt-1">✓ Breakfast & Airport Transfers</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-2xl">$700</p>
              <p class="text-[10px] text-nile-muted uppercase">10 nights</p>
            </div>
          </div>
          <!-- 4 Star -->
          <div class="bg-white p-5 rounded border-l-4 border-nile-gold shadow-md flex justify-between items-center relative transform scale-[1.02] transition hover:shadow-lg">
            <div class="absolute top-0 right-0 bg-nile-gold text-white text-[8px] font-bold px-2 py-1 rounded-bl">Most Chosen</div>
            <div>
              <h4 class="font-serif text-nile-blue text-lg">4★ Hotel</h4>
              <p class="text-nile-muted text-xs">Novotel / Hilton / Marriott</p>
              <p class="text-[10px] text-gray-500 mt-1">✓ Breakfast, Transfers & Priority Clinic</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-2xl">$1,200</p>
              <p class="text-[10px] text-nile-muted uppercase">10 nights</p>
            </div>
          </div>
          <!-- 5 Star -->
          <div class="bg-white p-5 rounded border-l-4 border-nile-blue shadow-sm flex justify-between items-center transition hover:shadow-md">
            <div>
              <h4 class="font-serif text-nile-blue text-lg">5★ Hotel</h4>
              <p class="text-nile-muted text-xs">Four Seasons / Ritz-Carlton</p>
              <p class="text-[10px] text-gray-500 mt-1">✓ Nile/Pyramids View + Dedicated Concierge</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-2xl">$2,500</p>
              <p class="text-[10px] text-nile-muted uppercase">10 nights</p>
            </div>
          </div>
          <!-- 5 Star Suite -->
          <div class="bg-white p-5 rounded border-l-4 border-nile-blue shadow-sm flex justify-between items-center transition hover:shadow-md">
            <div>
              <h4 class="font-serif text-nile-blue text-lg">5★ Suite VIP</h4>
              <p class="text-nile-muted text-xs">Four Seasons Nile Plaza / St. Regis</p>
              <p class="text-[10px] text-gray-500 mt-1">✓ Panoramic Suite + Private Chauffeur</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-2xl">$4,500</p>
              <p class="text-[10px] text-nile-muted uppercase">10 nights</p>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT: CONCIERGE ADD-ONS -->
      <div class="bg-nile-beige p-6 md:p-8 rounded-lg border border-nile-gold/30 shadow-sm">
        <div class="flex items-center gap-3 mb-6 border-b border-nile-gold/20 pb-4">
          <span class="bg-nile-gold text-white w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm">2</span>
          <h3 class="font-serif text-nile-blue text-2xl">Add Concierge Services</h3>
        </div>

        <div class="space-y-4">
          <!-- Recovery Care -->
          <div class="bg-white p-5 rounded border-l-4 border-nile-gold shadow-sm flex justify-between items-center transition hover:shadow-md">
            <div>
              <h4 class="font-serif text-nile-blue text-lg">Recovery Care</h4>
              <p class="text-nile-muted text-xs">Nurse, physio, pharmacy delivery</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">+$1,700</p>
              <p class="text-[10px] text-nile-muted uppercase">Per patient</p>
            </div>
          </div>
          <!-- Premium Concierge -->
          <div class="bg-white p-5 rounded border-l-4 border-nile-gold shadow-md flex justify-between items-center relative transform scale-[1.02] transition hover:shadow-lg">
            <div class="absolute top-0 right-0 bg-nile-gold text-white text-[8px] font-bold px-2 py-1 rounded-bl">Most Chosen</div>
            <div>
              <h4 class="font-serif text-nile-blue text-lg">Premium Concierge</h4>
              <p class="text-nile-muted text-xs">Coordinator, transfers, Nile cruise</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">+$1,700</p>
              <p class="text-[10px] text-nile-muted uppercase">Per patient</p>
            </div>
          </div>
          <!-- Signature VIP -->
          <div class="bg-white p-5 rounded border-l-4 border-nile-blue shadow-sm flex justify-between items-center transition hover:shadow-md">
            <div>
              <h4 class="font-serif text-nile-blue text-lg">Signature VIP</h4>
              <p class="text-nile-muted text-xs">Private chef, tours, yacht dinner</p>
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
    <div class="bg-nile-gold/10 border border-nile-gold/30 p-6 md:p-8 mt-10 max-w-4xl mx-auto rounded-lg text-center">
      <h3 class="font-serif text-nile-blue text-xl mb-6">How to Combine (Examples)</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-nile-muted">
        <div class="bg-white p-4 border border-nile-gold/20 shadow-sm rounded">
          <p class="font-semibold text-nile-blue mb-1">Budget-Conscious</p>
          <p>3★ Hotel + No Add-on = <strong class="text-nile-gold text-lg">$700</strong></p>
        </div>
        <div class="bg-white p-4 border border-nile-gold/40 shadow-md rounded transform scale-105">
          <p class="font-semibold text-nile-blue mb-1">Balanced</p>
          <p>4★ Hotel + Premium Concierge = <strong class="text-nile-gold text-lg">$2,900</strong></p>
        </div>
        <div class="bg-white p-4 border border-nile-gold/20 shadow-sm rounded">
          <p class="font-semibold text-nile-blue mb-1">Full VIP</p>
          <p>5★ Suite + Signature VIP = <strong class="text-nile-gold text-lg">$7,500</strong></p>
        </div>
      </div>
    </div>
  </div>
</section>
"""
    content = re.sub(r'<section id="travel-addons".*?</section>', new_travel_addons, content, flags=re.DOTALL)
    print("[OK] Redesigned: Travel Add-ons & Hotels UI")

    # ============================================================
    # 3. REORDER SECTIONS (AIDA FUNNEL)
    # ============================================================
    # Extract all sections
    section_pattern = re.compile(r'(<section id="([^"]+)".*?</section>)', re.DOTALL)
    sections = {}
    for match in section_pattern.finditer(content):
        sec_id = match.group(2)
        sec_html = match.group(1)
        sections[sec_id] = sec_html

    # Define New Order
    NEW_ORDER = [
        # 1. HOOK & PRICE
        'price-anchor', 'top-tier',
        # 2. AUTHORITY & PROOF
        'trust-stats', 'trust', 'founder', 'verify-us', 'results',
        # 3. THE OFFER (PRICES)
        'packages', 'savings', 'estimator',
        # 4. COMPARISON
        'comparison', 'destination-deep-dive',
        # 5. MECHANISM (WHY IT WORKS)
        'science', 'implant-systems', 'technology-stack', 'comfort', 'team',
        # 6. EDUCATION (WHY NOT CHEAP)
        'brutal-truth', 'cost-of-cheap', 'surface-material', 'clinical-protocol', 'why-prices', 'why-egypt', 'academic',
        # 7. RISK REVERSAL
        'guarantees', 'warranty-truth', 'implant-passport', 'peace-of-mind',
        # 8. OBJECTIONS & FAQ
        'risks', 'expectations', 'who-for', 'faq',
        # 9. JOURNEY & LOGISTICS
        'journey', 'timeline', 'recovery', 'travel', 'travel-addons',
        # 10. TOURISM
        'curated-tours', 'discover-egypt', 'location',
        # 11. EXTRA INFO
        'reviews', 'turkey-rescue', 'payment', 'doctor-credentials', 'bone-graft', 'crown-materials', 'orthodontics',
        # 12. LEGAL & ACTION
        'legal', 'consult'
    ]

    # Get the main content
    main_match = re.search(r'(<main id="main">)(.*?)(</main>)', content, flags=re.DOTALL)
    if main_match:
        # We need to preserve the Hero section as it has no ID (it's `<section class="hero">`)
        hero_match = re.search(r'(<section class="hero">.*?</section>)', main_match.group(2), flags=re.DOTALL)
        hero_html = hero_match.group(1) if hero_match else ""
        
        new_main_content = hero_html + "\n"
        
        for sec_id in NEW_ORDER:
            if sec_id in sections:
                new_main_content += sections[sec_id] + "\n"
                
        # Add any missing sections that were in the original but not in NEW_ORDER
        for sec_id, sec_html in sections.items():
            if sec_id not in NEW_ORDER:
                new_main_content += sec_html + "\n"

        content = content.replace(main_match.group(0), f"<main id=\"main\">\n{new_main_content}\n</main>")
        print("[OK] Reordered: Sections logically (AIDA funnel)")

    # ============================================================
    # 4. WRITE BACK
    # ============================================================
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("\nSUCCESS! Site is optimized.")
    print("1. Freezing issue resolved.")
    print("2. Travel Add-ons redesigned.")
    print("3. Sections reordered.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python site_makeover.py <path-to-html>")
    else:
        makeover_site(sys.argv[1])