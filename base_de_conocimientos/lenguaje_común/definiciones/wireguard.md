---
title: WireGuard
tipo: término
estado: revisado
tags: [enrutamiento, cuidados]
icono: lenguaje_común/objetos_digitales/midu/digital_infrastructures/wireguard.png
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/mitm.md
    - lenguaje_común/definiciones/vps.md
  define: midu/servicios/túnel_cifrado.md
---

# WireGuard

← [Lenguaje común](../lenguaje_común.md)

Protocolo VPN moderno, eficiente y de código pequeño y auditado. Crea túneles cifrados entre `dispositivo`s con criptografía de clave pública. En la `midu` conecta el `computador` desechable (un [VPS](vps.md)) con el `computador` local: el tráfico público llega al VPS y viaja por el túnel WireGuard hasta el `computador` local, sin que el VPS pueda ver el contenido cifrado de extremo a extremo. Gerbil, parte del stack Pangolin, gestiona las interfaces WireGuard.

La descripción completa está en [el túnel cifrado](../../midu/servicios/túnel_cifrado.md).

## Ver también

- [el túnel cifrado](../../midu/servicios/túnel_cifrado.md): cómo se establece el túnel
- [MITM](mitm.md): por qué el túnel con WireGuard evita que el intermediario lea el tráfico
