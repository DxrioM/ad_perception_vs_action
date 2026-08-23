"""
Etapa 5 — NLP y estadistica aplicada
========================================
1) NLP: frecuencia de palabras (CountVectorizer) sobre las descripciones,
   separado por anuncios de alto vs. bajo desempeño.
2) Comparacion IA: marco de "caso de uso" vs. "capacidad tecnica" (muestra
   pequeña, se presenta como comparacion de casos, no test formal).
3) Correlacion: numero de atributos (celebridad/IA/proposito/humor) vs. score.
4) HarrisX vs EDO: divergencia entre percepcion y accion real, para los
   anuncios donde tengo ambos datos.
"""
import pandas as pd
import numpy as np
import json
from scipy import stats
from sklearn.feature_extraction.text import CountVectorizer

PROC = "/home/claude/adsentiment_portfolio/data/processed/"
ads = pd.read_csv(PROC + "ads_harrisx.csv")
merged = pd.read_csv(PROC + "ads_merged.csv")

STOPWORDS_ES = set("""de la el en y a los con las un una que su para por no se al del su sus
como más muy fue son fueron o e quien esta este estos estas sobre entre general
aborda estimado puntos diferencia aprobación posición base según solo
donde cual cuando desde hasta todo toda todos todas otro otra ser hace
tras cada sin ese esa eso les lo le nos también ya así pero si sí
años año durante mismo misma primer primera segundo segunda tercer tercera""".split())

STOPWORDS_EN = set("""the a an and or of to in on for with that this these those
is are was were be been being it its their his her they them from by as
at than then so not no but if than about after before between during
score based only real overall said says also very more most into out up down""".split())

# ============================================================
# 1) NLP: FRECUENCIA DE PALABRAS (alto vs. bajo desempeño), ES y EN
# ============================================================
print("[1/4] Analisis NLP de frecuencia de palabras (ES + EN)...")
def top_words(texts, stopwords, n=12):
    vec = CountVectorizer(stop_words=list(stopwords), token_pattern=r"[a-zA-ZáéíóúñÁÉÍÓÚÑ]{4,}")
    X = vec.fit_transform(texts)
    freqs = np.asarray(X.sum(axis=0)).flatten()
    vocab = vec.get_feature_names_out()
    pairs = sorted(zip(vocab, freqs), key=lambda x: -x[1])
    return [{"palabra": w, "frecuencia": int(c)} for w, c in pairs[:n] if c > 0]

alto_es = ads[ads["harrisx_score"] >= 83]["descripcion"].tolist()
bajo_es = ads[ads["harrisx_score"] < 83]["descripcion"].tolist()
alto_en = ads[ads["harrisx_score"] >= 83]["descripcion_en"].tolist()
bajo_en = ads[ads["harrisx_score"] < 83]["descripcion_en"].tolist()
top_alto_es = top_words(alto_es, STOPWORDS_ES)
top_bajo_es = top_words(bajo_es, STOPWORDS_ES)
top_alto_en = top_words(alto_en, STOPWORDS_EN)
top_bajo_en = top_words(bajo_en, STOPWORDS_EN)
print(f"  ES - alto desempeño: {[w['palabra'] for w in top_alto_es[:6]]}")
print(f"  ES - bajo desempeño: {[w['palabra'] for w in top_bajo_es[:6]]}")
print(f"  EN - alto desempeño: {[w['palabra'] for w in top_alto_en[:6]]}")
print(f"  EN - bajo desempeño: {[w['palabra'] for w in top_bajo_en[:6]]}")

# ============================================================
# 2) COMPARACION IA: caso de uso vs. capacidad tecnica
# ============================================================
print("\n[2/4] Comparacion de marcos de IA...")
ia_ads = ads[ads["es_ia"] == 1]
caso_uso = ia_ads[ia_ads["marco_ia"] == "caso_de_uso"]["harrisx_score"]
capacidad = ia_ads[ia_ads["marco_ia"] == "capacidad"]["harrisx_score"]
print(f"  Caso de uso (n={len(caso_uso)}): {caso_uso.tolist()} -> media={caso_uso.mean():.1f}")
print(f"  Capacidad tecnica (n={len(capacidad)}): {capacidad.tolist()} -> media={capacidad.mean():.1f}")
diff_ia = caso_uso.mean() - capacidad.mean()
print(f"  Diferencia: {diff_ia:.1f} puntos (muestra pequeña -- se reporta como comparacion de casos)")

# ============================================================
# 3) CORRELACION: numero de atributos vs. score
# ============================================================
print("\n[3/4] Correlacion...")
r_attr, p_attr = stats.pearsonr(ads["num_atributos"], ads["harrisx_score"])
print(f"  Pearson r (num. atributos vs. score): {r_attr:.3f} (p={p_attr:.3f})")
print("  Interpretacion: acumular mas atributos (celebridad+IA+proposito+humor) no garantiza mejor score.")

# ============================================================
# 4) HARRISX VS EDO — divergencia percepcion vs. accion
# ============================================================
print("\n[4/4] Divergencia HarrisX vs. EDO...")
overlap = merged.dropna(subset=["edo_index"])
divergences = []
for _, row in overlap.iterrows():
    # normalizar HarrisX (0-100) a una escala comparable aproximada con EDO (base 100)
    harrisx_pct_of_max = row["harrisx_score"] / 93.2 * 100  # relativo al maximo del dataset
    divergences.append({
        "marca": row["marca"], "anuncio": row["nombre_anuncio"],
        "harrisx_score": float(row["harrisx_score"]), "harrisx_rank": int(row["harrisx_rank"]),
        "edo_index": float(row["edo_index"]),
    })
    print(f"  {row['marca']}: HarrisX #{int(row['harrisx_rank'])} ({row['harrisx_score']}) | EDO {row['edo_index']:.0f} (mediana=100)")

metrics = {
    "nlp_top_words_alto_desempeno": top_alto_es,
    "nlp_top_words_bajo_desempeno": top_bajo_es,
    "ia_comparacion": {
        "caso_de_uso_scores": caso_uso.tolist(), "caso_de_uso_mean": round(float(caso_uso.mean()), 1),
        "capacidad_scores": capacidad.tolist(), "capacidad_mean": round(float(capacidad.mean()), 1),
        "diferencia": round(float(diff_ia), 1), "n_caso_uso": int(len(caso_uso)), "n_capacidad": int(len(capacidad)),
    },
    "correlacion_atributos": {"r": round(float(r_attr), 3), "p": round(float(p_attr), 3)},
    "harrisx_vs_edo": divergences,
    "top10_avg": 88.9, "bottom_avg_approx": 62.0, "n_ads_total_evento": 70, "muestra_encuesta": 9707,
}
metrics_en = dict(metrics)
metrics_en["nlp_top_words_alto_desempeno"] = top_alto_en
metrics_en["nlp_top_words_bajo_desempeno"] = top_bajo_en

with open(PROC + "nlp_metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2, ensure_ascii=False)
with open(PROC + "nlp_metrics_en.json", "w", encoding="utf-8") as f:
    json.dump(metrics_en, f, indent=2, ensure_ascii=False)
print("\nGuardado: nlp_metrics.json y nlp_metrics_en.json")
