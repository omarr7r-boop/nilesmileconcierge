#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nile Smile — Architectural & Performance Fix
============================================
- Fixes Infinite Loop (MutationObserver)
- Fixes Layout Thrashing (Scroll & Mouse events)
- Fixes Z-Index hierarchy (Modals vs Header)
- Fixes Search Toggle logic
"""

import re
import shutil
import sys
from pathlib import Path

def fix_architecture(html_path):
    path = Path(html_path)
    if not path.exists():
        print(f"[X] File not found: {html_path}")
        return

    shutil.copy2(path, str(path) + ".backup_arch")
    print(f"[OK] Backup created: {path.name}.backup_arch\n")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # ============================================================
    # 1. REMOVE THE INFINITE LOOP (FINAL SECTION ORDER)
    # ============================================================
    # This script modifies the DOM and watches for DOM changes, causing a massive CPU spike.
    old_order_script = re.search(r'<script>\s*/\* ═══════════════════ FINAL SECTION ORDER v7.*?</script>', content, flags=re.DOTALL)
    if old_order_script:
        content = content.replace(old_order_script.group(0), '<!-- Removed Infinite Loop Script -->')
        print("[OK] Removed: FINAL SECTION ORDER (Infinite Loop)")

    # ============================================================
    # 2. REMOVE LAYOUT THRASHING (Magnetic Buttons)
    # ============================================================
    old_magnetic = re.search(r'if\(window\.innerWidth > 1024 && !prefersReduced\)\{\s*document\.querySelectorAll\(\'\.btn-gold\'\).*?\n  \}', content, flags=re.DOTALL)
    if old_magnetic:
        content = content.replace(old_magnetic.group(0), '/* Magnetic buttons disabled for performance */')
        print("[OK] Removed: Magnetic Buttons (Layout Thrashing)")

    # ============================================================
    # 3. FIX LAYOUT THRASHING (STICKY TOC SCROLL)
    # ============================================================
    old_toc = re.search(r'<script>\s*/\* ═════════ STICKY TOC.*?</script>', content, flags=re.DOTALL)
    if old_toc:
        new_toc = """
<script>
/* FIXED STICKY TOC — Optimized with requestAnimationFrame and Cached Positions */
(function(){
  const toc = document.getElementById('stickyToc');
  if (!toc) return;
  const dots = toc.querySelectorAll('.toc-dot');
  const sections = Array.from(dots).map(d => document.querySelector(d.getAttribute('href'))).filter(Boolean);
  let sectionTops = [];
  
  function calcTops() {
    sectionTops = sections.map(sec => ({
      id: sec.id,
      top: sec.getBoundingClientRect().top + window.scrollY - 200
    }));
  }
  
  let ticking = false;
  function updateToc(){
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const scrollY = window.scrollY;
      if (scrollY > 600) toc.classList.add('show');
      else toc.classList.remove('show');
      
      let current = null;
      for (let i = 0; i < sectionTops.length; i++) {
        if (scrollY >= sectionTops[i].top) current = sectionTops[i].id;
      }
      
      dots.forEach(d => {
        d.classList.toggle('active', d.getAttribute('href') === '#' + current);
      });
      ticking = false;
    });
  }
  
  window.addEventListener('load', calcTops);
  window.addEventListener('resize', () => { calcTops(); updateToc(); });
  window.addEventListener('scroll', updateToc, {passive: true});
  calcTops();
  updateToc();
})();
</script>
"""
        content = content.replace(old_toc.group(0), new_toc)
        print("[OK] Fixed: Sticky TOC (Optimized Scroll)")

    # ============================================================
    # 4. FIX Z-INDEX & MODALS HIERARCHY
    # ============================================================
    z_index_fix = """
<style id="zIndexAndModalFix">
/* Strict Z-Index Hierarchy to prevent overlapping bugs */
.site-header { z-index: 1000 !important; }
.apple-dock { z-index: 900 !important; }
.float-wa { z-index: 800 !important; }
.modal { z-index: 9000 !important; }
.search-modal { z-index: 9500 !important; }
.exit-popup { z-index: 10000 !important; }

/* Ensure exit popup clickability */
.exit-popup { pointer-events: none; }
.exit-popup.open { pointer-events: auto; }
.exit-popup-overlay { pointer-events: auto; }
.exit-popup-box { pointer-events: auto; }
</style>
"""
    content = content.replace('</head>', z_index_fix + '\n</head>')
    print("[OK] Fixed: Z-Index Hierarchy (Modals now appear ABOVE Header)")

    # ============================================================
    # 5. FIX SEARCH TOGGLE & THEME LOGIC (Dynamic UI)
    # ============================================================
    old_dynamic_script = re.search(r'<script id="dynamicUIScript">.*?</script>', content, flags=re.DOTALL)
    if old_dynamic_script:
        new_dynamic_script = """
<script id="dynamicUIScript">
(function() {
  'use strict';

  // 1. Search Modal Logic (Toggle & Fix)
  var trigger = document.getElementById('searchTrigger');
  var modal = document.getElementById('searchModal');
  
  if (trigger && modal) {
    trigger.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation(); // Prevent event bubbling
      
      var isOpen = modal.classList.contains('open');
      if (isOpen) {
        modal.classList.remove('open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      } else {
        modal.classList.add('open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        var input = document.getElementById('searchModalInput');
        if (input) setTimeout(function() { input.focus(); }, 100);
      }
    });
    
    // Close on overlay click or close button
    modal.addEventListener('click', function(e) {
      if (e.target === modal || e.target.hasAttribute('data-search-close') || e.target.closest('[data-search-close]')) {
        modal.classList.remove('open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      }
    });
    
    // ESC key to close
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && modal.classList.contains('open')) {
        modal.classList.remove('open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      }
    });
  }

  // 2. Dynamic Header & Dock Theming (Optimized with rAF)
  var header = document.getElementById('header');
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
  setTimeout(updateTheme, 200);

  // 3. Dock Active State
  var dockItems = document.querySelectorAll('.dock-item[data-target]');
  if (dockItems.length) {
    var navSections = Array.from(dockItems).map(function(item) {
      return { el: document.getElementById(item.getAttribute('data-target')), link: item };
    }).filter(function(s) { return s.el !== null; });

    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          dockItems.forEach(function(item) { item.classList.remove('active'); });
          var activeItem = navSections.find(function(s) { return s.el === entry.target; });
          if (activeItem) activeItem.link.classList.add('active');
        }
      });
    }, { rootMargin: '-20% 0px -50% 0px', threshold: 0 });

    navSections.forEach(function(s) { observer.observe(s.el); });
  }
})();
</script>
"""
        content = content.replace(old_dynamic_script.group(0), new_dynamic_script)
        print("[OK] Fixed: Search Toggle & Theming Logic")

    # ============================================================
    # 6. REMOVE REDUNDANT CLEANUP SCRIPTS
    # ============================================================
    content = re.sub(r'<script id="finalCleanup">.*?</script>', '', content, flags=re.DOTALL)
    print("[OK] Removed redundant cleanup scripts")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\nSUCCESS! The website architecture is now stable.")
    print("Please do a Hard Refresh (Ctrl+Shift+R) and test the site.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_architecture.py <path-to-html>")
    else:
        fix_architecture(sys.argv[1])