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
      url   = "github:imfing/hextra/v0.9.8";
      flake = false;
    };
  };

  outputs = inputs: inputs.flake-parts.lib.mkFlake { inherit inputs; } {
    imports = [ (inputs.import-tree ./modules) ];
    _module.args.configDir =
      let e = builtins.getEnv "NIXOS_CONFIG_DIR"; in
      if e != "" then e else "/etc/nixos";
  };
}
