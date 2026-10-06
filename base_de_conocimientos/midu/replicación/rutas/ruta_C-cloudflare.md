# Ruta C: túnel de Cloudflare

← [Conectarse a internet](../../conectarse_a_internet.md)

## Qué es esta ruta

El `computador` local vive en una red privada, una casa, una oficina, cualquier lugar con una conexión doméstica o corporativa. Esa conexión no tiene una IP pública fija ni puertos abiertos al exterior. Cloudflare Tunnel resuelve esto sin necesidad de un servidor intermediario propio: el agente `cloudflared` abre una conexión saliente hacia la red de Cloudflare, y Cloudflare reenvía el tráfico de internet a través de esa conexión hasta el `computador` local.

Nadie en internet conoce la IP real del `computador` local. El `computador` local nunca abre puertos al exterior.

## Arquitectura Zero Trust

Esta ruta se combina con la arquitectura Zero Trust del `computador` local: aunque el tráfico entra por Cloudflare, ningún servicio lo acepta sin verificación. [Caddy](../../servicios/caddy.md) recibe todo el tráfico y consulta a [Authelia](../../servicios/authelia.md) antes de reenviar cualquier solicitud.

- Ningún componente confía en ningún otro por defecto.
- Cada solicitud se autentica antes de llegar al servicio destino.
- Si un servicio fuera comprometido, los demás permanecen aislados.

Más detalle: [Arquitectura Zero Trust](../../cuidados/zero-trust.md)

## La tensión política de esta ruta

Cloudflare termina el [TLS](../../../lenguaje_común/lenguaje_común.md#tls) en su red antes de reenviar el tráfico al `computador` local. Técnicamente puede leer el contenido de las comunicaciones que pasan por el túnel. Es un hombre en el medio ([*man in the middle*](../../../lenguaje_común/lenguaje_común.md#mitm)) de confianza: tiene la capacidad técnica aunque no la use por política.

Para una [`interfaz`](../../../subjetividades/interfaces.md) cuyo propósito declarado es la [`soberanía`](../../../subjetividades/`soberanía`_digital.md) digital, esta es una tensión real que vale la pena nombrar con honestidad. Los servicios del `computador` local tienen cifrado propio (HTTPS, Signal Protocol en [Matrix](../../../lenguaje_común/lenguaje_común.md#matrix)) que añade capas adicionales. La decisión debe ser consciente.

Si el modelo de amenaza incluye a Cloudflare como adversario potencial, ver [Ruta A](ruta_A-vps+nixos.md) o [Ruta B](ruta_B-vps+podman.md).

## Configuración en alfabeto.digital

En `config.nix`, activar el túnel de Cloudflare con:

```nix
tunnel_type = "cloudflare";
```

El módulo [NixOS](../../arquitectura/nixos.md) que gestiona `cloudflared` está en:

```
nixos/modules/nixos/network/cloudflare.nix
```

`cloudflared` corre dentro de un contenedor [Podman](../../servicios/virtualización.md), aislado del sistema principal, con acceso limitado a lo estrictamente necesario.

## Cuándo elegir esta ruta

- No se quiere gestionar un VPS propio.
- Se prioriza la simplicidad de instalación sobre la `soberanía` completa del tráfico.
- Se confía en Cloudflare como proveedor o se acepta la compensación explícitamente.
- El presupuesto inicial no incluye un servidor adicional.

## Ver también

- [El túnel: Cloudflare o Newt](../../servicios/túnel_cifrado.md): análisis técnico completo de las dos opciones de túnel
- [Arquitectura Zero Trust](../../cuidados/zero-trust.md): el modelo de seguridad del `computador` local
- [Caddy](../../servicios/caddy.md): el proxy inverso que recibe el tráfico dentro del `computador` local
- [Ruta A: VPS con NixOS](ruta_A-vps+nixos.md): alternativa soberana con servidor propio
