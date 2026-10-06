# Ruta A: VPS con NixOS + Pangolin + Newt

Configuración del VPS con [NixOS](../../../base_de_conocimientos/midu/arquitectura/nixos.md) y el túnel cifrado para la `midu`.

→ [conectarse a internet: ruta A - VPS con NixOS](../../../base_de_conocimientos/conectarse_a_internet/ruta_A-vps+nixos.md)

## Archivos de configuración

### VPS (NixOS)

- [`.sops-vps.yaml.template`](.sops-vps.yaml.template): plantilla de configuración [sops](../../../base_de_conocimientos/midu/arquitectura/secretos.md); copiar como `.sops.yaml` en el VPS y completar con la clave [age](../../../base_de_conocimientos/midu/arquitectura/secretos.md) pública
- [`nixos/config-vps.nix.template`](../../nixos/config-vps.nix.template): configuración declarativa del VPS; contiene hostname, dominio e IP
- [`nixos/modules/nixos/network/pangolin-server.nix`](../../nixos/modules/nixos/network/pangolin-server.nix): módulo NixOS del túnel cifrado
- [`nixos/secrets/secrets-vps.plain.template`](../../nixos/secrets/secrets-vps.plain.template): plantilla de secretos del VPS

### `Computador` local (NixOS)

- [`nixos/modules/nixos/network/newt.nix`](../../nixos/modules/nixos/network/newt.nix): módulo NixOS del cliente [Newt](../../../base_de_conocimientos/midu/servicios/túnel_cifrado.md); activo con `tunnel_type = "newt"` en `config.nix`
