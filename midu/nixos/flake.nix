{
  description = "midu - Mínima Interfaz Digital Viable";

  inputs = {
    nixpkgs.url          = "github:nixos/nixpkgs/nixos-26.05";
    nixpkgs-unstable.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-parts.url      = "github:hercules-ci/flake-parts";
    import-tree.url      = "github:vic/import-tree";
    home-manager = {
      url = "github:nix-community/home-manager/release-26.05";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    sops-nix = {
      url = "github:Mic92/sops-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    # Contenido de info.<dominio>: la base de conocimientos vive fuera del flake
    # (en la raíz del repo), así que la tomamos como input. Al ser una ruta, cada
    # cambio en la bóveda cambia el hash del input y reconstruye el sitio.
    knowledgebase = {
      url   = "path:../../base_de_conocimientos";
      flake = false;
    };

    # Tema Hugo para info.<dominio>. Fijado a una versión; el hash lo bloquea flake.lock.
    hextra = {
      url   = "github:imfing/hextra/v0.13.0";
      flake = false;
    };

    # Librerías JS que Hextra baja de un CDN en tiempo de construcción (Mermaid,
    # FlexSearch). Las vendorizamos como inputs para construir sin red; se fijan
    # en flake.lock. Hextra las carga localmente si apuntamos params.*.js a ellas.
    mermaidjs = {
      # Fijado a la última estable (12.4.0). Hextra v0.13 apunta a la línea 11, pero la API
      # que usa (initialize/run) es estable en 12; si algún diagrama se rompiera, volver a
      # mermaid@11.17.2 (última de la línea 11). Mismo archivo dist/mermaid.min.js.
      url   = "file+https://cdn.jsdelivr.net/npm/mermaid@12.4.0/dist/mermaid.min.js";
      flake = false;
    };
    flexsearchjs = {
      url   = "file+https://cdn.jsdelivr.net/npm/flexsearch@0.8.143/dist/flexsearch.bundle.min.js";
      flake = false;
    };

    # Páginas raíz del sitio (viven fuera de base_de_conocimientos): el README es la
    # portada, más la hoja de ruta y el árbol del repositorio.
    readme  = { url = "path:../../README.md";  flake = false; };
    roadmap = { url = "path:../../ROADMAP.md"; flake = false; };
    tree    = { url = "path:../../TREE.md";    flake = false; };
  };

  outputs = inputs: inputs.flake-parts.lib.mkFlake { inherit inputs; } {
    imports = [ (inputs.import-tree ./modules) ];
    _module.args.configDir =
      let e = builtins.getEnv "NIXOS_CONFIG_DIR"; in
      if e != "" then e else "/etc/nixos";
  };
}
