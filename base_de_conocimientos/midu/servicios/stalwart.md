# Stalwart Mail

← [Servicios](servicios.md)

## ¿Qué es esto?

Stalwart es el servidor de correo de la `interfaz`. Gestiona tanto el envío como la recepción de mensajes para el dominio que administramos.

El correo electrónico es la columna vertebral de la identidad digital. Prácticamente toda cuenta en internet, desde el banco hasta las redes sociales, se vincula a una dirección de correo para recuperación de contraseñas, verificación y comunicación. Sin servidor de correo propio, esa identidad depende de Gmail, Outlook, Yahoo u otro proveedor externo.

## ¿Para qué sirve?

- **Enviar y recibir correo** con tu propio dominio (`tu@alfabeto.digital` en lugar de `tu@gmail.com`).
- **Independencia de proveedores**: si Gmail cierra tu cuenta por un error algorítmico, pierdes tu identidad digital. Con servidor propio, la cuenta existe mientras exista el servidor.
- **Privacidad de comunicaciones**: el contenido de los mensajes no es analizado para publicidad ni compartido con terceros.
- **Control de las reglas**: puedes configurar exactamente cómo se procesan los mensajes, qué se acepta y qué se rechaza.

## ¿Por qué Stalwart específicamente?

Los servidores de correo tradicionales (Postfix + Dovecot) funcionan bien pero son complejos de configurar correctamente, especialmente en lo que se refiere a autenticación SPF, DKIM y DMARC, que son los mecanismos que evitan que otros envíen correo haciéndose pasar por tu dominio.

Stalwart es una implementación moderna en Rust que integra SMTP e IMAP en un solo proceso, con soporte nativo para SPF, DKIM y DMARC, y una `interfaz` de administración web. Es más simple de mantener que el stack tradicional sin sacrificar funcionalidades.

## Los protocolos del correo

El correo electrónico usa protocolos abiertos, estándares definidos públicamente que cualquier software puede implementar. Esto es lo que lo hace interoperable: puedes enviar correo desde Gmail a Outlook, o desde un servidor propio a cualquier otro servidor del mundo.

- **SMTP** (*Simple Mail Transfer Protocol*), el protocolo de envío. Cuando mandas un correo, tu cliente de correo habla SMTP con tu servidor, y tu servidor habla SMTP con el servidor del destinatario. Puerto 25 (entre servidores), 465 (envío cifrado cliente→servidor), 587 (envío con autenticación).
- **IMAP** (*Internet Message Access Protocol*), el protocolo de sincronización. Tu cliente de correo (Thunderbird, la app nativa del teléfono) descarga los mensajes del servidor y mantiene una copia sincronizada. Puerto 143 (sin cifrar), 993 (cifrado).

Stalwart implementa ambos protocolos en el mismo proceso.

## ¿Cómo funciona en alfabeto.digital?

Stalwart corre en el `computador` local y usa PostgreSQL como base de `datos` para almacenar los mensajes, los buzones y las configuraciones.

Puertos que usa:

| Puerto | Protocolo | Uso |
|---|---|---|
| 25 | SMTP | Recepción de correo de otros servidores |
| 465 | SMTPS | Envío de correo con cifrado TLS desde el cliente |
| 143 | IMAP | Sincronización de correo sin cifrar (uso interno) |
| 993 | IMAPS | Sincronización de correo con cifrado TLS |
| 587 | HTTP | Puerto interno para el relay de Authelia |

**Bootstrap automático:** al arrancar por primera vez, Stalwart crea automáticamente el dominio, el usuario de relay para que Authelia pueda enviar correos de verificación, y la cuenta de administración. No requiere configuración manual inicial.

**Módulo NixOS:** `nixos/modules/nixos/communications/stalwart.nix`

## La decisión ética: Google lee tu correo

Durante años, Google admitió analizar el contenido de los correos en Gmail para personalizar publicidad. Aunque desde 2017 dejó de usar el contenido para anuncios, sigue analizando los mensajes para otros fines. Los términos de servicio de los principales proveedores de correo permiten acceder al contenido de los mensajes en diversas circunstancias.

Un servidor propio de correo significa que el contenido de los mensajes solo lo ve el servidor que administras tú. No hay análisis algorítmico, no hay publicidad, no hay términos de servicio que autoricen a terceros a leer los mensajes.

La contraparte es la responsabilidad: administrar un servidor de correo requiere mantener buenas prácticas de seguridad (SPF, DKIM, DMARC, TLS) y atender a los problemas técnicos cuando surgen. Pero esa es exactamente la definición de `soberanía` digital: tener el control implica también tener la responsabilidad.

## Ver también

- [PostgreSQL](postgresql.md): la base de `datos` que usa Stalwart
- [Authelia](authelia.md): usa el relay de Stalwart para enviar correos de verificación
- [Caddy](caddy.md): gestiona el acceso HTTPS al panel de administración
- [Dendrite](dendrite.md): el otro servicio de comunicaciones del sistema
