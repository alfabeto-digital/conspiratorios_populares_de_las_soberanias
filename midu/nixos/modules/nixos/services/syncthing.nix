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
  };
}
