---
title: Principio de menor privilegio
tipo: término
estado: revisado
tags: [cuidados]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/zero-trust.md
  usado_en:
    - midu/cuidados/zero-trust.md
---

# Principio de menor privilegio

← [Lenguaje común](../lenguaje_común.md)

Dar a cada componente del sistema solo los permisos que necesita para funcionar, y nada más. Un servicio de correo no necesita acceso a la base de `datos` de mensajería; un proceso de usuario no necesita permisos de root. El principio limita el daño posible si un componente se compromete: quien compromete un servicio solo obtiene los permisos de ese servicio. Es uno de los fundamentos de los [`cuidados`](../../midu/cuidados.md) de la `midu`.

## Ver también

- [desconfiar de los intermediarios: Zero Trust](zero-trust.md): el modelo de seguridad que lo acompaña
