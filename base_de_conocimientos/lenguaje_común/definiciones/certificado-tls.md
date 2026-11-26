---
title: Certificado TLS
tipo: término
estado: revisado
tags: [enrutamiento, cuidados]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/tls.md
    - lenguaje_común/definiciones/lets-encrypt.md
    - lenguaje_común/definiciones/acme.md
---

# Certificado TLS

← [Lenguaje común](../lenguaje_común.md)

Documento digital que certifica la identidad de un servidor y habilita la comunicación cifrada (HTTPS), el equivalente a un documento de identidad para un sitio web. Lo emite una autoridad certificadora de confianza, como [Let's Encrypt](lets-encrypt.md), después de verificar que quien lo solicita controla el dominio. Sin un certificado válido, los navegadores muestran la advertencia de "conexión no segura". Es la pieza que hace posible [TLS](tls.md).

## Ver también

- [TLS](tls.md): el protocolo de cifrado que el certificado habilita
- [ACME](acme.md): cómo se obtiene y renueva el certificado automáticamente
