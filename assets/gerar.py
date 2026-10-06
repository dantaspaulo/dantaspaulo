#!/usr/bin/env python3
"""Gera os SVG animados do README (cartões de case, números, método e governo).

O README do GitHub não roda JavaScript nem CSS próprio; SVG com @keyframes
servido como <img> anima. Fonte web não carrega dentro de <img>, por isso a
pilha é de sistema (Georgia faz o papel da serifada do site).

Uso: python3 assets/gerar.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

AQUI = Path(__file__).parent

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
SERIF = "Georgia,'Times New Roman',serif"
FUNDO, BORDA, TINTA, SUAVE, APAGADO = "#151310", "#2A2723", "#F1ECE3", "#A39A8A", "#8F8778"
CHAMPAGNE, CLARO, ESCURO = "#D6BD8F", "#E2CDA4", "#8C7148"


def defs(extra=""):
    return f"""<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CLARO}"/><stop offset="1" stop-color="{ESCURO}"/></linearGradient>
<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#F1E3C4" stop-opacity="0"/><stop offset=".5" stop-color="#F1E3C4" stop-opacity=".09"/><stop offset="1" stop-color="#F1E3C4" stop-opacity="0"/></linearGradient>
{extra}</defs>"""


BASE_CSS = f"""
.up{{opacity:0;animation:up .9s cubic-bezier(.2,.7,.2,1) forwards}}
@keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
.run{{stroke-dasharray:9 91;animation:run 7s linear infinite}}
@keyframes run{{to{{stroke-dashoffset:-100}}}}
.shine{{animation:shine 8s ease-in-out infinite}}
@keyframes shine{{0%,72%{{transform:translateX(-420px)}}100%{{transform:translateX(1300px)}}}}
"""


def moldura(w, h, rx=16):
    return f"""<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx}" fill="{FUNDO}" stroke="{BORDA}"/>
<clipPath id="c"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx}"/></clipPath>
<g clip-path="url(#c)"><g class="shine"><rect x="0" y="-20" width="150" height="{h+40}" fill="url(#sh)" transform="skewX(-18)"/></g></g>
<rect class="run" x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx}" fill="none" stroke="url(#g)" stroke-width="1.6" pathLength="100"/>"""


def svg(w, h, titulo, corpo, css):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(titulo)}">
<title>{escape(titulo)}</title>
<style>{BASE_CSS}{css}</style>
{defs()}
{corpo}
</svg>
"""


def cartao(slug, icone, nome, sub, selo, numero, rotulo, rodape, atraso=0.0):
    w, h = 420, 236
    a = lambda s: f'style="animation-delay:{atraso + s:.2f}s"'
    largura_selo = len(selo) * 7.4 + 22
    rotulo_svg = "".join(
        f'<text class="l" x="24" y="{166 + i * 19}">{escape(linha)}</text>' for i, linha in enumerate(rotulo)
    )
    css = f"""
.t{{font:700 21px {SANS};fill:{TINTA}}}
.s{{font:500 13px {SANS};fill:{SUAVE}}}
.p{{font:700 10.5px {SANS};letter-spacing:1.3px;fill:{CHAMPAGNE}}}
.n{{font:400 50px {SERIF};fill:url(#g)}}
.l{{font:500 14px {SANS};fill:#CFC6B6}}
.f{{font:500 12.5px {SANS};fill:{APAGADO}}}
.i{{font:22px 'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif}}
.ln{{stroke-dasharray:100;stroke-dashoffset:100;animation:ln 1.4s ease forwards}}
@keyframes ln{{to{{stroke-dashoffset:0}}}}
"""
    corpo = f"""{moldura(w, h)}
<rect x="22" y="22" width="40" height="40" rx="11" fill="#1F1C18" stroke="{BORDA}"/>
<text class="i" x="42" y="50" text-anchor="middle">{icone}</text>
<text class="t" x="76" y="40">{escape(nome)}</text>
<text class="s" x="76" y="59">{escape(sub)}</text>
<g class="up" {a(0.1)}><text class="n" x="22" y="138">{escape(numero)}</text></g>
<g class="up" {a(0.35)}>{rotulo_svg}</g>
<line class="ln" x1="24" y1="{h - 40}" x2="{w - 24}" y2="{h - 40}" stroke="{BORDA}" pathLength="100" {a(0.5)}/>
<g class="up" {a(0.6)}><text class="f" x="24" y="{h - 17}">{escape(rodape)}</text></g>
<rect x="{w - 22 - largura_selo:.1f}" y="22" width="{largura_selo:.1f}" height="22" rx="11" fill="#1F1C18" stroke="#3A352E"/>
<text class="p" x="{w - 22 - largura_selo / 2:.1f}" y="37" text-anchor="middle">{escape(selo)}</text>"""
    (AQUI / f"case-{slug}.svg").write_text(svg(w, h, f"{nome}: {numero} {' '.join(rotulo)}", corpo, css), encoding="utf-8")


def numeros():
    w, h = 840, 156
    itens = [
        ("1 mi+", ["peças jurídicas", "geradas no ChatADV"]),
        ("−95%", ["custo de nuvem do ChatADV,", "migração em uma semana"]),
        ("8", ["clientes liderados", "como FDE em um mês"]),
        ("20+", ["anos de software,", "10 de advocacia"]),
    ]
    css = f"""
.n{{font:400 48px {SERIF};fill:url(#g)}}
.l{{font:500 13.5px {SANS};fill:#CFC6B6}}
.v{{stroke-dasharray:100;stroke-dashoffset:100;animation:ln 1s ease forwards}}
@keyframes ln{{to{{stroke-dashoffset:0}}}}
"""
    partes = [moldura(w, h, 18)]
    for i, (n, rot) in enumerate(itens):
        cx = 105 + i * 210
        d = 0.15 + i * 0.18
        partes.append(f'<g class="up" style="animation-delay:{d:.2f}s"><text class="n" x="{cx}" y="74" text-anchor="middle">{escape(n)}</text></g>')
        partes.append(
            f'<g class="up" style="animation-delay:{d + 0.2:.2f}s">'
            + "".join(f'<text class="l" x="{cx}" y="{104 + j * 19}" text-anchor="middle">{escape(t)}</text>' for j, t in enumerate(rot))
            + "</g>"
        )
        if i:
            x = cx - 105
            partes.append(f'<line class="v" x1="{x}" y1="34" x2="{x}" y2="{h - 34}" stroke="{BORDA}" pathLength="100" style="animation-delay:{d:.2f}s"/>')
    (AQUI / "numeros.svg").write_text(svg(w, h, "1 mi+ peças, −95% de custo de nuvem, 8 clientes como FDE em um mês, 20+ anos de software", "\n".join(partes), css), encoding="utf-8")


def metodo():
    w, h = 840, 196
    passos = [
        ("Entender", ["a operação,", "o gargalo e o custo"]),
        ("Decompor", ["um caso de alto impacto,", "não dez de baixo"]),
        ("Construir", ["protótipo em semanas,", "software no ar"]),
        ("Medir", ["antes e depois,", "com número"]),
    ]
    xs = [105 + i * 210 for i in range(4)]
    ciclo = 9
    css = [f"""
.k{{font:400 20px {SERIF};fill:{CHAMPAGNE}}}
.t{{font:700 16px {SANS};fill:{TINTA}}}
.s{{font:500 12.5px {SANS};fill:{SUAVE}}}
.trilho{{stroke-dasharray:100;stroke-dashoffset:100;animation:trilho {ciclo}s ease-in-out infinite}}
@keyframes trilho{{0%{{stroke-dashoffset:100;opacity:1}}75%{{stroke-dashoffset:0;opacity:1}}92%{{stroke-dashoffset:0;opacity:1}}100%{{stroke-dashoffset:0;opacity:0}}}}
.ponto{{animation:ponto {ciclo}s ease-in-out infinite}}
@keyframes ponto{{0%{{transform:translateX(0);opacity:1}}75%{{transform:translateX({xs[-1] - xs[0]}px);opacity:1}}92%{{opacity:0}}100%{{transform:translateX(0);opacity:0}}}}
"""]
    partes = [moldura(w, h, 18)]
    partes.append(f'<line x1="{xs[0]}" y1="62" x2="{xs[-1]}" y2="62" stroke="{BORDA}" stroke-width="2"/>')
    partes.append(f'<line class="trilho" x1="{xs[0]}" y1="62" x2="{xs[-1]}" y2="62" stroke="{CHAMPAGNE}" stroke-width="2.4" pathLength="100"/>')
    for i, ((nome, sub), x) in enumerate(zip(passos, xs)):
        p = 25 * i
        css.append(
            f"@keyframes n{i}{{0%,{max(p - 1, 0)}%{{fill:{FUNDO};stroke:#3A352E}}{p + 3}%,90%{{fill:#2A2216;stroke:{CHAMPAGNE}}}100%{{fill:{FUNDO};stroke:#3A352E}}}}"
            f".n{i}{{animation:n{i} {ciclo}s ease infinite}}"
        )
        partes.append(f'<circle class="n{i}" cx="{x}" cy="62" r="22" fill="{FUNDO}" stroke="#3A352E" stroke-width="1.6"/>')
        partes.append(f'<text class="k" x="{x}" y="69" text-anchor="middle">{i + 1}</text>')
        partes.append(
            f'<g class="up" style="animation-delay:{0.15 + i * 0.15:.2f}s"><text class="t" x="{x}" y="120" text-anchor="middle">{escape(nome)}</text>'
            + "".join(f'<text class="s" x="{x}" y="{143 + j * 18}" text-anchor="middle">{escape(t)}</text>' for j, t in enumerate(sub))
            + "</g>"
        )
    partes.append(f'<circle class="ponto" cx="{xs[0]}" cy="62" r="5" fill="{CLARO}"/>')
    (AQUI / "metodo.svg").write_text(svg(w, h, "Entender, decompor, construir, medir", "\n".join(partes), "".join(css)), encoding="utf-8")


def governo():
    w, h = 840, 132
    itens = [("🔐", "Menor", "privilégio"), ("🤐", "Segredo", "isolado"), ("🚦", "Pessoa no", "ponto certo"), ("🧪", "Trava que", "recusa"), ("📋", "Rastro", "de tudo")]
    ciclo = 10
    css = [f"""
.i{{font:24px 'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif}}
.t{{font:700 13.5px {SANS};fill:{TINTA}}}
"""]
    partes = []
    cw, gap, x0 = 148, 15, 22
    for i, (ic, l1, l2) in enumerate(itens):
        x = x0 + i * (cw + gap)
        p = 20 * i
        css.append(
            f"@keyframes c{i}{{0%,{p}%{{stroke:{BORDA};fill:{FUNDO}}}{p + 4}%,{p + 18}%{{stroke:{CHAMPAGNE};fill:#211C15}}{p + 22}%,100%{{stroke:{BORDA};fill:{FUNDO}}}}}"
            f".c{i}{{animation:c{i} {ciclo}s ease infinite}}"
        )
        partes.append(
            f'<g class="up" style="animation-delay:{0.1 + i * 0.12:.2f}s">'
            f'<rect class="c{i}" x="{x}" y="10" width="{cw}" height="{h - 20}" rx="14" fill="{FUNDO}" stroke="{BORDA}" stroke-width="1.4"/>'
            f'<text class="i" x="{x + cw / 2}" y="52" text-anchor="middle">{ic}</text>'
            f'<text class="t" x="{x + cw / 2}" y="80" text-anchor="middle">{escape(l1)}</text>'
            f'<text class="t" x="{x + cw / 2}" y="98" text-anchor="middle">{escape(l2)}</text></g>'
        )
    (AQUI / "governo.svg").write_text(svg(w, h, "Menor privilégio, segredo isolado, pessoa no ponto certo, trava que recusa, rastro de tudo", "\n".join(partes), "".join(css)), encoding="utf-8")



def aberto(slug, icone, nome, dono, linhas, selo, atraso=0.0):
    w, h = 280, 168
    largura_selo = len(selo) * 6.9 + 18
    css = f"""
.t{{font:700 16px {SANS};fill:{TINTA}}}
.s{{font:500 12px {SANS};fill:{SUAVE}}}
.p{{font:700 9.5px {SANS};letter-spacing:1.2px;fill:{CHAMPAGNE}}}
.l{{font:500 12.5px {SANS};fill:#CFC6B6}}
.i{{font:18px 'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif}}
"""
    corpo = f"""{moldura(w, h, 14)}
<rect x="18" y="18" width="34" height="34" rx="9" fill="#1F1C18" stroke="{BORDA}"/>
<text class="i" x="35" y="41" text-anchor="middle">{icone}</text>
<rect x="{w - 18 - largura_selo:.1f}" y="24" width="{largura_selo:.1f}" height="20" rx="10" fill="#1F1C18" stroke="#3A352E"/>
<text class="p" x="{w - 18 - largura_selo / 2:.1f}" y="37.5" text-anchor="middle">{escape(selo)}</text>
<g class="up" style="animation-delay:{atraso:.2f}s"><text class="t" x="18" y="82">{escape(nome)}</text>
<text class="s" x="18" y="100">{escape(dono)}</text></g>
<g class="up" style="animation-delay:{atraso + 0.2:.2f}s">""" + "".join(
        f'<text class="l" x="18" y="{128 + i * 18}">{escape(t)}</text>' for i, t in enumerate(linhas)
    ) + "</g>"
    (AQUI / f"aberto-{slug}.svg").write_text(svg(w, h, f"{nome}: {' '.join(linhas)}", corpo, css), encoding="utf-8")


ABERTOS = [
    ("wize", "🧙", "Wize Development Kit", "qwize-br", ["10 agentes do brief ao código", "testado, com pentest por IA"], "QWIZE"),
    ("datajud", "🏛️", "skills-datajud-djen", "ChatADV", ["APIs do CNJ (DataJud e DJEN)", "como habilidade de agente"], "CHATADV"),
    ("trypost", "🗓️", "TryPost", "trypostit", ["agendador de redes open source:", "criação com IA e idioma"], "CONTRIBUIÇÃO"),
]

CASES = [
    ("chatadv", "⚖️", "ChatADV", "IA para advogados", "PRODUTO PRÓPRIO", "1 mi+", ["peças jurídicas geradas"], "API, web, RAG e agentes · −95% de nuvem"),
    ("radar-legal", "📡", "Radar Legal", "a posição do juiz, com a prova", "PRODUTO PRÓPRIO", "707/707", ["leituras auditadas com o trecho", "literal conferido na decisão"], "lei, tese ou processo monitorado"),
    ("postadv", "📣", "PostADV", "marketing jurídico com IA", "PRODUTO PRÓPRIO", "OAB ✓", ["cada post conferido com o", "Provimento 205 antes de sair"], "gera, agenda e publica nas redes"),
    ("concessionarias", "🏍️", "Agente de vendas", "rede de concessionárias", "DELTA ACADEMY", "2 dias", ["do início ao agente", "integrado ao Salesforce"], "14 lojas · 201 municípios · 633 testes"),
    ("sdr-fiscal", "🧾", "SDR no WhatsApp", "SaaS B2B da área fiscal", "DELTA ACADEMY", "1º dia", ["agente no ar, com CRM,", "agenda e follow-up em 5 toques"], "641 testes · humano no ponto certo"),
    ("ai-planta", "🌱", "AI Planta", "IoT e IA no cultivo", "PSD SOFTWARE", "IoT + IA", ["do sensor à recomendação,", "plataforma feita do zero"], "AGI Nanotech · API, app e nuvem"),
    ("aivets", "🐾", "AiVets", "IA para veterinários", "QWIZE", "100 mil+", ["páginas de literatura por", "trás de cada resposta"], "raciocínio clínico 24 h · web e WhatsApp"),
    ("sabia", "🌿", "SabIA", "IA para consultoria ambiental", "QWIZE", "19", ["agentes especializados", "numa plataforma só"], "documentos, estudos ambientais e CRM"),
]

if __name__ == "__main__":
    for i, c in enumerate(CASES):
        cartao(*c, atraso=(i % 2) * 0.25)
    for i, c in enumerate(ABERTOS):
        aberto(*c, atraso=i * 0.15)
    numeros()
    metodo()
    governo()
    print("ok:", ", ".join(sorted(p.name for p in AQUI.glob("*.svg"))))
