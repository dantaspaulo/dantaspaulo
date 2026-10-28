#!/usr/bin/env python3
"""Confere se o texto cabe nos cartões dos SVG (SVG não quebra linha sozinho).

Mede cada <text> com as fontes do sistema que a pilha do gerar.py usa (SF Pro, Helvetica e Arial; SF Mono e Menlo
no mono), fica com a maior largura e recusa o texto que passa da margem do cartão ou encosta no selo da mesma linha.
Não precisa de navegador: só do Pillow e das fontes do macOS.

Uso: python3 assets/gerar.py && python3 assets/conferir.py
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    from PIL import ImageFont
except ImportError:
    sys.exit("conferir.py precisa do Pillow (pip install pillow)")

AQUI = Path(__file__).parent
NS = "{http://www.w3.org/2000/svg}"
FONTES = {
    "sans": ["/System/Library/Fonts/SFNS.ttf", "/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf"],
    "sans-negrito": ["/System/Library/Fonts/SFNS.ttf", "/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"],
    "mono": ["/System/Library/Fonts/SFNSMono.ttf", "/System/Library/Fonts/Menlo.ttc"],
}
MARGEM, FOLGA_SELO = 16, 8
_cache = {}


def fontes(familia, peso, tamanho):
    chave = (familia, peso, tamanho)
    if chave in _cache:
        return _cache[chave]
    lista = FONTES["mono" if familia == "mono" else ("sans-negrito" if peso >= 600 else "sans")]
    saida = []
    for caminho in lista:
        if not Path(caminho).exists():
            continue
        if caminho.endswith(".ttc"):
            for i in range(8):
                try:
                    f = ImageFont.truetype(caminho, tamanho, index=i)
                except OSError:
                    break
                estilo = f.getname()[1].lower()
                if (peso >= 600) == ("bold" in estilo) and not any(x in estilo for x in ("oblique", "italic", "light")):
                    saida.append(f)
                    break
            continue
        f = ImageFont.truetype(caminho, tamanho)
        try:
            valores = []
            for e in f.get_variation_axes():
                nome = e.get("name", b"")
                nome = (nome.decode() if isinstance(nome, bytes) else str(nome)).lower()
                alvo = peso if nome.startswith("weight") else (tamanho if nome.startswith("optical") else e.get("default", e["minimum"]))
                valores.append(max(e["minimum"], min(e["maximum"], alvo)))
            f.set_variation_by_axes(valores)
        except (OSError, AttributeError):
            pass
        saida.append(f)
    if not saida:
        sys.exit("conferir.py não achou as fontes do macOS para medir o texto")
    _cache[chave] = saida
    return saida


def estilos(bruto):
    css = re.search(r"<style>(.*?)</style>", bruto, re.S).group(1)
    tabela = {}
    for nome, corpo in re.findall(r"\.([a-z]+)\{([^{}]*)\}", css):
        m = re.search(r"font:(\d+)?\s*([\d.]+)px\s*([^;]+)", corpo)
        if m and "Emoji" not in m.group(3):
            espaco = re.search(r"letter-spacing:([\d.]+)px", corpo)
            familia = "mono" if "monospace" in m.group(3) else "sans"
            tabela[nome] = (familia, int(m.group(1) or 400), float(m.group(2)), float(espaco.group(1)) if espaco else 0.0)
    return tabela


def conferir(caminho):
    bruto = caminho.read_text(encoding="utf-8")
    tab = estilos(bruto)
    erros, cartoes = [], 0
    for g in ET.fromstring(bruto).findall(f"{NS}g"):
        if not g.get("transform", "").startswith("translate"):
            continue
        moldura = g.find(f"{NS}rect")
        if moldura is None or moldura.get("x") != "1":
            continue
        cartoes += 1
        larg = float(moldura.get("width")) + 2
        pilula = None
        for r in g.iter(f"{NS}rect"):
            if r.get("height") in ("20", "22") and float(r.get("x")) > larg / 2:
                pilula = (float(r.get("x")), float(r.get("width")))
        for t in g.iter(f"{NS}text"):
            if t.get("class") not in tab:
                continue
            familia, peso, tamanho, espaco = tab[t.get("class")]
            texto = "".join(t.itertext())
            w = max(f.getlength(texto) for f in fontes(familia, peso, tamanho)) + espaco * len(texto)
            x, y = float(t.get("x")), float(t.get("y"))
            x0, x1 = (x - w / 2, x + w / 2) if t.get("text-anchor") == "middle" else (x, x + w)
            if pilula and t.get("text-anchor") == "middle" and x0 >= pilula[0] - 1:
                # texto do selo: o espaçamento entra depois de cada letra, inclusive a última; 2 px de folga por lado
                if w - espaco > pilula[1] - 4:
                    erros.append(f"selo '{texto}' tem {w:.0f}px numa pílula de {pilula[1]:.0f}px")
                continue
            if x0 < MARGEM - 0.5 or x1 > larg - MARGEM:
                erros.append(f"'{texto}' vai de {x0:.0f} a {x1:.0f}px num cartão de {larg:.0f}px")
            if pilula and y < 46 and x1 > pilula[0] - FOLGA_SELO:
                erros.append(f"'{texto}' termina em {x1:.0f}px e o selo começa em {pilula[0]:.0f}px")
    return cartoes, erros


if __name__ == "__main__":
    falhou = False
    for svg in sorted(AQUI.glob("*.svg")):
        cartoes, erros = conferir(svg)
        if not cartoes:
            continue
        print(f"{svg.name}: {cartoes} cartões, {'ok' if not erros else 'RECUSADO'}")
        for e in erros:
            print(f"  {e}")
        falhou |= bool(erros)
    sys.exit(1 if falhou else 0)
