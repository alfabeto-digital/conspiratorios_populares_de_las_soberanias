---
title: VPS
tipo: término
estado: revisado
tags: [infraestructuras, enrutamiento]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/ip.md
    - lenguaje_común/definiciones/isp.md
    - lenguaje_común/definiciones/wireguard.md
  define: midu/replicación/vps.md
---

# VPS

← [Lenguaje común](../lenguaje_común.md)

Un VPS (Virtual Private Server) es un servidor virtual alquilado a un proveedor de nube (Hetzner, DigitalOcean, Vultr, OVH): una porción de un servidor físico particionada con virtualización. En la `midu`, el VPS arrendado tiene una [IP](ip.md) pública fija y actúa como `computador` desechable, el punto de entrada del tráfico que lo reenvía al `computador` local, que puede estar detrás de una red doméstica. Se arrienda por pocos euros al mes; destruirlo no hace perder ningún `dato`.

La descripción completa está en [el VPS](../../midu/replicación/vps.md).

## Ver también

- [el VPS](../../midu/replicación/vps.md): la replicación del `computador` desechable
- [WireGuard](wireguard.md): el túnel entre el VPS y el `computador` local
