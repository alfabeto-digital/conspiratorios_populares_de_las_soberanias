# El Nix Flake

Si [NixOS](nixos.md) es el genoma del sistema, el Nix Flake es la forma en que ese genoma fija su material y su secuencia exacta para replicarse sin variaciones. Dos archivos lo componen:

- El `flake.nix` declara el material: de dónde viene cada pieza del sistema (los inputs) y qué organismos se pueden construir con ellas (los outputs).
- El `flake.lock` fija la secuencia exacta: ancla cada dependencia a un punto preciso de su historia, de modo que el sistema se reproduce igual en cualquier máquina y en cualquier momento.

## La estructura de `flake.nix`

El archivo `nixos/flake.nix` tiene dos secciones principales.

### Los inputs: las fuentes del material

```nix
inputs = {
  nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  home-manager.url = "github:nix-community/home-manager";
  sops-nix.url = "github:Mic92/sops-nix";
  flake-parts.url = "github:hercules-ci/flake-parts";
  import-tree.url = "github:vic/import-tree";
};
```

Cada input es una fuente externa de la que el sistema toma su material:

- **nixpkgs**: el repositorio de paquetes de NixOS, con decenas de miles de programas, bibliotecas y herramientas. Es el archivo del que el sistema toma todo lo que necesita.
- **home-manager**: extensión de NixOS para gestionar la configuración del entorno de la persona usuaria (shell, editor, atajos, dotfiles). Lo que NixOS hace para el sistema, home-manager lo hace para quien lo usa.
- **sops-nix**: integración entre la gestión de secretos (sops y age) y NixOS. Descifra los secretos durante la construcción del sistema y los pone a disposición de los servicios.
- **flake-parts**: un marco para organizar el flake en módulos más pequeños y manejables. Sin él, todo el código de configuración viviría en un único archivo enorme.
- **import-tree**: la herramienta que implementa el patrón dendrítico, carga de forma recursiva todos los módulos `.nix` de un directorio. Descrita en detalle en [el patrón dendrítico](patrón_dendrítico.md).

### Los outputs: los organismos que se construyen

```nix
outputs = { flake-parts, ... }@inputs:
  flake-parts.lib.mkFlake { inherit inputs; } {
    systems = [ "x86_64-linux" ];
    imports = [ ./flake-module.nix ];
  };
```

Los outputs definen qué organismos se pueden construir con este genoma. En este caso, los principales son dos configuraciones NixOS:

- La configuración del **`computador` local** (`alfabeto.digital`).
- La configuración del **`computador` desechable**.

Cuando ejecutamos `nixos-rebuild switch --flake .#alfabeto.digital`, Nix lee el flake, encuentra el output correspondiente a `alfabeto.digital` y construye el sistema.

## El archivo `flake.lock`: la secuencia fija

Nix genera este archivo la primera vez que construimos el sistema, y lo actualiza cuando ejecutamos `nix flake update`. Contiene el commit exacto de cada repositorio de los inputs:

```json
"nixpkgs": {
  "locked": {
    "rev": "a3a3dda3bacf61e8a39258a0b9c6abc6c7abc8d6",
    ...
  }
}
```

Gracias a este archivo, dos personas que clonen el repositorio y construyan el sistema obtendrán exactamente los mismos paquetes, con las mismas versiones, compilados con las mismas dependencias. No hay sorpresas por actualizaciones automáticas. El `flake.lock` sí se commitea al repositorio: es parte de la garantía de reproducibilidad.

## flake-parts: dividir el genoma en módulos

Sin ningún marco, todo el código de un flake vive en `flake.nix`. Para proyectos pequeños alcanza. Para una `interfaz` con dos `computadores`, decenas de módulos y varias capas de configuración, ese archivo se vuelve inmanejable.

**flake-parts** divide el genoma en módulos. En lugar de un `flake.nix` de mil líneas, la `interfaz` tiene:

- `flake.nix`, el punto de entrada, pequeño.
- `flake-module.nix`, donde se importan los demás módulos.
- Los módulos de configuración de cada `computador`, servicio y capa.

Cada módulo define sus propios inputs, outputs y configuración parcial. flake-parts los compone en el sistema final, igual que el patrón dendrítico organiza los genes en un genoma legible.

## ¿Hace falta entender todo esto para replicar la `interfaz`?

No necesariamente. Para replicar esta `interfaz` basta con seguir las instrucciones de [replicación](../replicación.md). Para modificar servicios existentes, editamos los módulos correspondientes sin tocar el flake.

Entender el flake importa cuando queremos:

- Actualizar las dependencias del sistema (`nix flake update`).
- Añadir una dependencia nueva (un input que todavía no existe).
- Entender por qué algo tiene una versión específica.

Para la mayoría de las tareas cotidianas, el flake es transparente.

## Ver también

- [NixOS](nixos.md)
- [el patrón dendrítico](patrón_dendrítico.md)
- [el `computador` local y el `computador` desechable](computadores.md)
