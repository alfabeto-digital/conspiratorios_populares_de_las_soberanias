{ inputs, ... }: {
  flake.nixosModules.storage = { config, lib, pkgs, cfg, storagePath, dataPath, ... }: {

    fileSystems."${storagePath}" = {
      device  = "/dev/disk/by-uuid/${cfg.storage_uuid}";
      fsType  = "ext4";
      options = [ "nofail" ];
    };

    systemd.services.unlock-data-disk = {
      description = "Unlock LUKS data disk (nvme1)";
      wantedBy    = [ "multi-user.target" ];
      before      = [ "postgresql.service" ];
      after       = [ "systemd-udev-settle.service" ];
      wants       = [ "systemd-udev-settle.service" ];
      unitConfig.ConditionPathExists = "!/dev/mapper/data-disk";
      serviceConfig = {
        Type            = "oneshot";
        RemainAfterExit = true;
      };
      script = ''
        ${pkgs.systemd}/bin/udevadm settle
        ${pkgs.cryptsetup}/bin/cryptsetup open \
          /dev/disk/by-uuid/${cfg.data_disk_uuid} \
          data-disk \
          --key-file ${config.sops.secrets.luks_data_key.path}
      '';
    };

    fileSystems."${dataPath}" = {
      device  = "/dev/mapper/data-disk";
      fsType  = "ext4";
      # `unlock-data-disk` corre tras `basic.target` (lo desbloqueamos con una llave que
      # vive en la raíz, ya arrancado el sistema), pero `local-fs.target` espera a todos
      # los montajes locales. Sin `nofail`, el montaje de datos va antes de `local-fs.target`
      # y después del desbloqueo, lo que cierra un ciclo de orden y systemd descarta el
      # montaje al arrancar: Postgres queda sin su disco y toda la cadena se cae. `nofail`
      # saca este montaje de `local-fs.target`, rompe el ciclo y deja que se monte tarde,
      # justo tras el desbloqueo. Postgres sigue requiriéndolo de forma explícita.
      options = [ "x-systemd.requires=unlock-data-disk.service" "nofail" ];
    };

    systemd.tmpfiles.rules = [
      "d ${storagePath}                                           0750 ${cfg.admin_username}       storage                     - -"
      "d ${storagePath}/exchange                                  0750 ${cfg.admin_username}       storage                     - -"
      "d ${storagePath}/helios         0755 ${cfg.syncthing_username} storage - -"
      "d /var/www/${cfg.domain}       0755 caddy                   caddy   - -"
      "d ${dataPath}            0750 postgres postgres - -"
      "d ${dataPath}/postgresql 0750 postgres postgres - -"
    ];
  };
}
