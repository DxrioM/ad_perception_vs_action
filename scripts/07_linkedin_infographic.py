"""
Infografia LinkedIn — Percepcion vs. Accion (Super Bowl LX)
================================================================
Diseño 90% visual: minimo texto, maximo protagonismo de graficos.
El contraste HarrisX (percepcion) vs EDO (accion real) se representa
con TAMAÑO de los elementos visuales -- no solo numeros -- para que
la contradiccion se sienta de un vistazo.
"""
import cairosvg
import json
import os
import math
import textwrap
from xml.sax.saxutils import escape as xml_escape

PROC = "/home/claude/adsentiment_portfolio/data/processed/"
OUT = "/home/claude/adsentiment_portfolio/assets_linkedin"
os.makedirs(OUT, exist_ok=True)

P = {
    "bg": "#0F1115", "card": "#171A20", "card2": "#1D212A", "border": "#262B34",
    "text": "#F3F4F6", "text2": "#98A0AC", "text3": "#656D79",
    "harrisx": "#FF7A59", "edo": "#3FC9E0", "gold": "#E8B84F",
    "green": "#4CAF6D", "red": "#E0524A",
}

def esc(s):
    return xml_escape(str(s))

def wrap_tspans(text, x, width, font_size, dy_mult=1.3, anchor=None):
    wrapped = textwrap.wrap(esc(text), width=width)
    attrs = f' text-anchor="{anchor}"' if anchor else ''
    lines = "".join(f'<tspan x="{x}" dy="{0 if i==0 else font_size*dy_mult}"{attrs}>{ln}</tspan>' for i, ln in enumerate(wrapped))
    return lines, len(wrapped)

def circle_metric(cx, cy, max_r, value, max_val, color, label_lines, value_label):
    """Circulo cuyo TAMAÑO representa la magnitud -- el elemento central del contraste."""
    r = max(18, (value/max_val) * max_r)
    svg = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="0.9"/>'
    svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="2" opacity="0.4"/>'
    fsize = min(26, max(13, r*0.32))
    svg += f'<text x="{cx}" y="{cy+fsize*0.35}" font-family="DejaVu Sans Mono" font-size="{fsize:.0f}" font-weight="bold" fill="{P["bg"]}" text-anchor="middle">{value_label}</text>'
    return svg, r

def bar_pair(x, y, w, h, val1, label1, color1, val2, label2, color2, max_val):
    svg = ""
    bw = (w - 20) / 2
    h1 = max(6, (val1/max_val)*h)
    h2 = max(6, (val2/max_val)*h)
    svg += f'<rect x="{x}" y="{y+h-h1}" width="{bw}" height="{h1}" rx="6" fill="{color1}"/>'
    svg += f'<text x="{x+bw/2}" y="{y+h-h1-12}" font-family="DejaVu Sans Mono" font-size="20" font-weight="bold" fill="{P["text"]}" text-anchor="middle">{label1}</text>'
    svg += f'<rect x="{x+bw+20}" y="{y+h-h2}" width="{bw}" height="{h2}" rx="6" fill="{color2}"/>'
    svg += f'<text x="{x+bw+20+bw/2}" y="{y+h-h2-12}" font-family="DejaVu Sans Mono" font-size="20" font-weight="bold" fill="{P["text"]}" text-anchor="middle">{label2}</text>'
    return svg

def build_svg(lang):
    if lang == "es":
        title1, title2 = "Gustar", "≠ Funcionar"
        subtitle = "70 anuncios del Super Bowl LX · percepción (HarrisX) vs. acción real (EDO)"
        s1_eyebrow = "LA CONTRADICCIÓN CENTRAL"
        header_eyebrow = "PORTAFOLIO DE DATA SCIENCE · MARKETING ANALYTICS"
        s1_left_name, s1_right_name = "LAY'S", "AI.COM"
        s1_left_sub, s1_right_sub = '"Last Harvest" — #1 en percepción', "Entre los 7 peor percibidos"
        s1_left_lbl1, s1_left_lbl2 = "HarrisX: #1 (93.2/100)", "EDO: solo 1.2x"
        s1_right_lbl1, s1_right_lbl2 = "HarrisX: bottom 7", "EDO: 9.1x — el más alto de TODOS"
        s1_caption = "El círculo grande = más acción real. Lay's ganó el gusto de la gente; ai.com ganó su comportamiento."
        s2_eyebrow = "CÓMO ENMARCAS LA IA, IMPORTA"
        s2_label1, s2_label2 = "Caso de uso\n(Ring, Google)", "Capacidad técnica\n(Anthropic)"
        s2_caption = "+24.3 puntos de diferencia por una sola decisión de storytelling. 42% de la audiencia terminó confundida con el anuncio de capacidad técnica."
        s3_eyebrow = "DOS PÚBLICOS, DOS SUPER BOWLS"
        s3_labels = ["Lay's\nGeneral", "Lay's\nGen Z", "Pringles\nGeneral", "Pringles\nGen Z"]
        s3_caption = "Pringles fue 22vo en el ranking general — pero #1 indiscutible entre Gen Z."
        kpi_labels = ["PERSONAS ENCUESTADAS", "ANUNCIOS EVALUADOS", "SCORE MÁS ALTO", "MEJOR ENGAGEMENT REAL"]
        cta = "Explora el dashboard interactivo + código completo"
        cta2 = "link en el post · ES / EN"
        footer = "Datos reales: HarrisX Ad Index (encuesta) y EDO TV Outcomes (engagement) · Super Bowl LX, 8 feb 2026"
    else:
        title1, title2 = "Liking", "≠ Working"
        subtitle = "70 Super Bowl LX ads · perception (HarrisX) vs. real action (EDO)"
        s1_eyebrow = "THE CORE CONTRADICTION"
        header_eyebrow = "DATA SCIENCE PORTFOLIO · MARKETING ANALYTICS"
        s1_left_name, s1_right_name = "LAY'S", "AI.COM"
        s1_left_sub, s1_right_sub = '"Last Harvest" — #1 in perception', "Among the 7 worst-perceived"
        s1_left_lbl1, s1_left_lbl2 = "HarrisX: #1 (93.2/100)", "EDO: only 1.2x"
        s1_right_lbl1, s1_right_lbl2 = "HarrisX: bottom 7", "EDO: 9.1x — the highest of ALL"
        s1_caption = "The bigger circle = more real action. Lay's won people's liking; ai.com won their behavior."
        s2_eyebrow = "HOW YOU FRAME AI MATTERS"
        s2_label1, s2_label2 = "Use case\n(Ring, Google)", "Technical capability\n(Anthropic)"
        s2_caption = "+24.3 point difference from a single storytelling decision. 42% of the audience ended up confused by the capability-focused ad."
        s3_eyebrow = "TWO AUDIENCES, TWO SUPER BOWLS"
        s3_labels = ["Lay's\nOverall", "Lay's\nGen Z", "Pringles\nOverall", "Pringles\nGen Z"]
        s3_caption = "Pringles ranked 22nd overall — but was the undisputed #1 with Gen Z."
        kpi_labels = ["PEOPLE SURVEYED", "ADS EVALUATED", "HIGHEST SCORE", "BEST REAL ENGAGEMENT"]
        cta = "Explore the interactive dashboard + full code"
        cta2 = "link in the post · ES / EN"
        footer = "Real data: HarrisX Ad Index (survey) and EDO TV Outcomes (engagement) · Super Bowl LX, Feb 8 2026"

    W = 1200
    svg_parts = [f'<rect width="{W}" height="__H__" fill="{P["bg"]}"/>']

    # ---------- HEADER (minimo texto) ----------
    y = 56
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans Mono" font-size="14" font-weight="bold" letter-spacing="1.5" fill="{P["gold"]}">{esc(header_eyebrow)}</text>')
    y += 56
    svg_parts.append(f'<text x="66" y="{y}" font-family="DejaVu Sans" font-size="46" font-weight="bold" fill="{P["harrisx"]}">{esc(title1)} </text>')
    tw = len(title1)*28
    svg_parts.append(f'<text x="{66+tw}" y="{y}" font-family="DejaVu Sans" font-size="46" font-weight="bold" fill="{P["text"]}">{esc(title2)}</text>')
    y += 32
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans" font-size="15" fill="{P["text2"]}">{esc(subtitle)}</text>')
    y += 34

    # ---------- KPI ROW (compacta) ----------
    kpi_vals = ["9,707", "70", "93.2", "9.1x"]
    kpi_colors = [P["text"], P["text"], P["harrisx"], P["edo"]]
    kpi_w = (W-140-3*14)/4
    for i in range(4):
        x0 = 70 + i*(kpi_w+14)
        svg_parts.append(f'<rect x="{x0}" y="{y}" width="{kpi_w}" height="66" rx="10" fill="{P["card"]}" stroke="{P["border"]}"/>')
        svg_parts.append(f'<text x="{x0+16}" y="{y+32}" font-family="DejaVu Sans Mono" font-size="21" font-weight="bold" fill="{kpi_colors[i]}">{kpi_vals[i]}</text>')
        lbl_lines, _ = wrap_tspans(kpi_labels[i], x0+16, 26, 9.5)
        svg_parts.append(f'<text x="{x0+16}" y="{y+50}" font-family="DejaVu Sans" font-size="9.5" font-weight="bold" fill="{P["text2"]}">{lbl_lines}</text>')
    y += 66 + 36

    # ============ SECCION 1: EL CONTRASTE (elemento mas grande y protagonico) ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans Mono" font-size="15" font-weight="bold" letter-spacing="1.2" fill="{P["gold"]}">{esc(s1_eyebrow)}</text>')
    y += 26
    s1_h = 420
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s1_h}" rx="16" fill="{P["card"]}" stroke="{P["border"]}"/>')
    mid_x = W/2
    svg_parts.append(f'<line x1="{mid_x}" y1="{y+30}" x2="{mid_x}" y2="{y+s1_h-70}" stroke="{P["border"]}" stroke-width="1"/>')

    # LAY'S (izquierda): circulo HarrisX grande, circulo EDO chico
    lx_cx = 70 + (W-140)/4
    svg_parts.append(f'<text x="{lx_cx}" y="{y+45}" font-family="DejaVu Sans" font-size="24" font-weight="bold" fill="{P["text"]}" text-anchor="middle">{esc(s1_left_name)}</text>')
    svg_parts.append(f'<text x="{lx_cx}" y="{y+68}" font-family="DejaVu Sans" font-size="13" fill="{P["text2"]}" text-anchor="middle">{esc(s1_left_sub)}</text>')
    c1, r1 = circle_metric(lx_cx-70, y+220, 95, 93.2, 100, P["harrisx"], [], "93.2")
    svg_parts.append(c1)
    c2, r2 = circle_metric(lx_cx+90, y+220, 95, 12, 100, P["edo"], [], "1.2x")
    svg_parts.append(c2)
    svg_parts.append(f'<text x="{lx_cx}" y="{y+s1_h-95}" font-family="DejaVu Sans Mono" font-size="14" fill="{P["harrisx"]}" text-anchor="middle">{esc(s1_left_lbl1)}</text>')
    svg_parts.append(f'<text x="{lx_cx}" y="{y+s1_h-75}" font-family="DejaVu Sans Mono" font-size="14" fill="{P["edo"]}" text-anchor="middle">{esc(s1_left_lbl2)}</text>')

    # AI.COM (derecha): circulo HarrisX chico, circulo EDO grande
    rx_cx = mid_x + (W-140)/4
    svg_parts.append(f'<text x="{rx_cx}" y="{y+45}" font-family="DejaVu Sans" font-size="24" font-weight="bold" fill="{P["text"]}" text-anchor="middle">{esc(s1_right_name)}</text>')
    svg_parts.append(f'<text x="{rx_cx}" y="{y+68}" font-family="DejaVu Sans" font-size="13" fill="{P["text2"]}" text-anchor="middle">{esc(s1_right_sub)}</text>')
    c3, r3 = circle_metric(rx_cx-90, y+220, 95, 62, 100, P["harrisx"], [], "62")
    svg_parts.append(c3)
    c4, r4 = circle_metric(rx_cx+70, y+220, 95, 91, 100, P["edo"], [], "9.1x")
    svg_parts.append(c4)
    svg_parts.append(f'<text x="{rx_cx}" y="{y+s1_h-95}" font-family="DejaVu Sans Mono" font-size="14" fill="{P["harrisx"]}" text-anchor="middle">{esc(s1_right_lbl1)}</text>')
    svg_parts.append(f'<text x="{rx_cx}" y="{y+s1_h-75}" font-family="DejaVu Sans Mono" font-size="14" fill="{P["edo"]}" text-anchor="middle">{esc(s1_right_lbl2)}</text>')

    cap_lines, ncap = wrap_tspans(s1_caption, mid_x, 84, 13, anchor="middle")
    svg_parts.append(f'<text x="{mid_x}" y="{y+s1_h-30}" font-family="DejaVu Sans" font-size="13" fill="{P["text2"]}" text-anchor="middle">{cap_lines}</text>')
    y += s1_h + 36

    # ============ SECCION 2: IA — caso de uso vs capacidad ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans Mono" font-size="15" font-weight="bold" letter-spacing="1.2" fill="{P["gold"]}">{esc(s2_eyebrow)}</text>')
    y += 26
    s2_h = 230
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s2_h}" rx="16" fill="{P["card"]}" stroke="{P["border"]}"/>')
    bar_h = 110
    svg_parts.append(bar_pair(70+60, y+30, W-140-120, bar_h, 89.3, "89.3", P["green"], 65.0, "65.0", P["red"], 100))
    l1a, l1b = s2_label1.split("\n"); l2a, l2b = s2_label2.split("\n")
    bw2 = (W-140-120-20)/2
    lx0 = 70+60
    svg_parts.append(f'<text x="{lx0+bw2/2}" y="{y+30+bar_h+26}" font-family="DejaVu Sans" font-size="14" font-weight="bold" fill="{P["text"]}" text-anchor="middle">{esc(l1a)}</text>')
    svg_parts.append(f'<text x="{lx0+bw2/2}" y="{y+30+bar_h+44}" font-family="DejaVu Sans" font-size="12" fill="{P["text2"]}" text-anchor="middle">{esc(l1b)}</text>')
    svg_parts.append(f'<text x="{lx0+bw2+20+bw2/2}" y="{y+30+bar_h+26}" font-family="DejaVu Sans" font-size="14" font-weight="bold" fill="{P["text"]}" text-anchor="middle">{esc(l2a)}</text>')
    svg_parts.append(f'<text x="{lx0+bw2+20+bw2/2}" y="{y+30+bar_h+44}" font-family="DejaVu Sans" font-size="12" fill="{P["text2"]}" text-anchor="middle">{esc(l2b)}</text>')
    cap2_lines, _ = wrap_tspans(s2_caption, mid_x, 92, 12.5, anchor="middle")
    svg_parts.append(f'<text x="{mid_x}" y="{y+s2_h-16}" font-family="DejaVu Sans" font-size="12.5" fill="{P["text2"]}" text-anchor="middle">{cap2_lines}</text>')
    y += s2_h + 36

    # ============ SECCION 3: GEN Z ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans Mono" font-size="15" font-weight="bold" letter-spacing="1.2" fill="{P["gold"]}">{esc(s3_eyebrow)}</text>')
    y += 26
    s3_h = 240
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s3_h}" rx="16" fill="{P["card"]}" stroke="{P["border"]}"/>')
    genz_vals = [93.2, 91.0, 78.5, 94.8]
    genz_colors = [P["harrisx"], "#8a5546", P["edo"], "#2d6e79"]
    bar_area_w = W-140-100
    bw3 = bar_area_w/4 * 0.55
    gap3 = bar_area_w/4
    bar_top = y+26
    bar_max_h = 130
    for i, v in enumerate(genz_vals):
        bx = 70+50 + i*gap3 + (gap3-bw3)/2
        bh = (v/100)*bar_max_h
        svg_parts.append(f'<rect x="{bx}" y="{bar_top+bar_max_h-bh}" width="{bw3}" height="{bh}" rx="6" fill="{genz_colors[i]}"/>')
        svg_parts.append(f'<text x="{bx+bw3/2}" y="{bar_top+bar_max_h-bh-10}" font-family="DejaVu Sans Mono" font-size="15" font-weight="bold" fill="{P["text"]}" text-anchor="middle">{v}</text>')
        la, lb = s3_labels[i].split("\n")
        svg_parts.append(f'<text x="{bx+bw3/2}" y="{bar_top+bar_max_h+22}" font-family="DejaVu Sans" font-size="12.5" font-weight="bold" fill="{P["text"]}" text-anchor="middle">{esc(la)}</text>')
        svg_parts.append(f'<text x="{bx+bw3/2}" y="{bar_top+bar_max_h+38}" font-family="DejaVu Sans" font-size="11" fill="{P["text2"]}" text-anchor="middle">{esc(lb)}</text>')
    cap3_lines, _ = wrap_tspans(s3_caption, mid_x, 88, 13, anchor="middle")
    svg_parts.append(f'<text x="{mid_x}" y="{y+s3_h-18}" font-family="DejaVu Sans" font-size="13" fill="{P["text2"]}" text-anchor="middle">{cap3_lines}</text>')
    y += s3_h + 36

    # ---------- CTA ----------
    cta_h = 66
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{cta_h}" rx="14" fill="{P["gold"]}"/>')
    svg_parts.append(f'<text x="100" y="{y+cta_h/2+6}" font-family="DejaVu Sans" font-size="16" font-weight="bold" fill="{P["bg"]}">{esc(cta)}</text>')
    svg_parts.append(f'<text x="{W-100}" y="{y+cta_h/2+5}" font-family="DejaVu Sans Mono" font-size="12.5" fill="{P["bg"]}" text-anchor="end">{esc(cta2)}</text>')
    y += cta_h + 30

    svg_parts.append(f'<text x="{mid_x}" y="{y}" font-family="DejaVu Sans Mono" font-size="11" fill="{P["text3"]}" text-anchor="middle">{esc(footer)}</text>')
    y += 34

    H = int(y)
    svg = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">' + "".join(svg_parts).replace("__H__", str(H)) + '</svg>'
    return svg, W, H

for lang in ["es", "en"]:
    svg_code, W, H = build_svg(lang)
    print(f"{lang}: {W}x{H}")
    svg_path = f"{OUT}/linkedin_infographic_{lang}.svg"
    png_path = f"{OUT}/linkedin_infographic_{lang}.png"
    open(svg_path, "w", encoding="utf-8").write(svg_code)
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=W, output_height=H)
    print(f"Generado: {png_path}")
