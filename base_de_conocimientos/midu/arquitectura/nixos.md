# NixOS

## El sistema operativo

El sistema operativo es la capa que está entre el hardware y los programas que usamos. Gestiona la memoria, los discos, los procesos y la red, y ofrece el entorno donde corren los servicios de la `midu`. Cada servicio, cada base de `datos`, cada archivo cifrado vive sobre el sistema operativo del `computador` local.

### Los sistemas operativos comunes

La mayoría de las personas usan uno de tres sistemas operativos. Windows y macOS son propietarios y cerrados: su código no es público y no podemos inspeccionar cómo funcionan por dentro. GNU/Linux es libre y auditable: su código es abierto, cualquiera puede leerlo, modificarlo y distribuirlo. La `midu` corre sobre Linux porque la `soberanía` sobre las `infraestructuras` empieza por poder ver y gobernar el sistema que gestiona las `memorias`.

### NixOS entre las distribuciones de Linux

Linux llega a cada máquina en forma de distribuciones: Ubuntu, Debian, Fedora, Arch y muchas otras empaquetan el núcleo de Linux junto con sus herramientas y una forma personalizada de instalar programas. La mayoría se configuran de manera imperativa y fragmentada: instalamos un paquete, editamos un archivo, deshabilitamos un servicio, y el sistema va acumulando un historial de decisiones que nadie registra por completo.

NixOS también es una distribución de Linux, con una diferencia profunda: es declarativa y reproducible. En lugar de acumular cambios aplicados a mano, describe el estado completo del sistema en código y lo construye para que coincida con esa descripción.

### El genoma de los otros sistemas operativos está disperso

El genoma de Windows y de macOS es cerrado: no podemos leerlo ni reconstruirlo. El de las distribuciones comunes de Linux es abierto, pero resulta de la acumulación de pasos manuales, paquetes instalados uno a uno y archivos editados a lo largo del tiempo. No existe una descripción única que permita replicar el sistema con exactitud. NixOS reúne todo ese genoma en un solo lugar.

## El genoma de la `midu`

Los organismos vivos codifican su forma y su función en el genoma: la información que se replica en cada célula y que permite reconstruir el organismo completo. Si logramos leer el genoma de un ser vivo, podemos entender exactamente cómo está construido, cómo puede ser replicado y modificado.

NixOS describe el sistema en un genoma, el `flake.nix` y sus módulos. Ese genoma dice exactamente qué servicios existen, cómo están configurados y qué dependencias tienen. Cuando queremos cambiar algo, modificamos el genoma y el sistema se reconstruye para coincidir con él. Si algo sale mal, volvemos a la versión anterior del genoma y el sistema vuelve a ser exactamente como era.

Un organismo cuyo genoma está completamente descrito puede replicarse con fidelidad estructural. Eso hace de NixOS la elección natural para una `midu`: un sistema que podemos entender, auditar y reproducir exactamente en otro hardware.

Esto tiene un nombre técnico: **configuración declarativa**. En lugar de ejecutar pasos ("instala esto", "cambia este archivo", "habilita este servicio"), describimos el *estado* que queremos que tenga el sistema. NixOS se encarga de hacer lo necesario para llegar ahí.

## La configuración declarativa

La mayoría de los sistemas operativos son *imperativos*: reciben instrucciones paso a paso.

```
# Imperativo (Ubuntu, Debian, etc.)
apt install nginx
systemctl enable nginx
nano /etc/nginx/nginx.conf   # editamos el archivo manualmente
systemctl restart nginx
```

NixOS es *declarativo*: describimos el resultado que queremos.

```nix
# Declarativo (NixOS)
services.nginx.enable = true;
services.nginx.virtualHosts."ejemplo.com" = { ... };
```

NixOS lee esa declaración y construye el sistema para que se ajuste a ella. Si nginx no está instalado, lo instala. Si está configurado de otra manera, lo reconfigura. Si eliminamos esas líneas, lo desinstala.

## Reproducibilidad: dos máquinas, el mismo sistema

Con el mismo código NixOS en dos máquinas diferentes, obtenemos exactamente el mismo sistema. Cada paquete con la misma versión, cada archivo de configuración con el mismo contenido, idéntico en las dos.

Esto se llama **reproducibilidad**. Es útil por varias razones:

- Podemos probar cambios en una máquina de prueba antes de aplicarlos en producción.
- Si una máquina se estropea, la reemplazamos aplicando el mismo código en hardware nuevo.
- Podemos auditar exactamente qué tiene el sistema: está todo en el código, no hay configuraciones ocultas aplicadas a mano meses atrás.

## Rollbacks: deshacer sin miedo

Cada vez que aplicamos una nueva configuración en NixOS, el sistema anterior sigue disponible: se convierte en una entrada del gestor de arranque. Si la nueva configuración tiene un problema, reiniciamos y seleccionamos la versión anterior. El sistema vuelve a funcionar exactamente como antes. El [`rollback`](../../lenguaje_común/lenguaje_común.md#rollback) es como tener control de versiones para el sistema operativo completo.

## Auditabilidad: los estados ocultos no existen

En un sistema operativo convencional, el estado del sistema es la suma de todo lo que se ha hecho en él desde que se instaló: paquetes instalados a mano, archivos de configuración editados, servicios activados con un comando hace dos años. Nadie tiene un registro completo.

En NixOS, si algo está en el sistema es porque está declarado en el código. No hay estado oculto. Esto tiene implicaciones de seguridad directas: es más fácil detectar si algo se añadió sin autorización, porque la única fuente de verdad es el código.

## NixOS como decisión de `soberanía`

Usar NixOS es apostar por la **transparencia radical** del sistema. Quien revise el repositorio de esta `interfaz` puede entender exactamente qué está corriendo en el `computador` local, cómo está configurado y por qué. No hay pasos manuales que sólo conoce quien montó el sistema originalmente.

Esta transparencia es compatible con la seguridad: lo que vive en el repositorio es el código que describe la configuración, no los secretos (contraseñas, claves). Los secretos tienen su propio sistema de gestión, descrito en [gestión de secretos](secretos.md).

## Ver también

- [El Nix Flake](flake.md)
- [el patrón dendrítico](patrón_dendrítico.md)
- [gestión de secretos](secretos.md)
