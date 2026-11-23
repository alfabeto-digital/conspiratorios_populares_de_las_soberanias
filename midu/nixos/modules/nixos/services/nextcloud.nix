{ inputs, ... }: {
  flake.nixosModules.nextcloud = { config, lib, pkgs, cfg, dataPath, storagePath, ... }: {

    # NextCloud corre detrás de Caddy, igual que el resto de servicios: su nginx
    # interno escucha solo en localhost y Caddy (o Cloudflare) termina TLS.
    services.nextcloud = {
      enable   = true;
      package  = pkgs.nextcloud32;   # versión disponible en nixpkgs 26.05 (la 31 fue removida)
      hostName = "cloud.${cfg.domain}";
      datadir  = "${dataPath}/nextcloud";
      https    = true;
      config = {
        dbtype        = "pgsql";
        dbname        = "nextcloud";
        dbuser        = "nextcloud";
        dbhost        = "/run/postgresql";   # socket Unix → peer auth, sin contraseña
        adminuser     = cfg.admin_username;
        adminpassFile = config.sops.secrets.nextcloud_admin_password.path;
      };
      settings = {
        trusted_proxies     = [ "127.0.0.1" ];
        overwriteprotocol   = "https";
        overwritehost       = "cloud.${cfg.domain}";
        "overwrite.cli.url" = "https://cloud.${cfg.domain}";
      };
    };

    # El nginx que genera el módulo escucha solo en localhost; Caddy hace el reverse_proxy.
    services.nginx.virtualHosts."cloud.${cfg.domain}" = {
      listen     = [{ addr = "127.0.0.1"; port = cfg.nextcloud_port; }];
      forceSSL   = lib.mkForce false;
      enableACME = lib.mkForce false;
    };

    # Acceso de NextCloud al raid1 (almacenamiento externo) vía el grupo `storage`.
    users.users.nextcloud.extraGroups = [ "storage" ];

    # datadir en el disco `data` (LUKS, montaje tardío) y external storage en el raid1:
    # ambos deben estar montados antes de php-fpm y del setup.
    systemd.services.nextcloud-setup.unitConfig.RequiresMountsFor  = [ dataPath storagePath ];
    systemd.services.phpfpm-nextcloud.unitConfig.RequiresMountsFor = [ dataPath storagePath ];

    # Contraseña del admin (owner nextcloud).
    sops.secrets.nextcloud_admin_password = { owner = "nextcloud"; mode = "0400"; };

    # Base de datos (la línea peer se añade en database.nix).
    services.postgresql.ensureDatabases = [ "nextcloud" ];
    services.postgresql.ensureUsers     = [{ name = "nextcloud"; ensureClauses.login = true; }];

    systemd.services.postgresql-nextcloud-setup = {
      description = "Grant nextcloud privileges on nextcloud database";
      wantedBy    = [ "multi-user.target" ];
      after       = [ "postgresql.service" ];
      requires    = [ "postgresql.service" ];
      serviceConfig = { Type = "oneshot"; User = "postgres"; RemainAfterExit = true; };
      script = ''
        set -e
        ${config.services.postgresql.package}/bin/psql -c \
          "GRANT ALL PRIVILEGES ON DATABASE nextcloud TO \"nextcloud\";"
        ${config.services.postgresql.package}/bin/psql -d nextcloud -c \
          "GRANT ALL ON SCHEMA public TO \"nextcloud\";"
      '';
    };

    # Almacenamiento externo Local hacia el raid1, automático e idempotente.
    systemd.services.nextcloud-external-storage-setup = {
      description = "Enable files_external and mount the raid1 as Local external storage";
      wantedBy    = [ "multi-user.target" ];
      after       = [ "nextcloud-setup.service" ];
      requires    = [ "nextcloud-setup.service" ];
      serviceConfig = { Type = "oneshot"; RemainAfterExit = true; };
      script = let occ = "${config.services.nextcloud.occ}/bin/nextcloud-occ"; in ''
        ${occ} app:enable files_external
        if ! ${occ} files_external:list | ${pkgs.gnugrep}/bin/grep -q "${storagePath}"; then
          ${occ} files_external:create "storage" local null::null \
            --config datadir="${storagePath}"
        fi
      '';
    };
  };
}
