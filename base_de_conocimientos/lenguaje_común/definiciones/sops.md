---
title: sops
tipo: término
estado: revisado
tags: [cuidados, datos]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/age.md
  define: midu/arquitectura/secretos.md
---

# sops

← [Lenguaje común](../lenguaje_común.md)

sops (Secrets OPerationS) es una herramienta de gestión de secretos que integra el cifrado ([age](age.md), PGP, AWS KMS) con repositorios git. Permite guardar archivos cifrados en git de forma segura: cifra los valores pero preserva la estructura del archivo (YAML, JSON), de modo que se ve qué claves existen sin revelar sus valores. Se configura con `.sops.yaml`, que indica con qué claves cifrar cada archivo.

La descripción completa está en [los secretos](../../midu/arquitectura/secretos.md).

## Ver también

- [los secretos](../../midu/arquitectura/secretos.md): cómo la `midu` gestiona el cifrado con sops y age
- [age](age.md): la herramienta de cifrado que sops usa
