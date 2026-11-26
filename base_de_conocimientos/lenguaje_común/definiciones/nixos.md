---
title: NixOS
tipo: término
estado: revisado
tags: [infraestructuras]
icono: lenguaje_común/objetos_digitales/midu/digital_infrastructures/operating_system_nixos.png
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/rollback.md
    - lenguaje_común/definiciones/flake.md
    - lenguaje_común/definiciones/modulo-nixos.md
  define: midu/arquitectura/nixos.md
---

# NixOS

← [Lenguaje común](../lenguaje_común.md)

Distribución de Linux con configuración declarativa y reproducible. En lugar de instalar paquetes con comandos que modifican el sistema de forma incremental, NixOS describe el estado completo del sistema en archivos `.nix` y lo construye; si algo falla, vuelve al estado anterior ([rollback](rollback.md)). El mismo archivo de configuración produce el mismo sistema en cualquier hardware.

La descripción completa está en [NixOS](../../midu/arquitectura/nixos.md).

## Ver también

- [NixOS](../../midu/arquitectura/nixos.md): el artículo completo
- [Rollback](rollback.md) y [Flake](flake.md): dos piezas de su reproducibilidad
