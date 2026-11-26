---
title: UPS
tipo: término
estado: revisado
tags: [infraestructuras]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/nvme.md
---

# UPS

← [Lenguaje común](../lenguaje_común.md)

Un UPS (Uninterruptible Power Supply, sistema de alimentación ininterrumpida) es un `dispositivo` que combina batería y regulador de voltaje. Mantiene el suministro eléctrico durante cortes breves y, cuando la batería se agota, avisa al `computador` para que se apague de forma ordenada antes de quedarse sin energía. Un apagado abrupto puede corromper los `datos` que se estaban escribiendo en disco. Para el `computador` local de la `midu`, que está encendido de forma continua, recomendamos un UPS de 600 a 1000 VA, suficiente para un mini-PC de bajo consumo.

## Ver también

- [las capas de la memoria](../../midu/arquitectura/capas_de_la_memoria.md): dónde encaja la resiliencia física
