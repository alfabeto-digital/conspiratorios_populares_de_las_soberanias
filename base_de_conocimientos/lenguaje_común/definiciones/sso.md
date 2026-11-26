---
title: SSO
tipo: término
estado: revisado
tags: [cuidados]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/totp.md
    - lenguaje_común/definiciones/zero-trust.md
  usado_en:
    - midu/servicios/authelia.md
---

# SSO

← [Lenguaje común](../lenguaje_común.md)

SSO (Single Sign-On) es el sistema de autenticación donde una sola cuenta y contraseña dan acceso a múltiples servicios. En lugar de recordar credenciales distintas para el correo, la mensajería o el almacenamiento, nos autenticamos una vez con [Authelia](../../midu/servicios/authelia.md) y accedemos a todos los servicios de la `midu`.

## Ver también

- [Authelia](../../midu/servicios/authelia.md): el servidor de SSO de la `midu`
- [TOTP](totp.md): el segundo factor que acompaña al inicio de sesión
