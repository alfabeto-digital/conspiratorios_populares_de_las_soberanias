# AdGuard Home

← [Servicios](servicios.md)

## ¿Qué es esto?

AdGuard Home es el servidor DNS del sistema. DNS, *Domain Name System*, sistema de nombres de dominio, es el directorio telefónico de internet: convierte nombres legibles (como `alfabeto.digital`) en las direcciones numéricas que las computadoras usan para encontrarse entre sí. Sin DNS, tendrías que saber de memoria que `1.2.3.4` es el servidor de correo. Con DNS, basta con escribir `mail.alfabeto.digital`.

AdGuard Home no solo traduce nombres: también decide qué nombres puede resolver tu red y cuáles no. Cuando un sitio de publicidad o un rastreador de comportamiento aparece en la lista de bloqueo, AdGuard simplemente no lo resuelve, y ese tráfico nunca sale del `dispositivo`.

## ¿Para qué sirve?

**Como servidor DNS:** todos los `dispositivo`s de la red apuntan a AdGuard Home como su servidor DNS. En lugar de usar el DNS de tu proveedor de internet o el de Google (8.8.8.8), la red usa su propio servidor, que tiene control sobre qué se resuelve y qué no.

**Como bloqueador de rastreadores:** los bloqueadores de publicidad en el navegador actúan por software, después de que el tráfico ya llegó. AdGuard actúa antes: si el dominio de un rastreador está en la lista de bloqueo, la petición nunca sale del `dispositivo`. Esto funciona para todas las aplicaciones del sistema, no solo para el navegador.

**Para la red interna:** AdGuard también puede resolver nombres internos del sistema, útil para que los servicios se encuentren entre sí por nombre en lugar de por IP.

## ¿Por qué AdGuard específicamente?

La alternativa más común es Pi-hole, que hace algo muy similar. AdGuard Home se eligió porque:

- Tiene una `interfaz` web más moderna y sin base de `datos` separada.
- Soporta DNS-over-HTTPS y DNS-over-TLS de fábrica, esto cifra las consultas DNS, de modo que el proveedor de internet no puede ver qué sitios estás resolviendo.
- El mantenimiento es activo y la integración con NixOS está bien mantenida.

## ¿Cómo funciona en alfabeto.digital?

AdGuard Home corre en el `computador` local y escucha en el puerto 53 (TCP y UDP), que es el puerto estándar del protocolo DNS.

Los `dispositivo`s de la red configuran su servidor DNS para apuntar al `computador` local. Las consultas DNS llegan a AdGuard, que las consulta contra sus listas de bloqueo. Si el dominio está bloqueado, devuelve una respuesta vacía. Si no, resuelve la consulta usando un resolver DNS de confianza configurado en AdGuard.

**Módulo NixOS:** `nixos/modules/nixos/security/adguard.nix`

## La decisión ética: el filtro como poder

Controlar el servidor DNS es controlar qué nombres puede resolver la red. Eso es una forma de filtrado, y el filtrado puede usarse tanto para proteger como para censurar.

En este sistema, el DNS se usa estrictamente para bloquear rastreadores de comportamiento y publicidad: dominios que, por diseño, recopilan `datos` sobre lo que haces en línea para vendérselos a terceros. La lista de bloqueo es pública, auditable y puede modificarse.

La diferencia entre esto y la censura es la transparencia y el control: el administrador del sistema decide qué se bloquea y puede cambiar esa lista. Los bloqueadores de DNS de los proveedores de internet, en cambio, operan de forma opaca, bloquean sin avisar y sin posibilidad de auditoría.

Tener el DNS bajo control propio significa que esas decisiones quedan en manos de quien administra el sistema, no del proveedor de internet, no de Google, no de Cloudflare.

## Ver también

- [Caddy](caddy.md): el proxy que gestiona el tráfico HTTPS
- [`cuidados`](../../`cuidados`/modelo_de_`cuidados`.md): el modelo de `cuidados` general
- [Arquitectura](../arquitectura/visión-general.md): el flujo completo del tráfico
