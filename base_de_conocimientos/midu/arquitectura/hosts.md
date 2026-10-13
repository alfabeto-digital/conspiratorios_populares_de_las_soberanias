# `computador` local y VPS

## Dos máquinas con roles muy distintos

Esta `interfaz` corre en dos máquinas. No son redundancia una de la otra, cada una tiene un papel específico y diferente.

| | `computador` local | VPS |
|---|---|---|
| **Tipo** | Máquina física, selfhosted | Servidor en la nube |
| **Rol** | Corre todos los servicios reales | Solo hace tunelado de tráfico |
| **`datos`** | Sí, en discos cifrados | No |
| **Expuesto a internet** | No directamente | Sí |
| **Si se compromete** | Problema grave | Problema manejable |

## El `computador` local: el núcleo

El `computador` local es una máquina física que corre en una ubicación controlada. Es el núcleo de la arquitectura: donde viven los `datos` y los servicios.

### Almacenamiento

Tiene dos discos NVMe:

- **nvme0**: el disco del sistema operativo. Contiene NixOS, la configuración, los binarios. Está cifrado con LUKS.
- **nvme1**: el disco de `datos`. Contiene las bases de `datos`, los archivos, los correos, todo lo que los servicios producen o almacenan. También está cifrado con LUKS.

La separación en dos discos tiene sentido práctico: si el sistema operativo se corrompe o quieres actualizar NixOS desde cero, puedes reformatear `nvme0` sin tocar los `datos` en `nvme1`. Los `datos` sobreviven a la reinstalación del sistema.

El cifrado LUKS significa que si alguien saca físicamente el disco de la máquina, no puede leer nada sin la clave de descifrado. Protege contra robo físico del hardware.

### Servicios que corre

El `computador` local corre todo:

- **Caddy**: proxy reverso interno, recibe el tráfico del túnel y lo dirige al servicio correcto
- **Authelia**: autenticación de dos factores para servicios protegidos
- **Stalwart**: servidor de correo electrónico
- **Dendrite**: servidor de chat (protocolo Matrix)
- **Vaultwarden**: gestor de contraseñas compatible con Bitwarden
- **Syncthing**: sincronización de archivos entre `dispositivo`s
- **ntfy**: notificaciones push
- **AdGuard Home**: DNS con bloqueo de rastreadores y anuncios
- **PostgreSQL**: base de `datos` para los servicios que la necesitan

### No está expuesto directamente a internet

El `computador` local no tiene puertos abiertos hacia internet. El único acceso exterior es a través del túnel cifrado con el VPS. Esto significa que los escaneos de puertos que constantemente recorren internet no encuentran nada en la IP del servidor.

## El VPS: la membrana

El VPS (Virtual Private Server) es un servidor en la nube contratado a un proveedor externo. Funciona como membrana: tiene una IP pública conocida, es el único punto de contacto con internet, y decide qué tráfico pasa hacia el núcleo.

### Lo que corre

Solo el stack de tunelado:

- **Pangolin**: gestiona los túneles entre el VPS y el `computador` local, decide qué tráfico va a dónde
- **Gerbil**: el componente de WireGuard de Pangolin, establece la red privada cifrada entre VPS y servidor
- **Traefik**: proxy reverso que recibe las peticiones HTTPS y las dirige a través del túnel

No corre bases de `datos`, no almacena archivos de usuario, no procesa `datos` sensibles.

### La decisión de proveedor

El VPS puede ser de cualquier proveedor cloud. Es deliberado: si el proveedor desaparece, te bloquea la cuenta o cambia los términos de servicio, puedes levantar un VPS nuevo en otro proveedor, aplicar la misma configuración NixOS y reconectar el túnel. Los `datos` siguen en el `computador` local y no se mueven.

Incluso se puede usar Cloudflare Tunnel como alternativa al VPS propio, es más simple de configurar, pero introduce dependencia de Cloudflare. La arquitectura está diseñada para que esa elección sea intercambiable.

## Por qué la separación importa: el modelo de amenaza

### Si el VPS se compromete

Un atacante que tome control del VPS puede:
- Cortar el acceso a los servicios (dejar de reenviar el tráfico)
- Ver qué dominios están siendo servidos
- Intentar modificar el tráfico en tránsito (aunque está cifrado por TLS extremo a extremo)

No puede:
- Acceder a los `datos` almacenados en el `computador` local
- Descifrar los secretos del `computador` local (las claves age son independientes)
- Modificar la configuración del `computador` local

### Las claves age son independientes

Cada máquina tiene su propia clave age para el sistema de secretos. Los secretos del `computador` local están cifrados con la clave age del `computador` local. Los secretos del VPS están cifrados con la clave age del VPS.

Si alguien compromete el VPS y obtiene su clave age, puede descifrar los secretos del VPS (que son solo configuración de tunelado). Los secretos del `computador` local permanecen cifrados e inaccesibles. Esta separación es explícita y deliberada.

El resultado es que el VPS puede comprometerse sin comprometer la integridad de los `datos`. No es una propiedad accidental, es una decisión de diseño.

Ver también:
- [Descripciones generales](descripciones_generales.md)
- [Gestión de secretos](secretos.md)
- [¿Qué es NixOS?](nixos.md)
