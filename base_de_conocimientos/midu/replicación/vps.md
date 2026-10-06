# Despliegue del VPS

El [VPS](../../lenguaje_común/lenguaje_común.md#vps) (Servidor Virtual Privado) es el punto de entrada público de toda la infraestructura. El `computador` local donde corren los servicios puede estar en una red doméstica sin IP pública fija, el VPS resuelve eso actuando como intermediario que recibe el tráfico y lo reenvía al servidor real.

← [`replicación`](../replicación.md)

## Path A vs Path B

Hay dos formas de configurar el VPS, según las preferencias y el sistema operativo disponible:

| | Path A, NixOS | Path B, Docker/Podman |
|--|----------------|------------------------|
| **Sistema operativo del VPS** | NixOS | Cualquier Linux |
| **Herramienta de despliegue** | nixos-anywhere + nixos-rebuild | docker compose / podman |
| **Gestión de secretos** | sops-nix con age key propia | Archivo `.env` |
| **Configuración** | `config-vps.nix` + `secrets-vps.yaml` | `pangolin.yaml` + `routes.toml` + `secrets.env` |
| **Directorio en el repo** | `nixos/` (con perfil `vps`) | `vps/` |
| **Reproducibilidad** | Alta, configuración declarativa | Media, depende del estado del host |
| **Complejidad inicial** | Mayor | Menor |

Elige el path que mejor se adapte a tu situación. Si ya tienes el VPS corriendo Linux con Docker, Path B es más directo.

## Path A: NixOS en el VPS

### nixos-anywhere

[nixos-anywhere](https://github.com/nix-community/nixos-anywhere) es una herramienta que instala NixOS en un servidor remoto desde tu máquina local, sin necesidad de acceso físico ni ISO de instalación. Solo necesitas acceso SSH con usuario `root`.

### 1. Copiar y completar config-vps.nix

En el repositorio (en tu máquina local o en el servidor):

```bash
cp nixos/config-vps.nix.template nixos/config-vps.nix
$EDITOR nixos/config-vps.nix
```

Campos clave a completar:

- `hostname`: nombre del VPS (ej: `vps-prod`)
- `domain`: el mismo dominio del `computador` local
- `vps_ip`: la IP pública del VPS
- `container_runtime`: `"docker"` o `"podman"` (si el VPS usará contenedores para algún servicio)

### 2. Instalar NixOS en el VPS (si aún no tiene NixOS)

Si el VPS corre Ubuntu, Debian u otro Linux, puedes reemplazarlo con NixOS sin acceso físico:

```bash
nix run github:nix-community/nixos-anywhere -- --flake .#vps root@<VPS_IP>
```

Esto conecta al VPS por SSH, formatea el disco, instala NixOS con la configuración del [flake](../../lenguaje_común/lenguaje_común.md#flake) (perfil `vps`), y reinicia. El proceso dura unos minutos.

### 3. Generar age key en el VPS

El VPS tiene su propia clave [age](../../lenguaje_común/lenguaje_común.md#age), independiente del `computador` local. Esto permite que el VPS descifre sus propios secretos sin acceso a los secretos del `computador` local.

Conecta al VPS por SSH y genera la clave:

```bash
ssh root@<VPS_IP>
nix-shell -p age
mkdir -p /root/.config/sops/age
age-keygen -o /root/.config/sops/age/keys.txt
age-keygen -y /root/.config/sops/age/keys.txt   # muestra la clave pública (age1...)
```

Copia la clave pública `age1...`.

### 4. Crear .sops.yaml del VPS

De vuelta en tu máquina de desarrollo (o en el `computador` local):

```bash
cp .sops-vps.yaml.template .sops.yaml
# completar con la clave pública del VPS (age1...)
```

Completa el campo de la clave age con la clave pública del VPS obtenida en el paso anterior.

### 5. Llenar y cifrar secrets-vps.yaml

```bash
cp nixos/secrets/secrets-vps.plain.template nixos/secrets/secrets-vps.plain
$EDITOR nixos/secrets/secrets-vps.plain
sops --encrypt --input-type yaml nixos/secrets/secrets-vps.plain > nixos/secrets/secrets-vps.yaml
rm nixos/secrets/secrets-vps.plain
```

El mismo proceso que para los secretos del `computador` local, pero para los secretos específicos del VPS.

### 6. Construir y activar la configuración del VPS

En el VPS:

```bash
nixos-rebuild switch --flake /root/alfabeto.digital/nixos#vps
```

### 7. Post-conexión Newt: anotar IP WireGuard

Cuando el `computador` local se conecta al VPS por primera vez usando Newt/Pangolin, el VPS asigna una IP [WireGuard](../../lenguaje_común/lenguaje_común.md#wireguard) al servidor (en el rango `10.x.x.x`). Esta IP es necesaria para que el VPS sepa a dónde reenviar el tráfico.

Después de la primera conexión:

1. En el VPS, anota la IP WireGuard asignada al peer (el `computador` local).
2. Actualiza `config-vps.nix` con esa IP.
3. Reconstruye: `nixos-rebuild switch --flake /root/alfabeto.digital/nixos#vps`

## Path B: Docker/Podman en cualquier Linux

Path B solo necesita el directorio `vps/` del repositorio. Si no quieres clonar todo el repositorio en el VPS, puedes hacer un **sparse checkout**: descargar solo esa parte.

### Sparse checkout

El sparse checkout permite clonar un repositorio git pero descargar solo los directorios que necesitas, ignorando el resto. Útil cuando el repositorio es grande y solo necesitas una parte.

```bash
git clone --filter=blob:none --sparse git@github.com:<org>/<repo>.git alfabeto.digital-vps
cd alfabeto.digital-vps
git sparse-checkout set vps
```

Qué hace cada opción:

- `--filter=blob:none` evita descargar los contenidos de los archivos hasta que se necesiten (descarga lazy).
- `--sparse` activa el modo de sparse checkout.
- `git sparse-checkout set vps` configura el checkout para mostrar solo el directorio `vps/`.

### Configurar Pangolin

```bash
$EDITOR vps/config/pangolin.yaml
```

Campos a completar:

- `base_domain`: el dominio principal (ej: `tusitio.com`)
- `base_endpoint`: la IP pública del VPS (ej: `203.0.113.42`)

### Configurar las rutas de tráfico

```bash
$EDITOR vps/config/dynamic/routes.toml
```

Completa el dominio. La IP [WireGuard](../../lenguaje_común/lenguaje_común.md#wireguard) del `computador` local se configura después de la primera conexión Newt (ver más abajo). Por ahora puedes dejar el placeholder.

### Configurar secretos

```bash
cp vps/secrets.env.template vps/secrets.env
$EDITOR vps/secrets.env
```

El único secreto necesario en el VPS (Path B) es `GERBIL_PANGOLIN_TOKEN`. Para generarlo:

1. Abre el panel de administración de Pangolin.
2. Ve a Settings → API Tokens.
3. Crea un nuevo token y cópialo en `secrets.env`.

### Levantar los servicios

Con Docker:

```bash
docker compose up -d
```

Con Podman:

```bash
# Podman necesita NET_ADMIN capability para gestionar interfaces WireGuard
# Ejecutar como root para asegurar los permisos necesarios
podman compose up -d
```

La diferencia con [Podman](../../lenguaje_común/lenguaje_común.md#podman): Docker siempre corre con privilegios de sistema, Podman puede correr sin ellos (rootless). Pero [WireGuard](../../lenguaje_común/lenguaje_común.md#wireguard) necesita permisos de red (NET_ADMIN) que en Podman rootless no están disponibles. La solución más simple es correr Podman como root en el VPS.

### Post-conexión Newt: actualizar IP WireGuard

Después de que el `computador` local establece su primera conexión Newt al VPS:

1. Anota la IP WireGuard asignada al `computador` local (en el rango `10.x.x.x`).
2. Actualiza `vps/config/dynamic/routes.toml` con esa IP.
3. Reinicia Traefik para que aplique la configuración:
   ```bash
   docker compose restart traefik
   ```

### Actualizar el VPS (Path B)

```bash
git pull && docker compose pull && docker compose up -d
```

Este comando actualiza el código de configuración, descarga las imágenes de contenedor más recientes, y reinicia los servicios. Los `datos` persisten porque están en volúmenes de Docker.

## Actualización del sistema NixOS

La gestión de versiones de NixOS en el `computador` local funciona con `nix flake update`. El proceso coordina tres lugares: el servidor, el repositorio git, y el VPS.

### Actualizar nixpkgs

```bash
# 1. En el servidor selfhosted:
cd /etc/nixos && nix flake update

# 2. En la máquina de desarrollo:
scp root@<server>:/etc/nixos/flake.lock nixos/
git add nixos/flake.lock && git commit -m "flake: update nixpkgs" && git push

# 3. En el VPS (si usa NixOS: Path A):
git pull && nixos-rebuild switch --flake /root/alfabeto.digital/nixos#vps
```

Por qué este flujo:

- `nix flake update` regenera `flake.lock`, que fija las versiones exactas de todos los paquetes. Correrlo en el servidor garantiza que la versión que se prueba es la misma que quedará registrada.
- Copiar `flake.lock` al repositorio git lo convierte en el nuevo "estado de referencia" del sistema. Otros administradores o el VPS pueden obtener exactamente los mismos paquetes haciendo `git pull`.
- El VPS actualiza desde git para sincronizarse con las mismas versiones.

### Aliases de shell disponibles

Los siguientes aliases están definidos en `home/default.nix` para uso cotidiano:

- `rebuild-nixos`, construye el sistema sin activarlo. Útil para verificar que no hay errores de compilación antes de aplicar cambios.
- `switch-nixos`, construye y activa el sistema inmediatamente.

Si `rebuild-nixos` muestra errores, puedes corregirlos antes de que afecten al sistema en producción. Si `switch-nixos` produce un resultado inesperado, recuerda que el [rollback](../../lenguaje_común/lenguaje_común.md#rollback) siempre está disponible.
