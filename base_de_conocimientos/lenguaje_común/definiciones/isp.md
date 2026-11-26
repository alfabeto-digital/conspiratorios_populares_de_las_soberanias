---
title: ISP
tipo: término
estado: revisado
tags: [enrutamiento, infraestructuras]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/ip.md
    - lenguaje_común/definiciones/vps.md
    - lenguaje_común/definiciones/dns.md
  usado_en:
    - midu/arquitectura/conectarse_en_internet.md
---

# ISP

← [Lenguaje común](../lenguaje_común.md)

El ISP (Internet Service Provider, proveedor de acceso a internet) es la empresa que conecta hogares u oficinas con internet. Asigna una dirección [IP](ip.md) al router; en contratos residenciales esa IP es dinámica y puede cambiar sin aviso. Los ISP residenciales también suelen bloquear los puertos de entrada estándar (80 y 443), lo que impide recibir conexiones externas directas. Por eso la `midu` usa un `computador` desechable con IP pública fija, un [VPS](vps.md) o Cloudflare, en lugar de exponer el `computador` local directamente a internet.

## Ver también

- [conectarse en internet](../../midu/arquitectura/conectarse_en_internet.md): el papel del ISP en la ruta del tráfico
- [VPS](vps.md): el intermediario con IP pública que sortea las limitaciones del ISP
