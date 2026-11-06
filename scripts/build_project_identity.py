#!/usr/bin/env python3
"""Build self-contained profile cards with project-specific vector artwork."""
from pathlib import Path
from html import escape
import re
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/projects'


def mascot(name, prefix, x, y, w, h):
    source = (OUT / 'source' / name).read_text()
    for ident in re.findall(r'\bid="([^"]+)"', source):
        source = source.replace(f'"{ident}"', f'"{prefix}-{ident}"').replace(f'#{ident})', f'#{prefix}-{ident})')
        source = re.sub(r'(?<=aria-labelledby=")([^\"]+)', lambda m: m[0].replace(ident, f'{prefix}-{ident}'), source)
    # Root dimensions only; preserve every original drawing coordinate.
    root_end = source.index('>')
    opening = re.sub(r'\s(?:width|height)="[^"]*"', '', source[:root_end])
    return opening + f' x="{x}" y="{y}" width="{w}" height="{h}">' + source[root_end+1:]


def art(kind):
    """100 × 100 thematic drawings, not official logos."""
    if kind == 'doctor':
        return '''<rect x="38" y="8" width="53" height="71" rx="8" fill="#EEF6FF" stroke="#60A5FA" stroke-width="3"/>
<rect x="52" y="3" width="25" height="13" rx="5" fill="#60A5FA"/>
<path d="M49 30h29 M49 40h20 M49 50h25" stroke="#91A7C1" stroke-width="3" stroke-linecap="round"/>
<path d="M12 15v19c0 23 29 23 29 0V15 M26 53v18c0 23 44 22 44 0v-7" fill="none" stroke="#22D3A6" stroke-width="6" stroke-linecap="round"/>
<path d="M12 13v9 M41 13v9" stroke="#60A5FA" stroke-width="8" stroke-linecap="round"/>
<circle cx="70" cy="64" r="11" fill="#0B1020" stroke="#22D3A6" stroke-width="4"/><circle cx="70" cy="64" r="4" fill="#A7F3D0"/>'''
    if kind == 'skills':
        return '''<rect x="21" y="8" width="60" height="73" rx="7" fill="#263A62" transform="rotate(9 50 50)"/>
<rect x="12" y="15" width="62" height="75" rx="7" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2"/>
<path d="M12 22q0-7 7-7h48q7 0 7 7v24H12Z" fill="#E85D6C"/>
<path d="M12 22q0-7 7-7h19v31H12Z" fill="#3B65B3"/>
<path d="m25 22 2.5 6 6.5.5-5 4 1.5 6-5.5-3.5-5.5 3.5 1.5-6-5-4 6.5-.5Z" fill="#fff"/>
<path d="m24 60-7 6 7 6 M60 60l7 6-7 6 M46 57l-7 18" fill="none" stroke="#334155" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'''
    if kind == 'io':
        return '''<defs><linearGradient id="io-monogram-accent" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#67e8f9"/><stop offset="1" stop-color="#a78bfa"/></linearGradient></defs>
<circle cx="50" cy="50" r="48" fill="#0b1b30" stroke="#2b3f5f" stroke-width="2"/>
<circle cx="50" cy="50" r="34" fill="none" stroke="url(#io-monogram-accent)" stroke-width="3"/>
<text x="50" y="62" text-anchor="middle" fill="#f8fafc" font-family="system-ui,sans-serif" font-size="34" font-weight="800" letter-spacing="4">IO</text>'''
    if kind == 'eauto':
        return '''<path d="M9 18h12l9 43h45l12-32H25" fill="#203553" stroke="#60A5FA" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M32 49h40 M44 31v19 M62 31v19" fill="none" stroke="#60A5FA" stroke-width="2"/>
<circle cx="37" cy="77" r="7" fill="#60A5FA"/><circle cx="72" cy="77" r="7" fill="#60A5FA"/>
<path d="M70 7 90 14v17c0 13-20 23-20 23S50 44 50 31V14Z" fill="#0B1020" stroke="#22D3A6" stroke-width="3"/>
<path d="m60 29 7 7 14-16" fill="none" stroke="#22D3A6" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'''
    if kind == 'zanax':
        return '''<path d="M51 10v14" stroke="#FBBF24" stroke-width="4" stroke-linecap="round"/><circle cx="51" cy="9" r="5" fill="#FBBF24"/>
<circle cx="45" cy="49" r="28" fill="#0B1020" stroke="#60A5FA" stroke-width="4"/>
<rect x="31" y="40" width="9" height="9" rx="2" fill="#60A5FA"/><rect x="50" y="40" width="9" height="9" rx="2" fill="#60A5FA"/>
<path d="M35 59h19" stroke="#60A5FA" stroke-width="4" stroke-linecap="round"/>
<path d="M88 31C94 69 62 98 28 83C59 84 82 62 88 31Z" fill="#FBBF24" stroke="#D99B14" stroke-width="2" stroke-linejoin="round"/>
<path d="m88 31-2-6 M28 83l-5-2" stroke="#8A6113" stroke-width="4" stroke-linecap="round"/>'''
    raise ValueError(kind)


def card(key, title, kicker, lines, caption, accent, illustration, big=True):
    w,h=(900,240) if big else (560,220)
    x=35 if big else 28
    title_y=110 if big else 82
    text_y=164 if big else 126
    fs=50 if big else 34
    text_size=22 if big else 16
    subtitle_y=198 if big else 169
    artwork=illustration
    descriptions={'panter-ai':'Panter, pantera con rasgos de ratón y cola conectora. ', 'zanallaima':'Zanahoria con lentes, humita azul y lista de cuatro revisiones. ', 'doctor-chile':'Estetoscopio junto a una ficha de investigación. ', 'skills-chile':'Tarjetas de conocimiento con estrella chilena y símbolos de código. ', 'io':'Monograma IO rodeado de un anillo cian y violeta. ', 'eauto-ai':'Carrito de comercio con escudo de aprobación. ', 'zanax':'Robot azul con antena amarilla junto a una banana. '}
    content=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{key}-title {key}-desc">
<title id="{key}-title">{escape(title)}</title>
<desc id="{key}-desc">{escape(descriptions[key]+caption)}</desc>
<style>.card-bg{{fill:#0B1020}}.card-panel{{fill:#111827}}.card-title{{fill:#F8FAFC}}.card-copy{{fill:#E2E8F0}}.card-muted{{fill:#AAB8C8}}.card-border{{stroke:#334155}}@media(prefers-color-scheme:light){{.card-bg{{fill:#F8FAFC}}.card-panel{{fill:#E2E8F0}}.card-title,.card-copy{{fill:#0B1020}}.card-muted{{fill:#475569}}.card-border{{stroke:#CBD5E1}}}}</style>
<rect class="card-bg card-border" x="1" y="1" width="{w-2}" height="{h-2}" rx="22" stroke-width="1"/>
<path d="M{x} {title_y+17}h75" stroke="{accent}" stroke-width="4" stroke-linecap="round"/>
<text x="{x}" y="38" font-family="ui-monospace,Consolas,monospace" font-size="{13 if big else 11}" font-weight="700" fill="{accent}">{escape(kicker)}</text>
<text class="card-title" x="{x}" y="{title_y}" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-weight="800" font-size="{fs}">{escape(title)}</text>
'''
    for i,line in enumerate(lines):
        content+=f'<text class="card-copy" x="{x}" y="{text_y+i*23}" font-family="system-ui,sans-serif" font-size="{text_size}" font-weight="600">{escape(line)}</text>\n'
    content+=f'<text class="card-muted" x="{x}" y="{subtitle_y if big else 199}" font-family="system-ui,sans-serif" font-size="{18 if big else 13}">{escape(caption.split(" · SVG:")[0])}</text>\n'
    content+=artwork+'\n</svg>\n'
    (OUT/f'{key}-identity.svg').write_text(content)

card('panter-ai','PANTER-AI','OPEN SOURCE · MIT',['Un equipo de agentes conectado por MCP'],'Misiones · permisos · evidencia · revisión', '#22D3A6',mascot('panter-mascot.svg','panter-art',682,18,202,202))
card('zanallaima','ZanaLLaima','MCP · EN DESARROLLO',['De ChatGPT al código revisado'],'Rama propia · pruebas · revisión por commit','#22D3A6',mascot('zanallaima-mascot.svg','zana-art',696,10,176,220))
card('doctor-chile','MCP DOCTOR CHILE','BUSCAMOS COLABORACIÓN',['Harness Médico Chile · investigación multiagente'],'Casos sintéticos · revisión clínica · privacidad','#F87171',f'<g transform="translate(695 26) scale(1.9)">{art("doctor")}</g>')
for key,title,kicker,lines,caption,color,kind in [
 ('skills-chile','SKILLS CHILE','CONOCIMIENTO LOCAL',['Conocimiento chileno en skills','reutilizables y verificables.'],'Chile · GRC · open skills','#F87171','skills'),
 ('io','IO','OPERACIÓN AGÉNTICA',['La empresa es la unidad;','el agente es un trabajador.'],'Heartbeat · costos · recibos','#22D3A6','io'),
 ('eauto-ai','EAUTO-AI','COMERCIO CON AUTORIDAD',['Señal → evidencia → aprobación','→ ejecución → resultado.'],'Android · gobernanza · comercio','#60A5FA','eauto'),
 ('zanax','zanaX','INVESTIGACIÓN Y PUBLICACIÓN',['Investigar, redactar y revisar','antes de publicar.'],'X · LangGraph · aprobación humana','#FBBF24','zanax')]:
    card(key,title,kicker,lines,caption,color,f'<g transform="translate(432 20)">{art(kind)}</g>',False)
