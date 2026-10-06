# Caddy

← [Servicios](servicios.md)

## ¿Qué es esto?

Caddy es el punto de entrada de la `interfaz`. Recibe todo el tráfico que llega desde internet y lo distribuye al servicio que corresponde según el dominio solicitado. Es un *reverse proxy*: un programa que se sitúa delante de todos los servicios, recibe las peticiones y las reenvía internamente al proceso correcto.

## ¿Para qué sirve?

Sin Caddy, cada servicio tendría que estar en un puerto distinto y con su propio certificado HTTPS. Nadie querría escribir `alfabeto.digital:8080` en lugar de `mail.alfabeto.digital`. Caddy resuelve eso:

- **Unificación de puertos**: todo llega al puerto 443 (HTTPS estándar). Caddy mira el nombre del dominio y decide a dónde enviarlo.
- **HTTPS automático**: gestiona los certificados TLS mediante el protocolo ACME y Let's Encrypt. Un certificado TLS es lo que hace que el navegador muestre el candado y que la comunicación esté cifrada entre el navegador y el servidor. Sin certificado, los `datos` viajan en texto plano y cualquier intermediario puede leerlos. Caddy los renueva automáticamente antes de que expiren, sin intervención manual.
- **Forward auth**: antes de pasar el tráfico a ciertos servicios, Caddy pregunta a Authelia si el usuario tiene sesión activa. Si no, lo redirige a la pantalla de inicio de sesión.

## ¿Por qué Caddy específicamente?

La alternativa más conocida es Nginx, y también existe Traefik (que se usa en el VPS). Caddy se eligió para el `computador` local porque:

- La gestión automática de certificados está integrada de fábrica, sin plugins ni configuraciones adicionales.
- Su formato de configuración (Caddyfile) es más legible que el de Nginx.
- El soporte para forward auth con Authelia es directo y bien documentado.

## ¿Cómo funciona en alfabeto.digital?

Caddy corre en el `computador` local y escucha en el puerto 443 (HTTPS). Recibe el tráfico que llega a través del túnel desde el VPS.

Para cada subdominio configurado, Caddy hace una o dos cosas:

1. Si el servicio requiere autenticación: consulta a Authelia antes de pasar el tráfico.
2. Pasa el tráfico al servicio correspondiente en su puerto interno.

Los certificados TLS se obtienen automáticamente de Let's Encrypt al arrancar el servicio por primera vez, y se renuevan cada 60 días sin intervención.

**Módulo NixOS:** `nixos/modules/nixos/network/caddy.nix`

## Ver también

- [Authelia](authelia.md): el sistema de autenticación al que Caddy consulta
- [Túnel](túnel.md): cómo llega el tráfico hasta Caddy desde internet
- [Pangolin](pangolin.md): el stack del VPS que reenvía el tráfico a Caddy
- [Visión general](../arquitectura/visión-general.md): el flujo completo de tráfico
