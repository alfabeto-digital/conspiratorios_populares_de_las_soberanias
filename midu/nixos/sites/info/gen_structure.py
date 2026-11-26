#!/usr/bin/env python3
"""Prepara el contenido de la bóveda para Hugo/Hextra.

1. Convierte cada nota índice en el _index.md de su carpeta:
   - P/X.md con carpeta hermana P/X/        -> P/X/_index.md
   - P/X.md nombrada igual que su carpeta P -> P/_index.md   (p. ej. lenguaje_común/lenguaje_común.md)
   Esto resuelve el choque de rutas y le da título y contenido a cada sección.

2. Asigna `weight` a páginas y secciones según el orden en que aparecen en la nota
   índice de su sección (el orden curado de la base de conocimientos). Lo no enlazado
   queda después, alfabético.

Uso: python gen_structure.py <content_dir>
"""
import re, sys, os, pathlib

CONTENT = pathlib.Path(sys.argv[1]).resolve()
LINK = re.compile(r'\]\(([^)#]+\.md)(?:#[^)]*)?\)')
# enlaces e imágenes markdown inline: captura destino relativo para reescribir
INLINE = re.compile(r'(!?\[[^\]]*\]\()([^)\s]+)(\))')

def rewrite_links(text, old_parent, new_parent):
    """Reescribe los destinos relativos para que sigan resolviendo desde la nueva
    ubicación (la nota se movió a _index.md, un nivel más adentro)."""
    def repl(m):
        pre, tgt, post = m.group(1), m.group(2), m.group(3)
        if tgt.startswith(('http://', 'https://', 'mailto:', '#', '/')):
            return m.group(0)
        path_part, hsep, frag = tgt.partition('#')
        if path_part == '':
            return m.group(0)
        T = (old_parent / path_part).resolve()
        newrel = os.path.relpath(T, new_parent).replace(os.sep, '/')
        return pre + newrel + (hsep + frag if hsep else '') + post
    return INLINE.sub(repl, text)

def is_content(p):
    s = p.as_posix()
    return ('.excalidraw.md' not in p.name
            and '/graphify/' not in s and not s.endswith('/graphify')
            and '/objetos_digitales/excalidraw/' not in s
            and p.name != 'notas_de_desarrollo.md')

mds = [p for p in CONTENT.rglob('*.md') if is_content(p)]

# --- 1. planear movimientos (nota índice -> _index.md) ---
# move_src[original] = destino ; sec_index[carpeta_sección] = original
move_src = {}
sec_index = {}
for p in mds:
    if p.name == '_index.md':
        continue
    sib = p.parent / p.stem
    if sib.is_dir():                      # P/X.md + P/X/
        move_src[p] = sib / '_index.md'; sec_index[sib] = p
    elif p.parent.name == p.stem:         # P/X.md con P llamada X
        move_src[p] = p.parent / '_index.md'; sec_index[p.parent] = p

# ruta (tras mover) de cualquier archivo
def final_path(p):
    return move_src.get(p, p)

# --- 2. calcular pesos por sección ---
# Para una sección (carpeta D) con su nota índice, el orden de sus hijos directos
# (páginas o subsecciones) sale del orden de aparición de los enlaces en esa nota.
weights = {}   # Path original -> weight

def direct_child(D, target):
    try:
        rel = target.relative_to(D)
    except ValueError:
        return None
    parts = rel.parts
    if len(parts) == 1:
        return target                       # página directa
    return D / parts[0]                      # subcarpeta (subsección)

def child_index_file(child):
    # archivo cuyo frontmatter recibe el weight del hijo
    if child.is_dir():
        return sec_index.get(child)          # la nota índice de la subsección
    return child                             # la página

def assign(section_dir, index_src):
    if not index_src or not index_src.exists():
        return
    text = index_src.read_text(encoding='utf-8')
    seen = []
    for m in LINK.finditer(text):
        tgt = (index_src.parent / m.group(1)).resolve()
        ch = direct_child(section_dir, tgt)
        if ch is None or ch == index_src or ch == section_dir:
            continue
        f = child_index_file(ch)
        if f and f not in seen:
            seen.append(f)
    for i, f in enumerate(seen, start=1):
        weights[f] = i

# raíz: usa el _index.md inyectado (home) como fuente de orden
root_index = CONTENT / '_index.md'
assign(CONTENT, root_index if root_index.exists() else None)
# cada sección con nota índice
for sec_dir, idx in sec_index.items():
    assign(sec_dir, idx)

# --- 3. aplicar weight al frontmatter y mover ---
def set_weight(path, w):
    t = path.read_text(encoding='utf-8')
    if not t.startswith('---'):
        return
    end = t.find('\n---', 3)
    if end == -1:
        return
    fm = t[3:end].split('\n')
    fm = [l for l in fm if not re.match(r'\s*weight:\s', l)]
    out, done = [], False
    for l in fm:
        out.append(l)
        if not done and re.match(r'title:\s', l):
            out.append(f'weight: {w}'); done = True
    if not done:
        out.insert(1, f'weight: {w}')
    path.write_text('---' + '\n'.join(out) + t[end:], encoding='utf-8')

for f, w in weights.items():
    if f.exists():
        set_weight(f, w)

moved = 0
for src, dst in move_src.items():
    if src.exists():
        text = rewrite_links(src.read_text(encoding='utf-8'), src.parent, dst.parent)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding='utf-8')
        src.unlink()
        moved += 1

print(f'secciones (_index.md): {moved} | pesos asignados: {len(weights)}')
