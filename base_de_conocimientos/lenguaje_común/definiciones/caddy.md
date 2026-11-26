---
title: Caddy
tipo: término
estado: revisado
tags: [enrutamiento, infraestructuras]
icono: lenguaje_común/objetos_digitales/midu/digital_infrastructures/caddy.png
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/reverse-proxy.md
    - lenguaje_común/definiciones/tls.md
    - lenguaje_común/definiciones/acme.md
  define: midu/servicios/caddy.md
  usado_en:
    - midu/servicios/túnel_cifrado.md
    - midu/replicación/configuración.md
---

# Caddy

← [Lenguaje común](../lenguaje_común.md)

Servidor web y [reverse proxy](reverse-proxy.md) que recibe las solicitudes HTTPS entrantes y las reenvía al servicio correcto según el subdominio, con renovación automática de certificados [TLS](tls.md) vía [ACME](acme.md). En la `midu` es la puerta de entrada de todo el tráfico web hacia el `computador` local.

La descripción completa (configuración, lugar en la arquitectura y módulo NixOS) está en [Caddy](../../midu/servicios/caddy.md).

## Ver también

- [Caddy](../../midu/servicios/caddy.md): el artículo completo del servicio
- [el túnel cifrado](../../midu/servicios/túnel_cifrado.md): cómo llega el tráfico hasta Caddy
