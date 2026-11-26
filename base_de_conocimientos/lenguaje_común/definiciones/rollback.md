---
title: Rollback
tipo: término
estado: revisado
tags: [infraestructuras]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/nixos.md
  usado_en:
    - midu/arquitectura/nixos.md
---

# Rollback

← [Lenguaje común](../lenguaje_común.md)

En [NixOS](nixos.md), el rollback es la capacidad de volver al instante a una configuración anterior del sistema. NixOS guarda cada "generación" del sistema construido, así que si una actualización rompe algo, podemos volver a la generación anterior desde el menú de arranque (GRUB) o con `nixos-rebuild switch --rollback`, sin pérdida de `datos`. Es el Ctrl+Z del sistema.

## Ver también

- [NixOS](../../midu/arquitectura/nixos.md): la configuración declarativa que hace posible el rollback
