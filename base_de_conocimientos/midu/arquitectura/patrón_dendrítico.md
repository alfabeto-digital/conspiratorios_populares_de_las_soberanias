# El patrón dendrítico

## Dendritas: crecer sin modificar el tronco

Las neuronas tienen dendritas: las ramificaciones que reciben señales de otras neuronas. Lo interesante de las dendritas no es solo que existen, sino cómo crecen: cuando una neurona necesita conectarse con más fuentes, forma nuevas ramas. No modifica las que ya tiene. No reemplaza el cuerpo de la neurona. Simplemente añade ramas.

El sistema de configuración de esta `interfaz` funciona de la misma manera. Cada servicio, cada capa de configuración, es una rama independiente. Añadir algo nuevo significa añadir un archivo. Quitar algo significa eliminar o ignorar ese archivo. Nunca hay que ir a un "archivo central" que conozca todos los servicios y actualizar una lista.

## El problema que resuelve

En muchos proyectos NixOS, la configuración principal tiene una sección donde se importan todos los módulos:

```nix
# Patrón convencional: hay que editar este archivo cada vez
imports = [
  ./modules/caddy.nix
  ./modules/stalwart.nix
  ./modules/vaultwarden.nix
  ./modules/syncthing.nix
  # cada nuevo servicio requiere añadir una línea aquí
];
```

Esto funciona, pero tiene un problema: cada vez que añades un servicio, tienes que acordarte de añadirlo a esta lista. Hay un archivo central que "sabe" sobre todos los demás. Es el tronco al que tienes que volver cada vez.

## La solución: import-tree

`import-tree` es una herramienta que lee recursivamente todos los archivos `.nix` de un directorio y los importa automáticamente. En la `interfaz`, la configuración del `computador` local hace algo como:

```nix
imports = [ (importTree ./modules) ];
```

Eso es todo. Nix lee esa línea y automáticamente encuentra y carga todos los archivos `.nix` que haya dentro de `./modules/` y sus subdirectorios.

La estructura actual del directorio de módulos refleja este árbol:

```
nixos/modules/nixos/
├── base.nix             , usuario admin, SSH, firewall, locales
├── storage.nix          , montaje de discos, LUKS
├── database.nix         , PostgreSQL
├── admin.nix            , home-manager del administrador
├── network/
│   ├── caddy.nix        , proxy reverso
│   ├── cloudflare.nix   , túnel Cloudflare
│   ├── newt.nix         , cliente Newt
│   └── pangolin-server.nix, stack Pangolin+Traefik
├── services/
│   ├── vaultwarden.nix
│   └── syncthing.nix
├── communications/
│   ├── stalwart.nix     , correo electrónico
│   ├── dendrite.nix     , chat Matrix
│   └── ntfy.nix         , notificaciones push
└── security/
    ├── authelia.nix     , autenticación
    └── adguard.nix      , DNS con bloqueo de anuncios
```

Para añadir un nuevo servicio, creas un archivo `.nix` en el directorio que corresponda. No hay nada más que hacer. `import-tree` lo encuentra en la siguiente construcción del sistema.

## Activar y desactivar módulos

Que un módulo esté en el directorio no significa que su servicio esté activo. Cada módulo tiene una opción de habilitación:

```nix
# En services/vaultwarden.nix
options.misServicios.vaultwarden.enable = mkEnableOption "Vaultwarden";

config = mkIf cfg.enable {
  services.vaultwarden.enable = true;
  # ... resto de la configuración
};
```

Y en la configuración del host se activa o desactiva:

```nix
# En hosts/alfabeto.digital/default.nix
misServicios.vaultwarden.enable = true;
misServicios.dendrite.enable = false;  # todavía no está listo
```

Así, tener el archivo del módulo en el árbol no activa nada por defecto. Solo se activa lo que el host declara explícitamente.

## El origen del nombre

El nombre "patrón dendrítico" viene de un archivo en el directorio `nixos/00-hallucinations/`: `nix_config_with_dendritic_pattern.vtt`. Es la transcripción de una conversación que exploró este enfoque de organización antes de que la configuración actual existiera. El directorio `00-hallucinations` guarda esos materiales de exploración inicial, útil para entender de dónde vienen las decisiones de diseño de esta `interfaz`.

## Por qué importa para la `soberanía`

Un sistema que cualquier persona técnica puede entender, extender y auditar sin necesidad de leer un archivo central enorme tiene un valor específico: democratiza el mantenimiento. No hay un único guardián que "sabe cómo está montado esto". El árbol es visible, cada rama es legible por separado, y añadir una rama nueva no requiere entender el árbol completo.

Ver también:
- [¿Qué es un Nix Flake?](flake.md)
- [¿Qué es NixOS?](nixos.md)
- [El `computador` local y el VPS](hosts.md)
