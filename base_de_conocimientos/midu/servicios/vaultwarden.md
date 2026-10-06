# Vaultwarden

← [Servicios](servicios.md)

## ¿Qué es esto?

Vaultwarden es el gestor de contraseñas de la `interfaz`. Las contraseñas se almacenan localmente, cifradas, en infraestructura que administramos, no en los servidores de Google, Apple, 1Password ni ningún otro servicio externo. La alternativa más común implica que otra organización almacena y puede acceder a esos `datos`; con Vaultwarden, ese acceso no existe fuera del sistema que controlamos.

Es compatible con los clientes oficiales de Bitwarden: las mismas aplicaciones para Android, iOS, escritorio y extensión de navegador funcionan con Vaultwarden en lugar de con los servidores de Bitwarden Inc.

## ¿Para qué sirve?

Las contraseñas son la puerta de entrada a toda tu vida digital. Si alguien tiene acceso a tu gestor de contraseñas, tiene acceso a todo lo demás: correo, banca, redes sociales, servicios de trabajo.

Un buen gestor de contraseñas permite:

- **Contraseñas únicas y largas para cada servicio**: sin necesidad de recordarlas todas. Una contraseña reutilizada en dos sitios significa que si uno de los dos es comprometido, el otro también lo está.
- **Autocompletado**: las aplicaciones clientes (extensión de navegador, app móvil) rellenan las contraseñas automáticamente, lo que también protege contra sitios de phishing que imitan el diseño de otro sitio pero tienen una URL diferente.
- **Almacenamiento de notas y `datos` sensibles**: códigos de recuperación, números de tarjeta, claves SSH.
- **Compartir contraseñas de forma segura**: con otras personas de confianza, sin enviarlas por mensaje de texto.

## ¿Por qué Vaultwarden específicamente?

Bitwarden Inc. ofrece un servidor oficial de código abierto, pero es más pesado en recursos. Vaultwarden es una reimplementación del servidor de Bitwarden en Rust, más eficiente, que funciona en hardware modesto y es compatible con todos los clientes oficiales de Bitwarden.

Decisión ética: las contraseñas son lo más sensible que existe en un sistema digital. Tenerlas en un servidor propio significa que:

- Nadie más tiene acceso a ellas. Ni Bitwarden Inc., ni Google, ni Apple, ni ningún tercero.
- No dependen de que una empresa decida cambiar sus condiciones de servicio, sea adquirida o cierre.
- El cifrado se verifica: Vaultwarden cifra todo antes de guardarlo, de modo que incluso si alguien accede directamente a los archivos de la base de `datos`, los `datos` son ilegibles sin la contraseña maestra.

## ¿Cómo funciona en alfabeto.digital?

Vaultwarden corre en el `computador` local y usa SQLite como base de `datos` propia, no depende de PostgreSQL. Esto lo hace más independiente: si PostgreSQL tuviera un problema, Vaultwarden sigue funcionando.

El acceso está protegido por Caddy (HTTPS) y opcionalmente por Authelia, aunque el propio Vaultwarden tiene su propio sistema de autenticación con soporte para 2FA.

**Módulo NixOS:** `nixos/modules/nixos/services/vaultwarden.nix`

## Ver también

- [Authelia](authelia.md): SSO que protege el acceso al panel de administración
- [Caddy](caddy.md): gestiona el HTTPS del servicio
- [`cuidados`](../../`cuidados`/modelo_de_`cuidados`.md): cifrado y protección de `datos` sensibles
