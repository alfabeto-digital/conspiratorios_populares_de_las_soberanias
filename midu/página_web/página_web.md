---
title: página web
tipo: servicio
estado: revisado
codigo: abierto
capa_memoria: descubribilidad
tags: [infraestructuras, objetos digitales]
nix:
  - midu/nixos/modules/nixos/network/caddy.nix
  - midu/nixos/modules/nixos/storage.nix
icono: ../../base_de_conocimientos/lenguaje_común/objetos_digitales/midu/digital_infrastructures/www.png
relaciones:
  parte_de: ../../base_de_conocimientos/midu/servicios.md
  requiere:
    - ../../base_de_conocimientos/midu/servicios/caddy.md
  relacionado:
    - ../../base_de_conocimientos/midu/servicios/hugo.md
    - ../../base_de_conocimientos/lenguaje_común/objetos_digitales.md
---

# página web

← [Servicios](../../base_de_conocimientos/midu/servicios.md)

Esta nota vive junto a los archivos del sitio, en `midu/página_web/`, para poder enlazar cada `objeto digital` de la página directamente. Documenta el sitio y lo indexa.

## ¿Qué es esto?

La página web es la cara pública de `alfabeto.digital`: el sitio que una persona encuentra al escribir el dominio en su navegador. Es la capa de descubribilidad de la `midu`, el primer lugar donde una comunidad se presenta y explica lo que hace antes de que alguien conozca los servicios internos.

El sitio actual es un conjunto de páginas estáticas escritas en HTML, CSS y JavaScript, sin ningún proceso de servidor detrás. Componemos la portada y las páginas (presentación, redes, terminal y una página de próxima apertura) a partir de componentes HTML reutilizables.

## ¿Para qué sirve?

**Presentarnos.** La portada y la página de presentación explican qué son los `Conspiratorios populares de las soberanías` y qué proponemos con la `midu`.

**Reunir los enlaces.** La página de redes concentra los puntos de contacto de la comunidad, de modo que una sola dirección basta para encontrar todo lo demás.

**Mostrar la estética del proyecto.** Las tipografías, los colores y la página de terminal comunican el registro técnico, político y sensible del proyecto desde la primera visita.

## ¿Cómo funciona en alfabeto.digital?

La página web se sirve sobre las mismas `infraestructuras` que el resto de los servicios. [Caddy](../../base_de_conocimientos/midu/servicios/caddy.md) atiende el dominio raíz y entrega los archivos estáticos directamente desde el disco, sin reenviar el tráfico a ningún otro servicio:

```nix
"${h cfg.domain}" = {
  extraConfig = ''
    root * /var/www/${cfg.domain}
    handle /assets/library/* {
      file_server browse
    }
    file_server
  '';
};
```

Los archivos del sitio viven en `/var/www/${dominio}`, un directorio que el sistema crea y asigna al usuario de Caddy mediante los `tmpfiles` declarados en el módulo de almacenamiento. Caddy termina el TLS y sirve el contenido; la ruta `/assets/library/` permite explorar su contenido como un listado navegable.

**Módulos NixOS:** `nixos/modules/nixos/network/caddy.nix` (sirve el dominio raíz) y `nixos/modules/nixos/storage.nix` (crea el directorio `/var/www`).

## Índice de los objetos digitales del sitio

La página web es, sobre todo, un conjunto de `objetos digitales`: las páginas, los componentes, las hojas de estilo, las tipografías, las imágenes y los scripts que la componen. Este es el índice completo, cada entrada enlaza al archivo. El repertorio visual de las visualizaciones de las `infraestructuras` se cataloga aparte, en [objetos digitales](../../base_de_conocimientos/lenguaje_común/objetos_digitales.md).

### Página de entrada

- [index.html](index.html)

### Páginas

- [about.html](pages/about.html)
- [search.html](pages/search.html)
- [social.html](pages/social.html)
- [soon.html](pages/soon.html)
- [terminal.html](pages/terminal.html)

### Componentes

- [about.html](components/about.html)
- [header.html](components/header.html)
- [landing.html](components/landing.html)
- [landing.old.html](components/landing.old.html)
- [menu.html](components/menu.html)

### Hojas de estilo

- [about.css](assets/css/about.css)
- [header.css](assets/css/header.css)
- [landing.css](assets/css/landing.css)
- [menu.css](assets/css/menu.css)
- [styles.css](assets/css/styles.css)

### Scripts

- [landing.js](assets/js/landing.js)
- [scripts.js](assets/js/scripts.js)

### Imágenes

- [bg-texture.jpg](assets/images/bg-texture.jpg)

### Biblioteca

- [transdisciplinariedad-martin-barbero.pdf](assets/library/transdisciplinariedad-martin-barbero.pdf)

### Tipografías

- **Gohu**
  - [COPYING-LICENSE](assets/fonts/Gohu/COPYING-LICENSE)
  - [GohuFont11NerdFont-Regular.ttf](assets/fonts/Gohu/GohuFont11NerdFont-Regular.ttf)
  - [GohuFont11NerdFontMono-Regular.ttf](assets/fonts/Gohu/GohuFont11NerdFontMono-Regular.ttf)
  - [GohuFont11NerdFontPropo-Regular.ttf](assets/fonts/Gohu/GohuFont11NerdFontPropo-Regular.ttf)
  - [GohuFont14NerdFont-Regular.ttf](assets/fonts/Gohu/GohuFont14NerdFont-Regular.ttf)
  - [GohuFont14NerdFontMono-Regular.ttf](assets/fonts/Gohu/GohuFont14NerdFontMono-Regular.ttf)
  - [GohuFont14NerdFontPropo-Regular.ttf](assets/fonts/Gohu/GohuFont14NerdFontPropo-Regular.ttf)
  - [GohuFontuni11NerdFont-Regular.ttf](assets/fonts/Gohu/GohuFontuni11NerdFont-Regular.ttf)
  - [GohuFontuni11NerdFontMono-Regular.ttf](assets/fonts/Gohu/GohuFontuni11NerdFontMono-Regular.ttf)
  - [GohuFontuni11NerdFontPropo-Regular.ttf](assets/fonts/Gohu/GohuFontuni11NerdFontPropo-Regular.ttf)
  - [GohuFontuni14NerdFont-Regular.ttf](assets/fonts/Gohu/GohuFontuni14NerdFont-Regular.ttf)
  - [GohuFontuni14NerdFontMono-Regular.ttf](assets/fonts/Gohu/GohuFontuni14NerdFontMono-Regular.ttf)
  - [GohuFontuni14NerdFontPropo-Regular.ttf](assets/fonts/Gohu/GohuFontuni14NerdFontPropo-Regular.ttf)
  - [README.md](assets/fonts/Gohu/README.md)
- **Monofur**
  - [LICENSE.txt](assets/fonts/Monofur/LICENSE.txt)
  - [MonofurNerdFont-Bold.ttf](assets/fonts/Monofur/MonofurNerdFont-Bold.ttf)
  - [MonofurNerdFont-Italic.ttf](assets/fonts/Monofur/MonofurNerdFont-Italic.ttf)
  - [MonofurNerdFont-Regular.ttf](assets/fonts/Monofur/MonofurNerdFont-Regular.ttf)
  - [MonofurNerdFontMono-Bold.ttf](assets/fonts/Monofur/MonofurNerdFontMono-Bold.ttf)
  - [MonofurNerdFontMono-Italic.ttf](assets/fonts/Monofur/MonofurNerdFontMono-Italic.ttf)
  - [MonofurNerdFontMono-Regular.ttf](assets/fonts/Monofur/MonofurNerdFontMono-Regular.ttf)
  - [MonofurNerdFontPropo-Bold.ttf](assets/fonts/Monofur/MonofurNerdFontPropo-Bold.ttf)
  - [MonofurNerdFontPropo-Italic.ttf](assets/fonts/Monofur/MonofurNerdFontPropo-Italic.ttf)
  - [MonofurNerdFontPropo-Regular.ttf](assets/fonts/Monofur/MonofurNerdFontPropo-Regular.ttf)
  - [README.md](assets/fonts/Monofur/README.md)
- **OpenDyslexic**
  - [LICENSE.txt](assets/fonts/OpenDyslexic/LICENSE.txt)
  - [OpenDyslexicAltNerdFont-Bold.otf](assets/fonts/OpenDyslexic/OpenDyslexicAltNerdFont-Bold.otf)
  - [OpenDyslexicAltNerdFont-BoldItalic.otf](assets/fonts/OpenDyslexic/OpenDyslexicAltNerdFont-BoldItalic.otf)
  - [OpenDyslexicAltNerdFont-Italic.otf](assets/fonts/OpenDyslexic/OpenDyslexicAltNerdFont-Italic.otf)
  - [OpenDyslexicAltNerdFont-Regular.otf](assets/fonts/OpenDyslexic/OpenDyslexicAltNerdFont-Regular.otf)
  - [OpenDyslexicAltNerdFontPropo-Bold.otf](assets/fonts/OpenDyslexic/OpenDyslexicAltNerdFontPropo-Bold.otf)
  - [OpenDyslexicAltNerdFontPropo-BoldItalic.otf](assets/fonts/OpenDyslexic/OpenDyslexicAltNerdFontPropo-BoldItalic.otf)
  - [OpenDyslexicAltNerdFontPropo-Italic.otf](assets/fonts/OpenDyslexic/OpenDyslexicAltNerdFontPropo-Italic.otf)
  - [OpenDyslexicAltNerdFontPropo-Regular.otf](assets/fonts/OpenDyslexic/OpenDyslexicAltNerdFontPropo-Regular.otf)
  - [OpenDyslexicMNerdFont-Regular.otf](assets/fonts/OpenDyslexic/OpenDyslexicMNerdFont-Regular.otf)
  - [OpenDyslexicMNerdFontMono-Regular.otf](assets/fonts/OpenDyslexic/OpenDyslexicMNerdFontMono-Regular.otf)
  - [OpenDyslexicMNerdFontPropo-Regular.otf](assets/fonts/OpenDyslexic/OpenDyslexicMNerdFontPropo-Regular.otf)
  - [OpenDyslexicNerdFont-Bold.otf](assets/fonts/OpenDyslexic/OpenDyslexicNerdFont-Bold.otf)
  - [OpenDyslexicNerdFont-BoldItalic.otf](assets/fonts/OpenDyslexic/OpenDyslexicNerdFont-BoldItalic.otf)
  - [OpenDyslexicNerdFont-Italic.otf](assets/fonts/OpenDyslexic/OpenDyslexicNerdFont-Italic.otf)
  - [OpenDyslexicNerdFont-Regular.otf](assets/fonts/OpenDyslexic/OpenDyslexicNerdFont-Regular.otf)
  - [OpenDyslexicNerdFontPropo-Bold.otf](assets/fonts/OpenDyslexic/OpenDyslexicNerdFontPropo-Bold.otf)
  - [OpenDyslexicNerdFontPropo-BoldItalic.otf](assets/fonts/OpenDyslexic/OpenDyslexicNerdFontPropo-BoldItalic.otf)
  - [OpenDyslexicNerdFontPropo-Italic.otf](assets/fonts/OpenDyslexic/OpenDyslexicNerdFontPropo-Italic.otf)
  - [OpenDyslexicNerdFontPropo-Regular.otf](assets/fonts/OpenDyslexic/OpenDyslexicNerdFontPropo-Regular.otf)
  - [README.md](assets/fonts/OpenDyslexic/README.md)
- **ShareTechMono**
  - [OFL.txt](assets/fonts/ShareTechMono/OFL.txt)
  - [README.md](assets/fonts/ShareTechMono/README.md)
  - [ShureTechMonoNerdFont-Regular.ttf](assets/fonts/ShareTechMono/ShureTechMonoNerdFont-Regular.ttf)
  - [ShureTechMonoNerdFontMono-Regular.ttf](assets/fonts/ShareTechMono/ShureTechMonoNerdFontMono-Regular.ttf)
  - [ShureTechMonoNerdFontPropo-Regular.ttf](assets/fonts/ShareTechMono/ShureTechMonoNerdFontPropo-Regular.ttf)

## Hacia Hugo

El sitio estático actual precede a la `base_de_conocimientos`. El plan es reconstruirlo con [Hugo](../../base_de_conocimientos/midu/servicios/hugo.md), el mismo generador con el que publicamos `info.alfabeto.digital` desde la `base_de_conocimientos`, para que la página web y la documentación compartan `infraestructuras` de publicación y estética.

## Ver también

- [Caddy](../../base_de_conocimientos/midu/servicios/caddy.md): el servidor web que sirve el sitio y termina el TLS
- [Hugo](../../base_de_conocimientos/midu/servicios/hugo.md): el generador con el que migraremos el sitio
- [objetos digitales](../../base_de_conocimientos/lenguaje_común/objetos_digitales.md): el repertorio visual del proyecto
