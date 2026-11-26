---
title: Zero Trust
tipo: término
estado: revisado
tags: [cuidados]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/authelia.md
    - lenguaje_común/definiciones/principio-de-menor-privilegio.md
    - lenguaje_común/definiciones/sso.md
  define: midu/cuidados/zero-trust.md
---

# Zero Trust

← [Lenguaje común](../lenguaje_común.md)

Modelo de seguridad que no confía en ningún componente por defecto, sin importar su posición en la red ("dentro" o "fuera" del perímetro): cada solicitud debe autenticarse y autorizarse de forma explícita. Contrasta con el modelo perimetral, donde todo lo que está "dentro de la red" se considera de confianza. En la `midu`, [Authelia](authelia.md) lo implementa: todos los servicios requieren autenticación, incluso desde la red local.

La descripción completa está en [desconfiar de los intermediarios](../../midu/cuidados/zero-trust.md).

## Ver también

- [desconfiar de los intermediarios](../../midu/cuidados/zero-trust.md): el artículo completo de los `cuidados`
- [el principio de menor privilegio](principio-de-menor-privilegio.md): el complemento de Zero Trust
