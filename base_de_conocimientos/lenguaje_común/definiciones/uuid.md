---
title: UUID
tipo: término
estado: revisado
tags: [infraestructuras]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/nvme.md
    - lenguaje_común/definiciones/luks.md
  usado_en:
    - midu/replicación/nixos.md
    - midu/replicación/configuración.md
---

# UUID

← [Lenguaje común](../lenguaje_común.md)

Un UUID (Universally Unique Identifier) es un identificador único de 128 bits, representado como 32 dígitos hexadecimales en el formato `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`. Los discos reciben un UUID al formatearse. Su ventaja sobre el nombre del `dispositivo` (`/dev/nvme1n1`) es la estabilidad: el nombre puede cambiar si se conectan discos nuevos o cambia el orden de arranque, pero el UUID identifica el disco sin importar dónde esté conectado. Por eso la `midu` monta los discos por UUID.

## Ver también

- [la replicación de NixOS](../../midu/replicación/nixos.md): cómo obtener el UUID de un disco
- [configuración de la replicación](../../midu/replicación/configuración.md): discos y puntos de montaje
