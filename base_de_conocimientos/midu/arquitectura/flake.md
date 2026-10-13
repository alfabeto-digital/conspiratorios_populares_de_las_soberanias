# ¿Qué es un Nix Flake?

## La receta y los ingredientes

Imagina que quieres hacer un plato que siempre salga igual, sin importar quién lo cocine ni cuándo. Para eso necesitas dos cosas:

1. **La lista de ingredientes** con las versiones exactas: no "harina", sino "harina de trigo, moltura media, marca X, lote de enero de 2025". Así, dos cocineros que sigan la misma receta con los mismos ingredientes obtienen exactamente el mismo resultado.

2. **La receta** que describe cómo combinar esos ingredientes y qué platos se pueden preparar con ellos.

Un **Nix Flake** es exactamente eso para un sistema NixOS.

- El archivo `flake.nix` es la receta: define los ingredientes (inputs) y qué se puede construir con ellos (outputs).
- El archivo `flake.lock` es la lista de ingredientes con versiones exactas: ancla cada dependencia a un commit específico, de modo que el sistema puede reproducirse exactamente.

## La estructura de `flake.nix`

El archivo `nixos/flake.nix` tiene dos secciones principales:

### Inputs: los ingredientes

```nix
inputs = {
  nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  home-manager.url = "github:nix-community/home-manager";
  sops-nix.url = "github:Mic92/sops-nix";
  flake-parts.url = "github:hercules-ci/flake-parts";
  import-tree.url = "github:vic/import-tree";
};
```

Cada input es una dependencia externa. Veamos para qué sirve cada una:

- **nixpkgs**: el repositorio de paquetes de NixOS. Contiene decenas de miles de paquetes (programas, bibliotecas, herramientas). Es el supermercado donde el sistema va a buscar todo lo que necesita.
- **home-manager**: extensión de NixOS para gestionar la configuración del entorno de usuario (shell, editor, atajos, dotfiles). Lo que NixOS hace para el sistema, home-manager lo hace para el usuario.
- **sops-nix**: integración entre el sistema de secretos (sops + age) y NixOS. Permite descifrar secretos durante la construcción del sistema y ponerlos disponibles para los servicios.
- **flake-parts**: un framework para organizar el flake en módulos más pequeños y manejables. Sin él, todo el código de configuración viviría en un único archivo enorme.
- **import-tree**: la herramienta que implementa el patrón dendrítico, carga recursivamente todos los módulos `.nix` de un directorio. Descrito en detalle en [El patrón dendrítico](patrón_dendrítico.md).

### Outputs: lo que se construye

```nix
outputs = { flake-parts, ... }@inputs:
  flake-parts.lib.mkFlake { inherit inputs; } {
    systems = [ "x86_64-linux" ];
    imports = [ ./flake-module.nix ];
  };
```

Los outputs definen qué se puede hacer con este flake. En este caso, lo principal son dos **configuraciones NixOS**:

- La configuración del **`computador` local** (`alfabeto.digital`)
- La configuración del **VPS**

Cuando ejecutas `nixos-rebuild switch --flake .#alfabeto.digital`, Nix lee el flake, encuentra el output correspondiente a `alfabeto.digital` y construye el sistema.

## El archivo `flake.lock`

Este archivo lo genera Nix automáticamente la primera vez que construyes el sistema, y se actualiza cuando ejecutas `nix flake update`. Contiene el commit exacto de cada repositorio en los inputs:

```json
"nixpkgs": {
  "locked": {
    "rev": "a3a3dda3bacf61e8a39258a0b9c6abc6c7abc8d6",
    ...
  }
}
```

Gracias a este archivo, dos personas que clonen el repositorio y construyan el sistema obtendrán exactamente los mismos paquetes, con las mismas versiones, compilados con las mismas dependencias. No hay sorpresas por actualizaciones automáticas.

El `flake.lock` sí se commitea al repositorio. Es parte de la garantía de reproducibilidad.

## flake-parts: dividir para no enloquecer

Sin ningún framework, todo el código de un flake vive en `flake.nix`. Para proyectos pequeños funciona. Para una `interfaz` con dos hosts, decenas de módulos y múltiples capas de configuración, ese archivo se vuelve inmanejable.

**flake-parts** resuelve esto permitiendo que el flake se divida en módulos. En lugar de tener un `flake.nix` de mil líneas, la `interfaz` tiene:

- `flake.nix`, el punto de entrada, pequeño
- `flake-module.nix`, donde se importan los demás módulos
- Los módulos de configuración de cada host, servicio y capa

Cada módulo puede definir sus propios inputs, outputs y configuración parcial. flake-parts los compone en el sistema final.

## ¿Tengo que entender todo esto para replicar esta `interfaz`?

No necesariamente. Para replicar esta `interfaz`, basta con seguir las instrucciones de [instalación](../`replicación`/). Para modificar servicios existentes, puedes editar los módulos correspondientes sin tocar el flake.

Entender el flake importa cuando quieres:

- Actualizar las dependencias del sistema (`nix flake update`)
- Añadir una dependencia nueva (un input que no existe todavía)
- Entender por qué algo tiene una versión específica

Para la mayoría de las tareas cotidianas, el flake es transparente.

Ver también:
- [¿Qué es NixOS?](nixos.md)
- [El patrón dendrítico](patrón_dendrítico.md)
- [El `computador` local y el VPS](hosts.md)
