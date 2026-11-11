"""Busca en guiones y textos de pantalla los términos que la ficha del sistema prohíbe (no gasta créditos).

Uso:  python3 qc_textos.py <fichas/DIVISION-SISTEMA.md> <archivo> [más archivos...]
      (archivos: el guion ES/EN, el texto que leerá la voz y los .py con textos de pantalla, etiquetas y portadas)

Lee de la ficha todas las tablas con columnas «Sí» y «No». En la columna «No»:
  · varias formas separadas por « / »        · «*» al final de una palabra = cualquier terminación (certificad*)
  · lo que va entre paréntesis es una nota y no se busca
La búsqueda ignora mayúsculas, tildes y signos, y admite un artículo entre palabras («sobre y bajo EL suelo técnico»).
Devuelve código 1 si encuentra alguno."""
import sys, re, unicodedata

ART = r'(?:(?:el|la|los|las|un|una|the|a|an)\s+)?'


def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9*]+', ' ', s)).strip()


def rules(ficha):
    out = []
    head = None
    for line in open(ficha, encoding='utf-8'):
        if not line.strip().startswith('|'):
            head = None
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if head is None:
            low = [norm(c) for c in cells]
            head = (low.index('si'), low.index('no')) if 'si' in low and 'no' in low else ()
            continue
        if not head or set(line.strip()) <= set('|-: '):
            continue
        yes, no = cells[head[0]], cells[head[1]]
        for term in re.sub(r'\([^)]*\)', '', no).split(' / '):
            words = norm(term).split()
            if not words:
                continue
            pat = r'\b' + (r'\s+' + ART).join(re.escape(w[:-1]) + r'\w*' if w.endswith('*') else re.escape(w) for w in words) + r'\b'
            out.append((term.strip(), yes if norm(yes) else '', re.compile(pat)))
    return out


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    rs = rules(sys.argv[1])
    if not rs:
        print('La ficha no tiene ninguna tabla «Sí | No».'); sys.exit(2)
    hits = 0
    for f in sys.argv[2:]:
        for n, line in enumerate(open(f, encoding='utf-8', errors='replace'), 1):
            nl = norm(line)
            for term, yes, pat in rs:
                if pat.search(nl):
                    hits += 1
                    print(f'✖ {f}:{n}: «{term}»' + (f' → usar «{yes}»' if yes else ' → no se dice') + f'\n      {line.strip()[:150]}')
    print(f'\n{len(rs)} términos prohibidos comprobados en {len(sys.argv) - 2} archivos: ' + ('ninguno encontrado ✔' if not hits else f'{hits} apariciones ✖'))
    sys.exit(1 if hits else 0)
