#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nile Smile — Final Performance & UI Makeover (Fixed Version)
=============================================================
"""

import re
import shutil
import sys
from pathlib import Path

def final_makeover(html_path):
    path = Path(html_path)
    if not path.exists():
        print(f"[X] File not found: {html_path}")
        return

    backup = path.with_suffix(path.suffix + ".backup_final")
    shutil.copy2(path, backup)
    print(f"[OK] Backup: {backup.name}\n")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # ============================================================
    # 1. REMOVE PERFORMANCE KILLERS (backdrop-filter & continuous animations)
    # ============================================================
    content = re.sub(r'backdrop-filter\s*:\s*[^;]+;', '', content)
    content = re.sub(r'-webkit-backdrop-filter\s*:\s*[^;]+;', '', content)

    continuous_anims = [
        'logoGlowPulse', 'heartbeat', 'autoShine', 'primaryShimmer', 'quickDot',
        'waPulse', 'trustFloat', 'monogramGlow', 'goldFlow', 'sectionFlow',
        'goldFlowSection', 'shimmer', 'breathe', 'pulse', 'float', 'blink'
    ]
    for anim in continuous_anims:
        content = re.sub(rf'animation\s*:\s*{anim}[^;]*;', '', content)
        content = re.sub(rf'animation-name\s*:\s*{anim}[^;]*;', '', content)
        content = re.sub(rf'\.{anim}\s*{{[^}}]*}}', '', content)

    content = re.sub(r'will-change\s*:\s*[^;]+;', '', content)
    print("[OK] Removed backdrop-filter, continuous animations, and will-change")

    # ============================================================
    # 2. REDESIGN TRAVEL ADD-ONS (Combined Hotels + Concierge)
    # ============================================================
    new_travel_section = """
<section id="travel-addons" class="section bg-white reveal">
  <div class="container">
    <div class="text-center max-w-3xl mx-auto mb-12">
      <p class="eyebrow mb-4">Build Your Stay — Your Way</p>
      <h2 class="text-nile-blue mb-5" style="font-size:clamp(1.75rem,4vw,2.75rem)">Hotels & Concierge Add-Ons</h2>
      <p class="text-nile-muted">Select a hotel tier and add any concierge services you need. All prices are for a standard 10-night stay and are confirmed in writing after your clinical review.</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-6xl mx-auto">

      <!-- Hotels Column -->
      <div class="bg-nile-beige p-6 md:p-8 rounded-lg border border-nile-gold/20">
        <div class="flex items-center gap-3 mb-6 pb-3 border-b border-nile-gold/20">
          <span class="bg-nile-gold text-white w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm">1</span>
          <h3 class="font-serif text-nile-blue text-2xl">Hotel Tier (10 Nights)</h3>
        </div>
        <div class="space-y-3">
          <div class="bg-white p-4 rounded border-l-4 border-gray-400 shadow-sm flex justify-between items-center">
            <div>
              <h4 class="font-serif text-nile-blue text-lg">3★ Hotel</h4>
              <p class="text-nile-muted text-xs">Sheikh Zayed / New Cairo · Breakfast & Transfers</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">$700</p>
              <p class="text-[10px] text-nile-muted">$70/night</p>
            </div>
          </div>
          <div class="bg-white p-4 rounded border-l-4 border-nile-gold shadow-md flex justify-between items-center relative">
            <div class="absolute top-0 right-0 bg-nile-gold text-white text-[8px] font-bold px-2 py-1 rounded-bl">Most Chosen</div>
            <div>
              <h4 class="font-serif text-nile-blue text-lg">4★ Hotel</h4>
              <p class="text-nile-muted text-xs">Novotel / Hilton / Marriott · Breakfast & Transfers</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">$1,200</p>
              <p class="text-[10px] text-nile-muted">$120/night</p>
            </div>
          </div>
          <div class="bg-white p-4 rounded border-l-4 border-nile-blue shadow-sm flex justify-between items-center">
            <div>
              <h4 class="font-serif text-nile-blue text-lg">5★ Hotel</h4>
              <p class="text-nile-muted text-xs">Four Seasons / Ritz-Carlton · Nile or Pyramids View</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">$2,500</p>
              <p class="text-[10px] text-nile-muted">$250/night</p>
            </div>
          </div>
          <div class="bg-white p-4 rounded border-l-4 border-nile-blue shadow-sm flex justify-between items-center">
            <div>
              <h4 class="font-serif text-nile-blue text-lg">5★ Suite VIP</h4>
              <p class="text-nile-muted text-xs">Four Seasons Nile Plaza / St. Regis · Private Chauffeur</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">$4,500</p>
              <p class="text-[10px] text-nile-muted">$450/night</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Concierge Column -->
      <div class="bg-nile-beige p-6 md:p-8 rounded-lg border border-nile-gold/20">
        <div class="flex items-center gap-3 mb-6 pb-3 border-b border-nile-gold/20">
          <span class="bg-nile-gold text-white w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm">2</span>
          <h3 class="font-serif text-nile-blue text-2xl">Concierge Add-Ons</h3>
        </div>
        <div class="space-y-3">
          <div class="bg-white p-4 rounded border-l-4 border-nile-gold shadow-sm flex justify-between items-center">
            <div>
              <h4 class="font-serif text-nile-blue text-lg">Recovery Care</h4>
              <p class="text-nile-muted text-xs">Daily nurse, physio, pharmacy delivery, soft meals</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">+$1,700</p>
              <p class="text-[10px] text-nile-muted">Per patient</p>
            </div>
          </div>
          <div class="bg-white p-4 rounded border-l-4 border-nile-gold shadow-md flex justify-between items-center relative">
            <div class="absolute top-0 right-0 bg-nile-gold text-white text-[8px] font-bold px-2 py-1 rounded-bl">Most Chosen</div>
            <div>
              <h4 class="font-serif text-nile-blue text-lg">Premium Concierge</h4>
              <p class="text-nile-muted text-xs">Coordinator, unlimited transfers, Nile dinner cruise</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">+$1,700</p>
              <p class="text-[10px] text-nile-muted">Per patient</p>
            </div>
          </div>
          <div class="bg-white p-4 rounded border-l-4 border-nile-blue shadow-sm flex justify-between items-center">
            <div>
              <h4 class="font-serif text-nile-blue text-lg">Signature VIP</h4>
              <p class="text-nile-muted text-xs">Private chef, Giza tour, Luxor trip, yacht dinner</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">+$3,000</p>
              <p class="text-[10px] text-nile-muted">Per patient</p>
            </div>
          </div>
        </div>
      </div>

    </div>

    <div class="bg-nile-gold/10 border border-nile-gold/30 p-6 md:p-8 mt-8 max-w-4xl mx-auto rounded-lg">
      <h3 class="font-serif text-nile-blue text-xl text-center mb-4">How to Combine (Examples)</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
        <div class="bg-white p-4 border border-nile-gold/20 rounded text-center">
          <p class="font-semibold text-nile-blue">Budget</p>
          <p>3★ Hotel + No Add-on</p>
          <p class="font-serif text-nile-gold text-lg">$700</p>
        </div>
        <div class="bg-white p-4 border border-nile-gold/40 rounded text-center shadow-md">
          <p class="font-semibold text-nile-blue">Balanced</p>
          <p>4★ Hotel + Premium Concierge</p>
          <p class="font-serif text-nile-gold text-lg">$2,900</p>
        </div>
        <div class="bg-white p-4 border border-nile-gold/20 rounded text-center">
          <p class="font-semibold text-nile-blue">Full VIP</p>
          <p>5★ Suite + Signature VIP</p>
          <p class="font-serif text-nile-gold text-lg">$7,500</p>
        </div>
      </div>
    </div>
  </div>
</section>
"""
    content = re.sub(r'<section id="travel-addons".*?</section>', new_travel_section, content, flags=re.DOTALL)
    print("[OK] Combined Hotels + Concierge into a single section")

    # ============================================================
    # 3. REORDER SECTIONS (Safe String Replacement)
    # ============================================================
    section_pattern = re.compile(r'(<section id="([^"]+)".*?</section>)', re.DOTALL)
    sections = {}
    for match in section_pattern.finditer(content):
        sec_id = match.group(2)
        sections[sec_id] = match.group(1)

    NEW_ORDER = [
        'price-anchor', 'top-tier', 'trust-stats', 'trust', 'founder', 'verify-us', 'results',
        'packages', 'savings', 'estimator', 'comparison', 'destination-deep-dive',
        'science', 'implant-systems', 'technology-stack', 'comfort', 'team',
        'brutal-truth', 'cost-of-cheap', 'surface-material', 'clinical-protocol', 'why-prices', 'why-egypt', 'academic',
        'guarantees', 'warranty-truth', 'implant-passport', 'peace-of-mind',
        'risks', 'expectations', 'who-for', 'faq',
        'journey', 'timeline', 'recovery', 'travel', 'travel-addons',
        'curated-tours', 'discover-egypt', 'location',
        'reviews', 'turkey-rescue', 'payment', 'doctor-credentials',
        'bone-graft', 'crown-materials', 'orthodontics',
        'legal', 'consult'
    ]

    hero_match = re.search(r'(<section class="hero">.*?</section>)', content, flags=re.DOTALL)
    hero_html = hero_match.group(1) if hero_match else ""

    new_main = hero_html + "\n"
    for sec_id in NEW_ORDER:
        if sec_id in sections:
            new_main += sections[sec_id] + "\n"

    for sec_id, sec_html in sections.items():
        if sec_id not in NEW_ORDER:
            new_main += sec_html + "\n"

    # ⚡ الأمان هنا: استخدام String Slicing بدل regex
    main_start = content.find('<main id="main">')
    main_end = content.find('</main>')
    if main_start != -1 and main_end != -1:
        content = content[:main_start] + '<main id="main">\n' + new_main + '\n</main>' + content[main_end + len('</main>'):]
        print("[OK] Reordered sections (Patient Journey)")

    # ============================================================
    # 4. WRITE BACK
    # ============================================================
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("\nSUCCESS! Site optimized.")
    print("- Freezing issue addressed (removed backdrop-filter & heavy animations)")
    print("- Hotels & Add-ons combined into one section")
    print("- Sections reordered for better conversion")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_crash.py <path-to-html>")
    else:
        final_makeover(sys.argv[1])