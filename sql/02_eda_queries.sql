-- ============================================================
-- Análisis Exploratorio — Recepción de Anuncios Super Bowl LX
-- ============================================================

-- 1. Ranking completo por score HarrisX
SELECT harrisx_rank, marca, nombre_anuncio, categoria, harrisx_score, tier
FROM ads_harrisx
ORDER BY harrisx_score DESC;

-- 2. Score promedio por categoría
SELECT categoria, COUNT(*) AS num_anuncios, ROUND(AVG(harrisx_score),1) AS score_promedio
FROM ads_harrisx
GROUP BY categoria
ORDER BY score_promedio DESC;

-- 3. Anuncios de IA: marco de comunicación vs. score
SELECT marca, nombre_anuncio, marco_ia, harrisx_score, harrisx_rank
FROM ads_harrisx
WHERE es_ia = 1
ORDER BY harrisx_score DESC;

-- 4. Impacto de cada atributo (celebridad, propósito social, humor) en el score
SELECT 'Con celebridad' AS atributo, ROUND(AVG(harrisx_score),1) AS score_promedio, COUNT(*) AS n
FROM ads_harrisx WHERE tiene_celebridad = 1
UNION ALL
SELECT 'Sin celebridad', ROUND(AVG(harrisx_score),1), COUNT(*) FROM ads_harrisx WHERE tiene_celebridad = 0
UNION ALL
SELECT 'Con propósito social', ROUND(AVG(harrisx_score),1), COUNT(*) FROM ads_harrisx WHERE es_proposito_social = 1
UNION ALL
SELECT 'Sin propósito social', ROUND(AVG(harrisx_score),1), COUNT(*) FROM ads_harrisx WHERE es_proposito_social = 0
UNION ALL
SELECT 'Con humor', ROUND(AVG(harrisx_score),1), COUNT(*) FROM ads_harrisx WHERE usa_humor = 1
UNION ALL
SELECT 'Sin humor', ROUND(AVG(harrisx_score),1), COUNT(*) FROM ads_harrisx WHERE usa_humor = 0;

-- 5. HarrisX (percepción) vs. EDO (acción real): los mismos anuncios en ambos sistemas
SELECT h.marca, h.nombre_anuncio, h.harrisx_score, h.harrisx_rank, e.edo_index
FROM ads_harrisx h
JOIN ads_edo e ON h.marca = e.marca AND h.nombre_anuncio = e.nombre_anuncio
ORDER BY h.harrisx_rank;

-- 6. Todos los anuncios EDO (incluyendo los que no tienen score HarrisX conocido)
SELECT marca, nombre_anuncio, edo_index FROM ads_edo ORDER BY edo_index DESC;
