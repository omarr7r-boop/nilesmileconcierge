#!/usr/bin/env python3
"""
Nile Smile HTML Cleaner — v1.0
Removes 25+ redundant style/script blocks, keeps only essential ones.

Usage:
    python clean_nile_smile.py "!DOCTYPE html.txt"
"""

import re
import sys
import os
import shutil
from datetime import datetime

# ═══════════════════════════════════════════════════════════
# BLOCKS TO DELETE
# ═══════════════════════════════════════════════════════════

DELETE_STYLE_IDS = [
    'finalHardening2026',
    'modernize2026',
    'goldRestoration',
    'criticalVisualFixes',
    'masterFixStyles',
    'finalConsistencyPatch',
    'glassAndSweepPatch',
    'ultimateFix',
    'trueFinalPatch',
    'nileSmileMasterCss',
    'nileEverythingCss',
    'nileUxPolishCss',
    'nileFinalFixV3',
    'fixMobileMenuVisibility',
    'mobileMenuDefinitiveFix',
    'ultimateContrastAndColorFix',
    'heroContrastFix',
    'nileGoldLock',
    'premiumRedesignFinal',
    'commandBarDockScroll',
    'emergencyCleanupV5',
    'absoluteFinalUI',
    'ZK_FINAL_LOCK',
]

DELETE_SCRIPT_IDS = [
    'finalHardening2026JS',
    'modernize2026JS',
    'goldRestorationJS',
    'masterFixScript',
    'finalConsistencyScript',
    'glassSweepEnsureJS',
    'ultimateFixJS',
    'trueFinalPatchJS',
    'nileSmileMasterFix',
    'nileTeethMapPosition',
    'nileEverythingJS',
    'nileUxPolishJs',
    'nileFinalFixV3JS',
    'mobileMenuDefinitiveFixJS',
    'nileGoldLockJS',
    'premiumRedesignFinalJS',
    'commandBarDockScrollJS',
    'emergencyCleanupV5JS',
    'absoluteFinalUI_JS',
]

# Content-based (unnamed script that blocks MutationObserver)
DELETE_BY_CONTENT = [
    '// ═══ 1. أوقف كل MutationObserver ═══',
]

# ═══════════════════════════════════════════════════════════
# MUST-KEEP blocks (verify at end)
# ═══════════════════════════════════════════════════════════

MUST_KEEP = [
    'id="liquidGlassHeader"',
    'id="teeth-map"',
    'id="leadForm"',
    'id="ZK_ULTIMATE_V5"',
    'id="premiumAppleDockStyles"',
    'id="liquidGlassHeaderJS"',
    'id="premiumAppleDockJS"',
    'id="ZK_ULTIMATE_V5_JS"',
]

# ═══════════════════════════════════════════════════════════
# REMOVAL FUNCTIONS
# ═══════════════════════════════════════════════════════════

def remove_tag_by_id(content, tag, block_id):
    """Remove <tag id="X" ...>...</tag> — one or more occurrences."""
    pattern = (
        r'<' + tag + r'\s+[^>]*\bid\s*=\s*["\']' + re.escape(block_id) +
        r'["\'][^>]*>[\s\S]*?</' + tag + r'>\s*\n?'
    )
    return re.subn(pattern, '', content)

def remove_script_by_content(content, marker):
    """Remove <script>...</script> containing a specific marker string."""
    pattern = (
        r'<script(?:\s[^>]*)?>[\s\S]{0,500}' +
        re.escape(marker) +
        r'[\s\S]*?</script>\s*\n?'
    )
    return re.subn(pattern, '', content)

# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print('❌ Usage: python clean_nile_smile.py "input.html" [output.html]')
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file

    if not os.path.exists(input_file):
        print(f'❌ File not found: {input_file}')
        sys.exit(1)

    # Read
    with open(input_file, 'r', encoding='utf-8') as f:
        original = f.read()

    orig_lines = original.count('\n')
    orig_size  = len(original)

    print('═' * 60)
    print(f'📖 Input:  {input_file}')
    print(f'   Lines:  {orig_lines:,}')
    print(f'   Size:   {orig_size:,} bytes')
    print('═' * 60)

    # Backup
    backup = f'{input_file}.bak_{datetime.now():%Y%m%d_%H%M%S}'
    shutil.copy2(input_file, backup)
    print(f'💾 Backup: {backup}')
    print()

    content = original
    removed_total = 0

    # ── Remove style blocks ──
    print('🗑️  Removing STYLE blocks:')
    for block_id in DELETE_STYLE_IDS:
        content, n = remove_tag_by_id(content, 'style', block_id)
        if n > 0:
            print(f'   ✓ <style id="{block_id}">  ({n})')
            removed_total += n
    print()

    # ── Remove script blocks ──
    print('🗑️  Removing SCRIPT blocks:')
    for block_id in DELETE_SCRIPT_IDS:
        content, n = remove_tag_by_id(content, 'script', block_id)
        if n > 0:
            print(f'   ✓ <script id="{block_id}">  ({n})')
            removed_total += n
    print()

    # ── Remove content-based ──
    print('🗑️  Removing CONTENT-BASED blocks:')
    for marker in DELETE_BY_CONTENT:
        content, n = remove_script_by_content(content, marker)
        if n > 0:
            short = marker[:45] + '...' if len(marker) > 45 else marker
            print(f'   ✓ Script containing: {short}  ({n})')
            removed_total += n
    print()

    # ── Clean extra blank lines ──
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    # ── Verification ──
    print('🔍 Verifying MUST-KEEP blocks:')
    all_ok = True
    for keep in MUST_KEEP:
        if keep in content:
            print(f'   ✓ {keep}')
        else:
            print(f'   ❌ MISSING: {keep}')
            all_ok = False
    print()

    # ── Save ──
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    new_lines = content.count('\n')
    new_size  = len(content)

    print('═' * 60)
    print('✅ DONE' if all_ok else '⚠️  DONE (WITH WARNINGS)')
    print(f'   Blocks removed:  {removed_total}')
    print(f'   Lines:  {orig_lines:,} → {new_lines:,}  (−{orig_lines - new_lines:,})')
    print(f'   Size:   {orig_size:,} → {new_size:,} bytes')
    print(f'   Output: {output_file}')
    print('═' * 60)

    if not all_ok:
        print('\n⚠️  Some MUST-KEEP blocks are missing!')
        print('   Check the backup file and restore manually.')
        sys.exit(2)

if __name__ == '__main__':
    main()