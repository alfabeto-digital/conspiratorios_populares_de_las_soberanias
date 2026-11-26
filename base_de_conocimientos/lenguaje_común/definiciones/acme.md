---
title: ACME
tipo: término
estado: revisado
tags: [enrutamiento, infraestructuras]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/tls.md
    - lenguaje_común/definiciones/lets-encrypt.md
  usado_en:
    - midu/servicios/caddy.md
    - midu/replicación/configuración.md
---

# ACME

← [Lenguaje común](../lenguaje_común.md)

**ACME** (Automatic Certificate Management Environment) es el protocolo estándar para obtener certificados [TLS](tls.md) de manera automática. [Let's Encrypt](lets-encrypt.md) lo implementa: en lugar de configurar el certificado a mano cada vez, el servidor demuestra que controla el dominio, respondiendo a un desafío HTTP o DNS, y recibe el certificado sin intervención manual. [Caddy](../../midu/servicios/caddy.md) usa ACME para que todos los servicios tengan HTTPS desde el primer arranque.

## Ver también

- [Caddy](../../midu/servicios/caddy.md): el proxy inverso que gestiona los certificados ACME
- [configuración de la replicación: red y dominio](../../midu/replicación/configuración.md)
