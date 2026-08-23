"""
Etapa 6 — Generar variante en ingles de eda_results.json
"""
import json

PROC = "/home/claude/adsentiment_portfolio/data/processed/"

CAT_ES_EN = {
    "Comida y Bebida": "Food & Beverage",
    "Tecnología / IA": "Tech / AI",
    "Causa Social": "Social Cause",
    "Belleza y Cuidado Personal": "Beauty & Personal Care",
    "Salud y Bienestar": "Health & Wellness",
    "Seguros": "Insurance",
    "Finanzas": "Finance",
}

eda = json.load(open(PROC + "eda_results.json", encoding="utf-8"))
eda_en = json.loads(json.dumps(eda))
for row in eda_en["ranking_completo"]:
    row["categoria"] = CAT_ES_EN.get(row["categoria"], row["categoria"])
for row in eda_en["score_por_categoria"]:
    row["categoria"] = CAT_ES_EN.get(row["categoria"], row["categoria"])
json.dump(eda_en, open(PROC + "eda_results_en.json", "w", encoding="utf-8"), ensure_ascii=False)
print("eda_results_en.json generado (nlp_metrics_en.json ya se genera en el script 04)")
