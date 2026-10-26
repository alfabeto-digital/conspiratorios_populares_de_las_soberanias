# Gestión de secretos

## ¿Qué es un secreto?

Un **secreto** es cualquier dato que no debería ser público: contraseñas, tokens de API, claves criptográficas, cadenas de conexión a bases de `datos`. Si alguien accede a esos `datos`, puede suplantar identidades, acceder a servicios sin autorización o descifrar información protegida.

El problema con la infraestructura como código es inmediato: si la configuración vive en un repositorio git, ¿dónde van los secretos? Guardarlos en texto plano en el repositorio es un error grave, cualquiera que acceda al código (colaboradores, servicios de CI, personas que encuentran el repo público) tendría acceso a todo.

Esta `interfaz` resuelve el problema con dos herramientas combinadas: **age** para el cifrado y **sops-nix** para la integración con NixOS.

## age: una llave por máquina

**age** (pronunciado "ah-geh", de "Actually Good Encryption") es una herramienta moderna de cifrado de archivos. Su filosofía es la simplicidad: hace una cosa bien, cifrar y descifrar archivos, sin complejidad innecesaria.

La idea central es que cada máquina tiene su propia clave age. La clave tiene dos partes:

- **Clave pública**: se puede compartir. Se usa para cifrar mensajes *para* esa máquina.
- **Clave privada**: nunca sale de la máquina. Se usa para descifrar mensajes cifrados con la clave pública correspondiente.

Es como un buzón físico: cualquiera puede meter una carta (cifrar con la clave pública), pero solo el dueño del buzón tiene la llave para sacarla (descifrar con la clave privada).

Para cifrar un secreto para el `computador` local, usas la clave pública del servidor. Solo el servidor, con su clave privada, puede descifrar ese secreto. Si alguien intercepta el archivo cifrado, no puede hacer nada sin la clave privada, que nunca sale de la máquina.

## sops: secretos en git, pero cifrados

**sops** (Secrets OPerationS) es la herramienta que gestiona archivos de secretos estructurados. Un archivo de secretos en esta `interfaz` se parece a esto antes de cifrarlo (`secrets.plain`):

```yaml
stalwart_admin_password: "mi-contraseña-super-segura"
postgres_password: "otra-contraseña"
cloudflare_token: "token-de-api-de-cloudflare"
```

Después de cifrarlo con sops y age, el archivo (`secrets.yaml`) se ve así:

```yaml
stalwart_admin_password: ENC[AES256_GCM,data:xK3mP...,iv:...,tag:...,type:str]
postgres_password: ENC[AES256_GCM,data:9rQl...,iv:...,tag:...,type:str]
cloudflare_token: ENC[AES256_GCM,data:zTp2...,iv:...,tag:...,type:str]
sops:
    age:
        - recipient: age1...  # clave pública del servidor
    ...
```

Este archivo cifrado **sí se guarda en git**. Nadie sin la clave privada de la máquina puede leerlo. Pero el archivo sigue siendo útil en el repositorio: se puede auditar su estructura, ver cuántos secretos hay, controlar sus versiones.

## sops-nix: secretos disponibles durante la construcción

**sops-nix** es el módulo de NixOS que integra sops con el sistema. Su trabajo es:

1. Durante la construcción del sistema (`nixos-rebuild switch`), detectar que hay secretos cifrados definidos en la configuración.
2. Usar la clave age de la máquina para descifrar esos secretos.
3. Ponerlos disponibles en rutas del sistema de archivos con los permisos correctos.

Los servicios de NixOS que necesitan un secreto no lo tienen en texto plano en su configuración, tienen una referencia a la ruta donde sops-nix colocará el valor descifrado:

```nix
services.stalwart-mail.settings.authentication.secret = config.sops.secrets.stalwart_admin_password.path;
```

El servicio lee el archivo en esa ruta en tiempo de ejecución. El valor nunca aparece en texto plano en el código fuente.

## El flujo completo

Paso a paso, así funciona la gestión de secretos en esta `interfaz`:

**1. Generar la clave age de la máquina**

Al instalar el servidor, se genera una clave age única para esa máquina. La clave privada vive en la máquina, protegida. La clave pública se anota para usarla en el siguiente paso.

**2. Configurar `.sops.yaml`**

El archivo `.sops.yaml` (o `.sops.yaml.template` en el repositorio) define qué clave(s) pueden descifrar cada archivo de secretos:

```yaml
keys:
  - &servidor age1...clave-publica-del-servidor...
  
creation_rules:
  - path_regex: secrets/secrets.yaml
    key_groups:
      - age:
        - *servidor
  - path_regex: secrets/secrets-vps.yaml
    key_groups:
      - age:
        - *vps
```

**3. Cifrar los secretos**

Con los valores reales en `secrets.plain`, se cifra con sops:

```bash
sops --encrypt secrets.plain > secrets/secrets.yaml
```

sops usa la configuración de `.sops.yaml` para saber con qué clave cifrar.

**4. Commitear el archivo cifrado**

`secrets/secrets.yaml` se puede commitear sin riesgo. `secrets.plain` nunca se commitea, está en `.gitignore`.

**5. El sistema descifra en construcción**

Cuando se ejecuta `nixos-rebuild switch`, sops-nix detecta los secretos declarados, busca la clave age de la máquina, descifra los valores y los coloca en las rutas configuradas.

## Dos máquinas, dos claves independientes

El `computador` local y el VPS tienen cada uno su propia clave age. Los secretos del `computador` local (`secrets.yaml`) solo pueden ser descifrados por la clave del `computador` local. Los secretos del VPS (`secrets-vps.yaml`) solo pueden ser descifrados por la clave del VPS.

Esto no es solo comodidad organizativa, es una decisión de seguridad. Si el VPS se ve comprometido y alguien obtiene su clave age, puede descifrar `secrets-vps.yaml`, que contiene configuración de tunelado. No puede descifrar `secrets.yaml`, que contiene las contraseñas de los servicios reales y los `datos`.

El radio de daño de un compromiso del VPS está acotado desde el diseño.

## Los templates: estructura sin valores

En el repositorio hay archivos template que sí se commitean:

- `secrets/secrets.plain.template`, muestra qué secretos existen y qué formato tienen, con valores vacíos o de ejemplo
- `secrets/secrets-vps.plain.template`, lo mismo para el VPS
- `.sops.yaml.template`, muestra la estructura de `.sops.yaml` con claves placeholder

Estos templates son documentación ejecutable: muestran exactamente qué hay que rellenar para poner en marcha el sistema, sin revelar ningún valor real.

Ver también:
- [El `computador` local y el VPS](computadores.md)
- [Descripciones generales](descripciones_generales.md)
- [¿Qué es NixOS?](nixos.md)
