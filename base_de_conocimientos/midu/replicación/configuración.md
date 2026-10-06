# Configuración de config.nix

`config.nix` es el archivo central de configuración del servidor. Contiene todos los valores específicos de tu instalación: nombre del servidor, usuario administrador, UUIDs de los discos, dominio, etc. Este paso consiste en copiar la plantilla y completar cada campo con los valores correctos.

← [`replicación`](../replicación.md)

## Por qué config.nix es gitignored

El archivo `config.nix` **no se sube al repositorio git**: está en el `.gitignore` por diseño.

La razón es de privacidad y seguridad: `config.nix` contiene información específica de tu servidor (nombres de usuario, dominio, UUIDs de discos) que no debería estar en un repositorio público, ni siquiera privado, si compartes acceso al repositorio con otras personas. El archivo vive solo en el servidor.

En su lugar, el repositorio incluye `config.nix.template`: una plantilla con todos los campos disponibles, comentados y con valores de ejemplo. Tú copias la plantilla, la completas, y el resultado se queda en el servidor.

## Paso 4: Copiar y completar config.nix

```bash
cp nixos/config.nix.template nixos/config.nix
$EDITOR nixos/config.nix
rm nixos/config-vps.nix.template   # no necesario en esta máquina
```

Abre `config.nix` con tu editor preferido (`nano`, `vim`, `micro`, etc.) y completa los campos. A continuación se explica cada sección.

## Campos de config.nix

### Versiones de NixOS

```nix
nixos_channel_version = "25.11";
nixos_state_version = "25.11";   # NUNCA cambiar después del primer build
```

Estos dos campos parecen similares pero tienen significados completamente distintos.

**`nixos_state_version`** es la versión de NixOS en el momento de la instalación inicial. NixOS la usa para mantener compatibilidad con el formato de `datos` de ciertas aplicaciones (bases de `datos`, directorios de usuario, etc.). Una vez que el sistema arranca por primera vez, este valor **nunca debe cambiarse**. Cambiarlo puede causar migraciones de `datos` incorrectas o rotura de servicios.

Piénsalo como el "idioma nativo" de tus `datos`: los `datos` se escribieron en ese formato, y cambiar la versión le diría al sistema que los `datos` están en un formato diferente cuando no es así.

**`nixos_channel_version`** es la versión del canal de paquetes de NixOS que se usa para las actualizaciones. Este sí puede (y debe) actualizarse cuando quieras subir a una versión más nueva de NixOS. Cambiarlo y ejecutar `nix flake update` actualizará todos los paquetes del sistema.

En resumen:
- `state_version`: se pone una vez al instalar y nunca se toca.
- `channel_version`: se actualiza cuando quieres hacer upgrade del sistema.

### Identidad del servidor

```nix
hostname = "mi-servidor";
timezone = "America/Mexico_City";
locale_default = "es_MX.UTF-8";
locale_messages = "en_US.UTF-8";
keyboard_layout = "latam";
keyboard_variant = "";
```

- `hostname`: el nombre del servidor en la red. Puede ser cualquier nombre sin espacios.
- `timezone`: zona horaria en formato IANA (lista completa en [Wikipedia: List of tz database time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)).
- `locale_*`: configuración de idioma y formato de fechas/números. `locale_messages` controla el idioma de los mensajes del sistema.
- `keyboard_*`: distribución del teclado para la consola local del servidor.

### Usuarios

```nix
admin_username = "alice";
admin_ssh_key = "ssh-ed25519 AAAA...";
syncthing_username = "alice";
ftp_username = "alice";
```

- `admin_username`: el usuario administrador del sistema (sin privilegios de root por defecto, pero con `sudo`).
- `admin_ssh_key`: la clave pública [SSH](../../lenguaje_común/lenguaje_común.md#ssh) del administrador. Con esta clave podrás conectarte al servidor. Para ver tu clave pública: `cat ~/.ssh/id_ed25519.pub` (o `id_rsa.pub` si usas RSA).
- `syncthing_username` y `ftp_username`: usuario para los servicios de sincronización de archivos y FTP. Generalmente el mismo usuario administrador.

### Base de `datos`

```nix
db_name = "appdb";
db_username = "appuser";
```

Nombre de la base de `datos` [PostgreSQL](../../lenguaje_común/lenguaje_común.md#postgresql) principal y el usuario que accede a ella. Los servicios del sistema escriben y leen sus `datos` aquí.

### Discos y puntos de montaje

```nix
data_mount_point = "/data";
data_disk_uuid = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx";
storage_mount_point = "/storage";
storage_name = "mi-storage";
storage_uuid = "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy";
```

- `data_mount_point`: dónde se monta `nvme1` en el sistema de archivos. `/data` es la convención de esta `interfaz`.
- `data_disk_uuid`: el [UUID](../../lenguaje_común/lenguaje_común.md#uuid) de `nvme1` que obtuviste en el Paso 2 con `blkid /dev/nvme1n1`.
- `storage_mount_point` y `storage_name`: punto de montaje y nombre del disco de almacenamiento opcional.
- `storage_uuid`: UUID del disco de almacenamiento opcional (obtener con `blkid /dev/<`dispositivo`>`).

Si no tienes disco de almacenamiento externo, puedes dejar los campos `storage_*` con los valores del template y desactivar el servicio correspondiente en la configuración.

### Red y dominio

```nix
domain = "tusitio.com";
email_acme = "tu@email.com";
```

- `domain`: el dominio principal del sistema. Todos los servicios se servirán bajo subdominios de este dominio (ej: `mail.tusitio.com`, `chat.tusitio.com`).
- `email_acme`: correo electrónico para registrar los certificados [TLS](../../lenguaje_común/lenguaje_común.md#tls) con [Let's Encrypt](../../lenguaje_común/lenguaje_común.md#lets-encrypt) vía el protocolo [ACME](../../lenguaje_común/lenguaje_común.md#acme). Let's Encrypt envía notificaciones de expiración a este correo.

### Tipo de túnel

```nix
tunnel_type = "cloudflare";  # o "newt"
```

Define cómo el [VPS](../../lenguaje_común/lenguaje_común.md#vps) conecta el tráfico público al servidor:

- `"cloudflare"`: usa Cloudflare Tunnel. Más simple de configurar, pero Cloudflare ve el tráfico ([MITM](../../lenguaje_común/lenguaje_común.md#mitm) benigno).
- `"newt"`: usa Pangolin/Newt con [WireGuard](../../lenguaje_común/lenguaje_común.md#wireguard). Tráfico cifrado de extremo a extremo, sin intermediario que vea el contenido. Requiere el Path A o B del VPS con Pangolin.

### Puertos de servicios

Los puertos tienen valores predeterminados en el template. Solo cámbialos si hay conflictos con otros servicios o necesidades específicas de red.

## Después de completar config.nix

Verifica que no haya campos con valores de placeholder (`xxxxxxxx`, `CAMBIAR_ESTO`, etc.). Un campo incompleto causará errores durante la construcción del sistema.

Cuando `config.nix` esté completo, continúa con [Secretos](secretos.md).
