#!/usr/bin/env python3
"""Gera os SVG animados do README do perfil.

O README do GitHub não roda JavaScript nem CSS próprio, mas SVG com
@keyframes servido como <img> anima. Cada bloco sai em duas versões: a de
computador (grade) e a de celular (uma coluna), trocadas no README por
<picture><source media="(max-width: 700px)">. Fonte web não carrega dentro
de <img>, por isso a pilha é de sistema (Georgia faz a serifada do site).

Uso: python3 assets/gerar.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

AQUI = Path(__file__).parent

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
SERIF = "Georgia,'Times New Roman',serif"
EMOJI = "'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif"
FUNDO, CAIXA, BORDA, BORDA2 = "#151310", "#1F1C18", "#2A2723", "#3A352E"
TINTA, CORPO, SUAVE, APAGADO = "#F1ECE3", "#CFC6B6", "#A39A8A", "#8F8778"
CHAMPAGNE, CLARO, ESCURO, ACESO = "#D6BD8F", "#E2CDA4", "#8C7148", "#211C15"

CSS_BASE = f"""
.up{{opacity:0;animation:up .9s cubic-bezier(.2,.7,.2,1) forwards}}
@keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
.run{{stroke-dasharray:9 91;animation:run 7s linear infinite}}
@keyframes run{{to{{stroke-dashoffset:-100}}}}
.shine{{animation:shine 8s ease-in-out infinite}}
@keyframes shine{{0%,72%{{transform:translateX(-420px)}}100%{{transform:translateX(1300px)}}}}
.ln{{stroke-dasharray:100;stroke-dashoffset:100;animation:ln 1.4s ease forwards}}
@keyframes ln{{to{{stroke-dashoffset:0}}}}
.emo{{font:22px {EMOJI}}}
.ct{{font:700 21px {SANS};fill:{TINTA}}}
.cs{{font:500 13px {SANS};fill:{SUAVE}}}
.cp{{font:700 10.5px {SANS};letter-spacing:1.3px;fill:{CHAMPAGNE}}}
.cn{{font:400 50px {SERIF};fill:url(#g)}}
.cl{{font:500 14px {SANS};fill:{CORPO}}}
.cf{{font:500 12.5px {SANS};fill:{APAGADO}}}
.nn{{font:400 46px {SERIF};fill:url(#g)}}
.nl{{font:500 13.5px {SANS};fill:{CORPO}}}
.mk{{font:400 20px {SERIF};fill:{CHAMPAGNE}}}
.mt{{font:700 16px {SANS};fill:{TINTA}}}
.ms{{font:500 12.5px {SANS};fill:{SUAVE}}}
.gt{{font:700 13.5px {SANS};fill:{TINTA}}}
.pt{{font:700 14.5px {SANS};fill:{TINTA}}}
.ps{{font:500 12.5px {SANS};fill:{SUAVE}}}
.at{{font:700 16px {SANS};fill:{TINTA}}}
.as{{font:500 12px {SANS};fill:{SUAVE}}}
.ap{{font:700 9.5px {SANS};letter-spacing:1.2px;fill:{CHAMPAGNE}}}
.al{{font:500 12.5px {SANS};fill:{CORPO}}}
"""

DEFS = f"""<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CLARO}"/><stop offset="1" stop-color="{ESCURO}"/></linearGradient>
<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#F1E3C4" stop-opacity="0"/><stop offset=".5" stop-color="#F1E3C4" stop-opacity=".09"/><stop offset="1" stop-color="#F1E3C4" stop-opacity="0"/></linearGradient>
</defs>"""


def atraso(s):
    return f'style="animation-delay:{s:.2f}s"'


def moldura(pfx, w, h, rx=16):
    """Fundo, brilho que passa e luz correndo na borda."""
    return f"""<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx}" fill="{FUNDO}" stroke="{BORDA}"/>
<clipPath id="c{pfx}"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx}"/></clipPath>
<g clip-path="url(#c{pfx})"><g class="shine"><rect x="0" y="-20" width="150" height="{h+40}" fill="url(#sh)" transform="skewX(-18)"/></g></g>
<rect class="run" x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx}" fill="none" stroke="url(#g)" stroke-width="1.6" pathLength="100"/>"""


def selo(x_dir, y, texto, cls="cp", passo=7.4, altura=22):
    larg = len(texto) * passo + 22
    return (
        f'<rect x="{x_dir - larg:.1f}" y="{y}" width="{larg:.1f}" height="{altura}" rx="{altura / 2}" fill="{CAIXA}" stroke="{BORDA2}"/>'
        f'<text class="{cls}" x="{x_dir - larg / 2:.1f}" y="{y + altura / 2 + 4}" text-anchor="middle">{escape(texto)}</text>'
    )


def linhas(cls, x, y0, passo, textos, anchor="start"):
    return "".join(f'<text class="{cls}" x="{x}" y="{y0 + i * passo}" text-anchor="{anchor}">{escape(t)}</text>' for i, t in enumerate(textos))


# ── peças ────────────────────────────────────────────────────────────────

def cartao(pfx, d, icone, nome, sub, rotulo_selo, numero, rotulo, rodape):
    w, h = 420, 236
    return w, h, f"""{moldura(pfx, w, h)}
<rect x="22" y="22" width="40" height="40" rx="11" fill="{CAIXA}" stroke="{BORDA}"/>
<text class="emo" x="42" y="50" text-anchor="middle">{icone}</text>
<text class="ct" x="76" y="40">{escape(nome)}</text>
<text class="cs" x="76" y="59">{escape(sub)}</text>
{selo(w - 22, 22, rotulo_selo)}
<g class="up" {atraso(d + .1)}><text class="cn" x="22" y="138">{escape(numero)}</text></g>
<g class="up" {atraso(d + .35)}>{linhas("cl", 24, 166, 19, rotulo)}</g>
<line class="ln" x1="24" y1="{h - 40}" x2="{w - 24}" y2="{h - 40}" stroke="{BORDA}" pathLength="100" {atraso(d + .5)}/>
<g class="up" {atraso(d + .6)}><text class="cf" x="24" y="{h - 17}">{escape(rodape)}</text></g>"""


def aberto(pfx, d, icone, nome, dono, textos, rotulo_selo):
    w, h = 280, 168
    return w, h, f"""{moldura(pfx, w, h, 14)}
<rect x="18" y="18" width="34" height="34" rx="9" fill="{CAIXA}" stroke="{BORDA}"/>
<text class="emo" x="35" y="43" text-anchor="middle" style="font-size:18px">{icone}</text>
{selo(w - 18, 24, rotulo_selo, "ap", 6.9, 20)}
<g class="up" {atraso(d)}><text class="at" x="18" y="82">{escape(nome)}</text><text class="as" x="18" y="100">{escape(dono)}</text></g>
<g class="up" {atraso(d + .2)}>{linhas("al", 18, 128, 18, textos)}</g>"""


def celula_numero(d, cx, numero, rotulo):
    return (
        f'<g class="up" {atraso(d)}><text class="nn" x="{cx}" y="0" text-anchor="middle">{escape(numero)}</text></g>'
        f'<g class="up" {atraso(d + .2)}>{linhas("nl", cx, 30, 19, rotulo, "middle")}</g>'
    )


def celula_papel(d, x, y, w, h, icone, titulo, sub):
    cx = x + w / 2
    return (
        f'<g class="up" {atraso(d)}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{FUNDO}" stroke="{BORDA}" stroke-width="1.2"/>'
        f'<text class="emo" x="{cx}" y="{y + 36}" text-anchor="middle" style="font-size:20px">{icone}</text>'
        f'<text class="pt" x="{cx}" y="{y + 64}" text-anchor="middle">{escape(titulo)}</text>'
        f'<text class="ps" x="{cx}" y="{y + 83}" text-anchor="middle">{escape(sub)}</text></g>'
    )


# ── composição ───────────────────────────────────────────────────────────

def salvar(nome, w, h, titulo, corpo, css_extra=""):
    (AQUI / f"{nome}.svg").write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(titulo)}">
<title>{escape(titulo)}</title>
<style>{CSS_BASE}{css_extra}</style>
{DEFS}
{corpo}
</svg>
""",
        encoding="utf-8",
    )


def grade(pecas, colunas, gap):
    """Posiciona peças (w, h, svg) em grade; devolve largura, altura e corpo."""
    pw, ph = pecas[0][0], pecas[0][1]
    linhas_n = -(-len(pecas) // colunas)
    w = colunas * pw + (colunas - 1) * gap
    h = linhas_n * ph + (linhas_n - 1) * gap
    corpo = "".join(
        f'<g transform="translate({(i % colunas) * (pw + gap)},{(i // colunas) * (ph + gap)})">{p[2]}</g>'
        for i, p in enumerate(pecas)
    )
    return w, h, corpo


CASES = [
    ("⚖️", "ChatADV", "IA para advogados", "PRODUTO PRÓPRIO", "1 mi+", ["peças jurídicas geradas"], "API, web, RAG e agentes · −95% de nuvem"),
    ("📡", "Radar Legal", "a posição do juiz, com a prova", "PRODUTO PRÓPRIO", "707/707", ["leituras auditadas com o trecho", "literal conferido na decisão"], "lei, tese ou processo monitorado"),
    ("📣", "PostADV", "marketing jurídico com IA", "PRODUTO PRÓPRIO", "OAB ✓", ["cada post conferido com o", "Provimento 205 antes de sair"], "gera, agenda e publica nas redes"),
    ("🏍️", "Agente de vendas", "rede de concessionárias", "DELTA ACADEMY", "2 dias", ["do início ao agente", "integrado ao Salesforce"], "14 lojas · 201 municípios · 633 testes"),
    ("🧾", "SDR no WhatsApp", "SaaS B2B da área fiscal", "DELTA ACADEMY", "1º dia", ["agente no ar, com CRM,", "agenda e follow-up em 5 toques"], "641 testes · humano no ponto certo"),
    ("🌱", "AI Planta", "IoT e IA no cultivo", "PSD SOFTWARE", "IoT + IA", ["do sensor à recomendação,", "plataforma feita do zero"], "AGI Nanotech · API, app e nuvem"),
    ("🐾", "AiVets", "IA para veterinários", "QWIZE", "100 mil+", ["páginas de literatura por", "trás de cada resposta"], "raciocínio clínico 24 h · web e WhatsApp"),
    ("🌿", "SabIA", "IA para consultoria ambiental", "QWIZE", "19", ["agentes especializados", "numa plataforma só"], "documentos, estudos ambientais e CRM"),
]

ABERTOS = [
    ("🧙", "Wize Development Kit", "qwize-br", ["10 agentes do brief ao código", "testado, com pentest por IA"], "QWIZE"),
    ("🏛️", "skills-datajud-djen", "ChatADV", ["APIs do CNJ (DataJud e DJEN)", "como habilidade de agente"], "CHATADV"),
    ("🗓️", "TryPost", "trypostit", ["agendador de redes open source:", "criação com IA e idioma"], "CONTRIBUIÇÃO"),
]

NUMEROS = [
    ("1 mi+", ["peças jurídicas", "geradas no ChatADV"]),
    ("−95%", ["custo de nuvem do ChatADV,", "migração em uma semana"]),
    ("8", ["clientes liderados", "como FDE em um mês"]),
    ("20+", ["anos de software,", "10 de advocacia"]),
]

PAPEIS = [
    ("🧭", "FDE na Delta Academy", "8 clientes no último mês"),
    ("🧪", "FDE na QWize", "mais 2 clientes"),
    ("⚖️", "Fundador do ChatADV", "e do PostADV"),
    ("🏗️", "Fundador da PSD", "agentes e automações"),
]

PASSOS = [
    ("Entender", ["a operação,", "o gargalo e o custo"]),
    ("Decompor", ["um caso de alto impacto,", "não dez de baixo"]),
    ("Construir", ["protótipo em semanas,", "software no ar"]),
    ("Medir", ["antes e depois,", "com número"]),
]

GOVERNO = [("🔐", "Menor", "privilégio"), ("🤐", "Segredo", "isolado"), ("🚦", "Pessoa no", "ponto certo"), ("🧪", "Trava que", "recusa"), ("📋", "Rastro", "de tudo")]


def gerar_cases():
    titulo = "Cases: " + "; ".join(f"{c[1]}, {c[4]} {' '.join(c[5])}" for c in CASES)
    for nome, colunas, gap in (("cases", 2, 20), ("cases-celular", 1, 14)):
        pecas = [cartao(f"{nome[0]}{i}", (i % colunas) * .25 + (i // colunas) * .1, *c) for i, c in enumerate(CASES)]
        w, h, corpo = grade(pecas, colunas, gap)
        salvar(nome, w, h, titulo, corpo)


def gerar_abertos():
    titulo = "Aberto no GitHub: " + ", ".join(a[1] for a in ABERTOS)
    for nome, colunas, gap in (("abertos", 3, 14), ("abertos-celular", 1, 12)):
        pecas = [aberto(f"{nome[0]}{i}", i * .15, *a) for i, a in enumerate(ABERTOS)]
        w, h, corpo = grade(pecas, colunas, gap)
        salvar(nome, w, h, titulo, corpo)


def gerar_numeros():
    titulo = ", ".join(f"{n} {' '.join(r)}" for n, r in NUMEROS)
    # computador: uma faixa
    w, h = 840, 156
    corpo = [moldura("n", w, h, 18)]
    for i, (n, r) in enumerate(NUMEROS):
        cx = 105 + i * 210
        corpo.append(f'<g transform="translate(0,74)">{celula_numero(.15 + i * .18, cx, n, r)}</g>')
        if i:
            corpo.append(f'<line class="ln" x1="{cx - 105}" y1="34" x2="{cx - 105}" y2="{h - 34}" stroke="{BORDA}" pathLength="100" {atraso(.15 + i * .18)}/>')
    salvar("numeros", w, h, titulo, "\n".join(corpo))
    # celular: 2 x 2
    w, h = 420, 270
    corpo = [moldura("m", w, h, 18)]
    for i, (n, r) in enumerate(NUMEROS):
        cx, cy = 105 + (i % 2) * 210, 72 + (i // 2) * 125
        corpo.append(f'<g transform="translate(0,{cy})">{celula_numero(.15 + i * .15, cx, n, r)}</g>')
    corpo.append(f'<line class="ln" x1="210" y1="28" x2="210" y2="{h - 28}" stroke="{BORDA}" pathLength="100"/>')
    corpo.append(f'<line class="ln" x1="28" y1="135" x2="{w - 28}" y2="135" stroke="{BORDA}" pathLength="100"/>')
    salvar("numeros-celular", w, h, titulo, "\n".join(corpo))


def gerar_papeis():
    titulo = ", ".join(f"{t} ({s})" for _, t, s in PAPEIS)
    cw, ch, gap = 198, 100, 16
    corpo = "".join(celula_papel(.1 + i * .12, 1 + i * (cw + gap), 1, cw, ch, *p) for i, p in enumerate(PAPEIS))
    salvar("papeis", 4 * cw + 3 * gap + 2, ch + 2, titulo, corpo)
    cw = 202
    corpo = "".join(celula_papel(.1 + i * .12, 1 + (i % 2) * (cw + gap), 1 + (i // 2) * (ch + gap), cw, ch, *p) for i, p in enumerate(PAPEIS))
    salvar("papeis-celular", 2 * cw + gap + 2, 2 * ch + gap + 2, titulo, corpo)


def gerar_metodo():
    titulo = "Entender, decompor, construir, medir"
    ciclo = 9

    def keyframes_nos(pfx):
        return "".join(
            f"@keyframes {pfx}{i}{{0%,{max(25 * i - 1, 0)}%{{fill:{FUNDO};stroke:{BORDA2}}}{25 * i + 3}%,90%{{fill:#2A2216;stroke:{CHAMPAGNE}}}100%{{fill:{FUNDO};stroke:{BORDA2}}}}}"
            f".{pfx}{i}{{animation:{pfx}{i} {ciclo}s ease infinite}}"
            for i in range(4)
        )

    def trilho(eixo, dist):
        return (
            f".trilho{{stroke-dasharray:100;stroke-dashoffset:100;animation:trilho {ciclo}s ease-in-out infinite}}"
            f"@keyframes trilho{{0%{{stroke-dashoffset:100;opacity:1}}75%,92%{{stroke-dashoffset:0;opacity:1}}100%{{stroke-dashoffset:0;opacity:0}}}}"
            f".ponto{{animation:ponto {ciclo}s ease-in-out infinite}}"
            f"@keyframes ponto{{0%{{transform:translate{eixo}(0);opacity:1}}75%{{transform:translate{eixo}({dist}px);opacity:1}}92%{{opacity:0}}100%{{transform:translate{eixo}(0);opacity:0}}}}"
        )

    # computador: horizontal
    w, h = 840, 196
    xs = [105 + i * 210 for i in range(4)]
    corpo = [moldura("d", w, h, 18),
             f'<line x1="{xs[0]}" y1="62" x2="{xs[-1]}" y2="62" stroke="{BORDA}" stroke-width="2"/>',
             f'<line class="trilho" x1="{xs[0]}" y1="62" x2="{xs[-1]}" y2="62" stroke="{CHAMPAGNE}" stroke-width="2.4" pathLength="100"/>']
    for i, ((nome, sub), x) in enumerate(zip(PASSOS, xs)):
        corpo.append(f'<circle class="md{i}" cx="{x}" cy="62" r="22" fill="{FUNDO}" stroke="{BORDA2}" stroke-width="1.6"/><text class="mk" x="{x}" y="69" text-anchor="middle">{i + 1}</text>')
        corpo.append(f'<g class="up" {atraso(.15 + i * .15)}><text class="mt" x="{x}" y="120" text-anchor="middle">{escape(nome)}</text>{linhas("ms", x, 143, 18, sub, "middle")}</g>')
    corpo.append(f'<circle class="ponto" cx="{xs[0]}" cy="62" r="5" fill="{CLARO}"/>')
    salvar("metodo", w, h, titulo, "\n".join(corpo), keyframes_nos("md") + trilho("X", xs[-1] - xs[0]))

    # celular: vertical
    w, h = 420, 400
    ys = [62 + i * 92 for i in range(4)]
    corpo = [moldura("e", w, h, 18),
             f'<line x1="56" y1="{ys[0]}" x2="56" y2="{ys[-1]}" stroke="{BORDA}" stroke-width="2"/>',
             f'<line class="trilho" x1="56" y1="{ys[0]}" x2="56" y2="{ys[-1]}" stroke="{CHAMPAGNE}" stroke-width="2.4" pathLength="100"/>']
    for i, ((nome, sub), y) in enumerate(zip(PASSOS, ys)):
        corpo.append(f'<circle class="me{i}" cx="56" cy="{y}" r="22" fill="{FUNDO}" stroke="{BORDA2}" stroke-width="1.6"/><text class="mk" x="56" y="{y + 7}" text-anchor="middle">{i + 1}</text>')
        corpo.append(f'<g class="up" {atraso(.15 + i * .15)}><text class="mt" x="96" y="{y - 4}">{escape(nome)}</text><text class="ms" x="96" y="{y + 16}">{escape(" ".join(sub))}</text></g>')
    corpo.append(f'<circle class="ponto" cx="56" cy="{ys[0]}" r="5" fill="{CLARO}"/>')
    salvar("metodo-celular", w, h, titulo, "\n".join(corpo), keyframes_nos("me") + trilho("Y", ys[-1] - ys[0]))


def gerar_governo():
    titulo = ", ".join(f"{a} {b}" for _, a, b in GOVERNO)
    ciclo = 10

    def keyframes(pfx):
        return "".join(
            f"@keyframes {pfx}{i}{{0%,{20 * i}%{{stroke:{BORDA};fill:{FUNDO}}}{20 * i + 4}%,{20 * i + 18}%{{stroke:{CHAMPAGNE};fill:{ACESO}}}{20 * i + 22}%,100%{{stroke:{BORDA};fill:{FUNDO}}}}}"
            f".{pfx}{i}{{animation:{pfx}{i} {ciclo}s ease infinite}}"
            for i in range(5)
        )

    # computador: 5 em linha
    cw, gap = 148, 15
    corpo = []
    for i, (ic, l1, l2) in enumerate(GOVERNO):
        x = 1 + i * (cw + gap)
        corpo.append(
            f'<g class="up" {atraso(.1 + i * .12)}><rect class="gd{i}" x="{x}" y="1" width="{cw}" height="110" rx="14" fill="{FUNDO}" stroke="{BORDA}" stroke-width="1.4"/>'
            f'<text class="emo" x="{x + cw / 2}" y="44" text-anchor="middle">{ic}</text>'
            f'<text class="gt" x="{x + cw / 2}" y="72" text-anchor="middle">{escape(l1)}</text>'
            f'<text class="gt" x="{x + cw / 2}" y="90" text-anchor="middle">{escape(l2)}</text></g>'
        )
    salvar("governo", 5 * cw + 4 * gap + 2, 112, titulo, "\n".join(corpo), keyframes("gd"))

    # celular: uma coluna
    rw, rh, gap = 418, 50, 10
    corpo = []
    for i, (ic, l1, l2) in enumerate(GOVERNO):
        y = 1 + i * (rh + gap)
        corpo.append(
            f'<g class="up" {atraso(.1 + i * .1)}><rect class="ge{i}" x="1" y="{y}" width="{rw}" height="{rh}" rx="12" fill="{FUNDO}" stroke="{BORDA}" stroke-width="1.4"/>'
            f'<text class="emo" x="36" y="{y + 33}" text-anchor="middle" style="font-size:20px">{ic}</text>'
            f'<text class="gt" x="66" y="{y + 30}" style="font-size:15px">{escape(l1 + " " + l2)}</text></g>'
        )
    salvar("governo-celular", rw + 2, 5 * rh + 4 * gap + 2, titulo, "\n".join(corpo), keyframes("ge"))


if __name__ == "__main__":
    for velho in AQUI.glob("*.svg"):
        velho.unlink()
    gerar_cases()
    gerar_abertos()
    gerar_numeros()
    gerar_papeis()
    gerar_metodo()
    gerar_governo()
    print("ok:", ", ".join(sorted(p.name for p in AQUI.glob("*.svg"))))
