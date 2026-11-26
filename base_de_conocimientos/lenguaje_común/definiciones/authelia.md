---
title: Authelia
tipo: término
estado: revisado
tags: [cuidados]
icono: lenguaje_común/objetos_digitales/midu/digital_infrastructures/authelia.png
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/sso.md
    - lenguaje_común/definiciones/totp.md
    - lenguaje_común/definiciones/zero-trust.md
  define: midu/servicios/authelia.md
---

# Authelia

← [Lenguaje común](../lenguaje_común.md)

Servidor de autenticación [SSO](sso.md) y segundo factor [TOTP](totp.md). Actúa como portero central: todos los servicios que requieren inicio de sesión pasan primero por Authelia, que verifica la identidad. Implementa el modelo [Zero Trust](zero-trust.md).

La descripción completa está en [Authelia](../../midu/servicios/authelia.md).

## Ver también

- [Authelia](../../midu/servicios/authelia.md): el artículo completo del servicio
