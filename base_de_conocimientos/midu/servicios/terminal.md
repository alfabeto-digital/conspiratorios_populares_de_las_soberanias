# herramientas de terminal

← [Servicios](servicios.md)

Las herramientas de terminal son la `interfaz` directa con el `computador`. No tienen `interfaz` gráfica: operan sobre el sistema declarativo de NixOS y el repositorio de configuración. Se gestionan con home-manager, declarado en `midu/nixos/modules/nixos/admin.nix`, que aplica la configuración del usuario `admin` cada vez que se reconstruye el sistema.

## git

Git gestiona el repositorio de configuración de la `midu`. Toda la infraestructura está declarada como código en ese repositorio, así que git es la herramienta central de versionado, historial de cambios y sincronización con el servidor remoto.

Comandos frecuentes en el flujo de trabajo:

```bash
git pull                    # sincronizar con el repositorio remoto
git add <archivo>           # preparar cambios para commit
git commit -m "mensaje"     # registrar los cambios
git push                    # enviar los cambios al repositorio remoto
```

## ssh

SSH es el protocolo que permite acceso remoto seguro al VPS. Se usa en dos momentos distintos: durante la instalación inicial del VPS con `nixos-anywhere`, y para el acceso regular de administración.

También se usa en el proceso de desbloqueo remoto del disco cifrado: el `computador` local arranca con SSH activo en el initrd antes de montar el sistema de archivos, lo que permite introducir la contraseña de LUKS de forma remota.

Ver: [`secretos`](../arquitectura/secretos.md) para el uso de SSH en la gestión de claves.

## neovim

Editor de texto del usuario `admin`. Configurado en `midu/nixos/home/default.nix` con una configuración mínima (números de línea, resaltado de sintaxis). Es el editor usado para editar archivos de configuración directamente en el `computador` o en el VPS.

```nix
home.file.".config/nvim/init.vim".text = ''
  set number
  syntax enable
'';
```

## nix y nixos-rebuild

`nixos-rebuild` aplica los cambios declarados en el repositorio al sistema en ejecución.

```bash
nixos-rebuild test          # aplica cambios temporalmente (sin activar en el arranque)
nixos-rebuild switch        # aplica cambios y los activa permanentemente
```

`nix` es la herramienta de bajo nivel para gestionar el store de paquetes y actualizar el flake:

```bash
nix flake update            # actualizar las versiones de los inputs del flake
nix-store --gc              # limpiar paquetes no usados
```

## nixos-anywhere

`nixos-anywhere` instala NixOS en un servidor remoto sin acceso físico ni ISO de instalación. Solo requiere acceso SSH con usuario `root`. Se usa una sola vez, durante la instalación inicial del VPS.

Ver: [despliegue del VPS](../`replicación`/vps.md) para el proceso completo.

## sops y age

`sops` es la herramienta de línea de comandos para cifrar y descifrar archivos de secretos. `age` es el algoritmo de cifrado que usa sops para los secretos de la `midu`.

```bash
sops -e secrets.plain > secrets.yaml    # cifrar
sops -d secrets.yaml                    # descifrar (requiere la clave age)
```

Ver: [`secretos`](../arquitectura/secretos.md) para la arquitectura completa de gestión de secretos.

## Ver también

- [`secretos`](../arquitectura/secretos.md): cómo se cifran y gestionan las claves
- [`replicación`: nixos](../`replicación`/nixos.md): instalar la `midu` desde cero
- [`replicación`: VPS](../`replicación`/vps.md): desplegar el VPS
