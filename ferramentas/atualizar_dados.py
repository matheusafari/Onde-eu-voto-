"""
Atualiza os dados do site "Onde eu voto?".

Uso (na pasta principal do projeto):
    pip install -r ferramentas/requirements.txt
    python ferramentas/atualizar_dados.py dados/fonte/locais-votacao-tre-rs.pdf

Lê o PDF salvo do site do TRE-RS, gera dados/locais-porto-alegre.json e .csv
e remonta o index.html a partir de ferramentas/modelo.html.
"""
import csv, json, re, sys
from pathlib import Path
import pdfplumber

RAIZ = Path(__file__).resolve().parent.parent

def extrair(caminho_pdf):
    recs = []; zone = None
    with pdfplumber.open(caminho_pdf) as pdf:
        for pi,p in enumerate(pdf.pages):
            ws=[w for w in p.extract_words(extra_attrs=["size","fontname"]) if 30<w['top']<790]
            # column bounds from headers
            heads={w['text']:w for w in ws if w['text'] in("LOCAL","SEÇÕES","ELEITORES","MUNICÍPIO")}
            hdr_tops=[w['top'] for w in ws if w['text']=="LOCAL"]
            H=[w for w in ws if any(abs(w['top']-t)<3 for t in hdr_tops)]
            sx=min(w['x0'] for w in H if w['text']=="SEÇÕES")-10
            ex=min(w['x0'] for w in H if w['text']=="ELEITORES")-5
            mx=min(w['x0'] for w in H if w['text']=="MUNICÍPIO")-5
            ws=[w for w in ws if w['top']>hdr_tops[0]-60 or pi>0]
            ws=[w for w in ws if not any(abs(w['top']-t)<3 for t in hdr_tops)]
            zones=[(w['top'],re.match(r'\d+',prev['text']).group()) for prev,w in zip(ws,ws[1:]) if w['text']=="Zona" and re.match(r'\d+º',prev['text'])]
            ztops=[t for t,_ in zones]
            ws=[w for w in ws if not any(abs(w['top']-t)<3 for t in ztops) and w['text']!='.d0705122']
            starts=sorted([w['top'] for w in ws if ex<=w['x0']<mx and w['text'].isdigit()])
            cur=recs[-1] if recs else None
            page_recs=[]
            for t in starts:
                z=zone
                for zt,zn in zones:
                    if zt<t: z=zn
                r={'zona':int(z),'nome':[],'end':[],'secoes':[],'eleitores':None,'top':t}
                page_recs.append(r)
            if zones: zone=zones[-1][1]
            def owner(top):
                o=cur
                for r in page_recs:
                    if top>=r['top']-4: o=r
                return o
            for w in sorted(ws,key=lambda w:(round(w['top']),w['x0'])):
                r=owner(w['top'])
                if r is None: continue
                if w['x0']<sx:
                    (r['nome'] if w['size']>11 else r['end']).append(w['text'])
                elif w['x0']<ex:
                    if w['text'].isdigit(): r['secoes'].append(int(w['text']))
                elif w['x0']<mx:
                    if w['text'].isdigit(): r['eleitores']=int(w['text'])
            recs+=page_recs
    locais = []
    for r in recs:
        locais.append({"zona": r["zona"], "local": " ".join(r["nome"]),
                       "endereco": " ".join(r["end"]), "secoes": r["secoes"],
                       "eleitores": r["eleitores"]})
    return locais

def main():
    pdf = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "dados/fonte/locais-votacao-tre-rs.pdf"
    locais = extrair(pdf)
    vistos = {}
    for l in locais:
        for s in l["secoes"]:
            chave = (l["zona"], s)
            if chave in vistos:
                print(f"AVISO: seção {s} da zona {l['zona']} aparece em dois locais")
            vistos[chave] = l["local"]
    dados = RAIZ / "dados"
    (dados / "locais-porto-alegre.json").write_text(
        json.dumps(locais, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(dados / "locais-porto-alegre.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["zona", "secao", "local", "endereco"])
        for l in locais:
            for s in l["secoes"]:
                w.writerow([l["zona"], s, l["local"], l["endereco"]])
    compacto = [{"z": l["zona"], "n": l["local"], "e": l["endereco"], "s": l["secoes"]} for l in locais]
    modelo = (RAIZ / "ferramentas/modelo.html").read_text(encoding="utf-8")
    pagina = modelo.replace("__DADOS__", json.dumps(compacto, ensure_ascii=False, separators=(",", ":")))
    (RAIZ / "index.html").write_text("<!doctype html>\n<html lang=\"pt-BR\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n" + pagina.replace("<div class=\"wrap\">", "</head>\n<body>\n<div class=\"wrap\">", 1) + "\n</body>\n</html>\n", encoding="utf-8")
    print(f"{len(locais)} locais e {len(vistos)} seções. index.html atualizado.")

if __name__ == "__main__":
    main()
