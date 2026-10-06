# Secretos: sops-nix, age y cifrado LUKS

Los secretos son contraseñas, tokens y claves que los servicios necesitan para funcionar: la contraseña de la base de `datos`, las claves de las APIs, el token de autenticación del correo, etc. Este paso los gestiona de forma segura usando [age](../../lenguaje_común/lenguaje_común.md#age) para el cifrado y [sops](../../lenguaje_común/lenguaje_común.md#sops) como capa de gestión.

← [`replicación`](../replicación.md)

## El problema que resuelve sops-nix

Guardar secretos en un repositorio git en texto plano es un error de seguridad clásico: cualquiera con acceso al repositorio puede leer las contraseñas. Pero tampoco es práctico guardar los secretos solo en el servidor sin ningún tipo de control de versiones ni respaldo.

La solución de esta `interfaz`: los secretos se cifran con `age` antes de ir al repositorio. El archivo `secrets.yaml` (cifrado) sí va a git. El archivo `secrets.plain` (en texto plano) nunca va a git. La clave de descifrado existe solo en el servidor.

## Cómo funciona age

[age](../../lenguaje_común/lenguaje_común.md#age) usa criptografía de clave pública. Cada entidad (persona o máquina) tiene:

- Una **clave pública**: puede ser compartida libremente. Cualquiera puede usarla para cifrar un mensaje dirigido al dueño de esa clave.
- Una **clave privada**: nunca se comparte. Es la única que puede descifrar lo que fue cifrado con su clave pública correspondiente.

En esta `interfaz`, el servidor tiene su propia clave age. Los secretos se cifran con la clave pública del servidor, y solo el servidor (con su clave privada) puede descifrarlos. Esto significa que aunque alguien obtenga el `secrets.yaml` del repositorio, no puede leerlo sin la clave privada del servidor.

## Paso 5: SSH deploy key, age key y secretos

### a) Entrar a nix-shell con las herramientas

```bash
nix-shell -p age sops
```

Esto pone `age` y `sops` disponibles temporalmente. No instala nada permanentemente.

### b) Generar la clave age del servidor

```bash
mkdir -p /root/.config/sops/age
age-keygen -o /root/.config/sops/age/keys.txt
age-keygen -y /root/.config/sops/age/keys.txt   # muestra la clave pública
```

Qué hace cada comando:

- `mkdir -p /root/.config/sops/age` crea el directorio donde `sops` espera encontrar la clave age. Esta ruta es una convención de `sops`.
- `age-keygen -o /root/.config/sops/age/keys.txt` genera un par de claves (pública + privada) y guarda ambas en `keys.txt`. La clave privada nunca sale del servidor.
- `age-keygen -y` lee `keys.txt` y muestra solo la clave pública (empieza con `age1...`). Copia esta clave, la necesitas en el siguiente paso.

### c) Crear .sops.yaml desde la plantilla

```bash
cp .sops.yaml.template .sops.yaml
# completar con la clave pública (age1...)
rm .sops-vps.yaml.template
rm nixos/secrets/secrets-vps.plain.template
```

`.sops.yaml` le dice a `sops` con qué claves debe cifrar cada archivo. Abre el archivo copiado y busca el campo para la clave age, reemplaza el placeholder con la clave pública `age1...` que obtuviste en el paso anterior.

Por qué `.sops.yaml` **sí va a git**: contiene solo la clave pública, que por definición es seguro compartir. De hecho, es necesario que esté en el repositorio para que `sops` sepa cómo cifrar cuando alguien nuevo genera secretos.

Los archivos `*.template` del VPS se eliminan porque no son necesarios en el `computador` local.

### d) Copiar y completar secrets.plain

```bash
cp nixos/secrets/secrets.plain.template nixos/secrets/secrets.plain
$EDITOR nixos/secrets/secrets.plain
# los comandos de generación están documentados en el template
```

`secrets.plain` es el archivo de secretos en texto plano. El template incluye comentarios que explican cómo generar cada valor (contraseñas aleatorias, tokens, etc.). Lee esos comentarios y completa cada campo.

Este archivo **nunca va a git**: está en `.gitignore`. Es temporal: existe solo el tiempo necesario para cifrarlo.

### e) Cifrar y eliminar el plain

```bash
sops --encrypt --input-type yaml nixos/secrets/secrets.plain > nixos/secrets/secrets.yaml
rm nixos/secrets/secrets.plain
```

Qué hace cada parte:

- `sops --encrypt` cifra el archivo usando la configuración de `.sops.yaml` (que incluye la clave pública age del servidor).
- `--input-type yaml` es importante: `secrets.plain` tiene extensión `.plain`, y sin esta opción `sops` lo trataría como `datos` binarios en lugar de YAML. El resultado sería un archivo cifrado que `sops` no puede descifrar correctamente después.
- `> nixos/secrets/secrets.yaml` guarda el resultado cifrado en `secrets.yaml`.
- `rm nixos/secrets/secrets.plain` elimina el archivo en texto plano. A partir de aquí, los secretos solo existen cifrados.

`secrets.yaml` (el archivo cifrado) **sí va a git**. `sops` cifra los valores pero preserva la estructura YAML, lo que permite ver qué claves existen sin revelar sus valores.

### f) Enrollar luks_data_key en el header LUKS de nvme1

Este paso conecta la gestión de secretos con el cifrado de disco. Aquí se programa el desbloqueo automático de `nvme1` en cada arranque.

```bash
LUKS_KEY=$(sops --decrypt --extract '["luks_data_key"]' nixos/secrets/secrets.yaml)
echo "$LUKS_KEY" | cryptsetup luksAddKey /dev/nvme1n1
# ingresar la passphrase de emergencia del paso 2 cuando lo pida
unset LUKS_KEY
```

Qué hace cada parte:

- `sops --decrypt --extract '["luks_data_key"]'` descifra solo el campo `luks_data_key` del archivo de secretos y lo guarda en la variable de entorno `LUKS_KEY`. El valor nunca toca el disco en texto plano.
- `cryptsetup luksAddKey` añade una segunda clave al header LUKS de `nvme1`. [LUKS](../../lenguaje_común/lenguaje_común.md#luks) soporta múltiples "slots" de clave, múltiples contraseñas que abren el mismo disco.
- `cryptsetup` pedirá la passphrase de emergencia del Paso 2 para verificar que tienes autorización para añadir una nueva clave.
- `unset LUKS_KEY` elimina la variable de entorno para que la clave no quede en la memoria del shell.

### Por qué dos claves en nvme1

LUKS almacena hasta 8 claves en el "header" (cabecera) del disco en slots numerados del 0 al 7. Después de este paso, `nvme1` tiene dos slots activos:

- **Slot 0**: la passphrase de emergencia que elegiste en el Paso 2. Existe como respaldo en caso de emergencia.
- **Slot 1**: `luks_data_key` gestionada por `sops-nix`. NixOS la lee automáticamente en cada arranque para desbloquear el disco sin intervención humana.

Para verificar que ambos slots están registrados:

```bash
cryptsetup luksDump /dev/nvme1n1 | grep "Key Slot"
```

El output debe mostrar dos slots en estado `ENABLED`.

## Resumen de qué va a git y qué no

| Archivo | ¿Va a git? | Por qué |
|---------|-----------|---------|
| `.sops.yaml` | Sí | Contiene solo claves públicas |
| `nixos/secrets/secrets.yaml` | Sí | Cifrado, los valores son ilegibles sin la clave privada |
| `nixos/secrets/secrets.plain` | No | Texto plano, se elimina después de cifrar |
| `/root/.config/sops/age/keys.txt` | No | Clave privada, nunca sale del servidor |

Con los secretos configurados y el disco `nvme1` listo para el desbloqueo automático, vuelve a [NixOS](nixos.md#paso-6-clonar-el-repositorio-y-construir-el-sistema) para el Paso 6: clonar el repositorio y construir el sistema por primera vez.
