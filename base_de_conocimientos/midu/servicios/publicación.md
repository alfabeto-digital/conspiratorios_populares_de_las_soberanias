# Publicación

← [Servicios](servicios.md)

Publicar la `base_de_conocimientos/` como sitio web la hace accesible sin clonar el repositorio, y transferible a personas que no usan git. Documentar es comunicar; publicar hace que esa comunicación llegue más lejos.

La herramienta elegida es **Hugo**: un generador de sitios estáticos en Go que sirve tanto el sitio principal (`alfabeto.digital`) como la base de conocimientos (`info.alfabeto.digital`) con el mismo generador y sin dependencias de runtime.

## Hugo

Hugo es un binario único compilado en Go: no necesita Python, Node ni ningún gestor de paquetes en el servidor. `pkgs.hugo` está disponible directamente en nixpkgs.

Construye el sitio completo en milisegundos a partir de los archivos Markdown existentes. La estructura de `base_de_conocimientos/` se mapea directamente como árbol de navegación.

Para `info.alfabeto.digital` usamos el tema **Hextra**, diseñado para documentación técnica:

| Capacidad | Detalle |
|---|---|
| Mermaid | Soporte nativo; los diagramas de `replicación.md` renderizan sin configuración adicional |
| Búsqueda | FlexSearch o Pagefind; índice generado en build time, búsqueda en el navegador |
| Navegación | Árbol lateral automático desde el árbol de directorios |
| Modo claro/oscuro | Toggle integrado |
| Español | `languageCode = "es"` en `hugo.toml` |

## Búsqueda en un sitio estático

La búsqueda no requiere un servidor dinámico. Funciona así:

1. En el paso de build, Pagefind lee el HTML generado y construye un índice comprimido en `public/_pagefind/`
2. El navegador descarga ese índice una vez y ejecuta todas las búsquedas localmente con WebAssembly
3. Nada sale del navegador; no hay llamadas a servicios externos

```bash
hugo build                      # genera public/
npx pagefind --site public      # genera public/_pagefind/
```

Pagefind soporta español sin configuración especial y es compatible con Hextra.

## La arquitectura de dos sitios

El repositorio contiene dos configuraciones Hugo independientes:

| Sitio | Fuente | Destino | Output |
|---|---|---|---|
| `alfabeto.digital` | `website/` → plantillas Hugo | `/srv/site` | Sitio principal |
| `info.alfabeto.digital` | `base_de_conocimientos/` | `/srv/info` | Base de conocimientos |

[Caddy](caddy.md) sirve ambos directorios como archivos estáticos:

```
alfabeto.digital {
  root * /srv/site
  file_server
}

info.alfabeto.digital {
  root * /srv/info
  file_server
}
```

La migración del sitio principal (`website/`) a Hugo puede hacerse en fases: Hugo gestiona el routing y sirve los archivos HTML artesanales al principio, migrando a plantillas progresivamente. La redirección desde `alfabeto.digital` hacia `info.alfabeto.digital` se define editorialmente.

## `hugo.toml` mínimo para `info.alfabeto.digital`

```toml
baseURL = "https://info.alfabeto.digital/"
languageCode = "es"
title = "alfabeto.digital — base de conocimientos"
theme = "hextra"

[params]
  mermaid = true
```

El directorio `base_de_conocimientos/` se monta como contenido del sitio:

```toml
[[module.mounts]]
  source = "../base_de_conocimientos"
  target = "content"
```

## Ver también

- [Caddy](caddy.md): el reverse proxy que sirve los archivos estáticos
- [Terminal](terminal.md): herramientas de línea de comandos para `hugo server` y `hugo build`
