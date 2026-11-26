---
title: LUKS
tipo: término
estado: revisado
tags: [cuidados, datos]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/initrd.md
    - lenguaje_común/definiciones/uuid.md
  usado_en:
    - midu/replicación/nixos.md
    - midu/replicación/secretos.md
    - midu/arquitectura/almacenamiento_federado.md
---

# LUKS

← [Lenguaje común](../lenguaje_común.md)

LUKS (Linux Unified Key Setup) es el estándar de cifrado de disco completo para Linux. Cifra todos los `datos` del disco a nivel de bloque: sin importar qué sistema de archivos esté dentro, todo se cifra antes de escribirse en el disco físico, y sin la clave correcta el contenido es ruido ilegible. Admite hasta ocho "key slots", varias contraseñas o claves que abren el mismo disco, lo que permite tener una clave de emergencia y otra gestionada automáticamente. En la `midu` cifra los discos del `computador` local.

## Ver también

- [la replicación de NixOS](../../midu/replicación/nixos.md): por qué ciframos los discos
- [el almacenamiento federado](../../midu/arquitectura/almacenamiento_federado.md): el cifrado en las capas de almacenamiento
