# Arquitectura del sistema

← [Inicio](../../README.md#la-midu)

La `midu` está construida como un organismo. Tiene un núcleo donde viven los `datos`, una membrana que filtra el tráfico de entrada y un genoma que describe cómo se configura todo. Estas no son metáforas decorativas; articulan la lógica de cada decisión técnica.

Cada documento de esta sección desarrolla uno de esos conceptos: cómo se mueve el tráfico, qué papel tiene cada máquina, por qué NixOS, cómo se organizan los módulos, cómo se protegen los secretos. Juntos construyen el argumento de que una `infraestructura` propia puede ser comprensible, reproducible y soberana.

## Documentos de esta sección

**[Descripciones generales](arquitectura/descripciones_generales.md)**: el flujo completo del tráfico como célula con membrana. El `computador` local es el núcleo donde viven los `datos`; el VPS es la membrana plasmática, el único punto de contacto con internet; el túnel cifrado es el citoplasma que conecta ambos sin exponer el núcleo. Un buen lugar para empezar.

**[El `computador` local y el VPS](arquitectura/hosts.md)**: las dos máquinas tienen roles deliberadamente asimétricos. El `computador` local almacena todo; el VPS sabe casi nada. Esa asimetría define el modelo de amenaza: si el VPS se compromete, los `datos` siguen seguros.

**[¿Qué es NixOS?](arquitectura/nixos.md)**: si la célula tiene genoma, el sistema tiene `flake.nix`. NixOS describe el estado completo de cada máquina en código: qué servicios corren, cómo están configurados, qué dependencias tienen. Modificar el genoma reconstruye el sistema; revertir el genoma lo restaura.

**[¿Qué es un Nix Flake?](arquitectura/flake.md)**: el punto de entrada del sistema, el archivo que actúa como información genética de la `midu`. Declara las dependencias exactas y cómo ensamblarlas; el `flake.lock` fija la secuencia precisa para que dos máquinas construidas desde el mismo repositorio produzcan el mismo sistema.

**[El patrón dendrítico](arquitectura/patrón_dendrítico.md)**: las dendritas de una neurona crecen hacia nuevas conexiones sin modificar el cuerpo de la neurona. El sistema de módulos funciona igual: añadir un servicio nuevo es crear un archivo nuevo en el directorio correcto. No hay un archivo central que tenga que actualizarse cada vez.

**[Gestión de secretos](arquitectura/secretos.md)**: la configuración vive en el repositorio; los secretos no. `age` cifra cada secreto para la máquina que lo necesita; `sops-nix` los descifra durante la construcción del sistema. El resultado es un repositorio auditable sin ningún valor sensible.

**[Las capas de la memoria](arquitectura/capas_de_la_memoria.md)**: las seis funciones de la `midu` como estratos de la memoria digital: comunicaciones, observabilidad, procesamiento, descubribilidad, reproducibilidad y resiliencia. Cada capa puede estar bajo control propio o delegada a `infraestructuras` externas; la `soberanía` es la capacidad de intervenir en cualquiera de ellas.

**[Almacenamiento federado](arquitectura/almacenamiento_federado.md)**: el modelo de tres capas de almacenamiento y la topología de federación entre nodos. Los `datos` permanecen cifrados, fragmentados y distribuidos geográficamente; ningún nodo alberga una copia completa de los `datos` de otro.

## Archivos de la `interfaz`

Esta tabla describe los archivos más importantes del repositorio y para qué sirve cada uno.

| Archivo | Descripción |
|---|---|
| `config.nix.template` | Plantilla de configuración del `computador` local |
| `config-vps.nix.template` | Plantilla de configuración del VPS |
| `config.nix` | Configuración del `computador` local; existe solo en el `computador` local, no se sube al repositorio |
| `config-vps.nix` | Configuración del VPS; existe solo en el VPS, no se sube al repositorio |
| `flake.nix` | Punto de entrada de Nix Flakes |
| `hardware-configuration.nix` | Generado automáticamente por el instalador; no editar ni subir al repositorio |
| `home/default.nix` | Configuración del entorno de usuario (home-manager) |
| `secrets/secrets.plain.template` | Plantilla de secretos del `computador` local; subir vacía al repositorio |
| `secrets/secrets-vps.plain.template` | Plantilla de secretos del VPS; subir vacía al repositorio |
| `secrets/secrets.yaml` | Secretos cifrados del `computador` local; no se sube al repositorio |
| `secrets/secrets-vps.yaml` | Secretos cifrados del VPS; no se sube al repositorio |
| `.sops.yaml.template` | Plantilla de reglas sops; subir con claves placeholder |
| `replicate-grub/` | ISOs y tema Ventoy para el USB de `replicación` |

Los archivos que no se suben al repositorio existen únicamente en la máquina donde deben estar: si alguien accede al repositorio, no encuentra nada que le sirva para comprometer el sistema. Los archivos `.template` contienen la estructura pero no los valores reales.

## Ver también

- [Conectarse a internet](conectarse_a_internet.md): cómo llega el tráfico externo hasta el `computador` local
- [`replicación`](replicación.md): cómo reproducir este sistema desde cero
