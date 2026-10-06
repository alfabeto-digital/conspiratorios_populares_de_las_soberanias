# Dendrite

← [Servicios](servicios.md)

## ¿Qué es esto?

Dendrite es el servidor de mensajería instantánea del sistema. Implementa Matrix, un protocolo abierto y federado de chat. Federado significa que tu servidor puede comunicarse con otros servidores Matrix en internet, igual que con el correo electrónico, donde puedes enviar un mensaje desde Gmail a Outlook aunque sean servidores distintos.

La analogía es directa: WhatsApp es como un teléfono de empresa, todos los usuarios tienen que estar en la misma red, y si la empresa cierra o cambia las reglas, te quedas sin servicio. Matrix es como el teléfono público, cualquier operadora puede conectarse con cualquier otra. Si tu servidor de Matrix habla con el servidor de Matrix de otra comunidad, los mensajes fluyen entre ellos sin necesidad de que estén en la misma empresa ni en el mismo país.

## ¿Para qué sirve?

- **Mensajería instantánea** en tiempo real: texto, imágenes, archivos, llamadas de voz y video.
- **Salas de grupo**: equivalente a grupos de WhatsApp o canales de Slack, pero bajo control propio.
- **Federación**: comunicación con usuarios en otros servidores Matrix en internet. No hay walled garden: si alguien usa matrix.org o el servidor Matrix de otra organización, pueden estar en la misma sala.
- **Historial cifrado de extremo a extremo**: con el cifrado activado, ni el servidor puede leer los mensajes. Solo los participantes de la sala tienen las claves.

## ¿Por qué Dendrite específicamente?

El homeserver Matrix más usado es Synapse, que es la implementación de referencia. Synapse es completo pero consume muchos recursos. Dendrite es una reimplementación más moderna en Go, diseñada para ser más eficiente en hardware modesto, ideal para un servidor doméstico.

Hay que ser honesto sobre las limitaciones: Dendrite implementa la mayoría del protocolo Matrix pero no el 100% de las funcionalidades más avanzadas. Para un uso estándar de mensajería, es suficiente. Para casos de uso más complejos (comunidades grandes, bridges a otras plataformas), Synapse sería una mejor opción.

## El protocolo Matrix

El protocolo Matrix fue creado en 2014 con un objetivo explícito: permitir la comunicación entre redes distintas de mensajería sin que ninguna empresa controle el sistema. Funciona así:

- Cada comunidad u organización puede correr su propio *homeserver* (servidor Matrix).
- Los usuarios de distintos homeservers pueden comunicarse entre sí: `@alguien:servidor-a.org` puede estar en una sala con `@otrx:servidor-b.net`.
- Los mensajes se *federan*: el contenido de una sala compartida entre servidores existe en múltiples servidores simultáneamente. No hay un único punto de control.

Esto es exactamente lo mismo que el correo electrónico, y es lo que hace que el correo sea resiliente. Si Gmail desapareciera mañana, el correo seguiría funcionando en el resto de servidores. Matrix aplica el mismo principio a la mensajería instantánea.

## ¿Cómo funciona en alfabeto.digital?

Dendrite corre en el `computador` local y usa PostgreSQL como base de `datos` para almacenar mensajes, usuarios y configuración de salas.

El acceso a Dendrite desde el exterior pasa por Caddy (HTTPS) y Authelia (autenticación). Los clientes de Matrix (Element en escritorio, FluffyChat o Element en móvil) se conectan al servidor usando sus propios mecanismos de autenticación del protocolo Matrix.

**Módulo NixOS:** `nixos/modules/nixos/communications/dendrite.nix`

## La decisión ética: dónde viven tus conversaciones

Los mensajes en WhatsApp pertenecen técnicamente a Meta. Los mensajes en Telegram están en servidores de Telegram Ltd. Los mensajes en Discord están en servidores de Discord Inc. En todos estos casos, la empresa tiene acceso a los metadatos de las conversaciones (quién habla con quién, cuándo, con qué frecuencia) aunque no al contenido si hay cifrado de extremo a extremo.

Con Dendrite en un servidor propio, los mensajes viven en el servidor que administras tú. Los metadatos solo son accesibles para el administrador del sistema. Si hay federación con otros servidores, los mensajes de esas salas también existen en esos otros servidores, lo cual es inherente a la federación, y algo a considerar al decidir qué se comparte en salas federadas.

## Ver también

- [PostgreSQL](postgresql.md): la base de `datos` de Dendrite
- [Stalwart](stalwart.md): el otro servicio de comunicaciones del sistema (correo)
- [ntfy](ntfy.md): notificaciones push, complemento a la mensajería
- [Caddy](caddy.md): gestiona el acceso HTTPS
