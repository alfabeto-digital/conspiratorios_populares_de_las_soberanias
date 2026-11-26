#!/usr/bin/env python3
"""Prepara el contenido de la bóveda para Hugo/Hextra: estructura plana, índices de
sección (_index.md), reescritura de enlaces a rutas absolutas y pesos curados.

Decisiones de navegación (plana, del README): orden curado explícito, no inferido de los
enlaces. Ver el plan. La bóveda nunca se toca; esto corre sobre la copia de construcción.

Uso: python gen_structure.py <content_dir>
"""
import re, sys, posixpath, pathlib

CONTENT = pathlib.Path(sys.argv[1]).resolve()
REPO = "https://github.com/alfabeto-digital/conspiratorios_populares_de_las_soberanias/blob/main"

# Páginas raíz copiadas del repo (aún sin frontmatter). readme=True usa base de repo.
ROOT_PAGES = {
    "_index.md":                {"title": "alfabeto.digital",       "readme": True},
    "hoja_de_ruta.md":          {"title": "hoja de ruta",           "readme": False},
    "árbol_del_repositorio.md": {"title": "árbol del repositorio",  "readme": False},
}

def is_note(rel):
    s = rel
    return not (s.endswith(".excalidraw.md") or s.startswith("graphify/")
                or "/objetos_digitales/excalidraw/" in s or s == "notas_de_desarrollo.md")

# Estructura plana: sacar tres carpetas de midu/ a la raíz.
RELOCATE = [("midu/servicios/", "servicios/"), ("midu/cuidados/", "cuidados/"),
            ("midu/replicación/", "replicación/")]
RELOCATE_FILE = {"midu/servicios.md": "servicios.md", "midu/cuidados.md": "cuidados.md",
                 "midu/replicación.md": "replicación.md"}

def relocate(rel):
    for o, n in RELOCATE:
        if rel.startswith(o):
            return n + rel[len(o):]
    return RELOCATE_FILE.get(rel, rel)

# Orden curado por sección (claves = ruta nueva de la sección; "" = raíz).
ORDER = {
    "": ["midu", "subjetividades", "servicios", "cuidados", "replicación",
         "lenguaje_común", "referencias", "hoja_de_ruta", "árbol_del_repositorio"],
    "midu": ["arquitectura"],
    "midu/arquitectura": ["computadores", "nixos", "flake", "patrón_dendrítico", "secretos",
                          "capas_de_la_memoria", "almacenamiento_federado", "tipos_de_midu",
                          "estimaciones", "conectarse_en_internet"],
    "servicios": ["stalwart", "dendrite", "ntfy", "pangolin", "túnel_cifrado", "caddy",
                  "adguard", "authelia", "nextcloud", "hugo", "virtualización", "terminal",
                  "postgresql", "syncthing", "vaultwarden"],
    "cuidados": ["cifrado", "privacidad", "zero-trust"],
    "replicación": ["documentación", "preparativos", "nixos", "configuración", "secretos",
                    "vps", "rutas"],
    "replicación/rutas": ["ruta_A-vps+nixos", "ruta_B-vps+podman", "ruta_C-cloudflare"],
    "subjetividades": ["pluriverso", "transdisciplinariedad", "interfaces", "soberanía_digital",
                       "imaginación_moral", "alfabetización_digital_popular", "replicación",
                       "ecologías_queer", "desarrollo", "infraestructuras", "contexto",
                       "gobernanza", "memorias_colectivas", "dispositivo", "conspiratorios"],
    "lenguaje_común": ["definiciones", "cartografía_de_lo_esencial", "graphify", "objetos_digitales"],
}

# ---- 1. listar notas y calcular rutas nuevas ----
notes = []
for p in CONTENT.rglob("*.md"):
    rel = p.relative_to(CONTENT).as_posix()
    if rel in ROOT_PAGES or is_note(rel):
        notes.append(rel)

reloc = {rel: relocate(rel) for rel in notes}
dirs = set()
for r in reloc.values():
    parts = r.split("/")
    for i in range(1, len(parts)):
        dirs.add("/".join(parts[:i]))

def to_index(r):
    if r in ROOT_PAGES:
        return r
    parts = r.split("/")
    stem = parts[-1][:-3]
    parent = "/".join(parts[:-1])
    sib = (parent + "/" + stem) if parent else stem
    if sib in dirs:
        return sib + "/_index.md"
    if parent and parent.split("/")[-1] == stem:
        return parent + "/_index.md"
    return r

newpath = {rel: to_index(reloc[rel]) for rel in notes}
new_set = set(newpath.values())

# Secciones sin nota índice propia: _index.md mínimo (solo título, para que puedan
# llevar peso y encabezar su lista; Hextra lista sus hijos). No es contenido nuevo.
SYNTH = {"lenguaje_común/definiciones/_index.md": "Definiciones"}
new_set |= set(SYNTH)

# ---- 2. reescritura de enlaces ----
INLINE = re.compile(r'(!?\[[^\]]*\]\()([^)\s]+)(\))')

def github(repo_rel):
    return f"{REPO}/{repo_rel}"

def emit_internal(cp, frag):
    # cp = ruta de contenido original (posix). Devuelve destino absoluto.
    if cp in newpath:
        return "/" + newpath[cp] + frag
    return "/" + cp + frag          # no-nota dentro del contenido (imagen, graphify, etc.)

def resolve_normal(orig, dest):
    if dest.startswith(("http://", "https://", "mailto:", "#", "/")):
        return dest
    path_part, sep, fr = dest.partition("#")
    frag = (sep + fr) if sep else ""
    base = posixpath.dirname(orig)
    T = posixpath.normpath(posixpath.join(base, path_part))
    if T.startswith(".."):
        return github(T[3:] if T.startswith("../") else T.lstrip("./"))
    return emit_internal(T, frag)

def resolve_readme(dest):
    if dest.startswith(("http://", "https://", "mailto:", "#")):
        return dest
    path_part, sep, fr = dest.partition("#")
    frag = (sep + fr) if sep else ""
    d = path_part.lstrip("/")
    if d == "ROADMAP.md":
        return "/hoja_de_ruta.md" + frag
    if d == "TREE.md":
        return "/árbol_del_repositorio.md" + frag
    if d.startswith("base_de_conocimientos/"):
        return emit_internal(d[len("base_de_conocimientos/"):], frag)
    return github(d)

def rewrite(text, orig, readme):
    def repl(m):
        pre, dest, post = m.group(1), m.group(2), m.group(3)
        new = resolve_readme(dest) if readme else resolve_normal(orig, dest)
        return pre + new + post
    return INLINE.sub(repl, text)

def clean_body(body):
    """Quita el primer encabezado H1 (Hextra ya muestra el título del frontmatter) y
    las migas de pan manuales (líneas que empiezan con ←; Hextra genera breadcrumbs)."""
    out, h1 = [], False
    for ln in body.split("\n"):
        s = ln.lstrip("﻿")
        if not h1 and re.match(r'#\s+\S', s):
            h1 = True
            continue
        if s.lstrip().startswith("←"):
            continue
        out.append(ln)
    while out and out[0].strip() == "":
        out.pop(0)
    return "\n".join(out)

# ---- 3. pesos ----
def weight_target(section, child):
    base = (section + "/") if section else ""
    for cand in (base + child + "/_index.md", base + child + ".md"):
        if cand in new_set:
            return cand
    return None

weights = {}
for section, children in ORDER.items():
    for i, child in enumerate(children, start=1):
        t = weight_target(section, child)
        if t:
            weights[t] = i

def set_weight(fm_lines, w):
    out = [l for l in fm_lines if not re.match(r'\s*weight:\s', l)]
    res, done = [], False
    for l in out:
        res.append(l)
        if not done and re.match(r'title:\s', l):
            res.append(f"weight: {w}"); done = True
    if not done:
        res.insert(0, f"weight: {w}")
    return res

# ---- 4. procesar cada nota: frontmatter raíz, reescritura, peso ----
def frontmatter_for(rel):
    cfg = ROOT_PAGES[rel]
    lines = [f'title: {cfg["title"]}']
    if cfg["readme"]:
        lines += ["cascade:", "  type: docs"]
    return lines

output = {}  # ruta_nueva -> texto final
for rel in notes:
    text = (CONTENT / rel).read_text(encoding="utf-8")
    readme = ROOT_PAGES.get(rel, {}).get("readme", False)
    if rel in ROOT_PAGES:
        fm = frontmatter_for(rel)
        body = text
    else:
        if not text.startswith("---"):
            output[newpath[rel]] = rewrite(clean_body(text), rel, readme); continue
        end = text.find("\n---", 3)
        fm = text[3:end].split("\n")
        # quitar líneas vacías de borde del bloque fm
        while fm and fm[0] == "": fm.pop(0)
        while fm and fm[-1] == "": fm.pop()
        body = text[end + 4:]
    np = newpath[rel]
    if np in weights:
        fm = set_weight(fm, weights[np])
    body = rewrite(clean_body(body), rel, readme)
    output[np] = "---\n" + "\n".join(fm) + "\n---\n" + body

# ---- 5. escribir y borrar originales ----
for np, text in output.items():
    dst = CONTENT / np
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")
for rel in notes:
    if newpath[rel] != rel:
        src = CONTENT / rel
        if src.exists():
            src.unlink()

# _index.md mínimos para secciones sin nota índice
for np, title in SYNTH.items():
    dst = CONTENT / np
    if dst.exists():
        continue
    fm = [f"title: {title}"]
    if np in weights:
        fm = set_weight(fm, weights[np])
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("---\n" + "\n".join(fm) + "\n---\n", encoding="utf-8")

print(f"notas: {len(notes)} | secciones (_index.md): "
      f"{sum(1 for v in newpath.values() if v.endswith('/_index.md'))} | pesos: {len(weights)}")
