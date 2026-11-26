{ inputs, self, ... }: {
  # info.<dominio>: publica la base de conocimientos como sitio estático con Hugo +
  # Hextra. La derivación construye el sitio desde el input `knowledgebase`; cada
  # cambio en la bóveda cambia el input y reconstruye el sitio en el próximo rebuild.
  flake.nixosModules.hugo = { config, lib, pkgs, cfg, ... }:
  let
    # Mismo prefijo de host que usa caddy.nix para el túnel de Cloudflare.
    h = name: if cfg.tunnel_type == "cloudflare" then "http://${name}" else name;

    infoSite = pkgs.stdenv.mkDerivation {
      pname = "info-alfabeto-digital";
      version = "1.0.0";
      dontUnpack = true;
      nativeBuildInputs = [ pkgs.hugo pkgs.perl ];

      buildPhase = ''
        export HOME=$TMPDIR
        mkdir -p work/content work/themes

        # Config + layouts del sitio (hugo.toml, render-hooks).
        cp -r --no-preserve=mode ${self}/sites/info/. work/
        # Contenido: la base de conocimientos.
        cp -r --no-preserve=mode ${inputs.knowledgebase}/. work/content/
        # Tema.
        ln -s ${inputs.hextra} work/themes/hextra

        # Librerías JS vendorizadas (Hextra las carga desde assets/js en vez del CDN).
        mkdir -p work/assets/js
        cp ${inputs.mermaidjs} work/assets/js/mermaid.min.js
        cp ${inputs.flexsearchjs} work/assets/js/flexsearch.bundle.min.js

        # Íconos y visualizaciones como estáticos, para que resuelvan las imágenes
        # embebidas y las referencias de los diagramas.
        mkdir -p "work/static/lenguaje_común/visualizaciones"
        cp -r --no-preserve=mode "${inputs.knowledgebase}/lenguaje_común/objetos_digitales" "work/static/lenguaje_común/"
        cp --no-preserve=mode "${inputs.knowledgebase}/lenguaje_común/visualizaciones/"*.png "work/static/lenguaje_común/visualizaciones/" 2>/dev/null || true

        # Grafo interactivo como estático (los demás artefactos de graphify van al navegador de código).
        mkdir -p work/static/graphify
        cp --no-preserve=mode "${inputs.knowledgebase}/graphify/graph.html" "work/static/graphify/" 2>/dev/null || true

        # Embeds de Obsidian ![[x.png|size]] -> imagen markdown ![](/x.png).
        find work/content -name '*.md' -print0 \
          | xargs -0 perl -0777 -pi -e 's{!\[\[\s*([^\[\]#|\\]+?\.png)[^\]]*\]\]}{![](/$1)}g'

        cd work
        hugo --minify --baseURL "https://info.${cfg.domain}/" --destination public
      '';

      installPhase = ''
        mkdir -p $out
        cp -r public/. $out/
      '';
    };
  in {
    # Caddy sirve la ruta del store como archivos estáticos. Público (sin Authelia).
    services.caddy.virtualHosts.${h "info.${cfg.domain}"} = {
      extraConfig = ''
        root * ${infoSite}
        encode gzip
        file_server
      '';
    };
  };
}
