# Servicios

← [Inicio](../../README.md)

## ¿Qué es un servicio?

En este `contexto`, un *servicio* es un programa que corre continuamente en el servidor y responde cuando lo necesitas. El correo electrónico es un servicio. El gestor de contraseñas es un servicio. El servidor DNS que traduce nombres a direcciones IP es un servicio.

La diferencia entre los servicios que componen esta `interfaz` y sus equivalentes externos es la diferencia entre controlar la configuración y depender de quien la controla. Cuando los servicios corren en `infraestructuras` que no administramos, las reglas de acceso, los `datos` y las decisiones sobre continuidad las toma otro. Usar servicios propios no elimina esa dependencia por completo; sigue habiendo hardware, proveedores de red, software de terceros. Pero desplaza el control hacia quien administra el sistema.

## Los servicios de `alfabeto.digital`

| Servicio | Descripción |
|---|---|
| [Caddy](caddy.md) | Reverse proxy HTTPS; recibe todo el tráfico y lo dirige al servicio correcto |
| [Authelia](authelia.md) | SSO / 2FA; inicio de sesión único con segundo factor |
| [AdGuard](adguard.md) | Servidor DNS con bloqueo de publicidad y rastreadores |
| [PostgreSQL](postgresql.md) | Base de `datos` compartida por varios servicios |
| [Vaultwarden](vaultwarden.md) | Gestor de contraseñas compatible con Bitwarden |
| [Syncthing](syncthing.md) | Sincronización de archivos P2P entre `dispositivo`s |
| [Stalwart](stalwart.md) | Servidor de correo electrónico (SMTP/IMAP) |
| [Dendrite](dendrite.md) | Homeserver de Matrix; chat federado |
| [ntfy](ntfy.md) | Servidor de notificaciones push |
| [Túnel](túnel.md) | Cómo el `computador` local se expone a internet: Cloudflare o Newt |
| [Pangolin](pangolin.md) | El stack del VPS: Pangolin, Gerbil y Traefik |
| [Virtualización](virtualización.md) | Docker y Podman: cómo se despliegan los servicios en contenedores |
| [Terminal](terminal.md) | Herramientas de terminal para administrar el `computador` |
| [Publicación](publicación.md) | Hugo genera el sitio web de la base de conocimientos a partir de los archivos Markdown |

## Por qué este conjunto específico es una `midu`

Una [`midu`](../../midu.md) no es simplemente "todos los servicios que existen". Es la respuesta a la pregunta: ¿cuáles son los servicios sin los cuales una comunidad no puede funcionar digitalmente de manera `soberana`?

La respuesta tiene cuatro pilares:

### 1. Comunicación

Sin comunicación, no hay comunidad. El correo electrónico sigue siendo la columna vertebral de la identidad digital: sin él no puedes crear cuentas, recuperar contraseñas ni comunicarte de forma interoperable con el resto del mundo. **Stalwart** cubre el correo. **Dendrite** cubre la mensajería instantánea mediante el protocolo Matrix, que permite comunicarse con personas en otros servidores. **ntfy** cubre las notificaciones, que son la forma en que los sistemas avisan a las personas que algo ocurrió.

### 2. Almacenamiento

Los `datos` tienen que vivir en algún lugar. **PostgreSQL** es la base de `datos` que usan internamente varios servicios. **Syncthing** permite que los archivos estén sincronizados entre `dispositivo`s sin pasar por servicios externos. **Vaultwarden** almacena las contraseñas de forma cifrada.

### 3. Autenticación

Una identidad digital `soberana` no puede depender de "Iniciar sesión con Google". **Authelia** gestiona la autenticación de todos los servicios del sistema con una sola contraseña y un segundo factor. **Vaultwarden** asegura que esas contraseñas (y las de todo lo demás) estén bajo control propio.

### 4. Red

Un servidor que no es accesible desde internet no sirve para comunicarse con el mundo. **Caddy** gestiona el HTTPS. **AdGuard** gestiona el DNS interno. El **túnel** (Cloudflare o Newt+Pangolin) permite que el `computador` local sea accesible desde fuera sin exponer la IP real ni abrir puertos directamente.

## La arquitectura en una imagen

Todos los servicios corren en el `computador` local. El tráfico de internet llega a través del túnel hasta Caddy, que lo distribuye. Authelia actúa como un filtro: antes de que cualquier petición llegue a la mayoría de los servicios, Caddy le pregunta a Authelia si el usuario tiene sesión activa.

```
INTERNET
    ↓
[Túnel: Cloudflare o WireGuard]
    ↓
[VPS: Pangolin + Traefik]    ← solo reenvía, no almacena `datos`
    ↓
[Caddy]                      ← gestiona HTTPS y dirige el tráfico
    ↓
[Authelia]                   ← ¿está autenticado este usuario?
    ↓
[Servicio: correo / chat / contraseñas / archivos / DNS...]
```

## Ver también

- [la `midu`](../../midu.md): la filosofía detrás de este conjunto de servicios
- [Arquitectura](../arquitectura.md): los componentes técnicos del sistema
- [`cuidados`](../../`cuidados`.md): cómo se protege el conjunto
- [Subjetividades](../../subjetividades.md): los fundamentos conceptuales
