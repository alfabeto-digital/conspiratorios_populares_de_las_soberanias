---
title: IP
tipo: término
estado: revisado
tags: [enrutamiento, infraestructuras]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/dns.md
    - lenguaje_común/definiciones/isp.md
    - lenguaje_común/definiciones/vps.md
---

# IP

← [Lenguaje común](../lenguaje_común.md)

Una dirección IP (Internet Protocol) es el número único que identifica un `dispositivo` en internet. Coexisten dos formatos: IPv4 (cuatro grupos de números, p. ej. `203.0.113.42`) e IPv6 (ocho grupos hexadecimales, p. ej. `2001:db8::1`). Los servidores necesitan una IP pública fija para ser accesibles desde internet. Los routers domésticos suelen asignar IPs privadas (`192.168.x.x`, `10.x.x.x`) que no son accesibles directamente desde afuera, y por eso la `midu` usa un [VPS](vps.md) con IP pública como `computador` desechable.

## Ver también

- [DNS](dns.md): cómo un nombre de dominio se traduce a una IP
- [VPS](vps.md): el servidor con IP pública que la `midu` usa como puerta de entrada
