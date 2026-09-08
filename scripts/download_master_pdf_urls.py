#!/usr/bin/env python3
"""Testa, em lotes retomáveis, URLs de PDF do corpus mestre."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from build_master_corpus import key

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "corpus" / "master-corpus.csv"
OUTPUT_DIR = ROOT / "data" / "document-resolution" / "master"
MANIFEST = OUTPUT_DIR / "source-url-download-manifest.csv"
DESTINATION = ROOT / "library" / "staging" / "master"
UA = "DesignConversacionalMundaneum/1.1 (systematic evidence mapping)"


def safe_name(corpus_id: str, title: str) -> str:
    title_slug = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-")[:80]
    return f"{corpus_id}-{title_slug or 'documento'}.pdf"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def retrieve(row: dict[str, str], timeout: int) -> dict[str, str]:
    url = row["source_pdf_url"].strip()
    target = DESTINATION / (Path(safe_name(row["corpus_id"], row["title"])).stem + '-' + hashlib.sha256(url.encode()).hexdigest()[:12] + '.pdf')
    result = {
        "corpus_id": row["corpus_id"],
        "title": row["title"],
        "doi": row["doi"],
        "url": url,
        "license": row["license"],
        "oa_status": row["oa_status"],
        "path": target.relative_to(ROOT).as_posix(),
        "downloaded": "false",
        "pdf_signature": "false",
        "bytes": "0",
        "sha256": "",
        "content_type": "",
        "http_status": "",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "error": "",
    }
    try:
        request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,*/*;q=0.5"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = response.read()
            result["content_type"] = response.headers.get("Content-Type", "")
            result["http_status"] = str(response.status)
        is_pdf = data.startswith(b"%PDF-")
        if is_pdf:
            target.write_bytes(data)
        result.update(
            {
                "downloaded": "true",
                "pdf_signature": str(is_pdf).lower(),
                "bytes": str(len(data)),
                "sha256": hashlib.sha256(data).hexdigest(),
                "error": "" if is_pdf else "response-is-not-pdf",
            }
        )
    except Exception as exc:
        result["error"] = repr(exc)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--retry-failures", action="store_true")
    args = parser.parse_args()

    corpus = read_rows(SOURCE)
    existing = read_rows(MANIFEST)
    attempted = {(key(row),row['url']) for row in existing}
    if args.retry_failures:
        attempted = {(key(row),row['url']) for row in existing if row.get('pdf_signature')=='true'}

    pending = [
        row for row in corpus
        if row.get('source_pdf_url') and row.get('collection_status')!='arquivo-recebido' and (key(row),row['source_pdf_url']) not in attempted
    ][: args.limit]
    DESTINATION.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    new_rows = []
    def checkpoint():
        combined_rows=existing+new_rows
        if not combined_rows:return
        temporary=MANIFEST.with_suffix('.csv.tmp')
        with temporary.open('w',encoding='utf-8-sig',newline='') as handle:
            writer=csv.DictWriter(handle,fieldnames=list(combined_rows[0]));writer.writeheader();writer.writerows(combined_rows)
        temporary.replace(MANIFEST)
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(retrieve, row, args.timeout): row["corpus_id"] for row in pending}
        for future in as_completed(futures):
            new_rows.append(future.result())
            checkpoint()
    new_rows.sort(key=lambda row: row["corpus_id"])

    combined = existing + new_rows
    fields = list(combined[0]) if combined else []
    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        if fields:
            writer.writeheader()
            writer.writerows(combined)

    summary = {
        "available_source_urls_pending_at_inventory": sum(row["document_status"] == "url-pdf-a-testar" for row in corpus),
        "attempted_total": len(combined),
        "attempted_this_run": len(new_rows),
        "pdf_signatures_total": sum(row["pdf_signature"] == "true" for row in combined),
        "failures_total": sum(bool(row["error"]) for row in combined),
        "remaining": sum(
            bool(row.get('source_pdf_url')) and row.get('collection_status')!='arquivo-recebido' and (key(row),row['source_pdf_url']) not in {(key(item),item['url']) for item in combined}
            for row in corpus
        ),
        "validity_pending": "Assinatura PDF não confirma correspondência bibliográfica nem integralidade.",
    }
    (OUTPUT_DIR / "source-url-download-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
