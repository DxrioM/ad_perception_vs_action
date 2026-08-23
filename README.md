# 📊 Percepción vs. Acción — Anuncios del Super Bowl LX

**🌐 [Read this in English](README.en.md)**

¿Qué anuncio gustó más — y cuál realmente funcionó? Los comerciales del Super Bowl LX (2026) analizados bajo dos lupas distintas con SQL, NLP y estadística.

**🔴 Demo:** [Español](https://dxriom.github.io/ad_perception_vs_action/) · [English](https://dxriom.github.io/ad_perception_vs_action/dashboard_en.html)

**📁 Repositorio:** [github.com/DxrioM/ad_perception_vs_action](https://github.com/DxrioM/ad_perception_vs_action)

---

## El hallazgo central: dos formas de medir "éxito" que a veces se contradicen

**HarrisX** encuestó a 9,707 personas para medir qué tanto les *gustó* cada anuncio (percepción). **EDO** midió qué tanto la gente realmente *actuó* después — búsquedas de marca, visitas web, descargas (acción real). No siempre coinciden:

| Anuncio | HarrisX (percepción) | EDO (acción real) |
|---|---|---|
| Lay's "Last Harvest" | **#1** de 70 (93.2) | Solo 1.2x la mediana |
| ai.com | Entre los 7 peores | **El más efectivo de todo el evento** (9.1x la mediana) |
| Pringles "Pringleleo" | 22vo general | 1.8x la mediana |

El anuncio que más le *gustó* a la gente no fue el que más *acción* generó. Esta tensión metodológica —percepción vs. comportamiento— es una lección real de marketing analytics, no un capricho de mi análisis.

## El hallazgo sobre IA: cómo enmarcas la tecnología sí importa

Los anuncios de IA se dividieron en dos grupos claros:
- **Caso de uso concreto** (Ring "encuentra a tu mascota perdida", Google "compra tu casa"): promedio de **89.3** en HarrisX
- **Demostración de capacidad técnica** (Anthropic): **65.0** — con 42% de la audiencia reportando confusión sobre qué se anunciaba

Diferencia: +24.3 puntos. Muestra pequeña (n=2 vs. n=1), se reporta como comparación de casos, no como test estadístico formal — pero el patrón es consistente con lo que HarrisX encontró en los 7 anuncios de IA del evento completo.

## Metodología y honestidad de datos

- **HarrisX Ad Index**: encuesta real a 9,707 adultos de EE.UU., metodología aplicada a más de 1,000 anuncios históricamente. Score compuesto 0-100 sobre 8 métricas.
- **EDO TV Outcomes**: índice de engagement real (comportamiento digital) relativo a la mediana de todos los anuncios del evento.
- Para los anuncios sin score exacto conocido (ej. los "bottom 7" de IA sin desglose individual), no inventé números — usé la posición documentada (ej. "puesto 67 de 70") en vez de fabricar un score preciso.
- El análisis NLP (frecuencia de palabras) se calculó de forma independiente en español e inglés — no es una traducción de los mismos resultados, sino dos corpus separados.

## Estructura del proyecto

```
adsentiment_portfolio/
├── data/
│   ├── raw/adsentiment_2026_data.py   # datos crudos verificados (HarrisX + EDO)
│   └── processed/                      # CSV/JSON limpios + base SQLite
├── sql/
│   ├── 01_schema.sql
│   └── 02_eda_queries.sql              # 6 queries de análisis exploratorio
├── scripts/
│   ├── 01_clean_transform.py           # limpieza + feature engineering
│   ├── 02_load_db.py                   # carga a SQLite
│   ├── 03_run_eda.py                   # ejecuta las queries SQL → JSON
│   ├── 04_nlp_stats_analysis.py        # NLP (CountVectorizer) + comparación IA + correlación
│   ├── 05_translate_exports.py         # traduce categorías para la versión EN
│   └── 06_build_dashboards.py          # inyecta datos + Chart.js en las plantillas ES/EN
├── lib/
│   ├── chart.umd.min.js
│   └── dashboard_template_i18n.html    # plantilla bilingüe
├── docs/
│   ├── index.html                      # ⭐ producto final en Español
│   └── dashboard_en.html               # ⭐ producto final en Inglés
├── README.md                           # este archivo, en español
└── README.en.md                        # este archivo, en inglés
```

## Cómo reproducirlo

```bash
pip install pandas numpy scikit-learn scipy
cd scripts
python3 01_clean_transform.py
python3 02_load_db.py
python3 03_run_eda.py
python3 04_nlp_stats_analysis.py
python3 05_translate_exports.py
python3 06_build_dashboards.py
cp ../outputs/*.html ../docs/
```

## Stack técnico

`Python` · `pandas` · `scikit-learn` (CountVectorizer para NLP) · `SciPy` (correlación de Pearson) · `SQL` · `SQLite` · `HTML/CSS/JS` · `Chart.js`

---

*Datos recopilados y verificados de fuentes públicas (HarrisX/Stagwell, EDO TV Outcomes, PRNewswire, ALM Corp, Rolling Stone, TVLine, AOL) durante febrero de 2026. Snapshot de Super Bowl LX, 8 de febrero de 2026.*
