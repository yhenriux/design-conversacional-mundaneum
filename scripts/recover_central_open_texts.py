#!/usr/bin/env python3
"""Resolve versões abertas para fontes centrais sem texto local suficiente.

O processo consulta OpenAlex por DOI, preserva todas as localizações abertas
declaradas pela base e, opcionalmente, baixa somente URLs que retornem um PDF.
Ele não tenta contornar paywalls e não substitui uma errata pelo artigo original.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "Corpus" / "indice-obras.json"
ANALYTIC_STATE = ROOT / "Corpus" / "estado-redacao-analitica.json"
MASTER = ROOT / "data" / "corpus" / "master-corpus.csv"
OUT = ROOT / "data" / "document-resolution" / "central-recovery"
ATTEMPTS = OUT / "openalex-attempts.csv"
LOCATIONS = OUT / "openalex-locations.csv"
DOWNLOADS = OUT / "download-manifest.csv"
PDFS = ROOT / "library" / "staging" / "central-recovery"
UA = "DesignConversacionalMundaneum/1.2 (open-access recovery; contact: research@example.com)"


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def clean_doi(value: str) -> str:
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", (value or "").strip(), flags=re.I)


def write_csv(path: Path, values: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(values)
    temporary.replace(path)


def query_openalex(record: dict[str, str], timeout: int) -> tuple[dict[str, str], list[dict[str, str]]]:
    doi = clean_doi(record.get("doi", ""))
    now = datetime.now(timezone.utc).isoformat()
    attempt = {
        "corpus_id": record["corpus_id"], "title": record["title"], "doi": doi,
        "resolved": "false", "locations": "0", "retrieved_at": now, "error": "",
    }
    if not doi:
        attempt["error"] = "doi-ausente"
        return attempt, []
    try:
        url = "https://api.openalex.org/works/https://doi.org/" + urllib.parse.quote(doi, safe="")
        request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            work = json.loads(response.read())
        found = []
        for number, location in enumerate(work.get("locations") or [], 1):
            source = location.get("source") or {}
            pdf_url = location.get("pdf_url") or ""
            if not (location.get("is_oa") or pdf_url):
                continue
            found.append({
                "corpus_id": record["corpus_id"], "title": record["title"], "doi": doi,
                "openalex_id": work.get("id") or "", "location_number": str(number),
                "is_oa": str(bool(location.get("is_oa"))).lower(), "pdf_url": pdf_url,
                "landing_url": location.get("landing_page_url") or "", "license": location.get("license") or "",
                "version": location.get("version") or "", "source_name": source.get("display_name") or "",
                "source_type": source.get("type") or "", "retrieved_at": now,
            })
        attempt.update({"resolved": "true", "locations": str(len(found))})
        return attempt, found
    except Exception as exc:  # provenance of an unsuccessful lookup is material
        attempt["error"] = repr(exc)
        return attempt, []


def safe_filename(record_id: str, url: str) -> Path:
    return PDFS / f"{record_id}-{hashlib.sha256(url.encode()).hexdigest()[:16]}.pdf"


def download(location: dict[str, str], timeout: int) -> dict[str, str]:
    url = location.get("pdf_url", "")
    target = safe_filename(location["corpus_id"], url)
    result = {
        "corpus_id": location["corpus_id"], "title": location["title"], "doi": location["doi"],
        "url": url, "license": location.get("license", ""), "version": location.get("version", ""),
        "source_name": location.get("source_name", ""), "path": str(target.relative_to(ROOT)),
        "downloaded": "false", "pdf_signature": "false", "bytes": "0", "sha256": "",
        "content_type": "", "retrieved_at": datetime.now(timezone.utc).isoformat(), "error": "",
    }
    if not url:
        result["error"] = "localizacao-sem-url-pdf"
        return result
    try:
        request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,*/*;q=0.5"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = response.read()
            result["content_type"] = response.headers.get("Content-Type", "")
        result.update({"downloaded": "true", "bytes": str(len(data)), "sha256": hashlib.sha256(data).hexdigest()})
        if data.startswith(b"%PDF-"):
            PDFS.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            result["pdf_signature"] = "true"
        else:
            result["error"] = "response-is-not-pdf"
    except Exception as exc:
        result["error"] = repr(exc)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--retry-errors", action="store_true")
    args = parser.parse_args()

    index = json.loads(INDEX.read_text(encoding="utf-8"))
    master = {item["corpus_id"]: item for item in rows(MASTER)}
    existing_attempts = rows(ATTEMPTS)
    existing_locations = rows(LOCATIONS)
    existing_downloads = rows(DOWNLOADS)
    done = {item["corpus_id"] for item in existing_attempts if not (args.retry_errors and item.get("error"))}
    central = [item for item in index if item.get("central") is True]
    analytic_state = json.loads(ANALYTIC_STATE.read_text(encoding="utf-8")) if ANALYTIC_STATE.exists() else {}
    insufficient = set(analytic_state.get("pendencias_texto_insuficiente", []))
    selected = []
    for item in sorted(central, key=lambda value: value["corpus_id"]):
        record = master.get(item["corpus_id"], {})
        if item["corpus_id"] in done or not record:
            continue
        if item.get("document_status") == "pdf-integral-validado-local" and item["corpus_id"] not in insufficient:
            continue
        selected.append(record)
    selected = selected[:args.batch_size]

    new_attempts, new_locations = [], []
    for record in selected:
        attempt, found = query_openalex(record, args.timeout)
        new_attempts.append(attempt)
        new_locations.extend(found)
        time.sleep(0.15)
    all_attempts = existing_attempts + new_attempts
    all_locations = existing_locations + new_locations
    attempt_fields = ["corpus_id", "title", "doi", "resolved", "locations", "retrieved_at", "error"]
    location_fields = ["corpus_id", "title", "doi", "openalex_id", "location_number", "is_oa", "pdf_url", "landing_url", "license", "version", "source_name", "source_type", "retrieved_at"]
    write_csv(ATTEMPTS, all_attempts, attempt_fields)
    write_csv(LOCATIONS, all_locations, location_fields)

    new_downloads = []
    if args.download:
        downloaded_urls = {item.get("url") for item in existing_downloads}
        for location in new_locations:
            if location.get("pdf_url") and location["pdf_url"] not in downloaded_urls:
                new_downloads.append(download(location, args.timeout))
        all_downloads = existing_downloads + new_downloads
        download_fields = ["corpus_id", "title", "doi", "url", "license", "version", "source_name", "path", "downloaded", "pdf_signature", "bytes", "sha256", "content_type", "retrieved_at", "error"]
        write_csv(DOWNLOADS, all_downloads, download_fields)

    summary = {
        "central_records": len(central), "attempted_this_run": len(new_attempts),
        "attempted_total": len(all_attempts), "open_locations_this_run": len(new_locations),
        "pdfs_retrieved_this_run": sum(item["pdf_signature"] == "true" for item in new_downloads),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rule": "PDF signature does not establish bibliographic correspondence or analytical sufficiency.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
