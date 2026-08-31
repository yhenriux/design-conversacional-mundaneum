#!/usr/bin/env python3
"""Aplica decisões humanas documentadas aos lotes da triagem ampliada."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


B01_EXCLUSIONS = {
    "X016": "Emprega conversação como metáfora de uma interface gráfica para modelagem de redes de filas; Design Conversacional não organiza o objeto ou a contribuição.",
    "X019": "Trata da modelagem gráfica de sistemas estocásticos; não foi identificada centralidade em interação conversacional humana.",
    "X027": "Usa conversacional como metáfora de um processo de criação arquitetônica com IA; Design Conversacional não é objeto de pesquisa ou estudo.",
    "X045": "Descreve uma implementação médica ampla, mas o resumo não apresenta questão, método ou contribuição centrados no design da conversa.",
}

B01_DUPLICATES = {
    "X007": "Duplicata bibliográfica de X003, com o mesmo título e conteúdo em outro registro de origem.",
    "X029": "Material suplementar do estudo X020; deve permanecer vinculado ao registro principal, não como estudo independente.",
}

B01_FULLTEXT = {
    "X010": "O resumo descreve estado e transições em um esquema de conversação, mas o uso histórico do termo precisa ser verificado no texto integral.",
    "X047": "O estudo investiga prompts para interações em linguagem natural; o texto integral deve mostrar se Design Conversacional é objeto de pesquisa ou apenas contexto técnico.",
}


def decide(record: dict[str, str]) -> tuple[str, str]:
    rid = record["expanded_id"]
    if rid in B01_EXCLUSIONS:
        return "exclude-ontology", B01_EXCLUSIONS[rid]
    if rid in B01_DUPLICATES:
        return "exclude-duplicate", B01_DUPLICATES[rid]
    if rid in B01_FULLTEXT:
        return "full-text-review", B01_FULLTEXT[rid]
    return (
        "provisional-include",
        "O título e o resumo tratam Design Conversacional, sua fundamentação, seus métodos, suas práticas ou seus efeitos como objeto central; a decisão depende de confirmação no texto integral.",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("batch", help="CSV do lote, por exemplo data/screening/batches/B01.csv")
    parser.add_argument("--output-dir", default="data/screening/expanded-decisions")
    args = parser.parse_args()

    batch_path = Path(args.batch)
    batch_id = batch_path.stem
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with batch_path.open(encoding="utf-8-sig", newline="") as handle:
        records = list(csv.DictReader(handle))

    if batch_id != "B01":
        raise SystemExit(f"Ainda não há decisões humanas codificadas para {batch_id}.")

    output_rows = []
    for record in records:
        decision, reason = decide(record)
        total = int(record["expanded_possible_score"] or 0)
        if decision in {"exclude-ontology", "exclude-duplicate"}:
            total = min(total, 6)
        output_rows.append(
            {
                **record,
                "screening_decision": decision,
                "screening_reason": reason,
                "screening_stage": "titulo-resumo-humano",
                "screening_score": total,
                "full_text_required": "sim" if decision in {"provisional-include", "full-text-review"} else "nao",
            }
        )

    csv_path = output_dir / f"{batch_id}-decisions.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)

    counts = Counter(row["screening_decision"] for row in output_rows)
    summary = {
        "batch_id": batch_id,
        "records": len(output_rows),
        "decisions": dict(sorted(counts.items())),
        "method": "Leitura humana de título e resumo, com centralidade ontológica estrita e decisão provisória sujeita ao texto integral.",
        "output": csv_path.as_posix(),
    }
    summary_path = output_dir / f"{batch_id}-summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
