---
title: Let's Encrypt
tipo: término
estado: revisado
tags: [enrutamiento, cuidados]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/acme.md
    - lenguaje_común/definiciones/tls.md
    - lenguaje_común/definiciones/certificado-tls.md
---

# Let's Encrypt

← [Lenguaje común](../lenguaje_común.md)

Autoridad de certificación gratuita, automática y abierta. Emite certificados [TLS](tls.md) válidos mediante el protocolo [ACME](acme.md), que servidores como [Caddy](../../midu/servicios/caddy.md) implementan de forma nativa, y los renueva automáticamente cada 90 días. Antes de Let's Encrypt, obtener un certificado TLS costaba dinero y requería un proceso manual; desde 2016 cualquier servidor puede tener HTTPS gratuito.

## Ver también

- [ACME](acme.md): el protocolo con el que Let's Encrypt emite los certificados
- [Caddy](../../midu/servicios/caddy.md): el servicio que los solicita y renueva
