---
title: Flake
tipo: término
estado: revisado
tags: [infraestructuras]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/nixos.md
    - lenguaje_común/definiciones/modulo-nixos.md
  define: midu/arquitectura/flake.md
---

# Flake

← [Lenguaje común](../lenguaje_común.md)

Sistema de gestión de configuración y dependencias para [NixOS](nixos.md). El archivo `flake.nix` define las entradas (qué versiones de paquetes usar y de dónde) y las salidas (los sistemas a construir), y el `flake.lock` fija las versiones exactas, de modo que el sistema construido hoy sea idéntico al de dentro de seis meses.

La descripción completa está en [el flake](../../midu/arquitectura/flake.md).

## Ver también

- [el flake](../../midu/arquitectura/flake.md): el artículo completo
- [NixOS](nixos.md): la distribución que el flake configura
