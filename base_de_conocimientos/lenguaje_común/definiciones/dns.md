---
title: DNS
tipo: término
estado: revisado
tags: [enrutamiento, infraestructuras]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/ip.md
    - lenguaje_común/definiciones/registrador-de-dominio.md
  usado_en:
    - midu/servicios/adguard.md
---

# DNS

← [Lenguaje común](../lenguaje_común.md)

DNS (Domain Name System) es el directorio telefónico de internet: convierte nombres de dominio legibles por personas (`alfabeto.digital`, `mail.tusitio.com`) en direcciones [IP](ip.md) numéricas que las computadoras usan para comunicarse. Cuando escribimos una URL en el navegador, la computadora consulta primero un servidor DNS para saber a qué IP dirigirse. En la `midu`, AdGuard resuelve estas consultas localmente.

## Ver también

- [AdGuard](../../midu/servicios/adguard.md): el servidor DNS local de la `midu`
- [el registrador de dominio](registrador-de-dominio.md): quién decide qué servidor DNS responde por un nombre
