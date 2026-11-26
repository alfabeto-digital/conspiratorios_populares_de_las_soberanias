---
title: initrd
tipo: término
estado: revisado
tags: [infraestructuras, cuidados]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/luks.md
    - lenguaje_común/definiciones/ssh.md
    - lenguaje_común/definiciones/nixos.md
  usado_en:
    - midu/replicación/nixos.md
---

# initrd

← [Lenguaje común](../lenguaje_común.md)

initrd (initial RAM disk) es el sistema de archivos mínimo que NixOS carga en memoria durante los primeros segundos del arranque, antes de que los discos reales estén disponibles. Contiene lo imprescindible para montar el sistema de archivos principal. En la `midu` añadimos un servidor [SSH](ssh.md) al initrd para desbloquear de forma remota el disco cifrado con [LUKS](luks.md) de `nvme0` tras un reinicio, sin necesidad de acceso físico al servidor.

## Ver también

- [la replicación de NixOS](../../midu/replicación/nixos.md): SSH en el initrd y desbloqueo remoto
- [LUKS](luks.md): el cifrado de disco que el initrd ayuda a desbloquear
