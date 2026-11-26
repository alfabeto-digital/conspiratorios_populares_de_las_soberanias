---
title: NVMe
tipo: término
estado: revisado
tags: [infraestructuras]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/uuid.md
    - lenguaje_común/definiciones/luks.md
  usado_en:
    - midu/replicación/nixos.md
---

# NVMe

← [Lenguaje común](../lenguaje_común.md)

NVMe (Non-Volatile Memory Express) es un tipo de disco de estado sólido de alta velocidad que se conecta directamente al bus PCIe del `computador`, a diferencia de los discos SATA, que usan una `interfaz` más lenta. Los discos NVMe son mucho más rápidos en lectura y escritura aleatoria, lo que beneficia a bases de `datos` como [PostgreSQL](../../midu/servicios/postgresql.md). Se identifican como `/dev/nvme0n1`, `/dev/nvme1n1`, etc.

## Ver también

- [la replicación de NixOS](../../midu/replicación/nixos.md): los prerequisitos de disco
- [UUID](uuid.md): cómo identificamos cada disco de forma estable
