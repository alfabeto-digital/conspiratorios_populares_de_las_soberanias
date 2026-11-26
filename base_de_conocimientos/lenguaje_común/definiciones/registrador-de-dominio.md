---
title: Registrador de dominio
tipo: término
estado: revisado
tags: [enrutamiento, infraestructuras]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/dns.md
  usado_en:
    - midu/arquitectura/conectarse_en_internet.md
---

# Registrador de dominio

← [Lenguaje común](../lenguaje_común.md)

Empresa acreditada para vender y gestionar nombres de dominio. Mantiene el registro oficial de quién es el propietario y controla qué servidores de nombres son autoritativos para ese dominio, es decir, qué servidor [DNS](dns.md) responde las consultas sobre ese nombre. Cambiar los nameservers en el registrador redirige todas las consultas hacia otro proveedor. Algunos registradores comunes son Namecheap, Porkbun, Gandi y Cloudflare Registrar.

## Ver también

- [conectarse en internet: ISP, DNS y registrador de dominio](../../midu/arquitectura/conectarse_en_internet.md)
