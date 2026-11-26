---
title: SSH
tipo: término
estado: revisado
tags: [infraestructuras, cuidados]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/definiciones/initrd.md
  usado_en:
    - midu/servicios/terminal.md
    - midu/replicación/nixos.md
---

# SSH

← [Lenguaje común](../lenguaje_común.md)

SSH (Secure Shell) es el protocolo para acceder de forma remota y cifrada a un servidor, ejecutando comandos como si estuviéramos frente a él. Es más seguro que las contraseñas cuando se usa con pares de claves criptográficas: la clave privada queda en nuestra máquina y la pública se instala en el servidor, de modo que solo quien tiene la privada puede conectarse. En la `midu` lo usamos para administrar el `computador` local y para desbloquear el disco cifrado desde el [initrd](initrd.md).

## Ver también

- [Terminal](../../midu/servicios/terminal.md): las herramientas de línea de comandos del `computador` local
- [initrd](initrd.md): SSH temprano para el desbloqueo remoto
