# Privacidad por diseño

## La privacidad como afterthought

La mayoría de los servicios digitales funcionan así: primero se construye el producto, se optimiza para crecimiento y monetización, y al final —cuando hay problemas legales o presión de usuarios— se añaden controles de privacidad. Un botón para borrar tu cuenta. Una opción para desactivar el seguimiento de anuncios. Un aviso de cookies.

Esto se llama privacidad como afterthought, como algo que se añade después. El problema es que cuando la arquitectura ya está construida para recopilar y compartir `datos`, los controles superficiales no cambian la naturaleza del sistema.

**Privacidad por diseño** es lo opuesto: la privacidad es una consideración desde el primer momento del diseño del sistema, no un añadido al final. El resultado es una arquitectura donde proteger los `datos` es el comportamiento por defecto, no la excepción.

## Qué significa en la práctica

**Los `datos` no salen del hardware propio**

Correo, chat, contraseñas, archivos, calendarios, contactos: todo vive en el servidor físico de la `interfaz`. No hay una copia en "la nube" de Google, Microsoft o Amazon. No hay sincronización automática a servidores de terceros.

Cuando envías un mensaje a través de la instancia de Matrix (Dendrite), ese mensaje viaja del cliente al servidor propio y del servidor propio al destinatario. No pasa por los servidores de ninguna empresa de comunicaciones.

Cuando guardas una contraseña en Vaultwarden, ese dato vive en el disco cifrado del servidor. No en los servidores de Bitwarden ni en ningún otro lugar.

**DNS local: la privacidad que se olvida**

Las consultas DNS son un vector de vigilancia que mucha gente ignora. Cada vez que visitas un sitio web, tu `dispositivo` pregunta a un servidor DNS: "¿cuál es la dirección IP de este dominio?" Esa consulta revela qué sitios visitas, a qué hora, con qué frecuencia.

Si usas el DNS de Google (8.8.8.8) o el de Cloudflare (1.1.1.1), esas empresas tienen un registro detallado de tu comportamiento en internet.

Esta `interfaz` usa **AdGuard Home** como servidor DNS local. Todas las consultas DNS de la red local se resuelven a través de él, sin salir a proveedores externos. Además bloquea dominios de rastreo y publicidad a nivel de DNS, antes de que lleguen al navegador.

**Notificaciones sin Google ni Apple**

Las aplicaciones móviles normalmente usan Firebase Cloud Messaging (de Google) o APNs (Apple Push Notification Service) para enviar notificaciones push. Esto significa que cada notificación —"tienes un mensaje nuevo", "tu tarea está lista"— pasa por los servidores de Google o Apple.

Esta `interfaz` usa **ntfy**, un servidor de notificaciones push autoalojado y de código abierto. Las notificaciones van directamente del servidor al cliente sin pasar por terceros.

**El `computador` local nunca está expuesto directamente**

El `computador` local —donde viven los `datos`— no tiene puertos abiertos a internet. No es accesible directamente desde fuera. Solo el VPS (el servidor en la nube que hace de intermediario) está expuesto a internet, y su función es únicamente reenviar tráfico a través del túnel cifrado.

Esto significa que el `computador` local no aparece en ningún escaneo de puertos de internet. Su existencia es, desde el exterior, invisible.

**Cifrado en reposo**

Si alguien obtiene acceso físico al servidor —lo roba, lo confisca, lo inspecciona— los discos son ilegibles sin la clave LUKS. No hay carpetas de fotos, bases de `datos` de correo ni archivos de configuración accesibles sin descifrar primero el disco.

## La tensión honesta: el túnel de Cloudflare

Esta `interfaz` puede configurarse de dos maneras para el tunelado:

1. **Newt + Pangolin**: el tráfico va del usuario al VPS propio, a través del túnel WireGuard, hasta el `computador` local. Ningún tercero ve el tráfico.

2. **Cloudflare Tunnel**: el tráfico pasa por la red de Cloudflare antes de llegar al servidor. Cloudflare puede ver el tráfico HTTPS.

La opción con Cloudflare es más sencilla de configurar y más resiliente ante ataques DDoS. Pero implica que Cloudflare tiene acceso al tráfico que pasa por su red. Aunque el contenido de las aplicaciones individuales puede estar cifrado adicionalmente, la capa de transporte HTTPS la gestiona Cloudflare.

Esta es una decisión que cada administrador toma según su modelo de amenaza. No hay una respuesta universalmente correcta.

## Tu modelo de amenaza

Un **modelo de amenaza** es una manera de pensar sistemáticamente en los riesgos. En lugar de intentar protegerse de todo (imposible), se responden preguntas concretas:

- ¿De quién te estás protegiendo?
- ¿Qué recursos tiene ese adversario?
- ¿Qué consecuencias tiene un fallo?

Los modelos de amenaza más comunes:

**Publicistas y rastreadores comerciales**: recopilan `datos` sobre tu comportamiento para venderte publicidad. Son omnipresentes pero no muy sofisticados. DNS local, ntfy y no usar servicios de Google/Meta ya es suficiente protección contra ellos.

**Atacantes oportunistas**: buscan sistemas con vulnerabilidades conocidas para comprometer, ransomware, acceso no autorizado. El modelo Zero Trust, TOTP, y mantener el software actualizado es protección suficiente.

**Proveedores de servicios**: la empresa cuyo servicio usas tiene acceso a tus `datos` por definición. La única protección real es no usar sus servicios y alojar los propios. Eso es exactamente lo que hace esta `interfaz`.

**Adversarios con recursos estatales**: agencias de inteligencia con capacidad de interceptar tráfico a escala, comprometer hardware, presionar a proveedores. Protegerse de este nivel de amenaza requiere medidas adicionales que están fuera del alcance de esta `interfaz`.

Saber contra qué te proteges ayuda a tomar decisiones razonables: Cloudflare puede ser aceptable si tu modelo de amenaza son publicistas y atacantes oportunistas, y no lo es si tu adversario es Cloudflare mismo.

Ver también: [Modelo de `cuidados`](modelo.md) · [Cifrado en capas](cifrado.md) · [Servicios: túnel](../servicios/túnel_cifrado.md) · [Servicios: DNS](../servicios/)
