"""
Etapa 2 — Limpieza y transformacion
======================================
"""
import sys, os
sys.path.insert(0, "/home/claude/adsentiment_portfolio/data/raw")
import adsentiment_2026_data as raw
import pandas as pd

OUT_DIR = "/home/claude/adsentiment_portfolio/data/processed"
os.makedirs(OUT_DIR, exist_ok=True)

cols = ["marca", "nombre_anuncio", "categoria", "harrisx_score", "harrisx_rank",
        "tiene_celebridad", "es_ia", "marco_ia", "es_proposito_social", "usa_humor",
        "descripcion", "descripcion_en"]
ads = pd.DataFrame(raw.ADS_HARRISX, columns=cols)

# feature engineering
ads["tier"] = pd.cut(ads["harrisx_score"], bins=[0, 75, 85, 100],
                      labels=["Bajo desempeño", "Desempeño medio", "Alto desempeño"])
ads["num_atributos"] = ads[["tiene_celebridad", "es_ia", "es_proposito_social", "usa_humor"]].sum(axis=1)

edo_cols = ["marca", "nombre_anuncio", "edo_index", "nota_edo"]
edo = pd.DataFrame(raw.ADS_EDO, columns=edo_cols)

# cruce HarrisX x EDO donde el mismo anuncio aparece en ambos (por nombre)
merged = ads.merge(edo[["marca", "nombre_anuncio", "edo_index"]], on=["marca", "nombre_anuncio"], how="left")

ads.to_csv(f"{OUT_DIR}/ads_harrisx.csv", index=False)
edo.to_csv(f"{OUT_DIR}/ads_edo.csv", index=False)
merged.to_csv(f"{OUT_DIR}/ads_merged.csv", index=False)

print(f"Anuncios HarrisX: {len(ads)}")
print(f"Anuncios EDO: {len(edo)}")
print(f"Anuncios con ambos scores (para comparar percepcion vs. accion): {merged['edo_index'].notna().sum()}")
print(f"\nPor categoria:")
print(ads.groupby("categoria")["harrisx_score"].agg(["count", "mean"]).round(1))
print(f"\nPor atributo (celebridad, IA, proposito, humor):")
for attr in ["tiene_celebridad", "es_ia", "es_proposito_social", "usa_humor"]:
    print(f"  {attr}: n={ads[attr].sum()}, score promedio={ads[ads[attr]]['harrisx_score'].mean():.1f} vs. sin={ads[~ads[attr]]['harrisx_score'].mean():.1f}")
