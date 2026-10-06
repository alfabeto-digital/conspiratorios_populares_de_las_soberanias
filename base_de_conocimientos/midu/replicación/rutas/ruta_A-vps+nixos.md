# Ruta A: VPS con NixOS + Pangolin + Newt

← [Conectarse a internet](../../conectarse_a_internet.md)

## Qué es esta ruta

Esta ruta usa un VPS (Servidor Virtual Privado) propio como punto de entrada público. El tráfico de internet llega al VPS, viaja por un túnel [WireGuard](../../../lenguaje_común/lenguaje_común.md#wireguard) cifrado hasta el `computador` local, y llega a los servicios sin pasar por ninguna empresa externa.

El VPS no almacena nada importante; es descartable. Si fuera comprometido, se destruye y reconstruye en minutos. Los `datos` permanecen en el `computador` local, que no es directamente accesible desde internet.

## Las piezas

### Pangolin: el sistema del túnel cifrado

Pangolin es el sistema que vive en el VPS y gestiona el tráfico. Son tres componentes que trabajan juntos:

- **[Traefik](../../../lenguaje_común/lenguaje_común.md#reverse-proxy)**: recibe el tráfico de internet y lo clasifica por nombre de dominio.
- **Pangolin**: sabe a qué túnel enviar cada petición y gestiona los pares de conexión.
- **[Gerbil](../../servicios/pangolin.md)**: crea y mantiene las interfaces WireGuard.

Más detalle: [Pangolin](../../servicios/pangolin.md)

### Newt: el cliente del túnel

Newt vive en el `computador` local y establece la conexión WireGuard hacia el VPS. Es el extremo del túnel en el lado del `computador` local. La configuración de túnel en `config.nix`:

```nix
tunnel_type = "newt";
```

### WireGuard: el protocolo del túnel

WireGuard es el protocolo VPN que cifra todo el tráfico entre el VPS y el `computador` local. Es moderno, auditable y resistente a cambios de red. Nadie en el camino, ni el proveedor de internet ni el datacenter del VPS, puede leer el contenido del tráfico.

## Por qué NixOS en el VPS

[NixOS](../../arquitectura/nixos.md) permite declarar la configuración completa del VPS en un archivo. Ese archivo vive en el repositorio junto con el resto de la configuración de la `midu`. El VPS es reproducible; se puede destruir y reconstruir con exactamente el mismo estado en cualquier momento.

La herramienta `nixos-anywhere` instala NixOS en un servidor remoto desde la máquina local, sin acceso físico ni ISO de instalación. Solo se necesita acceso [SSH](../../../lenguaje_común/lenguaje_común.md#ssh) con usuario `root`.

Módulo NixOS del VPS: `nixos/modules/nixos/network/pangolin-server.nix`

## Instalación del VPS

El proceso completo de instalación está documentado en:

→ [Despliegue del VPS: Ruta A (NixOS)](../../replicación/vps.md)

Pasos clave:

1. Completar `nixos/config-vps.nix` con el hostname, dominio e IP del VPS.
2. Instalar NixOS en el VPS con `nixos-anywhere`.
3. Generar la clave [`age`](../../arquitectura/secretos.md) del VPS para gestión de secretos con [`sops-nix`](../../arquitectura/secretos.md).
4. Cifrar y desplegar `secrets-vps.yaml`.
5. Activar la configuración con `nixos-rebuild switch`.

## Cuándo elegir esta ruta

- Se quiere [`soberanía`](../../../subjetividades/soberanía_digital.md) completa sobre el tráfico; ninguna empresa externa puede leerlo.
- Se usa NixOS en el `computador` local y se quiere consistencia declarativa también en el VPS.
- Se puede invertir tiempo en la configuración inicial y en mantener el VPS.
- El presupuesto incluye un VPS (entre 4 y 6 USD al mes en proveedores como Hetzner o BuyVM).

## Ver también

- [Pangolin](../../servicios/pangolin.md): el sistema del túnel cifrado
- [El túnel: Cloudflare o Newt](../../servicios/túnel_cifrado.md): análisis de la decisión
- [Despliegue del VPS](../../replicación/vps.md): instrucciones de instalación paso a paso
- [Ruta B: VPS con Podman](ruta_B-vps+podman.md): alternativa si el VPS no corre NixOS
