#!/usr/bin/env python3
"""Recupera PDFs indicados como abertos na triagem ampliada, sem inferir validade."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


UA = "DesignConversacionalMundaneum/1.0 (systematic evidence mapping)"


def safe_name(record_id: str, title: str) -> str:
    title_slug = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-")[:80]
    return f"{record_id}-{title_slug or 'documento'}.pdf"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("decisions", type=Path)
    parser.add_argument("--batch", required=True)
    parser.add_argument("--delay", type=float, default=0.25)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    destination = root / "library" / "staging" / "expanded" / args.batch
    output_dir = root / "data" / "document-resolution" / "expanded" / args.batch
    destination.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    with args.decisions.open(encoding="utf-8-sig", newline="") as handle:
        records = list(csv.DictReader(handle))
    selected = [
        row for row in records
        if row["screening_decision"] in {"provisional-include", "full-text-review"} and row.get("pdf_url")
    ]

    results = []
    for row in selected:
        url = row["pdf_url"].strip()
        target = destination / safe_name(row["expanded_id"], row["title"])
        result = {
            "expanded_id": row["expanded_id"],
            "title": row["title"],
            "doi": row.get("doi", ""),
            "url": url,
            "license": row.get("license", ""),
            "oa_status": row.get("oa_status", ""),
            "path": target.relative_to(root).as_posix(),
            "downloaded": "false",
            "pdf_signature": "false",
            "bytes": "0",
            "sha256": "",
            "content_type": "",
            "retrieved_at": "",
            "error": "",
        }
        try:
            request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,*/*;q=0.5"})
            with urllib.request.urlopen(request, timeout=90) as response:
                data = response.read()
                content_type = response.headers.get("Content-Type", "")
            is_pdf = data.startswith(b"%PDF-")
            if is_pdf:
                target.write_bytes(data)
            result.update(
                {
                    "downloaded": "true",
                    "pdf_signature": str(is_pdf).lower(),
                    "bytes": str(len(data)),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "content_type": content_type,
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "error": "" if is_pdf else "response-is-not-pdf",
                }
            )
        except Exception as exc:
            result["error"] = repr(exc)
        results.append(result)
        time.sleep(args.delay)

    manifest = output_dir / "download-manifest.csv"
    fields = list(results[0]) if results else []
    with manifest.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        if fields:
            writer.writeheader()
            writer.writerows(results)
    summary = {
        "batch": args.batch,
        "urls_attempted": len(results),
        "responses": sum(row["downloaded"] == "true" for row in results),
        "pdf_signatures": sum(row["pdf_signature"] == "true" for row in results),
        "failures": sum(bool(row["error"]) for row in results),
        "validity_pending": "A assinatura PDF não confirma correspondência de título nem integralidade.",
    }
    (output_dir / "download-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
