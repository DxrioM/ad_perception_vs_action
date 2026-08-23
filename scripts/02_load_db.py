"""
Etapa 3 — Carga a SQLite
"""
import sqlite3
import pandas as pd

DB_PATH = "/home/claude/adsentiment_portfolio/data/processed/adsentiment.db"
SCHEMA_PATH = "/home/claude/adsentiment_portfolio/sql/01_schema.sql"
PROC = "/home/claude/adsentiment_portfolio/data/processed/"

ads = pd.read_csv(PROC + "ads_harrisx.csv")
for col in ["tiene_celebridad", "es_ia", "es_proposito_social", "usa_humor"]:
    ads[col] = ads[col].astype(int)
edo = pd.read_csv(PROC + "ads_edo.csv")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
with open(SCHEMA_PATH) as f:
    cur.executescript(f.read())

ads.to_sql("ads_harrisx", conn, if_exists="append", index=False)
edo.to_sql("ads_edo", conn, if_exists="append", index=False)
conn.commit()

for table in ["ads_harrisx", "ads_edo"]:
    n = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"  {table}: {n} filas")
conn.close()
print(f"\nBase de datos creada en: {DB_PATH}")
