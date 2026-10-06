# El túnel: Cloudflare o Newt

← [Servicios](servicios.md)

## El problema de fondo

El `computador` local vive en una red privada, una casa, una oficina, un espacio físico con una conexión a internet convencional. Esa conexión no tiene una IP pública fija, o si la tiene, exponer los puertos directamente a internet abre una superficie de ataque enorme: cualquier persona en el mundo puede intentar conectarse directamente a la máquina.

La solución es un túnel: en lugar de que el servidor hable directamente con internet, el servidor abre una conexión saliente hacia un punto público (el VPS o la red de Cloudflare). El tráfico de internet llega a ese punto público y es reenviado por el túnel hasta el servidor real. Nadie en internet conoce la IP real del servidor.

## Las dos opciones

alfabeto.digital implementa dos mecanismos de túnel distintos. Solo se usa uno a la vez. La elección se hace en el archivo `config.nix` con una línea:

```nix
tunnel_type = "cloudflare";   # Opción A
# o
tunnel_type = "newt";         # Opción B
```

## Opción A: Cloudflare Tunnel

Cloudflare es una empresa que opera una de las redes de distribución de contenido más grandes del mundo. Su servicio de túneles (*Cloudflare Tunnel*, antes Argo Tunnel) permite conectar un servidor privado a la red de Cloudflare de forma gratuita: el cliente `cloudflared` abre una conexión saliente hacia Cloudflare, y Cloudflare reenvía el tráfico de internet a través de esa conexión.

**Ventajas:**
- Configuración simple: funciona en minutos con una cuenta gratuita de Cloudflare.
- Sin necesidad de VPS propio.
- Protección DDoS incluida, la red de Cloudflare absorbe el tráfico malicioso antes de que llegue al servidor.
- Cloudflare gestiona los certificados TLS públicos.

**El costo real:**

Cloudflare termina el TLS en su red. Esto significa que entre el navegador del usuario y los servidores de Cloudflare, la conexión está cifrada. Pero entre Cloudflare y el servidor, el tráfico puede descifrarse en la red de Cloudflare antes de ser reenviado. Cloudflare es, técnicamente, un hombre en el medio (*man in the middle*): tiene la capacidad técnica de leer el tráfico.

La empresa tiene una política de privacidad y no lee el contenido de los túneles de sus clientes, pero esa protección es una promesa legal y de confianza, no una garantía técnica. Si Cloudflare quisiera (o fuera obligada legalmente) a acceder al contenido de tu tráfico, podría hacerlo.

Para muchos casos de uso esto es aceptable. Para una `interfaz` cuyo propósito declarado es la `soberanía` digital, es una tensión que vale la pena nombrar.

En alfabeto.digital, `cloudflared` corre dentro de un contenedor Podman, aislado del sistema principal, con acceso limitado a lo estrictamente necesario.

**Módulo NixOS:** `nixos/modules/nixos/network/cloudflare.nix`

## Opción B: Newt + WireGuard (soberano)

Newt es el cliente del proyecto Pangolin. En lugar de depender de la infraestructura de Cloudflare, el tráfico va cifrado mediante WireGuard hasta el VPS propio.

WireGuard es un protocolo VPN moderno: más rápido, más simple y más auditado que los protocolos VPN anteriores (OpenVPN, IPSec). El túnel entre el `computador` local y el VPS está completamente cifrado con WireGuard, nadie en el camino puede leer el contenido, ni el proveedor de internet, ni el datacenter donde vive el VPS.

**Ventajas:**
- Nadie excepto tú tiene acceso técnico al tráfico. El VPS solo ve paquetes WireGuard cifrados.
- No hay dependencia de una empresa externa.
- El protocolo WireGuard es auditado, de código abierto y confiable.
- Si no te gusta el VPS, cambias de proveedor sin perder nada.

**El costo real:**

Requiere un VPS propio. Un VPS básico tiene un costo mensual (típicamente entre 4 y 6 dólares al mes en proveedores como Hetzner o BuyVM). Requiere más configuración inicial: instalar Pangolin en el VPS, gestionar las claves WireGuard, mantener el sistema.

El VPS también es un punto de entrada que hay que mantener seguro. Si el VPS es comprometido, el atacante puede ver el tráfico antes de que entre al túnel WireGuard (aunque no el contenido, que está cifrado de extremo a extremo por TLS).

**Módulo NixOS:** `nixos/modules/nixos/network/newt.nix`

## La tensión real

Esta elección ilustra con claridad una de las tensiones más honestas de la `soberanía` digital: **conveniencia contra independencia**.

Cloudflare es más fácil. Funciona de inmediato, no requiere VPS, tiene más documentación en internet y la mayoría de las personas no necesita preocuparse por lo que Cloudflare pueda hacer con el tráfico, especialmente si los servicios tienen cifrado propio (HTTPS, Signal Protocol en Matrix) que añade una capa adicional.

Newt + WireGuard es más soberano. El tráfico no pasa por ninguna empresa externa. El control es completo. Pero es más trabajo, más costo y más responsabilidad.

No hay una respuesta correcta universal. La respuesta depende del modelo de amenaza de quien administra el sistema: ¿de quién quieres protegerte? ¿Cuánto tiempo y dinero puedes invertir? ¿Cuánta complejidad puedes mantener a largo plazo?

Lo que sí es importante es que la decisión sea consciente. No elegir Cloudflare porque es "lo que viene por defecto" sin entender qué implica, sino elegirlo (o no) sabiendo exactamente qué se está cediendo y qué se está ganando.

## Ver también

- [Pangolin](pangolin.md): el stack del VPS que recibe el tráfico del túnel Newt
- [Caddy](caddy.md): el proxy que recibe el tráfico dentro del `computador` local
- [Visión general](../arquitectura/visión-general.md): el flujo completo de tráfico
- [`soberanía` digital](../../fundamentos/`soberanía`-digital.md): el concepto político que rodea esta decisión
