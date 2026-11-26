---
title: SMTP
tipo: término
estado: revisado
tags: [comunicaciones, infraestructuras]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/imap.md
    - lenguaje_común/definiciones/federacion.md
  usado_en:
    - midu/servicios/stalwart.md
---

# SMTP

← [Lenguaje común](../lenguaje_común.md)

SMTP (Simple Mail Transfer Protocol) es el protocolo para enviar correo electrónico entre servidores y desde los clientes hacia el servidor. Cuando enviamos un correo, el cliente contacta al servidor SMTP saliente, que lo entrega al servidor SMTP del destinatario. Junto con [IMAP](imap.md), es uno de los protocolos [federados](federacion.md) del correo. En la `midu`, Stalwart implementa SMTP.

## Ver también

- [IMAP](imap.md): el protocolo complementario para recibir correo
- [Stalwart](../../midu/servicios/stalwart.md): el servidor de correo de la `midu`
