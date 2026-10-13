# ¿Qué es NixOS?

## El genoma del sistema

Un organismo no se configura órgano por órgano, en sesiones de trabajo que nadie registra. Su forma y función están codificadas en el genoma: la información que se replica con fidelidad en cada célula y que permite reconstruir el organismo completo. Si supiéramos leer el genoma de un ser vivo, podríamos entender exactamente cómo está construido, no como fue configurado una vez, sino cómo está ahora y cómo puede replicarse.

Los sistemas operativos convencionales funcionan de la otra manera: los configuras paso a paso, instalas cosas, cambias archivos, deshabilitas servicios que dejaron de funcionar. Con el tiempo, el sistema acumula un historial de decisiones que nadie registró completamente. Si algo se rompe, no sabes exactamente qué cambió.

NixOS propone algo diferente: el sistema está descrito en un genoma, el `flake.nix` y sus módulos. Ese genoma dice exactamente qué servicios existen, cómo están configurados, qué dependencias tienen. Cuando quieres cambiar algo, modificas el genoma y el sistema se reconstruye para coincidir con él. Si algo sale mal, vuelves a la versión anterior del genoma y el sistema vuelve a ser exactamente como era.

Un organismo cuyo genoma está completamente descrito puede replicarse con fidelidad estructural. Eso es lo que hace de NixOS la elección natural para una MIDV: un sistema que se puede entender, auditar y reproducir exactamente en otro hardware.

Esto tiene un nombre técnico: **configuración declarativa**. En lugar de ejecutar pasos ("instala esto", "cambia este archivo", "habilita este servicio"), describes el *estado* que quieres que tenga el sistema. NixOS se encarga de hacer lo necesario para llegar ahí.

## ¿Qué significa "declarativo"?

La mayoría de los sistemas operativos son *imperativos*: les das instrucciones paso a paso.

```
# Imperativo (Ubuntu, Debian, etc.)
apt install nginx
systemctl enable nginx
nano /etc/nginx/nginx.conf   # editas el archivo manualmente
systemctl restart nginx
```

NixOS es *declarativo*: describes el resultado que quieres.

```nix
# Declarativo (NixOS)
services.nginx.enable = true;
services.nginx.virtualHosts."ejemplo.com" = { ... };
```

NixOS lee esa declaración y construye el sistema para que se ajuste a ella. Si nginx no está instalado, lo instala. Si ya está configurado diferente, lo reconfigura. Si eliminas esas líneas, lo desinstala.

La diferencia parece sutil pero tiene consecuencias enormes.

## Reproducibilidad: dos máquinas, el mismo sistema

Si tienes el mismo código NixOS en dos máquinas diferentes, obtienes exactamente el mismo sistema. No "parecido", igual. Cada paquete con la misma versión, cada archivo de configuración con el mismo contenido.

Esto se llama **reproducibilidad**. Es útil por varias razones:

- Puedes probar cambios en una máquina de prueba antes de aplicarlos en producción.
- Si una máquina se estropea, la reemplazas aplicando el mismo código en hardware nuevo.
- Puedes auditar exactamente qué tiene el sistema: está todo en el código, no hay configuraciones ocultas aplicadas manualmente meses atrás.

## Rollbacks: deshacer sin miedo

Cada vez que aplicas una nueva configuración en NixOS, el sistema anterior no desaparece: se convierte en una entrada del gestor de arranque. Si la nueva configuración tiene un problema, reinicias y seleccionas la versión anterior. El sistema vuelve a funcionar exactamente como antes.

Es como tener control de versiones para el sistema operativo completo.

## Auditabilidad: el estado oculto no existe

En un sistema operativo convencional, el estado del sistema es la suma de todo lo que se ha hecho en él desde que se instaló: paquetes instalados a mano, archivos de configuración editados, servicios activados con un comando hace dos años. Nadie tiene un registro completo.

En NixOS, si algo está en el sistema es porque está declarado en el código. No hay estado oculto. Esto tiene implicaciones de seguridad directas: es más fácil detectar si algo ha sido añadido sin autorización, porque la única fuente de verdad es el código.

## NixOS como decisión de `soberanía`

Usar NixOS es apostar por la **transparencia radical** del sistema. Si alguien revisa el repositorio de esta `interfaz`, puede entender exactamente qué está corriendo en el servidor, cómo está configurado y por qué. No hay pasos manuales que solo conoce quien montó el sistema originalmente.

Esta transparencia es compatible con la seguridad: lo que está en el repositorio es el código que describe la configuración, no los secretos (contraseñas, claves). Los secretos tienen su propio sistema de gestión, descrito en [Gestión de secretos](secretos.md).

Ver también:
- [¿Qué es un Nix Flake?](flake.md)
- [El patrón dendrítico](patrón_dendrítico.md)
- [Gestión de secretos](secretos.md)
