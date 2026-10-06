# Ruta C: túnel de Cloudflare

Configuración del túnel de Cloudflare para el `computador` local de la `midu`.

→ [conectarse a internet: ruta C - cloudflare](../../../base_de_conocimientos/conectarse_a_internet/ruta_C-cloudflare.md)

## Archivos de configuración

### `Computador` local (NixOS)

- [`nixos/modules/nixos/network/cloudflare.nix`](../../nixos/modules/nixos/network/cloudflare.nix): módulo [NixOS](../../../base_de_conocimientos/lenguaje_común/lenguaje_común.md#nixos) del agente `cloudflared`
- [`nixos/config.nix.template`](../../nixos/config.nix.template): configuración principal; activa el túnel con `tunnel_type = "cloudflare"`
