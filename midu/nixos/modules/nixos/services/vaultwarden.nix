{ inputs, ... }: {
  flake.nixosModules.vaultwarden = { config, lib, pkgs, cfg, servicesPath, pkgsUnstable, ... }: {

    systemd.tmpfiles.rules = [
      "d ${servicesPath}/vaultwarden 0750 vaultwarden vaultwarden - -"
    ];

    systemd.services.vaultwarden = {
      serviceConfig = {
        ReadWritePaths = [ "${servicesPath}/vaultwarden" ];
        ProtectHome    = lib.mkForce "no";
      };
    };

    services.vaultwarden = {
      enable  = true;
      package = pkgsUnstable.vaultwarden;
      config = {
        DOMAIN         = "https://warden.${cfg.domain}";
        ROCKET_ADDRESS = "0.0.0.0";
        ROCKET_PORT    = cfg.vaultwarden_port;
        DATA_FOLDER    = "${servicesPath}/vaultwarden";
      };
    };
  };
}
