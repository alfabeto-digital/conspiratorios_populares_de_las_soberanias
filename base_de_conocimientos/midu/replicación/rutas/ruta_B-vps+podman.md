---
title: "Ruta B: VPS con Podman (sin NixOS)"
tipo: ruta
estado: borrador
tags: [replicación, enrutamiento]
relaciones:
  parte_de: midu/replicación.md
  relacionado:
    - midu/arquitectura/conectarse_en_internet.md
    - midu/replicación/rutas/ruta_A-vps+nixos.md
    - midu/servicios/virtualización.md
    - midu/arquitectura/nixos.md
    - lenguaje_común/lenguaje_común.md
    - midu/servicios/pangolin.md
    - midu/replicación/vps.md
    - subjetividades/soberanía_digital.md
    - midu/servicios/túnel_cifrado.md
---

﻿# Ruta B: VPS con Podman (sin NixOS)

← [Conectarse en internet](../../arquitectura/conectarse_en_internet.md)

## Qué es esta ruta

Esta ruta también usa un VPS arrendado como punto de entrada público, igual que la [Ruta A](ruta_A-vps+nixos.md). La diferencia es que el VPS puede correr cualquier sistema operativo Linux, Ubuntu, Debian, Alpine, lo que el proveedor ofrezca, y el túnel cifrado se despliega con [Podman](../../servicios/virtualización.md) en lugar de [NixOS](../../arquitectura/nixos.md).

Es la ruta más directa si ya se tiene un VPS corriendo o si no se quiere gestionar NixOS en el servidor remoto.

## Podman como alternativa libre a Docker

Podman es una alternativa libre y de código abierto a [Docker](../../servicios/virtualización.md). Principales diferencias:

- **Sin demonio en segundo plano**: Docker requiere un proceso central (`dockerd`) corriendo siempre. Podman ejecuta contenedores directamente, sin ese intermediario.
- **Sin raíz por diseño**: Podman puede correr contenedores sin privilegios de superusuario (*rootless*). Docker siempre corre con privilegios de sistema por defecto.
- **Compatible con Docker Compose**: Podman soporta la misma sintaxis de `docker compose`.

**Nota sobre [WireGuard](../../../lenguaje_común/lenguaje_común.md#wireguard)**: [Gerbil](../../servicios/pangolin.md) (el componente de [Pangolin](../../servicios/pangolin.md) que gestiona el túnel WireGuard) necesita la capacidad `NET_ADMIN` para crear interfaces de red. En Podman sin raíz (*rootless*) esa capacidad no está disponible. La solución es ejecutar Podman como `root` en el VPS para este caso específico.

## Qué se necesita en el VPS

Solo el directorio `vps/` del repositorio. Si no se quiere clonar el repositorio completo, se puede usar *sparse checkout*:

```bash
git clone --filter=blob:none --sparse git@github.com:<org>/<repo>.git alfabeto.digital-vps
cd alfabeto.digital-vps
git sparse-checkout set vps
```

`--filter=blob:none` evita descargar el contenido de los archivos hasta que se necesiten. `git sparse-checkout set vps` limita el árbol de trabajo al directorio `vps/`.

## Instalación del VPS

El proceso completo está documentado en:

→ [Despliegue del VPS: Ruta B (Docker/Podman)](../../replicación/vps.md)

Pasos clave:

1. Configurar `vps/config/pangolin.yaml` con el dominio y la IP pública del VPS.
2. Configurar las rutas de tráfico en `vps/config/dynamic/routes.toml`.
3. Copiar `vps/secrets.env.template` a `vps/secrets.env` y completar el token de Pangolin.
4. Levantar los servicios con `podman compose up -d`.
5. Después de la primera conexión Newt, anotar la IP WireGuard asignada y actualizar `routes.toml`.

Los secretos se gestionan con un archivo `.env` plano. Es más directo, pero requiere cuidado para no exponer el archivo en el repositorio.

## Actualizar el VPS

```bash
git pull && podman compose pull && podman compose up -d
```

Los `datos` persisten porque están en volúmenes de Podman, no en el contenedor.

## Cuándo elegir esta ruta

- El VPS ya existe y corre otro sistema operativo (no NixOS).
- Se quiere [`soberanía`](../../../subjetividades/soberanía_digital.md) sobre el tráfico sin gestionar NixOS en el servidor remoto.
- Se prefiere Podman sobre Docker por sus garantías de libertad de software.
- La configuración declarativa de NixOS no es una prioridad para el VPS.

## Los archivos de la ruta

El despliegue de esta ruta vive en `midu/conectarse_a_internet/ruta_B-vps+podman/`. Estos son sus archivos:

- [setup.sh](../../../../midu/conectarse_a_internet/ruta_B-vps+podman/setup.sh): el script que prepara el VPS y levanta el stack
- [docker-compose.yml](../../../../midu/conectarse_a_internet/ruta_B-vps+podman/docker-compose.yml): la definición de los contenedores de Pangolin, Gerbil y Traefik
- [config/pangolin.yaml](../../../../midu/conectarse_a_internet/ruta_B-vps+podman/config/pangolin.yaml): el dominio y la IP pública del VPS
- [config/gerbil.yaml](../../../../midu/conectarse_a_internet/ruta_B-vps+podman/config/gerbil.yaml): la configuración del gestor de túneles WireGuard
- [config/traefik.toml](../../../../midu/conectarse_a_internet/ruta_B-vps+podman/config/traefik.toml): la configuración del proxy de entrada
- [config/dynamic/routes.toml](../../../../midu/conectarse_a_internet/ruta_B-vps+podman/config/dynamic/routes.toml): las rutas de tráfico hacia el `computador` local
- [secrets.env.template](../../../../midu/conectarse_a_internet/ruta_B-vps+podman/secrets.env.template): la plantilla del token de Pangolin y demás secretos
- [README.md](../../../../midu/conectarse_a_internet/ruta_B-vps+podman/README.md): las instrucciones del despliegue
- [.gitignore](../../../../midu/conectarse_a_internet/ruta_B-vps+podman/.gitignore): los archivos que no van a git

## Ver también

- [Pangolin](../../servicios/pangolin.md): el sistema del túnel cifrado
- [El túnel: Cloudflare o Newt](../../servicios/túnel_cifrado.md): análisis de la decisión
- [Despliegue del VPS](../../replicación/vps.md): instrucciones de instalación paso a paso
- [Ruta A: VPS con NixOS](ruta_A-vps+nixos.md): alternativa declarativa con NixOS
