# Ruta B: VPS con Podman

Configuración del VPS con [Podman](../../../base_de_conocimientos/midu/servicios/virtualización.md) y el túnel cifrado para la `midu`.

→ [conectarse a internet: ruta B - VPS con Podman](../../../base_de_conocimientos/conectarse_a_internet/ruta_B-vps+podman.md)

## Archivos de configuración

### VPS

- [`docker-compose.yml`](docker-compose.yml): definición de los servicios del túnel cifrado
- [`config/pangolin.yaml`](config/pangolin.yaml): configuración principal; contiene dominio base y IP pública del VPS
- [`config/gerbil.yaml`](config/gerbil.yaml): configuración del gestor de interfaces [WireGuard](../../../base_de_conocimientos/lenguaje_común/lenguaje_común.md#wireguard)
- [`config/traefik.toml`](config/traefik.toml): configuración del proxy inverso
- [`config/dynamic/routes.toml`](config/dynamic/routes.toml): rutas de tráfico; completar con la IP WireGuard del `computador` local después de la primera conexión [Newt](../../../base_de_conocimientos/midu/servicios/túnel_cifrado.md)
- [`secrets.env.template`](secrets.env.template): plantilla del archivo de secretos; copiar como `secrets.env` y completar con el token de [Pangolin](../../../base_de_conocimientos/midu/servicios/pangolin.md)

### `Computador` local (NixOS)

- [`nixos/modules/nixos/network/newt.nix`](../../nixos/modules/nixos/network/newt.nix): módulo NixOS del cliente Newt; activo con `tunnel_type = "newt"` en `config.nix`
