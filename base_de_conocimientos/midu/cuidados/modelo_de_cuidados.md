# Modelo de `cuidados`

Todo sistema de seguridad parte de un conjunto de principios que guían las decisiones de diseño. Antes de hablar de herramientas concretas, vale la pena entender el modelo mental que está detrás de esta `interfaz`.

## Defensa en profundidad

El principio más importante: ninguna capa de seguridad es la última línea de defensa.

Si el único mecanismo de protección es una contraseña, basta robar esa contraseña para tener acceso a todo. En cambio, cuando hay capas apiladas —contraseña más segundo factor más disco cifrado más tráfico cifrado— un atacante tiene que comprometer todas ellas de manera simultánea.

Esta `interfaz` tiene cuatro capas activas en todo momento:

1. El disco de `datos` está cifrado (LUKS).
2. Los secretos del sistema están cifrados (age/sops-nix).
3. El tráfico está cifrado (TLS + WireGuard).
4. El acceso requiere dos factores (contraseña + TOTP).

Un fallo en cualquiera de ellas —por ejemplo, que alguien intercepte el tráfico TLS— no da acceso a los `datos`, porque el disco sigue cifrado y la autenticación sigue requiriendo TOTP.

## Principio de menor privilegio

Cada componente del sistema tiene exactamente los permisos que necesita para funcionar, y ninguno más.

Algunos ejemplos concretos:

- El usuario de base de `datos` que usa Authelia puede leer y escribir solo en la base de `datos` de Authelia. No puede tocar la base de `datos` de Dendrite (el servidor de chat), ni la de ningún otro servicio.
- El VPS (el servidor en la nube que actúa como punto de entrada) reenvía tráfico cifrado hacia el `computador` local. No tiene acceso a los `datos`. No puede leer correos, archivos ni mensajes.
- El usuario del sistema que ejecuta Syncthing puede acceder a los directorios de sincronización asignados. No puede modificar los archivos de Vaultwarden (el gestor de contraseñas) ni de ningún otro servicio.
- La clave SSH de despliegue (la que usa el proceso automatizado de actualización) tiene permisos de solo lectura sobre el repositorio. No puede modificar nada.

La razón es sencilla: si ese componente se ve comprometido, el daño está contenido. Un atacante que toma el control del proceso de Syncthing no obtiene acceso a las contraseñas almacenadas en Vaultwarden.

## Separación de responsabilidades

El sistema está dividido en dos máquinas con roles claramente distintos:

- **`computador` local** (en casa o en un datacenter propio): aquí viven los `datos`. Correo, archivos, chat, contraseñas. Esta máquina no está expuesta directamente a internet.
- **VPS** (servidor en la nube): su única función es recibir tráfico de internet y reenviarlo al `computador` local a través de un túnel cifrado. No almacena `datos`. No procesa información.

Este diseño tiene una consecuencia importante: comprometer el VPS no da acceso a los `datos`. El VPS solo ve tráfico cifrado que no puede descifrar.

## Asumir compromiso

Este es quizás el principio más contraintuitivo: el sistema está diseñado asumiendo que cualquier componente puede ser comprometido en algún momento.

No es pesimismo. Es realismo. Y obliga a hacerse preguntas incómodas pero útiles:

- ¿Qué pasa si el VPS cae o es tomado por un atacante? → Los `datos` siguen en el `computador` local, cifrados en reposo. El atacante solo obtiene un servidor vacío que reenvía tráfico cifrado.
- ¿Qué pasa si una contraseña de un servicio se filtra (por ejemplo, la contraseña de la `interfaz` web de Nextcloud)? → Los `datos` del disco siguen cifrados con LUKS. Acceder al servicio a través de la web no da acceso al disco completo.
- ¿Qué pasa si alguien roba físicamente el servidor? → Sin la clave LUKS, el disco es ilegible.
- ¿Qué pasa si el repositorio git se hace público por error? → Los secretos están cifrados con age. Sin la clave age de la máquina, son ilegibles.

Diseñar asumiendo compromiso lleva a construir compartimentos estancos. Si uno falla, los demás siguen en pie.

## Superficie de ataque mínima

La superficie de ataque es el conjunto de puntos por donde un atacante podría intentar entrar. Cuanto más pequeña, mejor.

El `computador` local no está directamente expuesto a internet. No tiene puertos abiertos al mundo. El único camino para llegar a él es:

1. Entrar al VPS (que está expuesto a internet).
2. Pasar por el túnel WireGuard cifrado.
3. Llegar a Caddy, que actúa como proxy inverso.
4. Pasar por la verificación de Authelia (usuario + contraseña + TOTP).
5. Finalmente llegar al servicio solicitado.

Son cinco puertas en serie. No en paralelo.

Ver también: [Cifrado en capas](cifrado.md) · [Arquitectura Zero Trust](zero-trust.md) · [Arquitectura general](../arquitectura/)
