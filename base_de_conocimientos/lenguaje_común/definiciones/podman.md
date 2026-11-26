---
title: Podman
tipo: término
estado: revisado
tags: [infraestructuras, cuidados]
icono: lenguaje_común/objetos_digitales/midu/digital_infrastructures/podman.png
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/docker.md
  define: midu/servicios/virtualización.md
---

# Podman

← [Lenguaje común](../lenguaje_común.md)

Alternativa a [Docker](docker.md) para ejecutar contenedores, compatible con los mismos formatos e instrucciones, pero con una diferencia importante: puede correr sin privilegios de root (rootless), lo que reduce la superficie de ataque. En la `midu`, el `computador` desechable de la Ruta B puede usar Podman, con la salvedad de que WireGuard requiere permisos de red (NET_ADMIN) que en Podman rootless no están disponibles.

La descripción completa está en [Virtualización](../../midu/servicios/virtualización.md).

## Ver también

- [Virtualización](../../midu/servicios/virtualización.md): Docker y Podman en la `midu`
