#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nile Smile — Fix Scroll Jitter & Badge Overlap
================================================
1. Fixes horizontal page shift during scroll (overflow-x).
2. Fixes "Most Chosen" badge overlapping prices.
"""

import re
import shutil
import sys
from pathlib import Path

def fix_jitter(path_arg):
    path = Path(path_arg)
    if not path.exists():
        print(f"[X] File not found: {path_arg}")
        return

    backup = path.with_suffix(path.suffix + ".backup_jitter")
    shutil.copy2(path, backup)
    print(f"[OK] Backup: {backup.name}\n")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # ============================================================
    # 1. FIX HORIZONTAL JITTER (The "Dancing" issue)
    # ============================================================
    # Inject a CSS fix at the end of <head> to force no horizontal overflow
    jitter_css = """
<style id="fixJitterCSS">
  html, body {
    overflow-x: hidden !important;
    width: 100% !important;
    max-width: 100vw !important;
    position: relative;
  }
  /* Prevent any section from causing horizontal scroll */
  section, .container, .container-narrow {
    max-width: 100%;
  }
</style>
"""
    if '</head>' in content:
        content = content.replace('</head>', jitter_css + '\n</head>')
        print("[OK] Injected CSS to fix horizontal jitter (overflow-x)")

    # ============================================================
    # 2. FIX "MOST CHOSEN" BADGE OVERLAP
    # ============================================================
    # Replace the travel-addons section with a fixed version (inline badges)
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
          
          <!-- 3 Star -->
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

          <!-- 4 Star -->
          <div class="bg-white p-4 rounded border-l-4 border-nile-gold shadow-md flex justify-between items-center relative overflow-hidden">
            <div>
              <div class="flex items-center gap-2 mb-1">
                <h4 class="font-serif text-nile-blue text-lg">4★ Hotel</h4>
                <span class="bg-nile-gold text-white text-[8px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">Most Chosen</span>
              </div>
              <p class="text-nile-muted text-xs">Novotel / Hilton / Marriott · Breakfast & Transfers</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">$1,200</p>
              <p class="text-[10px] text-nile-muted">$120/night</p>
            </div>
          </div>

          <!-- 5 Star -->
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

          <!-- 5 Star Suite -->
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
          
          <!-- Recovery Care -->
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

          <!-- Premium Concierge -->
          <div class="bg-white p-4 rounded border-l-4 border-nile-gold shadow-md flex justify-between items-center relative overflow-hidden">
            <div>
              <div class="flex items-center gap-2 mb-1">
                <h4 class="font-serif text-nile-blue text-lg">Premium Concierge</h4>
                <span class="bg-nile-gold text-white text-[8px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">Most Chosen</span>
              </div>
              <p class="text-nile-muted text-xs">Coordinator, unlimited transfers, Nile dinner cruise</p>
            </div>
            <div class="text-right">
              <p class="font-serif text-nile-gold text-xl">+$1,700</p>
              <p class="text-[10px] text-nile-muted">Per patient</p>
            </div>
          </div>

          <!-- Signature VIP -->
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
    
    # Replace section
    content = re.sub(r'<section id="travel-addons".*?</section>', new_travel_section, content, flags=re.DOTALL)
    print("[OK] Fixed: 'Most Chosen' badge overlaps (moved inline with title)")

    # Save
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("\nSUCCESS! Jitter and badge issues resolved.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_jitter.py <path-to-html>")
    else:
        fix_jitter(sys.argv[1])