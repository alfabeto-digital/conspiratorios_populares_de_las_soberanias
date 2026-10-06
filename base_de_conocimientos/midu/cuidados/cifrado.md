# Cifrado en capas

El cifrado es el proceso de convertir información legible en `datos` ininteligibles sin la clave correcta. Esta `interfaz` usa cuatro formas distintas de cifrado, cada una protegiendo una cosa diferente en un momento diferente.

## LUKS: el disco cifrado

LUKS (Linux Unified Key Setup) es el estándar de cifrado de disco en Linux. La analogía más cercana: imagina meter tus documentos dentro de un sobre sellado antes de guardarlos en el archivador. Alguien que robe el archivador solo tiene sobres sellados. Sin la clave para abrirlos, no puede leer nada.

En esta `interfaz` hay dos discos, y ambos están cifrados:

**nvme0, el disco del sistema operativo**

Este disco se cifró durante la instalación de NixOS. Contiene el sistema operativo y la configuración. Para poder arrancar, NixOS necesita descifrar este disco primero.

El problema: ¿cómo descifrar un disco de forma remota si el sistema operativo aún no ha arrancado? La solución es el **desbloqueo por SSH en initrd**.

initrd (initial RAM disk) es un sistema mínimo que carga antes del sistema operativo completo. Esta `interfaz` lo configura para arrancar un servidor SSH mínimo durante esa fase inicial. Desde cualquier lugar del mundo, un administrador puede conectarse por SSH a ese servidor mínimo, introducir la passphrase de LUKS, y el sistema continúa arrancando normalmente.

Una vez que el disco está desbloqueado, initrd monta el sistema de archivos real y el arranque de NixOS sigue su curso normal.

**nvme1, el disco de `datos`**

Aquí viven las bases de `datos` de todos los servicios: correo, chat, archivos, contraseñas. También está cifrado con LUKS.

A diferencia del disco del SO, este se desbloquea **automáticamente al arrancar** usando una clave gestionada por sops-nix (ver la sección siguiente). Hay además una passphrase de emergencia como respaldo, en caso de que el sistema de gestión de claves falle.

Resultado práctico: si alguien roba físicamente el disco de `datos`, obtiene un bloque de `datos` aleatorios ilegibles.

## age + sops-nix: los secretos cifrados

Los secretos son las contraseñas, tokens y claves que los servicios necesitan para funcionar: la contraseña del administrador de la base de `datos`, el token de API de Cloudflare, los secretos de Authelia, las contraseñas de las cuentas de correo.

Estos secretos tienen que estar en algún lugar del sistema para que los servicios los puedan usar. Pero guardarlos en texto plano en el repositorio git sería un desastre de seguridad.

La solución es **age** (una herramienta de cifrado moderno) combinada con **sops-nix** (integración de SOPS con NixOS).

La analogía: un sistema de cajas fuertes donde cada caja tiene su propia llave única. Hay una caja para el `computador` local y otra para el VPS. Cada una tiene su llave propia. Lo que está dentro de la caja del `computador` local solo lo puede abrir la llave del `computador` local.

Así funciona en la práctica:

- Cada máquina genera una **clave age** única durante la instalación. La parte privada de esa clave nunca sale de la máquina y nunca va al repositorio git.
- Los secretos se cifran con esa clave age usando SOPS y se guardan en `secrets.yaml`. Ese archivo **sí va al repositorio git**, pero cifrado. Incluso si el repositorio fuera público, los secretos serían ilegibles sin la clave age de la máquina.
- Cuando NixOS construye la configuración del sistema, sops-nix descifra los secretos en memoria y los pone en los lugares donde los servicios los esperan.
- El `computador` local y el VPS tienen claves age completamente independientes. Los secretos del `computador` local no se pueden descifrar con la clave del VPS, y viceversa.

Secretos que gestiona este sistema: contraseñas de root y admin, contraseñas de bases de `datos`, token de Cloudflare, tokens de Newt (el cliente de túnel), clave privada de Dendrite, secretos de Authelia, contraseñas de Stalwart (el servidor de correo), token de Gerbil.

## TLS: el tráfico cifrado

TLS (Transport Layer Security) es el protocolo que cifra el tráfico entre tu navegador y un servidor web. Cuando ves el candado en la barra de direcciones del navegador, es TLS en acción.

La analogía: un sobre sellado para cada paquete que viaja por internet. Aunque alguien intercepte el paquete en tránsito, no puede leer su contenido sin la clave.

En esta `interfaz`, **Caddy** gestiona los certificados TLS automáticamente. Utiliza el protocolo ACME (Automatic Certificate Management Environment) para obtener certificados gratuitos de **Let's Encrypt**, una autoridad de certificación sin ánimo de lucro. El proceso es completamente automático: Caddy solicita el certificado, Let's Encrypt verifica que el dominio pertenece al servidor, y el certificado se renueva automáticamente antes de que expire.

Todo el tráfico externo hacia alfabeto.digital pasa por TLS. No hay excepciones para servicios "internos" que sean accesibles desde internet.

**WireGuard** añade una capa adicional de cifrado para el túnel entre el VPS y el `computador` local. El tráfico que llega al VPS ya está cifrado por TLS, y luego viaja a través del túnel WireGuard (que también cifra), y llega al `computador` local donde Caddy lo procesa. Son dos capas de cifrado en tránsito simultáneas para ese segmento de la ruta.

## TOTP: el segundo factor de autenticación

TOTP (Time-based One-Time Password) es el sistema de códigos de un solo uso que cambian cada 30 segundos. Lo conoces de la verificación en dos pasos de bancos y servicios web.

La analogía: un candado que cambia su combinación cada 30 segundos. Incluso si alguien roba tu contraseña, necesita también el código TOTP del momento exacto. Y ese código expira en 30 segundos.

En esta `interfaz`, **Authelia** exige TOTP además de la contraseña para acceder a cualquier servicio. La aplicación recomendada para generar los códigos es **Aegis** (Android, código abierto, sin telemetría).

El flujo completo de autenticación:

1. El usuario llega a un servicio (por ejemplo, `nextcloud.dominio.com`).
2. Caddy intercepta la solicitud y pregunta a Authelia: "¿está autenticado este usuario?"
3. Authelia redirige al usuario a la pantalla de login.
4. El usuario introduce su contraseña y el código TOTP del momento.
5. Authelia verifica ambos factores y emite una cookie de sesión.
6. Caddy deja pasar la solicitud al servicio.

## Tabla resumen

| Qué protege | Herramienta | Cuándo cifra |
|---|---|---|
| Disco del SO | LUKS | En reposo; desbloqueo remoto por SSH |
| Disco de `datos` | LUKS | En reposo; desbloqueo automático con clave sops |
| Secretos (contraseñas, tokens) | age + sops-nix | En reposo; descifrado por NixOS al construir |
| Tráfico externo | TLS (Caddy / Let's Encrypt) | En tránsito |
| Túnel VPS ↔ Servidor | WireGuard | En tránsito |
| Identidad de usuario | TOTP (Authelia) | En la autenticación |

Ver también: [Modelo de `cuidados`](modelo.md) · [Arquitectura Zero Trust](zero-trust.md) · [Servicios: túnel](../servicios/túnel_cifrado.md)
