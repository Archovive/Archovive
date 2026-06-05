#!/usr/bin/env python3
"""Render ARCHOVIVE_DASHBOARD.html from compliance_report.json (static, on-prem)."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    report_path = root / "compliance_report.json"
    if not report_path.is_file():
        print(f"missing {report_path}", file=sys.stderr)
        return 1
    report = json.loads(report_path.read_text(encoding="utf-8"))
    packs = report.get("packs_evaluated") or []
    formal = report.get("formal_predicates") or {}
    preds = formal.get("predicates") or []
    rows = "".join(
        f"<tr><td>{p.get('predicate_id')}</td><td>{'PASS' if p.get('passed') else 'FAIL'}</td>"
        f"<td>{p.get('rationale', '')[:120]}</td></tr>"
        for p in preds[:40]
    )
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Archovive Dashboard</title>
<style>body{{font-family:system-ui;margin:2rem}}table{{border-collapse:collapse;width:100%}}
td,th{{border:1px solid #ccc;padding:8px}}.fail{{color:#b00}}</style></head>
<body><h1>Archovive Compliance Dashboard</h1>
<p>Analysis: <code>{report.get('analysis_root','')}</code></p>
<p>Packs: {', '.join(packs)} · Formal pass: <b>{formal.get('passed')}</b></p>
<h2>Formal predicates</h2><table><tr><th>ID</th><th>Status</th><th>Rationale</th></tr>{rows}</table>
<p><small>Generated from compliance_report.json — no server required.</small></p></body></html>"""
    out = root / "ARCHOVIVE_DASHBOARD.html"
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
