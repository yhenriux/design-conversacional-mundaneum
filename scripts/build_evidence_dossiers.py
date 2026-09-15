"""Create page-located evidence dossiers for central records with extracted full text.

The script never invents interpretation. It stores source excerpts and provenance that
make later analytical reading auditable. Existing hand-written analytical notes remain
untouched.
"""
import argparse, csv, json, re, time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Corpus" / "Dossies-de-evidencias"
CHECK = OUT / "checkpoint.json"

KEYS = {
    "resumo": ("abstract", "resumo"),
    "metodo": ("method", "methodology", "methods", "metod", "materials"),
    "resultados": ("results", "findings", "achados", "resultados"),
    "discussao": ("discussion", "discussão"),
    "limitacoes": ("limitation", "limitations", "limitações", "challenges", "cautions"),
    "conclusao": ("conclusion", "conclusão"),
}

def pages(text):
    parts = re.split(r"===== PAGE\s+(\d+)\s+=====", text, flags=re.I)
    return [(int(parts[i]), parts[i + 1]) for i in range(1, len(parts), 2)]

def excerpt(page_no, page_text, terms):
    for term in terms:
        m = re.search(r"(?is)(.{0,250}\b" + re.escape(term) + r"\w*.{0,900})", page_text)
        if m:
            value = re.sub(r"\s+", " ", m.group(1)).strip()
            return page_no, value[:1150]
    return None

def source_rows():
    central = {p.name[:9] for p in (ROOT / "Corpus" / "Fichas-analiticas").glob("*.md")}
    manifests = {}
    for manifest in (ROOT / "data" / "document-resolution").rglob("extraction-manifest.csv"):
        try:
            for row in csv.DictReader(manifest.open(encoding="utf-8-sig")):
                if row.get("record_id") in central and row.get("text_path"):
                    manifests[row["record_id"]] = row
        except (OSError, UnicodeDecodeError):
            continue
    return manifests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    records = source_rows()
    ids = sorted(records)
    start = 0
    if args.resume and CHECK.exists():
        start = int(json.loads(CHECK.read_text(encoding="utf-8")).get("next_offset", 0))
    end = min(start + args.batch_size, len(ids))
    created, pending = [], []
    for record_id in ids[start:end]:
        row = records[record_id]
        text_path = ROOT / row["text_path"]
        target = OUT / f"{record_id}.md"
        try:
            text = text_path.read_text(encoding="utf-8", errors="ignore")
            split_pages = pages(text)
            if len(text.strip()) < 1500 or not split_pages:
                pending.append({"record_id": record_id, "reason": "texto-extraido-insuficiente"})
                continue
            sections = []
            for label, terms in KEYS.items():
                found = None
                for page_no, page_text in split_pages:
                    found = excerpt(page_no, page_text, terms)
                    if found:
                        break
                if found:
                    page_no, value = found
                    sections.append(f"### {label.capitalize()}\n\n**Localização: p. {page_no}.**\n\n> {value}\n")
                else:
                    sections.append(f"### {label.capitalize()}\n\nNR no trecho extraído por busca automática. Requer leitura dirigida.\n")
            headings = []
            for page_no, page_text in split_pages:
                for line in page_text.splitlines():
                    line = re.sub(r"\s+", " ", line).strip()
                    if 3 < len(line) < 105 and (line.isupper() or re.match(r"^\d+(?:\.\d+)*\s+[A-Z]", line)):
                        headings.append(f"p. {page_no}: {line}")
            dossier = f"""---
record_id: {record_id}
tipo: dossie-de-evidencias-extraidas
fonte_textual: \"{row['text_path']}\"
paginas_extraidas: {row.get('pages', 'ND')}
caracteres_extraidos: {row.get('characters', 'ND')}
status: evidencia-extraida-nao-interpretada
---

# Dossiê de evidências: {record_id}

Este dossiê preserva trechos da fonte e sua localização. Ele não substitui a leitura crítica; nenhum trecho abaixo é uma interpretação do fichamento.

## Mapa de seções detectadas

{chr(10).join('- ' + item for item in headings[:80]) or 'NR'}

## Evidências por aspecto

{chr(10).join(sections)}

## Procedência

- Texto integral extraído de `{row['text_path']}`.
- Hash textual: `{row.get('text_sha256', 'ND')}`.
- Estado de extração: `{row.get('extraction_status', 'ND')}`.
"""
            target.write_text(dossier, encoding="utf-8")
            created.append(record_id)
        except OSError as error:
            pending.append({"record_id": record_id, "reason": f"erro-io: {error}"})
    state = {"updated_at": datetime.now(timezone.utc).isoformat(), "total_eligible": len(ids), "next_offset": end, "created_this_batch": created, "pending_this_batch": pending}
    CHECK.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(state, ensure_ascii=False))

if __name__ == "__main__":
    main()
