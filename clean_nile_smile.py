import re
import os
import shutil
from datetime import datetime

# اسم الملف
FILE_PATH = 'index.html'

# الكود النهائي اللي هنحقنه في آخر الملف
FINAL_FIX_CODE = """
<!-- ═══════════════════════════════════════════════════════════════
     NILE SMILE — THE DEFINITIVE FINAL FIX (v10.0)
     ═══════════════════════════════════════════════════════════════ -->
<style id="ZK_DEFINITIVE_FIX">
  #liquidGlassHeader { min-height: 60px !important; background: rgba(255, 255, 255, 0.75) !important; backdrop-filter: blur(24px) saturate(180%) !important; -webkit-backdrop-filter: blur(24px) saturate(180%) !important; border: 1px solid rgba(255, 255, 255, 0.6) !important; box-shadow: 0 8px 32px rgba(31, 42, 54, 0.08) !important; }
  #liquidGlassHeader.on-dark { background: rgba(10, 13, 16, 0.75) !important; border-color: rgba(232, 200, 138, 0.3) !important; }
  #liquidGlassHeader .lgh-inner { min-height: 60px !important; padding: 0.4rem 1rem !important; }
  .lgh-logo { display: flex !important; flex-direction: column !important; align-items: flex-start !important; gap: 0 !important; }
  .lgh-logo > span:last-child { display: flex !important; flex-direction: column !important; align-items: flex-start !important; margin-top: -2px !important; }
  .lgh-logo-script { font-size: 1.8rem !important; line-height: 0.9 !important; }
  .lgh-logo-text { font-size: 0.55rem !important; letter-spacing: 0.25em !important; color: #4F6070 !important; }
  .lgh-logo-sub { display: block !important; margin-top: 2px !important; font-size: 0.42rem !important; color: #6B7D8E !important; }
  #liquidGlassHeader.on-dark .lgh-logo-text { color: #E8C88A !important; }
  #liquidGlassHeader.on-dark .lgh-logo-sub { color: #8FA1B2 !important; }
  .lgh-mobile-actions .lgh-cta { display: none !important; }
  @media (max-width: 767px) {
    .hero-content .flex.flex-col.sm\\:flex-row { flex-direction: row !important; flex-wrap: nowrap !important; gap: 10px !important; width: 100% !important; }
    .hero-content .btn { flex: 1 1 50% !important; border-radius: 100px !important; min-height: 52px !important; padding: 0.8rem 0.5rem !important; font-size: 0.65rem !important; white-space: normal !important; justify-content: center !important; }
  }
  .float-wa, .sticky-mobile { display: none !important; }
  #appleDock { width: calc(100% - 24px) !important; max-width: 400px !important; padding: 6px 12px !important; justify-content: space-between !important; }
  .dock-item { width: 42px !important; height: 42px !important; }
  .dock-item svg { width: 20px !important; height: 20px !important; }
  .wa-dock-btn { background: rgba(174, 145, 100, 0.05) !important; border: 1.5px solid #AE9164 !important; color: #AE9164 !important; border-radius: 50% !important; display: flex !important; align-items: center !important; justify-content: center !important; transition: all 0.3s ease !important; }
  .wa-dock-btn svg { fill: #AE9164 !important; }
  .wa-dock-btn:hover { background: rgba(174, 145, 100, 0.2) !important; transform: scale(1.05) !important; }
  .exit-popup, .modal, .search-modal { z-index: 99999 !important; }
  .exit-popup { padding-top: 80px !important; }
</style>
<script id="ZK_DEFINITIVE_FIX_JS">
(function () {
  'use strict';
  function applyFinalFixes() {
    document.querySelectorAll('.lgh-hamburger, .lgh-mobile-menu').forEach(function(el) { el.remove(); });
    document.querySelectorAll('.float-wa, .sticky-mobile').forEach(function (el) { el.remove(); });
    var dock = document.getElementById('appleDock');
    if (dock && !dock.querySelector('.wa-dock-btn')) {
      var waBtn = document.createElement('a');
      waBtn.href = 'https://wa.me/201503308333'; waBtn.target = '_blank'; waBtn.rel = 'noopener'; waBtn.className = 'dock-item wa-dock-btn'; waBtn.setAttribute('aria-label', 'WhatsApp');
      waBtn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.82 9.82 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>';
      dock.appendChild(waBtn);
    }
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', applyFinalFixes); } else { applyFinalFixes(); }
  setTimeout(applyFinalFixes, 500);
  setTimeout(applyFinalFixes, 1500);
})();
</script>
<!-- ═══════════════════════════════════════════════════════════════ -->
"""

def clean_file():
    if not os.path.exists(FILE_PATH):
        print("❌ Error: index.html not found in this directory.")
        return

    # 1. Backup
    backup_name = f"{FILE_PATH}.bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy(FILE_PATH, backup_name)
    print(f"✅ Created backup: {backup_name}")

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    original_size = len(content)

    # 2. Blocks to remove
    ids_to_remove = [
        'ZK_ULTIMATE_V5', 'ZK_ULTIMATE_V5_JS',
        'ZK_NUCLEAR_FIX', 'ZK_NUCLEAR_FIX_JS',
        'ZK_FINAL_V9', 'ZK_FINAL_V9_JS',
        'nileSmileFixPatch', 'designScience2026', 'designScience2026JS',
        'liquidGlassHeaderStyles', 'liquidGlassHeaderJS',
        'premiumAppleDockStyles', 'premiumAppleDockJS'
    ]

    print("\n🧹 Removing old redundant blocks...")
    for block_id in ids_to_remove:
        # Remove Style
        style_pattern = re.compile(rf'<style[^>]*id=["\']?{block_id}["\']?[^>]*>.*?</style>', re.DOTALL | re.IGNORECASE)
        content = style_pattern.sub('', content)
        
        # Remove Script
        script_pattern = re.compile(rf'<script[^>]*id=["\']?{block_id}["\']?[^>]*>.*?</script>', re.DOTALL | re.IGNORECASE)
        content = script_pattern.sub('', content)
        print(f"  ✓ Removed: {block_id}")

    # Remove general patch comments
    content = re.sub(r'<!-- ═+\s*NILE SMILE\s*—\s*[^>]*?\s*═+ -->', '', content)
    
    # Remove empty lines (3 or more)
    content = re.sub(r'\n{3,}', '\n\n', content)

    # 3. Inject the Final Fix
    print("\n✨ Injecting the clean final fix...")
    if '</body>' in content:
        content = content.replace('</body>', FINAL_FIX_CODE + '\n</body>')
    else:
        content += FINAL_FIX_CODE

    # 4. Save
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    new_size = len(content)
    saved = original_size - new_size
    
    print("\n✅ DONE! File cleaned successfully.")
    print(f"📉 Old Size: {original_size:,} bytes")
    print(f"📉 New Size: {new_size:,} bytes")
    print(f"🗑️  Saved:    {saved:,} bytes")

if __name__ == "__main__":
    clean_file()