---
title: IMAP
tipo: término
estado: revisado
tags: [comunicaciones, infraestructuras]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/smtp.md
    - lenguaje_común/definiciones/federacion.md
  usado_en:
    - midu/servicios/stalwart.md
---

# IMAP

← [Lenguaje común](../lenguaje_común.md)

IMAP (Internet Message Access Protocol) es el protocolo para recibir y sincronizar correo electrónico entre el servidor y los clientes (Thunderbird, Apple Mail, K-9 Mail). A diferencia de POP3, que descarga y borra, IMAP mantiene los correos en el servidor y sincroniza el estado entre varios `dispositivo`s: si marcamos un correo como leído en el teléfono, aparece leído también en el `computador`. En la `midu`, Stalwart implementa IMAP.

## Ver también

- [SMTP](smtp.md): el protocolo complementario para enviar correo
- [Stalwart](../../midu/servicios/stalwart.md): el servidor de correo de la `midu`
