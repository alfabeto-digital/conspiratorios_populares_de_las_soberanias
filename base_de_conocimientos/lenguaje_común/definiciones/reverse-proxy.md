---
title: Reverse proxy
tipo: término
estado: revisado
tags: [enrutamiento, infraestructuras]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/caddy.md
  usado_en:
    - midu/servicios/caddy.md
    - midu/servicios/túnel_cifrado.md
---

# Reverse proxy

← [Lenguaje común](../lenguaje_común.md)

Un reverse proxy (proxy inverso) es un servidor intermediario que recibe las solicitudes de los clientes y las reenvía al servicio interno apropiado. Permite tener varios servicios en el mismo servidor usando el mismo puerto (443/HTTPS): el proxy decide a cuál servicio reenviar cada solicitud según el subdominio (`mail.tusitio.com` va al correo, `chat.tusitio.com` va a la mensajería). En la `midu`, [Caddy](caddy.md) cumple este papel en el `computador` local y Traefik lo cumple en el `computador` desechable.

## Ver también

- [Caddy](caddy.md): el reverse proxy del `computador` local
