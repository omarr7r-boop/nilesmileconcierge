#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nile Smile — Surgical Fix v4.0
================================
Fixes ONLY the critical issues (safe, atomic, verifiable):

1. Removes `<script id="perf-scroll">` which:
   - Hijacks window.addEventListener globally (breaks future code)
   - Hijacks c.appendChild on #implant3d (blocks any additions)

2. Fixes 4 price inconsistencies across 4 locations:
   - Zirconia Crowns — Premium:  $7,490 → $4,990
   - All-on-6 — Premium:         $8,490 → $7,990
   - All-on-4 — Signature:       $7,490 → $8,490
   - All-on-6 — Signature:       $8,990 → $9,990
   (Plus matching save amounts in cards + tables)

USAGE:
    python fix_nile_v4.py index.html --dry-run   # Preview
    python fix_nile_v4.py index.html             # Apply + backup
    python fix_nile_v4.py index.html --verify    # Verify current state

SAFETY:
    - Creates timestamped backup before saving
    - Won't corrupt file if pattern doesn't match
    - Reports every change + warning + verification
"""

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path


# ═══════════════════════════════════════════════════════════════
#  PRICE MAP
# ═══════════════════════════════════════════════════════════════
PRICE_FIXES = {
    'Zirconia Crowns — Premium': {
        'old_raw': '7490', 'new_raw': '4990',
        'old_fmt': '7,490', 'new_fmt': '4,990',
        'old_save': '2,010', 'new_save': '4,510',
    },
    'All-on-6 — Premium': {
        'old_raw': '8490', 'new_raw': '7990',
        'old_fmt': '8,490', 'new_fmt': '7,990',
        'old_save': '3,000', 'new_save': '3,500',
    },
    'All-on-4 — Signature': {
        'old_raw': '7490', 'new_raw': '8490',
        'old_fmt': '7,490', 'new_fmt': '8,490',
        'old_save': '2,500', 'new_save': '1,500',
    },
    'All-on-6 — Signature': {
        'old_raw': '8990', 'new_raw': '9990',
        'old_fmt': '8,990', 'new_fmt': '9,990',
        'old_save': '3,000', 'new_save': '2,000',
    },
}

# The estimator dropdown uses different names for Signature tier
ESTIMATOR_NAME_MAP = {
    'Zirconia Crowns — Premium': 'Zirconia Crowns — Premium',
    'All-on-6 — Premium':        'All-on-6 Premium',
    'All-on-4 — Signature':      'All-on-4 Top Tier',
    'All-on-6 — Signature':      'All-on-6 Top Tier',
}


class Fixer:
    def __init__(self, html):
        self.html = html
        self.original = html
        self.changes = []
        self.warnings = []

    def log(self, kind, msg):
        if kind == 'change':
            self.changes.append(msg)
            print(f"   ✅ {msg}")
        else:
            self.warnings.append(msg)
            print(f"   ⚠️  {msg}")

    # ─── 1. Remove perf-scroll ─────────────────────────────────
    def fix_perf_scroll(self):
        pattern = r'<script\s+id="perf-scroll"[^>]*>.*?</script>'
        if re.search(pattern, self.html, re.DOTALL):
            self.html = re.sub(
                pattern,
                '<!-- perf-scroll removed by fix_nile_v4 '
                '(was hijacking window.addEventListener & appendChild) -->',
                self.html, flags=re.DOTALL
            )
            self.log('change', 'Removed <script id="perf-scroll"> (fixed both hijacks)')
        else:
            self.log('warn', 'perf-scroll not found (already removed?)')

    # ─── 2. Schema.org prices ──────────────────────────────────
    def fix_schema_prices(self):
        for name, p in PRICE_FIXES.items():
            pat = (
                r'("name":\s*"' + re.escape(name) + r'"'
                r'[\s\S]{0,500}?"price":\s*")' + p['old_raw'] + r'(")'
            )
            n = len(re.findall(pat, self.html))
            if n:
                self.html = re.sub(pat, r'\g<1>' + p['new_raw'] + r'\g<2>', self.html)
                self.log('change', f'Schema: "{name}" {p["old_raw"]}→{p["new_raw"]} ({n}x)')
            else:
                self.log('warn', f'Schema: "{name}" pattern not found')

    # ─── 3. Estimator dropdown ─────────────────────────────────
    def fix_estimator_prices(self):
        for name, p in PRICE_FIXES.items():
            est_name = ESTIMATOR_NAME_MAP.get(name, name)
            pat = (
                r'(<option value=")' + p['old_raw'] + r'(\|\d+">'
                + re.escape(est_name) + r'[^<]*?\$)' + re.escape(p['old_fmt'])
                + r'(</option>)'
            )
            n = len(re.findall(pat, self.html))
            if n:
                self.html = re.sub(
                    pat,
                    r'\g<1>' + p['new_raw'] + r'\g<2>' + p['new_fmt'] + r'\g<3>',
                    self.html
                )
                self.log('change', f'Estimator: "{est_name}" → ${p["new_fmt"]}')
            else:
                self.log('warn', f'Estimator: "{est_name}" pattern not found')

    # ─── 4. Card prices ────────────────────────────────────────
    def fix_card_prices(self):
        for name, p in PRICE_FIXES.items():
            pat = (
                r'(<h3[^>]*>' + re.escape(name) + r'</h3>[\s\S]{0,800}?\$)'
                + re.escape(p['old_fmt'])
            )
            n = len(re.findall(pat, self.html))
            if n:
                self.html = re.sub(pat, r'\g<1>' + p['new_fmt'], self.html)
                self.log('change', f'Card: "{name}" ${p["old_fmt"]}→${p["new_fmt"]}')
            else:
                self.log('warn', f'Card: "{name}" pattern not found')

    # ─── 5. Card save amounts ──────────────────────────────────
    def fix_card_save_amounts(self):
        # (unique prefix pattern, old save, new save, label)
        saves = [
            ('Standard: $9,500</span> <span style="color:#AE9164;font-style:italic">— save $',
             '2,010', '4,510', 'Zirconia'),
            ('Standard: $11,490</span> <span style="color:#AE9164;font-style:italic">— save $',
             '3,000', '3,500', 'All-on-6 Premium'),
            ('Standard: $9,990</span> <span style="color:#AE9164;font-style:italic">— save $',
             '2,500', '1,500', 'All-on-4 Signature'),
            ('Standard: $11,990</span> <span style="color:#AE9164;font-style:italic">— save $',
             '3,000', '2,000', 'All-on-6 Signature'),
        ]
        for prefix, old_s, new_s, label in saves:
            old = prefix + old_s
            new = prefix + new_s
            if old in self.html:
                self.html = self.html.replace(old, new, 1)
                self.log('change', f'Save amount ({label}): ${old_s}→${new_s}')
            else:
                self.log('warn', f'Save amount ({label}) not found')

    # ─── 6. Reviews tables ─────────────────────────────────────
    def fix_review_tables(self):
        # 6a. Founding-vs-Standard table (full row replacement)
        founding = {
            'Zirconia Crowns — Premium': {
                'old': '<tr><td class="td-label">Zirconia Crowns — Premium</td><td class="td-center">$7,490</td><td class="td-muted td-center"><span style="text-decoration:line-through">$9,500</span></td><td class="td-gold td-center">$2,010</td></tr>',
                'new': '<tr><td class="td-label">Zirconia Crowns — Premium</td><td class="td-center">$4,990</td><td class="td-muted td-center"><span style="text-decoration:line-through">$9,500</span></td><td class="td-gold td-center">$4,510</td></tr>',
            },
            'All-on-6 — Premium': {
                'old': '<tr><td class="td-label">All-on-6 — Premium</td><td class="td-center">$8,490</td><td class="td-muted td-center"><span style="text-decoration:line-through">$11,490</span></td><td class="td-gold td-center">$3,000</td></tr>',
                'new': '<tr><td class="td-label">All-on-6 — Premium</td><td class="td-center">$7,990</td><td class="td-muted td-center"><span style="text-decoration:line-through">$11,490</span></td><td class="td-gold td-center">$3,500</td></tr>',
            },
            'All-on-4 — Signature': {
                'old': '<tr><td class="td-label">All-on-4 — Signature</td><td class="td-center">$7,490</td><td class="td-muted td-center"><span style="text-decoration:line-through">$9,990</span></td><td class="td-gold td-center">$2,500</td></tr>',
                'new': '<tr><td class="td-label">All-on-4 — Signature</td><td class="td-center">$8,490</td><td class="td-muted td-center"><span style="text-decoration:line-through">$9,990</span></td><td class="td-gold td-center">$1,500</td></tr>',
            },
            'All-on-6 — Signature': {
                'old': '<tr><td class="td-label">All-on-6 — Signature</td><td class="td-center">$8,990</td><td class="td-muted td-center"><span style="text-decoration:line-through">$11,990</span></td><td class="td-gold td-center">$3,000</td></tr>',
                'new': '<tr><td class="td-label">All-on-6 — Signature</td><td class="td-center">$9,990</td><td class="td-muted td-center"><span style="text-decoration:line-through">$11,990</span></td><td class="td-gold td-center">$2,000</td></tr>',
            },
        }
        for name, r in founding.items():
            if r['old'] in self.html:
                self.html = self.html.replace(r['old'], r['new'], 1)
                self.log('change', f'Reviews (Founding table): {name}')
            else:
                self.log('warn', f'Reviews (Founding): {name} row not found')

        # 6b. Recap table (Which Package Is Right for You?)
        recap = {
            'Zirconia': (
                '<td class="td-label">Zirconia Crowns — Premium</td><td class="td-center">1 (single jaw)</td><td class="td-muted td-center">— crowns only</td><td class="td-center">12–14</td><td class="td-gold td-center">$7,490</td>',
                '<td class="td-label">Zirconia Crowns — Premium</td><td class="td-center">1 (single jaw)</td><td class="td-muted td-center">— crowns only</td><td class="td-center">12–14</td><td class="td-gold td-center">$4,990</td>',
            ),
            'All-on-6 Premium': (
                '<td class="td-label">All-on-6 — Premium</td><td class="td-center">1 (single jaw)</td><td class="td-center">6</td><td class="td-center">12–14</td><td class="td-gold td-center">$8,490</td>',
                '<td class="td-label">All-on-6 — Premium</td><td class="td-center">1 (single jaw)</td><td class="td-center">6</td><td class="td-center">12–14</td><td class="td-gold td-center">$7,990</td>',
            ),
            'All-on-4 Signature': (
                '<td class="td-label">All-on-4 — Signature</td><td class="td-center">1 (single jaw)</td><td class="td-center">4</td><td class="td-center">10–12</td><td class="td-gold td-center">$7,490</td>',
                '<td class="td-label">All-on-4 — Signature</td><td class="td-center">1 (single jaw)</td><td class="td-center">4</td><td class="td-center">10–12</td><td class="td-gold td-center">$8,490</td>',
            ),
            'All-on-6 Signature': (
                '<td class="td-label">All-on-6 — Signature</td><td class="td-center">1 (single jaw)</td><td class="td-center">6</td><td class="td-center">12–14</td><td class="td-gold td-center">$8,990</td>',
                '<td class="td-label">All-on-6 — Signature</td><td class="td-center">1 (single jaw)</td><td class="td-center">6</td><td class="td-center">12–14</td><td class="td-gold td-center">$9,990</td>',
            ),
        }
        for label, (old, new) in recap.items():
            if old in self.html:
                self.html = self.html.replace(old, new, 1)
                self.log('change', f'Reviews (Recap): {label}')
            else:
                self.log('warn', f'Reviews (Recap): {label} not found')

    # ─── RUN ───────────────────────────────────────────────────
    def run(self):
        print("\n🔧 Applying fixes...\n")
        self.fix_perf_scroll()
        self.fix_schema_prices()
        self.fix_estimator_prices()
        self.fix_card_prices()
        self.fix_card_save_amounts()
        self.fix_review_tables()
        return self.html


# ═══════════════════════════════════════════════════════════════
#  VERIFICATION
# ═══════════════════════════════════════════════════════════════
def verify(html):
    issues = []
    if 'id="perf-scroll"' in html:
        issues.append('perf-scroll still present')
    if 'window.addEventListener = function' in html:
        issues.append('window.addEventListener hijack still present')
    if 'c.appendChild = function()' in html:
        issues.append('c.appendChild hijack still present')

    for name, p in PRICE_FIXES.items():
        # Look for the OLD price near the package name
        pat = re.escape(name) + r'[\s\S]{0,800}?\$' + re.escape(p['old_fmt'])
        if re.search(pat, html):
            issues.append(f'Old price still present: {name} (${p["old_fmt"]})')
    return issues


# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser(
        description='Nile Smile — surgical fix v4 (hijacks + prices)'
    )
    ap.add_argument('file', help='Path to index.html')
    ap.add_argument('--dry-run', action='store_true', help='Preview without saving')
    ap.add_argument('--verify', action='store_true', help='Verify current state only')
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f'❌ File not found: {path}')
        sys.exit(1)

    print(f'\n{"═"*66}')
    print(f'  🔧 Nile Smile — Surgical Fix v4.0')
    print(f'  📄 {path.name} — {path.stat().st_size:,} bytes')
    print(f'{"═"*66}\n')

    html = path.read_text(encoding='utf-8')

    # ─── VERIFY MODE ───
    if args.verify:
        issues = verify(html)
        if issues:
            print('❌ Issues found:')
            for i in issues:
                print(f'   • {i}')
            sys.exit(1)
        print('✅ Clean — no critical issues')
        sys.exit(0)

    # ─── APPLY ───
    fixer = Fixer(html)
    new_html = fixer.run()

    # ─── VERIFY AFTER ───
    print("\n🔍 Verifying after fixes:\n")
    remaining = verify(new_html)
    if remaining:
        for r in remaining:
            print(f'   ❌ {r}')
    else:
        print('   ✅ All clear — no hijacks, no stale prices')

    # ─── SIZE ───
    print(f'\n📦 Size: {len(html):,} → {len(new_html):,} bytes '
          f'({len(new_html)-len(html):+,})')

    # ─── SAVE ───
    if args.dry_run:
        print('\n⚠️  DRY RUN — nothing saved\n')
        return
    if new_html == html:
        print('\n⚠️  No changes made — file unchanged\n')
        return

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup = path.with_name(f'{path.stem}.backup_{ts}{path.suffix}')
    shutil.copy2(path, backup)
    print(f'\n💾 Backup: {backup.name}')

    path.write_text(new_html, encoding='utf-8')
    print(f'💾 Saved: {path.name}')
    print(f'\n✅ Done. Test the site:')
    print(f'   • Mobile: NO scroll freeze')
    print(f'   • Prices: logical tiers (Premium < Signature)')
    print(f'   • No console errors\n')


if __name__ == '__main__':
    main()