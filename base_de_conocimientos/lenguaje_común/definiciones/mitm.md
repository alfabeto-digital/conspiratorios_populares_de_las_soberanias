---
title: MITM
tipo: término
estado: revisado
tags: [cuidados, enrutamiento]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/wireguard.md
  usado_en:
    - midu/servicios/túnel_cifrado.md
    - midu/cuidados/zero-trust.md
---

# MITM

← [Lenguaje común](../lenguaje_común.md)

MITM (Man In The Middle) es un ataque, o una configuración intencional, donde un tercero se interpone entre dos partes que se comunican y puede leer o modificar los mensajes. En la `midu`, Cloudflare Tunnel es técnicamente un MITM benigno: el tráfico HTTPS llega a Cloudflare, que lo descifra, lo reenvía al servidor y lo cifra de nuevo, de modo que Cloudflare puede ver el contenido. La alternativa sin MITM es el túnel con [WireGuard](wireguard.md) y Newt, donde el `computador` desechable nunca ve el contenido cifrado de extremo a extremo.

## Ver también

- [el túnel cifrado](../../midu/servicios/túnel_cifrado.md): las rutas con y sin MITM
- [desconfiar de los intermediarios](../../midu/cuidados/zero-trust.md): por qué asumimos que el intermediario puede leer el tráfico
