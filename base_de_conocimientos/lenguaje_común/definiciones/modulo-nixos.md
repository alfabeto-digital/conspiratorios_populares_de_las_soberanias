---
title: Módulo NixOS
tipo: término
estado: revisado
tags: [infraestructuras]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/nixos.md
    - lenguaje_común/definiciones/flake.md
  define: midu/arquitectura/nixos.md
---

# Módulo NixOS

← [Lenguaje común](../lenguaje_común.md)

Archivo `.nix` que describe una parte del sistema: un servicio, una configuración de red, un conjunto de paquetes. Los módulos se combinan para construir la configuración completa. La arquitectura modular permite activar o desactivar un servicio con una sola línea y mantener cada parte del sistema en su propio archivo.

La descripción completa está en [NixOS](../../midu/arquitectura/nixos.md).

## Ver también

- [NixOS](../../midu/arquitectura/nixos.md): cómo se organizan y combinan los módulos
