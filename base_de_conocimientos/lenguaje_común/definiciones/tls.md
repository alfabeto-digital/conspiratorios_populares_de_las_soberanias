---
title: TLS
tipo: término
estado: revisado
tags: [enrutamiento, cuidados]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/certificado-tls.md
    - lenguaje_común/definiciones/acme.md
    - lenguaje_común/definiciones/lets-encrypt.md
---

# TLS

← [Lenguaje común](../lenguaje_común.md)

TLS (Transport Layer Security) es el protocolo de cifrado para las comunicaciones en internet; HTTPS es HTTP sobre TLS. Garantiza dos cosas: que la comunicación entre el cliente y el servidor está cifrada, de modo que nadie puede interceptarla, y que el servidor es quien dice ser, mediante un [certificado TLS](certificado-tls.md). Sustituye al protocolo SSL, obsoleto e inseguro.

## Ver también

- [Certificado TLS](certificado-tls.md): el documento que autentica al servidor
- [ACME](acme.md) y [Let's Encrypt](lets-encrypt.md): cómo se obtienen los certificados automáticamente
