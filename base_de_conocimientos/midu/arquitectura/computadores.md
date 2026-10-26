# El `computador` local y el `computador` desechable

## Dos máquinas con roles distintos

Esta [`interfaz`](../../subjetividades/interfaces.md) distribuye sus funciones en dos máquinas diferentes. Cada una tiene un rol específico en la arquitectura, y la asimetría entre ellas es el corazón del modelo de amenaza. El `computador` local es el núcleo de cualquier [tipo de `midu`](tipos_de_midu.md): la máquina donde viven los `datos`. El `computador` desechable es la membrana pública que la protege.

| | `computador` local | `computador` desechable |
|---|---|---|
| **Tipo** | Máquina física, en una ubicación controlada | Intermediario público (VPS arrendado o cuenta de Cloudflare) |
| **Rol** | Corre todos los servicios | Sólo reenvía el tráfico |
| **`datos`** | Sí, en discos cifrados | No |
| **Expuesto a internet** | No directamente | Sí |

## El `computador` local: el núcleo

El `computador` local es una máquina física que corre en una ubicación que nosotros controlamos. Es el núcleo de la arquitectura: donde viven los `datos` y corren todos los servicios que usamos para interactuar con nuestras `memorias`.

### El almacenamiento

Las `memorias` de la `midu` se guardan en varias [capas de resiliencia](almacenamiento_federado.md). En la configuración de referencia, el `computador` local tiene dos discos NVMe que sostienen las dos primeras capas:

- **nvme0**: la **capa operativa**. Contiene [NixOS](nixos.md), la configuración y los binarios. Está cifrado con [LUKS](../../lenguaje_común/lenguaje_común.md#luks).
- **nvme1**: la **capa local**, el almacenamiento persistente. Contiene las bases de `datos`, los archivos, los correos, todo lo que los servicios producen o almacenan. También está cifrado con LUKS.

La separación en dos discos tiene sentido práctico: si el sistema operativo se corrompe o queremos reinstalar NixOS desde cero, podemos formatear `nvme0` sin tocar los `datos` de `nvme1`. Las `memorias` sobreviven a la reinstalación del sistema.

El cifrado LUKS significa que, si alguien saca físicamente el disco de la máquina, no puede leer nada sin la clave de descifrado. Protege contra el acceso físico al hardware.

En configuraciones más complejas, la capa local gana una réplica en espejo (RAID1) y se suma una tercera capa, la federada, repartida entre varias `midu`. Las distintas configuraciones de hardware están en [tipos de `midu`](tipos_de_midu.md) y el modelo de resiliencia completo en [almacenamiento federado](almacenamiento_federado.md).

### Los servicios

El `computador` local corre todos los servicios soberanos:

- [Caddy](../servicios/caddy.md): proxy inverso interno, recibe el tráfico del túnel y lo dirige al servicio correcto.
- [Authelia](../servicios/authelia.md): inicio de sesión único con segundo factor para los servicios protegidos.
- [Stalwart](../servicios/stalwart.md): servidor de correo electrónico.
- [Dendrite](../servicios/dendrite.md): servidor de mensajería (protocolo Matrix).
- [Vaultwarden](../servicios/vaultwarden.md): gestor de contraseñas compatible con Bitwarden.
- [Syncthing](../servicios/syncthing.md): sincronización de archivos entre `dispositivos`.
- [ntfy](../servicios/ntfy.md): notificaciones push.
- [AdGuard Home](../servicios/adguard.md): DNS con bloqueo de rastreadores y anuncios.
- [PostgreSQL](../servicios/postgresql.md): base de `datos` para los servicios que la necesitan.

### Cuidarse en internet

El `computador` local no tiene puertos abiertos hacia internet. El único acceso exterior pasa por el [túnel cifrado](../servicios/túnel_cifrado.md) con el `computador` desechable. Los atacantes que escanean automáticamente puertos abiertos en internet no pueden ver la máquina local.

## El `computador` desechable: la membrana

El `computador` desechable es el intermediario público. Tiene una IP pública conocida, es el único punto de contacto con internet y decide qué tráfico pasa hacia el núcleo. Puede ser un VPS arrendado a un proveedor o una cuenta de Cloudflare. Es desechable por diseño: destruirlo no afecta ningún `dato`.

### Los servicios que corre

Sólo el sistema del túnel. En las rutas con VPS arrendado, el `computador` desechable corre [Pangolin](../servicios/pangolin.md), el stack completo del túnel: incluye Gerbil, que gestiona los pares [WireGuard](../../lenguaje_común/lenguaje_común.md#wireguard), y Traefik, que recibe las peticiones HTTPS y las reenvía por el túnel. El túnel usa WireGuard como protocolo; Newt es el cliente que corre en el `computador` local y lo conecta con Pangolin.

El `computador` desechable no corre bases de `datos`, no almacena archivos de las personas usuarias ni conoce `datos` sensibles.

### Un intermediario que no es indispensable

El `computador` desechable puede ser de cualquier proveedor. Si el proveedor desaparece, nos bloquea la cuenta o cambia los términos de servicio, podemos cambiarnos a otro, replicar la configuración y reconectar el túnel a través de un nuevo intermediario. Los `datos` siguen en el `computador` local y no se ven afectados por el cambio.

En la Ruta C, el `computador` desechable es una cuenta de Cloudflare. Es más simple de configurar pero introduce una dependencia de Cloudflare, que se dedica explícitamente a monitorear patrones de tráfico con propósitos comerciales. Las tres rutas posibles se comparan en [conectarse en internet](conectarse_en_internet.md). La arquitectura está diseñada para que esa elección no afecte la capacidad de gestión soberana de servicios.

## La separación importa: el modelo de amenaza

### Si el `computador` desechable es comprometido

Quien tome control del `computador` desechable puede cortar el acceso a los servicios (dejar de reenviar el tráfico), ver qué dominios se están sirviendo e intentar modificar el tráfico en tránsito, que viaja cifrado de extremo a extremo con TLS.

No puede acceder a los `datos` almacenados en el `computador` local, no puede acceder a los servicios locales que están protegidos detrás de su propia página de autenticación, no puede descifrar sus secretos ni modificar su configuración.

### Las claves age son independientes

Cada máquina tiene su propia clave age para la [gestión de secretos](secretos.md). Los secretos del `computador` local están cifrados con la clave age del `computador` local; los del `computador` desechable, con la suya.

Si alguien compromete el `computador` desechable y obtiene su clave age, puede descifrar sus secretos pero estos sólo sirven para replicar la configuración del túnel. Los secretos del `computador` local permanecen cifrados e inaccesibles. Esta separación deliberada imita el comportamiento de una célula: la membrana se puede reemplazar sin dañar el núcleo.

## Ver también

- [gestión de secretos](secretos.md): cómo `age` y `sops-nix` cifran los secretos para cada máquina.
- [NixOS](nixos.md): la configuración declarativa que describe ambas máquinas.
- [conectarse en internet](conectarse_en_internet.md): las rutas del `computador` desechable y el túnel cifrado.
- [almacenamiento federado](almacenamiento_federado.md): las capas de resiliencia de las `memorias`.
- [tipos de `midu`](tipos_de_midu.md): las configuraciones de hardware del `computador` local.
