{ inputs, ... }: {
  flake.nixosModules.storage = { config, lib, pkgs, cfg, storagePath, dataPath, ... }: {

    fileSystems."${storagePath}" = {
      device  = "/dev/disk/by-uuid/${cfg.storage_uuid}";
      fsType  = "btrfs";
      options = [ "x-systemd.requires=unlock-local-raid.service" "compress=zstd" "nofail" ];
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
      options = [ "x-systemd.requires=unlock-data-disk.service" "nofail" ];
    };

    systemd.services.unlock-local-raid = {
      description = "Unlock LUKS raid1 disks and register btrfs (capa local)";
      wantedBy    = [ "multi-user.target" ];
      after       = [ "systemd-udev-settle.service" ];
      wants       = [ "systemd-udev-settle.service" ];
      unitConfig.ConditionPathExists = "!/dev/mapper/local-0";
      serviceConfig = {
        Type            = "oneshot";
        RemainAfterExit = true;
      };
      script = ''
        ${pkgs.systemd}/bin/udevadm settle
        ${pkgs.cryptsetup}/bin/cryptsetup open \
          /dev/disk/by-uuid/${cfg.storage_disk0_uuid} local-0 \
          --key-file ${config.sops.secrets.luks_local_0_key.path}
        ${pkgs.cryptsetup}/bin/cryptsetup open \
          /dev/disk/by-uuid/${cfg.storage_disk1_uuid} local-1 \
          --key-file ${config.sops.secrets.luks_local_1_key.path}
        ${pkgs.btrfs-progs}/bin/btrfs device scan
      '';
    };

    # El estado de estos servicios ahora vive en el disco `data` (LUKS), que se
    # monta tarde (unlock-data-disk en multi-user.target). Sin esto, en el arranque
    # pueden iniciar antes del montaje y fallar por rutas inexistentes.
    systemd.services.vaultwarden.unitConfig.RequiresMountsFor    = dataPath;
    systemd.services.syncthing.unitConfig.RequiresMountsFor      = dataPath;
    systemd.services.syncthing-init.unitConfig.RequiresMountsFor = dataPath;
    systemd.services.adguardhome.unitConfig.RequiresMountsFor    = dataPath;
    systemd.services.dendrite.unitConfig.RequiresMountsFor       = dataPath;
    systemd.services.authelia-main.unitConfig.RequiresMountsFor  = dataPath;
    systemd.services.ntfy-sh.unitConfig.RequiresMountsFor        = dataPath;
    systemd.services.stalwart-mail.unitConfig.RequiresMountsFor  = dataPath;

    systemd.tmpfiles.rules = [
      "d ${storagePath}                                           0770 ${cfg.admin_username}       storage                     - -"
      "d ${dataPath}/helios            0755 ${cfg.syncthing_username} storage - -"
      "d /var/www/${cfg.domain}       0755 caddy                   caddy   - -"
      "d ${dataPath}            0755 postgres postgres - -"
      "d ${dataPath}/services   0755 ${cfg.admin_username} storage - -"
      "d ${dataPath}/postgresql 0750 postgres postgres - -"
    ];
  };
}
