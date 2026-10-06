# ntfy

← [Servicios](servicios.md)

## ¿Qué es esto?

ntfy es un servidor de notificaciones push. Una notificación push es un mensaje que el servidor te envía a ti, al teléfono, a la computadora, sin que tengas que estar mirando la aplicación ni hacer ninguna consulta activa. Es la tecnología detrás de las notificaciones de correo nuevo, los avisos de mensajes y las alertas del sistema.

Sin notificaciones push, tendrías que abrir la aplicación para ver si hay algo nuevo. Con notificaciones push, la aplicación sabe en tiempo real que algo ocurrió y puede avisarte inmediatamente.

## ¿Para qué sirve?

- **Alertas del sistema**: cuando algo ocurre en el servidor (un servicio se cae, el disco se llena, hay un error), ntfy puede enviar una notificación al teléfono del administrador.
- **Notificaciones de otras aplicaciones auto-hospedadas**: herramientas de automatización, scripts, servicios que necesitan avisarte de algo pueden enviar un mensaje a ntfy y ntfy lo muestra como notificación en el `dispositivo`.
- **Alternativa a los servicios de notificación comerciales**: en lugar de usar un servicio externo de terceros, las aplicaciones propias pueden usar ntfy directamente.

## El problema que ntfy resuelve

Por defecto, las notificaciones push en Android pasan por servidores de Google (Firebase Cloud Messaging) y en iOS por servidores de Apple (APNs). Esto significa que incluso si usas una aplicación de código abierto instalada en tu propio servidor, las notificaciones de esa aplicación pasan por Google o Apple antes de llegar a tu `dispositivo`.

ntfy permite enviar notificaciones sin ningún intermediario, usando su propio protocolo basado en HTTP. Las aplicaciones pueden publicar mensajes a ntfy, y la app de ntfy en el teléfono los recibe directamente desde tu servidor.

## ¿Por qué ntfy específicamente?

ntfy destaca por su simplicidad. Para enviar una notificación, basta con hacer una petición HTTP a un endpoint. No hay SDKs complejos, no hay configuraciones elaboradas. Un script de shell puede enviar una notificación con una sola línea.

Alternativas como Gotify hacen algo similar, pero ntfy tiene soporte para iOS sin depender de servidores puente de terceros (usando WebSockets) y una API más simple.

## ¿Cómo funciona en alfabeto.digital?

ntfy corre en el `computador` local y usa SQLite como base de `datos` propia, liviano e independiente de PostgreSQL.

Cualquier servicio o script del sistema puede publicar un mensaje a ntfy mediante una petición HTTP. La app de ntfy instalada en el teléfono se suscribe a los topics relevantes y muestra las notificaciones cuando llegan.

**Módulo NixOS:** `nixos/modules/nixos/communications/ntfy.nix`

## Ver también

- [Dendrite](dendrite.md): mensajería instantánea del sistema
- [Stalwart](stalwart.md): correo electrónico del sistema
- [Caddy](caddy.md): gestiona el acceso HTTPS al servidor ntfy
- [Authelia](authelia.md): protege el acceso al panel de administración
