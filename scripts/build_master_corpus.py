#!/usr/bin/env python3
"""Consolida todos os estudos únicos descobertos e seus estados documentais."""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = "20260831T003810Z"
SOURCE = ROOT / "data" / "search-runs" / RUN / "candidates-deduplicated.csv"
OUTPUT_DIR = ROOT / "data" / "corpus"


def normalize_doi(value: str) -> str:
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", (value or "").strip(), flags=re.I).lower()


def normalize_title(value: str) -> str:
    return re.sub(r"[^\w]+", " ", unicodedata.normalize("NFKC", value or "").casefold()).strip()


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def key(row: dict[str, str]) -> tuple[str, str]:
    doi = normalize_doi(row.get("doi", ""))
    return (doi, "") if doi else ("", normalize_title(row.get("title", "")))


def identity(row):
    doi = normalize_doi(row.get("doi", ""))
    if doi:
        return "doi:" + doi
    if row.get("source_id"):
        return "source:" + row["source_id"].strip()
    return "metadata:" + json.dumps([normalize_title(row.get("title", "")), row.get("authors", ""), row.get("year", ""), row.get("type", "")], ensure_ascii=False)


def main() -> None:
    candidates = read_rows(SOURCE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    registry_path = OUTPUT_DIR / "identity-registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    for old in read_rows(OUTPUT_DIR / "master-corpus.csv"):
        registry.setdefault(identity(old), old["corpus_id"])
    next_id = max((int(value.split("-")[-1]) for value in registry.values()), default=0) + 1
    supplemental_paths = sorted((ROOT / "data" / "discovery").glob("*.csv"))
    occurrences = list(candidates)
    for supplemental in supplemental_paths:
        for record in read_rows(supplemental):
            occurrences.append(record)
    unique = {}
    for record in occurrences:
        unique.setdefault(identity(record), record)
    candidates = list(unique.values())
    for record in candidates:
        ident = identity(record)
        if ident not in registry:
            registry[ident] = f"DCM-{next_id:05d}"
            next_id += 1
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    provenance = [{"corpus_id": registry[identity(r)], "source_api": r.get("source_api", ""), "source_id": r.get("source_id", ""), "run_id": r.get("run_id", ""), "query": r.get("query", ""), "title": r.get("title", ""), "pdf_url": r.get("pdf_url", "")} for r in occurrences]
    with (OUTPUT_DIR / "discovery-provenance.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(provenance[0])); writer.writeheader(); writer.writerows(provenance)
    resolution_root = ROOT / "data" / "document-resolution"
    validated_paths = sorted(set(resolution_root.rglob("validated-documents.csv")))
    download_paths = sorted(set(resolution_root.rglob("*download-manifest.csv")))

    validated = {}
    for path in validated_paths:
        for row in read_rows(path):
            validated[key(row)] = {**row, "manifest": path.relative_to(ROOT).as_posix()}

    attempts: dict[tuple[str, str], list[dict[str, str]]] = {}
    for path in download_paths:
        for row in read_rows(path):
            attempts.setdefault(key(row), []).append({**row, "manifest": path.relative_to(ROOT).as_posix()})

    rows = []
    for number, candidate in enumerate(candidates, 1):
        candidate_key = key(candidate)
        validation = validated.get(candidate_key)
        candidate_attempts = attempts.get(candidate_key, [])
        received_pdf = any(
            row.get("valid_pdf") == "true" or row.get("pdf_signature") == "true"
            for row in candidate_attempts
        )
        if validation:
            status = "pdf-integral-validado-local"
        elif received_pdf:
            status = "pdf-recebido-a-validar"
        elif candidate_attempts:
            status = "recuperacao-tentada-sem-pdf-valido"
        elif candidate.get("pdf_url"):
            status = "url-pdf-a-testar"
        elif candidate.get("doi"):
            status = "sem-url-pdf-resolucao-pendente"
        else:
            status = "sem-doi-busca-por-titulo-pendente"

        rows.append(
            {
                "corpus_id": registry[identity(candidate)],
                "collection_status": "arquivo-recebido" if validation or received_pdf else "transferencia-falhou" if candidate_attempts else "endereco-pdf-localizado" if candidate.get("pdf_url") else "obra-descoberta",
                "bibliographic_status": "estudo-unico-descoberto",
                "document_status": status,
                "run_id": candidate.get("run_id", ""),
                "source_api": candidate.get("source_api", ""),
                "source_id": candidate.get("source_id", ""),
                "doi": candidate.get("doi", ""),
                "title": candidate.get("title", ""),
                "year": candidate.get("year", ""),
                "authors": candidate.get("authors", ""),
                "type": candidate.get("type", ""),
                "abstract": candidate.get("abstract", ""),
                "landing_url": candidate.get("landing_url", ""),
                "source_pdf_url": candidate.get("pdf_url", ""),
                "license": candidate.get("license", ""),
                "oa_status": candidate.get("oa_status", ""),
                "ontology_score": candidate.get("ontology_score", ""),
                "screening_state": candidate.get("decision", ""),
                "download_attempts": str(len(candidate_attempts)),
                "validated_local_path": (validation or {}).get("local_path", ""),
                "document_manifest": (validation or {}).get("manifest", ""),
            }
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / "master-corpus.csv"
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    status_counts = Counter(row["document_status"] for row in rows)
    summary = {
        "run_id": RUN,
        "unique_discovered_studies": len(rows),
        "supplemental_discovery_files": [path.relative_to(ROOT).as_posix() for path in supplemental_paths],
        "bibliographic_rule": "Todo registro deduplicado integra o corpus mestre; disponibilidade de PDF é estado documental.",
        "with_doi": sum(bool(row["doi"]) for row in rows),
        "with_source_pdf_url": sum(bool(row["source_pdf_url"]) for row in rows),
        "document_status": dict(sorted(status_counts.items())),
        "collection_status": dict(sorted(Counter(row['collection_status'] for row in rows).items())),
        "current_phase": "Descoberta e coleta; análise de conteúdo posterior.",
        "output": output.relative_to(ROOT).as_posix(),
    }
    (OUTPUT_DIR / "master-corpus-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
