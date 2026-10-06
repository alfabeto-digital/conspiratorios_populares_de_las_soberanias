# Pangolin: el túnel cifrado del VPS

← [Servicios](servicios.md)

## ¿Qué es esto?

Pangolin es el sistema que vive en el VPS y gestiona el tráfico que llega de internet antes de enviarlo al `computador` local. No es un solo programa: es un conjunto de tres piezas que trabajan juntas, Pangolin, Gerbil y Traefik, más el protocolo WireGuard que conecta todo.

El VPS (Virtual Private Server) es un servidor alquilado en la nube con una dirección IP pública fija y conocida. Su único rol es ser la dirección postal visible del sistema: recibe el tráfico que viene de internet y lo reenvía por el túnel cifrado al `computador` local, donde viven los `datos`. El VPS no almacena nada importante.

## Las tres piezas

### Traefik: el recepcionista del VPS

Traefik es un reverse proxy, igual que Caddy en el `computador` local, pero orientado al tráfico que entra desde internet hacia el VPS. Recibe las peticiones HTTP y HTTPS que llegan al VPS, mira el nombre de dominio y las reenvía al destino correcto.

Traefik se elige aquí porque está diseñado para funcionar bien con contenedores Docker y configuración dinámica, cuando se define un nuevo servicio en Pangolin, Traefik lo detecta automáticamente sin necesidad de reiniciar ni editar archivos de configuración manualmente.

### Pangolin: el orquestador

Pangolin es el sistema central de gestión. Es el que sabe qué servicios existen, bajo qué dominios son accesibles y a través de qué túneles WireGuard llegan. Tiene un panel de administración web donde se gestionan los sitios, los dominios y los pares WireGuard.

La analogía: si Traefik es el recepcionista, Pangolin es la directora de la oficina, decide quién puede entrar, a dónde va cada cosa y mantiene el registro de todos los túneles activos.

### Gerbil: el gestor de WireGuard

Gerbil es el componente que crea y mantiene las interfaces WireGuard. WireGuard necesita configurar interfaces de red en el sistema operativo para establecer los túneles. Gerbil gestiona esas interfaces: cuando el cliente Newt del `computador` local se conecta, Gerbil crea el par WireGuard correspondiente y configura el enrutamiento del tráfico.

## WireGuard: el túnel cifrado

WireGuard es un protocolo VPN (Virtual Private Network, red privada virtual) moderno. Una VPN crea un túnel cifrado entre dos puntos de la red, de modo que el tráfico que viaja por el túnel no puede ser leído por nadie en el camino.

WireGuard se destaca porque:

- **Es simple**: su código es mucho más corto que OpenVPN o IPSec, lo que lo hace más fácil de auditar y menos propenso a errores de seguridad.
- **Es rápido**: usa criptografía moderna y tiene una latencia muy baja.
- **Es confiable**: el protocolo es robusto ante cambios de red (si el `computador` local cambia de IP, el túnel se recupera solo).

El túnel WireGuard entre el VPS y el `computador` local es completamente transparente para los usuarios: el tráfico entra por Traefik en el VPS, viaja cifrado por WireGuard hasta el `computador` local, y llega a Caddy como si viniera del VPS directamente.

## ¿Cómo funciona en alfabeto.digital?

```
INTERNET
    ↓
[Traefik] ← recibe y clasifica el tráfico por dominio
    ↓
[Pangolin] ← sabe a qué túnel enviar cada petición
    ↓
[Gerbil / WireGuard] ← túnel cifrado hasta el computador local
    ↓
[computador local: Caddy]
```

El stack de Pangolin puede correr de dos formas:

- **Como módulos NixOS**: si el VPS corre NixOS. La configuración está declarada en `nixos/modules/nixos/network/pangolin-server.nix`.
- **Como contenedores Docker**: si el VPS corre cualquier otra distribución de Linux. La configuración está en `vps/docker-compose.yml`. Esta es la opción más común para VPS de proveedores que no ofrecen NixOS como imagen base.

## El rol del VPS en la arquitectura de seguridad

El VPS es el único punto del sistema con una IP pública. Cualquier ataque que venga de internet llega primero al VPS, no al `computador` local. Si el VPS fuera comprometido completamente, lo peor que podría pasar es que el servicio deje de ser accesible, los `datos` siguen en el `computador` local, que no es accesible desde internet directamente.

Esta separación es intencional: el VPS es descartable. Se puede destruir y reconstruir en minutos sin perder ningún dato, porque no almacena nada importante.

## Ver también

- [Túnel](túnel.md): la decisión entre Cloudflare y Newt+WireGuard
- [Caddy](caddy.md): el reverse proxy del `computador` local que recibe el tráfico del VPS
- [Visión general](../arquitectura/visión-general.md): el flujo completo de tráfico
- [El `computador` local y el VPS](../arquitectura/hosts.md): las dos máquinas, sus roles y por qué están separadas
