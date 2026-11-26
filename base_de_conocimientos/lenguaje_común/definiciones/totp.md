---
title: TOTP
tipo: término
estado: revisado
tags: [cuidados]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/sso.md
  usado_en:
    - midu/servicios/authelia.md
---

# TOTP

← [Lenguaje común](../lenguaje_común.md)

TOTP (Time-based One-Time Password) es un código de seis dígitos que cambia cada 30 segundos, generado por una app de autenticación (Aegis, Authy, Google Authenticator). Es el segundo factor de autenticación (2FA) más común: la clave secreta compartida entre el servidor y la app genera el mismo código en el mismo instante, lo que permite verificar la identidad sin transmitir la contraseña. Si alguien roba nuestra contraseña, todavía necesita acceso físico al `dispositivo` con la app de TOTP.

## Ver también

- [Authelia](../../midu/servicios/authelia.md): el servicio que verifica el segundo factor
- [SSO](sso.md): el inicio de sesión único al que acompaña
