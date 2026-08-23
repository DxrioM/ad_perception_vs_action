"""
Etapa 1 — Datos crudos: Recepcion de Audiencia de los Anuncios del Super Bowl LX
====================================================================================
Fuentes: HarrisX Ad Index (encuesta real a 9,707 adultos de EE.UU., PRNewswire /
ALM Corp / HarrisX.com / Morningstar, todas republicando el mismo comunicado
oficial de HarrisX, feb 2026), EDO TV Outcomes (Engagement Index, edo.com),
Rolling Stone, TVLine, AOL, ScreenRant, Billboard, Tom's Guide, HipHopWired,
Mashed (cobertura editorial, feb 2026).

HarrisX Ad Index: score compuesto 0-100 sobre 8 metricas (atractivo,
credibilidad, claridad, memorabilidad, intencion de compartir, comparabilidad,
impacto en reputacion, llamado a la accion). Metodologia de encuesta -- mide
PERCEPCION/COMPRENSION.

EDO Engagement Index: indice de engagement real (busquedas de marca, visitas
web, descargas de apps) relativo a la mediana de todos los anuncios del
Super Bowl (mediana = 100). Metodologia de comportamiento digital real -- mide
ACCION, no percepcion. Los dos sistemas a veces coinciden y a veces divergen
fuertemente (ver notas en cada anuncio).
"""

# ============================================================
# ANUNCIOS con score real de HarrisX (0-100) — donde se conoce
# ============================================================
# (marca, nombre_anuncio, categoria, harrisx_score, harrisx_rank,
#  tiene_celebridad, es_ia, marco_ia, es_proposito_social, usa_humor, nota)
ADS_HARRISX = [
    ("Lay's", "Last Harvest", "Comida y Bebida", 93.2, 1, False, False, None, False, False,
     "Historia multigeneracional de una familia agricultora, sin celebridades ni comedia, dirigida por Taika Waititi. 92% le gustó, 90% la recordó, 71% dijo que los hizo más propensos a comprar.",
     "A multigenerational story about a farming family, no celebrities or comedy, directed by Taika Waititi. 92% liked it, 90% remembered it, 71% said it made them more likely to buy."),
    ("Ring", "Be a Hero in Your Neighborhood", "Tecnología / IA", 91.8, 2, True, True, "caso_de_uso", False, False,
     "Debut de Ring con su función de IA 'Search Party' para encontrar mascotas perdidas, mostrada a través de un problema humano concreto, no la tecnología en abstracto.",
     "Ring's debut featuring its 'Search Party' AI feature for finding lost pets, shown through a concrete human problem rather than the technology in the abstract."),
    ("Pepsi", "The Choice", "Comida y Bebida", 87.2, 3, False, False, None, False, True,
     "Un oso polar (referencia visual al oso de Coca-Cola) hace una prueba a ciegas y elige Pepsi, luego lidia con la disonancia en el diván de un psiquiatra. El anuncio más mencionado en redes.",
     "A polar bear (a visual reference to the Coca-Cola bear) takes a blind taste test and picks Pepsi, then deals with the fallout on a psychiatrist's couch. The most-mentioned ad on social media."),
    ("Google", "New Home", "Tecnología / IA", 86.8, 4, False, True, "caso_de_uso", False, False,
     "Gemini de Google mostrado durante el proceso estresante de comprar una casa, ancla la IA a un momento de vida universalmente entendido.",
     "Google's Gemini shown during the stressful process of buying a home, anchoring AI to a universally understood life moment."),
    ("Blue Square Alliance Against Hate", "Sticky Note", "Causa Social", 85.4, 5, False, False, None, True, False,
     "Fundada por el dueño de los Patriots, aborda el antisemitismo con una nota adhesiva y una estadística real sobre adolescentes judíos.",
     "Founded by the Patriots' owner, addresses antisemitism through a sticky note and a real statistic about Jewish teens."),
    ("Dove", "The Game Is Ours", "Belleza y Cuidado Personal", 85.0, 6, False, False, None, True, False,
     "Enfocado en la participación de niñas en el deporte, extiende la plataforma de propósito de Dove sobre confianza corporal.",
     "Focused on girls' participation in sports, extending Dove's long-running purpose platform around body confidence."),
    ("Novartis", "Relax Your Tight End", "Salud y Bienestar", 83.8, 7, True, False, None, True, True,
     "Segundo año consecutivo en el Top 10. Usa humor con temática de fútbol americano para promover el examen de próstata.",
     "Second consecutive Top 10 finish. Uses football-themed humor to promote prostate cancer screening."),
    ("Budweiser", "American Icons", "Comida y Bebida", 83.6, 8, False, False, None, False, False,
     "150 aniversario, Clydesdales junto a un águila calva, con 'Free Bird' de Lynyrd Skynyrd. Ganó el AdMeter de USA Today (#1) pero quedó 8vo en HarrisX.",
     "150th anniversary spot pairing the Clydesdales with a bald eagle, set to Lynyrd Skynyrd's 'Free Bird.' Won USA Today's AdMeter (#1) but placed 8th in HarrisX."),
    ("Xfinity", "Jurassic Park...Works", "Tecnología / IA", 82.5, 9, False, False, None, False, True,
     "Usa la nostalgia de Jurassic Park para argumentar confiabilidad de red.",
     "Uses Jurassic Park nostalgia to make a network-reliability argument."),
    ("NFL", "You Are Special", "Causa Social", 82.0, 10, False, False, None, True, False,
     "Segundo año consecutivo en el Top 10. Enfocado en participación juvenil y mentoría comunitaria.",
     "Second consecutive Top 10 finish. Focused on youth participation and community mentorship."),
    ("Pringles", "Pringleleo", "Comida y Bebida", 78.5, 22, True, False, None, False, True,
     "Sabrina Carpenter construye a su hombre ideal con Pringles. #1 entre Gen Z (94.8) pero solo 22vo en general — la mayor divergencia generacional del año.",
     "Sabrina Carpenter builds her ideal man out of Pringles chips. #1 with Gen Z (94.8) but only 22nd overall — the year's biggest generational divergence."),
    ("MAHA Center Inc.", "Health Awareness", "Causa Social", 75.1, 31, True, False, None, True, False,
     "Con Mike Tyson. 74% de aprobación general, con solo 12 puntos de diferencia entre republicanos y demócratas.",
     "Featuring Mike Tyson. 74% overall approval, with only a 12-point gap between Republicans and Democrats."),
    ("State Farm", "Stop Livin' on a Prayer", "Seguros", 75.0, 34, True, False, None, False, True,
     "Formato con múltiples celebridades (Bon Jovi, Hailee Steinfeld, KATSEYE) apuntando a un competidor. Score estimado medio-70s.",
     "Multi-celebrity format (Bon Jovi, Hailee Steinfeld, KATSEYE) aimed at a competitor. Estimated score in the mid-70s."),
    ("Invest America", "Trump Accounts", "Finanzas", 70.1, 44, False, False, None, True, False,
     "Promueve cuentas de inversión infantil. 75% de aprobación general, con 15 puntos de diferencia entre partidos.",
     "Promotes children's investment accounts. 75% overall approval, with a 15-point gap between parties."),
    ("Anthropic", "Can I Get a Six Pack Quickly?", "Tecnología / IA", 65.0, 67, False, True, "capacidad", False, False,
     "42% de la audiencia reportó confusión sobre qué se estaba anunciando. Enfatizó la capacidad técnica de Claude en vez de un caso de uso claro. Score estimado con base en su posición (puesto 67 de 70).",
     "42% of the audience reported confusion about what was being advertised. Emphasized Claude's technical capability rather than a clear use case. Score estimated from its position (67th of 70)."),
]

# ============================================================
# EDO Engagement Index — multiplicador vs. mediana (100 = mediana)
# donde se conoce. Sirve para contrastar con HarrisX (percepcion vs. accion real)
# ============================================================
# (marca, nombre_anuncio, edo_index, nota)
ADS_EDO = [
    ("ai.com", "ai.com Ad", 910, "El anuncio más efectivo de TODO el Super Bowl LX según EDO — 9.1x el engagement de la mediana. Contradice directamente su posición en el fondo de HarrisX."),
    ("Lay's", "Free Chips QR", 710, "Segundo anuncio de Lay's (oferta de chips gratis vía QR), no 'Last Harvest'. 7.1x de engagement."),
    ("Dunkin'", "Good Will Dunkin'", 500, "Parodia de 'Good Will Hunting' con Ben Affleck y elenco de sitcoms clásicas. 5x de engagement."),
    ("Liquid Death", "Liquid Death Ad", 220, "2.2x de engagement, fuerte para una marca de bebida saludable."),
    ("Novo Nordisk", "Wegovy GLP-1", 370, "Ganador de la categoría farmacéutica con 3.7x de engagement."),
    ("T-Mobile", "Backstreet Boys", 250, "Número musical con Backstreet Boys. 2.5x de engagement."),
    ("Pringles", "Pringleleo", 180, "1.8x de engagement — consistente con su fuerte desempeño en Gen Z."),
    ("Xfinity", "Jurassic Park...Works", 130, "1.3x de engagement."),
    ("Lay's", "Last Harvest", 120, "El ganador #1 de HarrisX (percepción) solo generó 1.2x en EDO (acción real) — la divergencia más notable entre ambos sistemas."),
]

CONTEXT_FACTS = {
    "fecha_evento": "2026-02-08",
    "sede": "Levi's Stadium, Santa Clara, California",
    "peak_viewers_millones": 137.8,
    "total_ads_evaluados_harrisx": 70,
    "muestra_harrisx": 9707,
    "respuestas_por_anuncio_harrisx": 500,
    "top5_avg_harrisx": 88.9,
    "bottom5_avg_harrisx": 62.0,
    "num_ads_ia": 7,
    "num_ads_ia_bottom7": 5,
    "narrativa": "HarrisX (percepción/comprensión) y EDO (acción/engagement real) a veces coinciden y a veces divergen fuertemente sobre el mismo anuncio.",
}

if __name__ == "__main__":
    print(f"Anuncios con score HarrisX: {len(ADS_HARRISX)}")
    print(f"Anuncios con indice EDO: {len(ADS_EDO)}")
    ia_ads = [a for a in ADS_HARRISX if a[6]]
    print(f"Anuncios de IA en el dataset HarrisX: {len(ia_ads)}")
    for a in ia_ads:
        print(f"  {a[0]} - {a[3]} - marco: {a[7]}")
