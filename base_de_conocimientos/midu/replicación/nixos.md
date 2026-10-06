# NixOS y configuración de discos

Esta sección cubre los pasos 1 al 3 de la instalación: instalar NixOS en el disco principal, cifrar el disco de `datos` manualmente, y configurar el acceso SSH en la fase de arranque para poder desbloquear el servidor de forma remota.

← [`replicación`](../replicación.md)

## Por qué ciframos los discos

[LUKS](../../lenguaje_común/lenguaje_común.md#luks) (Linux Unified Key Setup) cifra todos los `datos` del disco a nivel de bloque. Esto significa que si alguien físicamente roba el servidor o extrae los discos, no puede leer ningún dato sin la clave de cifrado. Es el equivalente digital de una caja fuerte.

En esta `interfaz`, los dos discos tienen tratamientos distintos:

- **`nvme0` (sistema operativo)**: se cifra durante la instalación de NixOS. El instalador lo hace automáticamente y genera la configuración correspondiente en `hardware-configuration.nix`.
- **`nvme1` (`datos` de aplicaciones)**: se cifra manualmente antes de la primera construcción del sistema. La clave de cifrado se gestiona después con `sops` y se enrolla en el header LUKS del disco, esto permite que NixOS lo desbloquee automáticamente en cada arranque.

Separar SO y `datos` tiene otra ventaja: si necesitas reinstalar el sistema operativo, los `datos` de las aplicaciones en `nvme1` permanecen intactos y cifrados.

## Paso 0: Prerequisitos de disco

Antes de arrancar el instalador, identifica qué disco es cuál en tu servidor:

- `nvme0`, recibirá NixOS. El instalador lo cifrará con LUKS cuando lo solicites.
- `nvme1`, recibirá los `datos` de las aplicaciones (PostgreSQL y otros). Se cifra manualmente en el Paso 2.
- Disco de almacenamiento externo (opcional), **no se cifra en esta etapa**.

## Paso 1: Instalar NixOS en nvme0

Arranca el servidor desde la memoria USB con la ISO de NixOS. Sigue el instalador gráfico o de texto normalmente. El único punto crítico:

**Cuando el instalador pregunta sobre cifrado de disco, habilita LUKS para `nvme0`.**

El instalador te pedirá una passphrase (contraseña de cifrado). Esta passphrase desbloquea el disco en cada arranque. Guárdala en un lugar seguro, sin ella, el sistema no puede arrancar.

Después de la instalación, el instalador genera automáticamente `/etc/nixos/hardware-configuration.nix` con la configuración LUKS de `nvme0` incluida. No necesitas editar ese archivo manualmente.

## Paso 2: Cifrar nvme1 (disco de `datos`)

Una vez instalado NixOS y reiniciado en el nuevo sistema, hay que preparar el segundo disco. Este proceso tiene dos partes: formatear el disco con LUKS y anotar su [UUID](../../lenguaje_común/lenguaje_común.md#uuid) para la configuración.

### a) Formatear con LUKS y crear el sistema de archivos

```bash
cryptsetup luksFormat /dev/nvme1n1    # elegir una passphrase de emergencia
cryptsetup luksOpen /dev/nvme1n1 data-disk
mkfs.ext4 /dev/mapper/data-disk
cryptsetup luksClose data-disk
```

Qué hace cada comando:

- `luksFormat` inicializa el cifrado LUKS en el disco y solicita una passphrase. Esta es la **passphrase de emergencia**: solo se usará si el mecanismo automático de desbloqueo falla. Guárdala en un lugar seguro (gestor de contraseñas, papel en lugar físico seguro).
- `luksOpen` desbloquea el disco temporalmente y lo mapea a `/dev/mapper/data-disk`.
- `mkfs.ext4` crea el sistema de archivos dentro del espacio cifrado. El disco ahora tiene estructura para guardar archivos.
- `luksClose` vuelve a cerrar y bloquear el disco.

### b) Obtener el UUID del disco

```bash
blkid /dev/nvme1n1
```

Esto imprime algo como:

```
/dev/nvme1n1: UUID="a1b2c3d4-e5f6-7890-abcd-ef1234567890" TYPE="crypto_LUKS"
```

Copia ese UUID. Lo necesitarás en el Paso 4 (configuración) para el campo `data_disk_uuid`.

El [UUID](../../lenguaje_común/lenguaje_común.md#uuid) es un identificador único del disco que no cambia aunque lo muevas a otro servidor o reinicies el sistema. NixOS lo usa para encontrar el disco correcto en cada arranque.

## Paso 3: SSH en initrd: desbloqueo remoto de nvme0

### Qué es initrd y por qué importa

El [initrd](../../lenguaje_común/lenguaje_común.md#initrd) (initial RAM disk) es un sistema de archivos mínimo que NixOS carga en memoria durante los primeros segundos del arranque, antes de montar los discos reales. Es la primera fase del sistema.

El problema con LUKS en `nvme0` es este: el disco del SO está cifrado, así que el sistema no puede arrancar completamente sin desbloquearlo primero. Normalmente eso requiere estar físicamente delante del servidor para escribir la passphrase.

La solución es habilitar [SSH](../../lenguaje_común/lenguaje_común.md#ssh) dentro del initrd. Esto permite conectarse al servidor durante esa fase temprana del arranque y escribir la passphrase de forma remota, sin necesidad de acceso físico. El servidor escucha en el puerto 2222 durante el initrd, y en el puerto 22 una vez arrancado normalmente.

### Generar la clave SSH para initrd

Este par de claves es independiente del SSH del sistema principal. El initrd es un entorno muy limitado y necesita su propia clave.

```bash
mkdir -p /etc/secrets/initrd
ssh-keygen -t ed25519 -N "" -f /etc/secrets/initrd/ssh_host_ed25519_key
echo "ssh-ed25519 AAAA... user@host" > /etc/secrets/initrd/authorized_keys
chmod 600 /etc/secrets/initrd/authorized_keys
```

Qué hace cada comando:

- `mkdir -p /etc/secrets/initrd` crea el directorio para los secretos del initrd. Este directorio vive solo en el servidor (no va al repositorio git).
- `ssh-keygen -t ed25519 -N ""` genera un par de claves ed25519 sin passphrase (`-N ""`). El initrd necesita poder leer la clave sin intervención humana.
- La línea `echo "ssh-ed25519 AAAA..."` añade tu clave pública personal al archivo de claves autorizadas del initrd. Sustituye `ssh-ed25519 AAAA... user@host` con tu propia clave pública SSH (la que usas normalmente para conectarte a servidores).
- `chmod 600` restringe los permisos del archivo para que solo el propietario pueda leerlo.

### Cómo desbloquear el servidor después de un reinicio

Después de un reinicio, el servidor espera en el initrd hasta que alguien desbloquee `nvme0`:

```bash
ssh -p 2222 root@<server-ip>
# escribir la passphrase de nvme0
```

La conexión se hace al puerto 2222 (initrd) en lugar del 22 (sistema normal). Una vez escrita la passphrase correcta, el servidor completa el arranque y en unos segundos está accesible por el puerto 22 habitual.

## Paso 6: Clonar el repositorio y construir el sistema

Este paso viene después de completar la [configuración](configuración.md) y los [secretos](secretos.md). Se incluye aquí para mantener la numeración del README original, pero ejecutarlo antes de esos pasos causará errores.

```bash
nix-shell -p git
cp /etc/nixos/hardware-configuration.nix /tmp/hardware-configuration.nix
git clone git@github.com:<your-org>/<your-repo>.git ~/alfabeto.digital
ln -sf ~/alfabeto.digital/nixos /etc/nixos
cp /tmp/hardware-configuration.nix /etc/nixos/hardware-configuration.nix
cd /etc/nixos
nixos-rebuild switch --flake .#$(nix eval --raw 'import ./config.nix'.hostname)
```

Qué hace cada parte:

- `nix-shell -p git` instala git temporalmente para poder clonar el repositorio.
- Se guarda `hardware-configuration.nix` en `/tmp` porque el siguiente paso reemplaza `/etc/nixos` con un enlace simbólico, lo que borraría el archivo.
- `git clone` descarga el repositorio con toda la configuración del sistema.
- `ln -sf ~/alfabeto.digital/nixos /etc/nixos` hace que `/etc/nixos` apunte al directorio `nixos/` del repositorio clonado. A partir de aquí, NixOS lee su configuración directamente desde el repositorio.
- Se restaura `hardware-configuration.nix` porque ese archivo es específico de este servidor (lo generó el instalador) y no está en el repositorio.
- `nixos-rebuild switch` construye y activa el sistema. `--flake .#$(...)` le dice a NixOS que use el hostname definido en `config.nix` para seleccionar la configuración correcta del flake.

La primera construcción puede tardar varios minutos: NixOS descarga y compila todo lo necesario.

Cuando el sistema construya sin errores, continúa con [VPS](vps.md) para desplegar el punto de entrada público.
