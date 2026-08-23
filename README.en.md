# 📊 Perception vs. Action — Super Bowl LX Ads

**🌐 [Leer esto en Español](README.md)**

Which ad did people like most — and which one actually worked? Super Bowl LX (2026) commercials analyzed under two different lenses with SQL, NLP, and statistics.

**🔴 Demo:** [Español](https://dxriom.github.io/ad_perception_vs_action/) · [English](https://dxriom.github.io/ad_perception_vs_action/dashboard_en.html)

**📁 Repository:** [github.com/DxrioM/ad_perception_vs_action](https://github.com/DxrioM/ad_perception_vs_action)

---

## The core finding: two ways of measuring "success" that sometimes contradict each other

**HarrisX** surveyed 9,707 people to measure how much they *liked* each ad (perception). **EDO** measured how much people actually *acted* afterward — brand searches, website visits, app downloads (real action). They don't always agree:

| Ad | HarrisX (perception) | EDO (real action) |
|---|---|---|
| Lay's "Last Harvest" | **#1** of 70 (93.2) | Only 1.2x the median |
| ai.com | Among the bottom 7 | **The most effective ad of the entire event** (9.1x the median) |
| Pringles "Pringleleo" | 22nd overall | 1.8x the median |

The ad people *liked* most wasn't the one that drove the most *action*. This methodological tension — perception vs. behavior — is a real marketing analytics lesson, not a quirk of my analysis.

## The AI finding: how you frame the technology genuinely matters

AI ads split into two clear groups:
- **Concrete use case** (Ring "find your lost pet," Google "buy your home"): averaged **89.3** on HarrisX
- **Technical capability demonstration** (Anthropic): **65.0** — with 42% of the audience reporting confusion about what was being advertised

Difference: +24.3 points. Small sample (n=2 vs. n=1), reported as a case comparison rather than a formal statistical test — but the pattern is consistent with what HarrisX found across all 7 AI ads in the full event.

## Methodology and data honesty

- **HarrisX Ad Index**: a real survey of 9,707 U.S. adults, using a methodology applied to over 1,000 ads historically. Composite score 0-100 across 8 metrics.
- **EDO TV Outcomes**: a real engagement index (digital behavior) relative to the median of all ads at the event.
- For ads without a known exact score (e.g., the "bottom 7" AI ads without an individual breakdown), I didn't invent numbers — I used the documented position (e.g., "67th of 70") instead of fabricating a precise score.
- The NLP analysis (word frequency) was computed independently in Spanish and English — not a translation of the same results, but two separate corpora.

## Project structure

```
adsentiment_portfolio/
├── data/
│   ├── raw/adsentiment_2026_data.py   # verified raw data (HarrisX + EDO)
│   └── processed/                      # clean CSV/JSON + SQLite database
├── sql/
│   ├── 01_schema.sql
│   └── 02_eda_queries.sql              # 6 exploratory analysis queries
├── scripts/
│   ├── 01_clean_transform.py           # cleaning + feature engineering
│   ├── 02_load_db.py                   # load into SQLite
│   ├── 03_run_eda.py                   # runs the SQL queries → JSON
│   ├── 04_nlp_stats_analysis.py        # NLP (CountVectorizer) + AI comparison + correlation
│   ├── 05_translate_exports.py         # translates categories for the EN version
│   └── 06_build_dashboards.py          # injects data + Chart.js into the ES/EN templates
├── lib/
│   ├── chart.umd.min.js
│   └── dashboard_template_i18n.html    # bilingual template
├── docs/
│   ├── index.html                      # ⭐ final product in Spanish
│   └── dashboard_en.html               # ⭐ final product in English
├── README.md                           # this file, in Spanish
└── README.en.md                        # this file, in English
```

## How to reproduce it

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

## Tech stack

`Python` · `pandas` · `scikit-learn` (CountVectorizer for NLP) · `SciPy` (Pearson correlation) · `SQL` · `SQLite` · `HTML/CSS/JS` · `Chart.js`

---

*Data collected and verified from public sources (HarrisX/Stagwell, EDO TV Outcomes, PRNewswire, ALM Corp, Rolling Stone, TVLine, AOL) during February 2026. Super Bowl LX snapshot, February 8, 2026.*
