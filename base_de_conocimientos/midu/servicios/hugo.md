---
title: Hugo
tipo: servicio
estado: revisado
codigo: abierto
capa_memoria: descubribilidad
tags: [descubribilidad, memorias]
icono: lenguaje_común/objetos_digitales/midu/digital_infrastructures/hugo.png
nix:
  - midu/nixos/modules/nixos/network/hugo.nix
relaciones:
  parte_de: midu/servicios.md
  requiere:
    - midu/servicios/caddy.md
  relacionado:
    - midu/servicios/terminal.md
  reemplaza_a:
    - lenguaje_común/definiciones/servicios_no_soberanos/wordpress.md
    - lenguaje_común/definiciones/servicios_no_soberanos/joomla.md
---

# Hugo

← [Servicios](../servicios.md)

Publicamos la `base_de_conocimientos/` como sitio web para hacerla accesible sin clonar el repositorio, y transferible a quienes no usan git. Documentar es comunicar; publicar hace que esa comunicación llegue más lejos. Para eso usamos Hugo, un generador de sitios estáticos escrito en Go con el que publicamos la base de conocimientos en `info.alfabeto.digital`, sin dependencias de runtime. El mismo generador servirá más adelante al sitio principal (`alfabeto.digital`).

## El generador

Hugo es un binario único compilado en Go: no necesita Python, Node ni ningún gestor de paquetes en el servidor, y `pkgs.hugo` está disponible directamente en nixpkgs. Construye el sitio completo en milisegundos a partir de los archivos Markdown existentes, y mapea la estructura de `base_de_conocimientos/` directamente como árbol de navegación.

## El tema Hextra

Para `info.alfabeto.digital` usamos el tema Hextra, diseñado para documentación técnica:

| Capacidad | Detalle |
|---|---|
| Mermaid | Soporte nativo; los diagramas de `replicación.md` renderizan sin configuración adicional |
| Búsqueda | FlexSearch o Pagefind; índice generado en tiempo de construcción, búsqueda en el navegador |
| Navegación | Árbol lateral automático desde el árbol de directorios |
| Modo claro y oscuro | Toggle integrado |
| Español | `languageCode = "es"` en `hugo.toml` |

## La búsqueda en un sitio estático

La búsqueda no requiere un servidor dinámico. Hextra genera su índice (FlexSearch) durante la construcción; el navegador lo descarga una vez y ejecuta todas las búsquedas localmente. Nada sale del navegador, no hay llamadas a servicios externos.

## La construcción automática en NixOS

`info.alfabeto.digital` se construye de forma declarativa, sin pasos manuales. El módulo [`nixos/modules/nixos/network/hugo.nix`](../../../midu/nixos/modules/nixos/network/hugo.nix) define una derivación de Nix que:

1. Toma la `base_de_conocimientos/` como un input del flake (`knowledgebase`). La bóveda vive fuera del flake, así que se declara como `path:../../base_de_conocimientos`. Cada cambio en una nota cambia el hash del input y reconstruye el sitio en el siguiente `rebuild`.
2. Toma el tema Hextra como otro input, fijado a una versión y bloqueado en `flake.lock`.
3. Corre `hugo --minify` con el dominio real, y deja el sitio en una ruta del store de Nix.

[Caddy](caddy.md) sirve esa ruta del store como archivos estáticos en `info.<dominio>`, público y sin autenticación. La construcción es reproducible: el mismo contenido produce el mismo sitio, bit a bit.

## Los render-hooks: de la bóveda al sitio

La bóveda usa convenciones de Obsidian que Hugo no entiende directamente. Dos render-hooks de enlaces e imágenes las traducen durante la construcción:

- **Visualizaciones de Excalidraw**: un enlace a `midu-xxx[-slideshow].excalidraw.md` se reescribe a su imagen `midu-xxx.png`.
- **Enlaces internos**: un enlace a otra nota `.md` apunta a su página en el sitio.
- **Enlaces que escapan de la bóveda**: las notas enlazan archivos fuera de `base_de_conocimientos/` (los `.nix`, `TREE.md`, los archivos de despliegue de las rutas). Esos se reescriben al navegador de código del repositorio, de modo que siguen llevando al archivo real.
- **Embeds de íconos**: los `![[...]]` de Obsidian se convierten en imágenes antes de construir; los íconos de `objetos_digitales/` y los PNG de `visualizaciones/` se publican como archivos estáticos.

## Lo que no se publica

No todo el contenido de la bóveda es una página. Mediante `ignoreFiles` en `hugo.toml`, el sitio excluye `.obsidian/`, el cache de graphify (`graphify/cache/`), `notas_de_desarrollo.md`, y los archivos fuente de las animaciones (`*.excalidraw.md`, `*-slideshow.py`). Todo eso permanece en la bóveda para Obsidian; solo no se publica como página.

## El sitio principal

La migración del sitio principal (`alfabeto.digital`, la [página web](../../../midu/página_web/página_web.md) actual) a Hugo es una fase aparte. `info.alfabeto.digital` comparte el mismo generador y tema, de modo que ambos sitios convergen en una sola estética y un solo flujo de publicación.

## Ver también

- [Caddy](caddy.md): el proxy inverso que sirve los archivos estáticos
- [página web](../../../midu/página_web/página_web.md): el sitio estático actual que migraremos a Hugo
- [Terminal](terminal.md): las herramientas de línea de comandos para `hugo server` y `hugo build`
