# virtualización

← [Servicios](servicios.md)

## qué es la virtualización

La virtualización de procesos es una técnica que permite ejecutar múltiples aplicaciones aisladas en un mismo sistema operativo, como si cada una viviera en su propio entorno separado. A diferencia de las máquinas virtuales, que simulan hardware completo, los contenedores comparten el núcleo del sistema operativo y son mucho más ligeros.

El estándar para definir estos entornos es la imagen de contenedor: un archivo que describe exactamente qué programas, bibliotecas y configuración necesita una aplicación para correr, independiente del sistema donde se ejecute.

## Docker

Docker popularizó los contenedores. Su modelo requiere un proceso central, `dockerd`, que corre en segundo plano con privilegios de sistema y gestiona todos los contenedores. Las aplicaciones se definen en archivos `docker compose` que describen qué imágenes corren, cómo se comunican entre sí y qué `datos` persisten.

Es el estándar de facto en la industria y la referencia que usan la mayoría de las documentaciones de software.

## Podman: la alternativa libre

[Podman](https://podman.io/) es una alternativa libre y de código abierto a Docker. Las diferencias principales:

- **Sin demonio en segundo plano**: Docker requiere `dockerd` corriendo siempre con privilegios de sistema. Podman ejecuta cada contenedor como un proceso directo.
- **Rootless por diseño**: Podman puede correr contenedores sin privilegios de superusuario. Reduce la superficie de ataque en caso de que un contenedor sea comprometido.
- **Compatible con Docker Compose**: Podman entiende la misma sintaxis de `docker compose`. Los archivos de configuración son intercambiables.

## en la `midu`

La Ruta B del túnel de internet despliega el stack del VPS (Traefik, Pangolin, Gerbil) con Podman en lugar de NixOS. Es la opción cuando el VPS corre cualquier distribución Linux y no se quiere gestionar NixOS en el servidor remoto.

**Nota sobre NET_ADMIN:** [Gerbil](pangolin.md), el componente que crea las interfaces WireGuard, necesita la capacidad `NET_ADMIN` del sistema operativo. En Podman rootless esa capacidad no está disponible. La solución es ejecutar Podman como `root` en el VPS para este caso específico.

La Ruta A (VPS con NixOS) también puede usar Podman o Docker como `container_runtime` alternativo al modo nativo de NixOS. El módulo `pangolin-server.nix` expone la variable `container_runtime` con tres opciones: `flake` (NixOS nativo), `podman`, `docker`.

## Ver también

- [Pangolin](pangolin.md): el stack del túnel cifrado que se puede desplegar con Podman
- [el túnel: Cloudflare o Newt](túnel.md): análisis de las opciones de conexión al VPS
- [conectarse a internet: ruta B - VPS con Podman](../replicación/rutas/ruta_B-vps+podman.md): la guía completa para la ruta con Podman
