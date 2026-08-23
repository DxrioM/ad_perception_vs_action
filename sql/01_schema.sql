-- ============================================================
-- Esquema — Recepción de Audiencia: Anuncios del Super Bowl LX
-- ============================================================
DROP TABLE IF EXISTS ads_harrisx;
DROP TABLE IF EXISTS ads_edo;

CREATE TABLE ads_harrisx (
    marca               TEXT NOT NULL,
    nombre_anuncio      TEXT NOT NULL,
    categoria           TEXT NOT NULL,
    harrisx_score       REAL NOT NULL,
    harrisx_rank        INTEGER NOT NULL,
    tiene_celebridad    INTEGER NOT NULL,
    es_ia               INTEGER NOT NULL,
    marco_ia            TEXT,
    es_proposito_social INTEGER NOT NULL,
    usa_humor           INTEGER NOT NULL,
    descripcion         TEXT,
    descripcion_en      TEXT,
    tier                TEXT,
    num_atributos       INTEGER,
    PRIMARY KEY (marca, nombre_anuncio)
);

CREATE TABLE ads_edo (
    marca       TEXT NOT NULL,
    nombre_anuncio TEXT NOT NULL,
    edo_index   REAL NOT NULL,
    nota_edo    TEXT,
    PRIMARY KEY (marca, nombre_anuncio)
);

CREATE INDEX idx_harrisx_categoria ON ads_harrisx(categoria);
