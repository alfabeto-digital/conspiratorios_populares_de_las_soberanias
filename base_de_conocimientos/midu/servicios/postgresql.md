# PostgreSQL

← [Servicios](servicios.md)

## ¿Qué es esto?

PostgreSQL es la biblioteca compartida del sistema. Una base de `datos` es un sistema diseñado para guardar, organizar y recuperar información de forma eficiente y confiable. Varios servicios del sistema necesitan guardar información estructurada, usuarios, sesiones, mensajes, configuraciones, y PostgreSQL es el lugar donde lo hacen.

Cada servicio tiene su propio espacio en esa biblioteca: como si hubiera estantes separados para el correo, para el chat y para la autenticación, cada uno accesible solo con la llave correcta.

## ¿Para qué sirve?

PostgreSQL no es un servicio que los usuarios vean directamente. Es la capa de almacenamiento que usan otros servicios internamente.

En alfabeto.digital, estos servicios guardan sus `datos` en PostgreSQL:

- **Authelia**: sesiones de usuario, configuraciones de 2FA, registros de acceso
- **Stalwart Mail**: buzones, mensajes, reglas de correo
- **Dendrite**: mensajes de Matrix, salas, usuarios

Otros servicios del sistema usan bases de `datos` propias más simples (SQLite): Vaultwarden, ntfy y el propio AdGuard. La decisión de usar PostgreSQL o SQLite depende de la complejidad y el volumen de `datos` esperado.

## ¿Por qué compartir una sola base de `datos`?

La alternativa sería que cada servicio corriera su propio motor de base de `datos` independiente. Eso tiene ventajas de aislamiento, si una base de `datos` falla, no afecta las demás, pero también tiene costos:

- Cada instancia de PostgreSQL consume RAM y CPU, incluso en reposo.
- Administrar múltiples instancias (actualizaciones, backups, monitoreo) multiplica el trabajo.

Compartir una sola instancia de PostgreSQL es más eficiente en recursos. El aislamiento entre servicios se logra a nivel de base de `datos` y usuario, no a nivel de instancia.

## ¿Por qué PostgreSQL específicamente?

PostgreSQL es uno de los sistemas de bases de `datos` relacionales más maduros, confiables y con mejor soporte en el ecosistema de software libre. Los tres servicios que lo usan (Authelia, Stalwart, Dendrite) lo soportan oficialmente y están probados contra él.

## ¿Cómo funciona en alfabeto.digital?

PostgreSQL corre en el `computador` local. Cada servicio tiene su propio usuario de base de `datos` con permisos mínimos:

| Usuario de BD | Permisos |
|---|---|
| `authelia-main` | Solo acceso a la base de `datos` de Authelia |
| `stalwart-mail` | Solo acceso a la base de `datos` de Stalwart |
| `dendrite` | Solo acceso a la base de `datos` de Dendrite |

Este es el **principio de menor privilegio**: cada componente del sistema tiene exactamente los permisos que necesita para funcionar, y ninguno más. Si la cuenta de base de `datos` de Stalwart fuera comprometida, el atacante no podría acceder a los `datos` de Authelia ni de Dendrite, cada uno vive en su propia base de `datos` con su propia llave.

**Módulo NixOS:** `nixos/modules/nixos/database.nix`

## Ver también

- [Authelia](authelia.md): usa PostgreSQL para sesiones y usuarios
- [Stalwart](stalwart.md): usa PostgreSQL para correo
- [Dendrite](dendrite.md): usa PostgreSQL para mensajes Matrix
- [`cuidados`](../../`cuidados`/modelo_de_`cuidados`.md): principio de menor privilegio y aislamiento
