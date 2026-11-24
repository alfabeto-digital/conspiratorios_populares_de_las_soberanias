{ inputs, ... }: {
  flake.nixosModules.nextcloud = { config, lib, pkgs, cfg, dataPath, servicesPath, storagePath, ... }: {

    # NextCloud corre detrás de Caddy, igual que el resto de servicios: su nginx
    # interno escucha solo en localhost y Caddy (o Cloudflare) termina TLS.
    services.nextcloud = {
      enable   = true;
      package  = pkgs.nextcloud33;   # 31 removida, 32 quedó EOL; probamos la mantenida
      hostName = "cloud.${cfg.domain}";
      datadir  = "${servicesPath}/nextcloud";
      https    = true;

      # Tienda de apps habilitada de forma declarativa. Con appstoreEnable = null
      # (default) el módulo no escribe `appstoreenabled`, y aquí quedó en `false`
      # en el config.php mutable (puesto a mano en el setup inicial). Fijarlo en
      # true lo fuerza en el override de Nix. El directorio escribible store-apps
      # (${home}/store-apps, writable=true) ya lo provisiona el módulo.
      # Nota: las apps instaladas desde la tienda no las gestiona Nix (no se
      # actualizan por rebuild; se actualizan desde la propia interfaz).
      appstoreEnable = true;

      # notify_push ("Client Push") queda PENDIENTE: su auto-test de trusted-proxy
      # no pasa detrás del túnel de Cloudflare, que reescribe el X-Forwarded-For,
      # así que el self-test resuelve "::1" en vez del valor de prueba y el unit
      # entra en bucle de reinicio, colgando el switch. Se retoma como tarea
      # aparte apuntando el push server a la URL interna (nginx en localhost) y
      # afinando trusted_domains/trusted_proxies.
      # notify_push.enable = true;

      # El panel avisa que el buffer de strings internos de OPcache (default 8) se
      # queda corto. Las entradas de phpOptions son defaults, así que esta se
      # fusiona con el resto sin pisarlas.
      phpOptions."opcache.interned_strings_buffer" = "16";

      config = {
        dbtype        = "pgsql";
        dbname        = "nextcloud";
        dbuser        = "nextcloud";
        dbhost        = "/run/postgresql";   # socket Unix → peer auth, sin contraseña
        adminuser     = cfg.nextcloud_admin_username;   # login del admin de cloud (independiente de admin_username)
        adminpassFile = config.sops.secrets.nextcloud_admin_password.path;
      };
      settings = {
        # 127.0.0.1 = nginx local; ::1 = el salto de cloudflared→Caddy por loopback
        # IPv6. Sin ::1, NextCloud toma "::1" como IP del cliente (todo el tráfico
        # parece venir de ahí) y el anti-fuerza-bruta lo throttlea. Con ::1 confiado,
        # camina el X-Forwarded-For ("<cliente_real>, ::1") hasta la IP real.
        trusted_proxies     = [ "127.0.0.1" "::1" ];
        overwriteprotocol   = "https";
        overwritehost       = "cloud.${cfg.domain}";
        "overwrite.cli.url" = "https://cloud.${cfg.domain}";

        # Ventana de mantenimiento (hora UTC; bloque de 4h): corre las tareas
        # pesadas de fondo fuera del horario de uso. 4 = 04:00–08:00 UTC.
        maintenance_window_start = 4;
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

    # NextCloud escribe en el almacenamiento externo (raid1 y folders de Syncthing)
    # como el usuario `nextcloud`. umask 0002 → archivos con escritura de grupo
    # `storage`, para compartir R/W con Syncthing en ${dataPath}/helios.
    systemd.services.phpfpm-nextcloud.serviceConfig.UMask = "0002";

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
        # Disco `data` como almacenamiento externo "data". helios (dentro) es R/W
        # vía el grupo storage; el nivel superior (${dataPath}) es root:root, así
        # que NextCloud lo lista pero no puede crear/borrar ahí. Eso protege
        # services/ y postgresql/ de borrado (su contenido además queda bloqueado
        # por sus propios permisos); sus nombres sí son visibles en el nivel superior.
        if ! ${occ} files_external:list | ${pkgs.gnugrep}/bin/grep -qE "${dataPath}[ |]"; then
          ${occ} files_external:create "data" local null::null \
            --config datadir="${dataPath}"
        fi
      '';
    };

    # ------------------------------------------------------------------ #
    # Collabora Online (CODE) para Nextcloud Office (richdocuments)        #
    # ------------------------------------------------------------------ #
    # Servidor de edición de documentos en loopback; Caddy termina TLS y lo
    # expone en collabora.<dominio> (el vhost está en caddy.nix).
    services.collabora-online = {
      enable = true;
      port   = cfg.collabora_port;   # 9980, solo loopback
      # Autoriza a NextCloud como host WOPI (quién puede pedir/guardar documentos).
      aliasGroups = [ { host = "https://cloud.${cfg.domain}:443"; } ];
      settings = {
        # TLS lo termina Caddy; Collabora habla http en loopback y usa el
        # X-Forwarded-Proto para construir sus URLs como https.
        ssl.enable      = false;
        ssl.termination = true;
        server_name     = "collabora.${cfg.domain}";
        net = {
          proto  = "IPv4";
          listen = "loopback";
        };
      };
    };

    # Cablea NextCloud Office (richdocuments) al Collabora local. richdocuments
    # se instala desde la tienda (no es declarativa), así que solo fijamos su
    # config si la app está presente. wopi_url interno (server-a-server, sin
    # pasar por el túnel); public_wopi_url público (lo usa el navegador).
    systemd.services.nextcloud-collabora-setup = {
      description = "Point Nextcloud Office (richdocuments) at the local Collabora server";
      wantedBy    = [ "multi-user.target" ];
      after       = [ "nextcloud-setup.service" ];
      requires    = [ "nextcloud-setup.service" ];
      serviceConfig = { Type = "oneshot"; RemainAfterExit = true; };
      script = let occ = "${config.services.nextcloud.occ}/bin/nextcloud-occ"; in ''
        if ${occ} app:list | ${pkgs.gnugrep}/bin/grep -q richdocuments; then
          ${occ} config:app:set richdocuments wopi_url        --value="http://127.0.0.1:${toString cfg.collabora_port}"
          ${occ} config:app:set richdocuments public_wopi_url --value="https://collabora.${cfg.domain}"
        fi
      '';
    };
  };
}
