{ inputs, ... }: {
  flake.nixosModules.syncthing = { config, lib, pkgs, cfg, dataPath, servicesPath, ... }: {

    systemd.tmpfiles.rules = [
      "d ${servicesPath}/syncthing 0750 syncthing syncthing - -"
    ];

    services.syncthing = {
      enable          = true;
      user            = cfg.syncthing_username;
      group           = "storage";
      dataDir         = "${dataPath}/helios";
      configDir       = "${servicesPath}/syncthing";
      guiAddress      = "127.0.0.1:${toString cfg.syncthing_port}";
      overrideDevices = false;
      overrideFolders = false;
      settings.gui.insecureSkipHostcheck = true;
    };

    # NextCloud (grupo storage) comparte R/W con Syncthing sobre ${dataPath}/helios.
    # umask 0002 → los archivos que crea Syncthing nacen con escritura de grupo
    # (0664), de modo que NextCloud pueda modificarlos. Con el setgid del directorio
    # (storage.nix) el grupo de lo nuevo es `storage`.
    systemd.services.syncthing.serviceConfig.UMask = "0002";
  };
}
