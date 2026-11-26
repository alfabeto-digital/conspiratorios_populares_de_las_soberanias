---
title: age
tipo: término
estado: revisado
tags: [cuidados, datos]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/sops.md
  define: midu/arquitectura/secretos.md
  usado_en:
    - midu/arquitectura/secretos.md
    - midu/replicación/secretos.md
---

# age

← [Lenguaje común](../lenguaje_común.md)

Herramienta moderna de cifrado de archivos con clave pública y privada: cada máquina o persona tiene una clave pública, que puede compartirse, y una privada, que nunca se comparte. Lo que se cifra con la pública solo se descifra con la privada correspondiente. En la `midu`, cada servidor tiene su propia clave age para descifrar sus secretos, y [sops](sops.md) la usa para cifrarlos dentro del repositorio.

## Ver también

- [los secretos](../../midu/arquitectura/secretos.md): cómo la `midu` cifra con age y sops
