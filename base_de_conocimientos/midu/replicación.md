---
title: replicación
tipo: índice
estado: borrador
tags: [replicación, midu]
relaciones:
  parte_de: midu.md
  relacionado:
    - midu/replicación/documentación.md
    - midu/replicación/preparativos.md
    - midu/arquitectura/nixos.md
    - midu/replicación/nixos.md
    - midu/replicación/configuración.md
    - lenguaje_común/lenguaje_común.md
    - midu/replicación/secretos.md
    - midu/arquitectura/conectarse_en_internet.md
    - midu/replicación/vps.md
    - midu/cuidados/zero-trust.md
    - lenguaje_común/objetos_digitales.md
---

# `replicación`

← [Inicio](../../README.md#la-replicación)

## La complejidad

Replicar una `midu` requiere de tiempo y trabajo. Es un proceso complejo, no es difícil pero reconocemos que existe una curva de aprendizaje para toda persona o comunidad que decida aprender a configurar y personalizar la `interfaz` con la que `interactúa` con sus `datos`, la posibilidad de participar activamente en un ejercicio de `gobernanza participativa` nos invita a imaginar el lugar que queremos ocupar en las **infraestructuras humanas** que nos sea posible `construir` gracias a las **infraestructuras digitales y físicas** que estamos `desplegando`. En el proceso queremos entender que la posibilidad de `soberanía` nos exije de `autonomía` y `responsabilidad`, dos habilidades igualmente necesarias a la hora de `cuidar` la `vida`.

En los `Conspiratorios populares de las soberanías` nos interesa darle `cuerpo` a una `entidad` que se nos ha descrito como `abstracta`; **"la nube"**, al igual que la **inteligencia artificial**, funcionan como formas de simplificar, agrupar e invisibilizar las `infraestructuras` que las hacen posibles; observar y manipular su `materialidad` nos permite interiorizar una gran cantidad de prácticas de `cuidado`. Esta es una `interpretación` de conceptos que, traducidos a técnicas, buscan garantizar la `viabilidad` de la `midu` y de nuestras `memorias colectivas`.

Más allá de ser un proceso técnico, la replicación es un ejemplo de `transdisciplinariedad`: las `subjetividades` que pretendemos `transferir` están compuestas de reflexiones sobre la **confianza** y el **cuidado colectivo**, las decisiones técnicas operan como representaciones concretas de una serie de **principios** y **valores**.

## El descubrimiento

Puede ser que mucha de esta información nos resulte nueva y confusa al principio. Eso está bien, significa que acabamos de encontrar un mundo que no conocíamos, debemos aprender a `comunicarnos` en un nuevo `lenguaje`, crear nuestras propias `relaciones` para interpretarlo. Toda esta información está dispuesta para facilitar ese aprendizaje, la `documentación` de la experiencia de `replicación` es parte del proceso de `transferencia`.

### La documentación como práctica pedagógica continua

Documentar el proceso de `replicación` es parte del proceso mismo. Registrar las decisiones que tomamos, los obstáculos que encontramos y las adaptaciones que hacemos convierte cada `replicación` en una práctica pedagógica: el conocimiento que generamos puede transferirse a quien venga después.

> [Documentar el proceso de `replicación`](replicación/documentación.md)

### Los preparativos

Para prepararnos podemos empezar por `respirar` y disponernos en una actitud semejante a aquella en la que se inicia una exploración. La naturaleza colectiva de los `Conspiratorios populares de las soberanías` nos invita a no hacerlo solos; sin embargo, este material pretende contener lo necesario para `replicar` la `midu` por cuenta propia, de manera `autónoma`.

> [Preparativos](replicación/preparativos.md)

### El sistema operativo: nixos I

[NixOS](arquitectura/nixos.md) es el `sistema operativo` de la `midu`. La primera fase de la replicación cubre tres pasos: instalar NixOS en el disco principal, cifrar los dos discos con LUKS, y configurar el acceso remoto por SSH en la fase de arranque para poder desbloquear el `computador` de forma remota.

> [Instalación y cifrado de discos duros](replicación/nixos.md)

### Personalizar la configuración

`config.nix` conecta la configuración genérica del repositorio con los valores específicos de cada instalación: nombre del `computador`, idioma del sistema, UUIDs de los discos, dominio. Este paso consiste en copiar la plantilla y completar cada campo.

> [Personalizar configuración: `config.nix`](replicación/configuración.md)

### Generar secretos

Los servicios de la `midu` necesitan contraseñas, tokens y claves para funcionar. Este paso genera las claves de cifrado con [age](../lenguaje_común/lenguaje_común.md#age) y cifra los secretos con [sops](../lenguaje_común/lenguaje_común.md#sops) para que puedan ser leídos por los servicios del sistema.

> [Generar secretos](replicación/secretos.md)

### El sistema operativo: nixos II

Una vez hemos completado `config.nix` y cifrado los secretos, el sistema puede construirse por primera vez. Este paso clona el repositorio, enlaza la configuración de NixOS y ejecuta la primera construcción del sistema.

> [Clonar el `repositorio` y construir el sistema](replicación/nixos.md#paso-6-clonar-el-repositorio-y-construir-el-sistema)

### Conectarse en internet

La `midu` necesita un intermediario con IP pública fija para recibir tráfico desde internet. Hay tres rutas posibles; la elección determina el nivel de `exposición` del tráfico entrante y saliente.

> [Servicios de internet, nombres de dominio y rutas](arquitectura/conectarse_en_internet.md)

#### El `computador` desechable

El [servidor virtual privado](../lenguaje_común/lenguaje_común.md#vps) es el punto de entrada público de la `midu`, un `computador` arrendado en "la nube" que actúa como intermediario. Es desechable por diseño: la estrategia consiste en poder reemplazarlo sin perder ningún `dato`. El túnel ZeroTrust es una `abstracción` de la idea del `computador` **desechable**, en este caso lo que sería desechable es la `cuenta` asociada a los recursos de Cloudflare que usaremos.

> [Despliegue del VPS](replicación/vps.md)
> [Túnel ZeroTrust](cuidados/zero-trust.md)

## La secuencia de replicación

| Paso | Contenido | Tiempo estimado |
|---------|-----------|-----------------|
| [Documentar el proceso](replicación/documentación.md) | Registrar decisiones, obstáculos y adaptaciones durante la `replicación` | Continuo |
| [Prepararse](replicación/preparativos.md) | Hardware, herramientas y conocimientos previos | 15 min (lectura) |
| [Instalar NixOS y cifrar discos](replicación/nixos.md) | Configurar el SO, cifrado LUKS, SSH en initrd | 45–90 min |
| [Personalizar la configuración](replicación/configuración.md) | Completar `config.nix` con los valores del `computador` | 20–30 min |
| [Generar los secretos](replicación/secretos.md) | Claves age, sops-nix, cifrado de secretos y LUKS | 30–45 min |
| [Construir el sistema](replicación/nixos.md#paso-6-clonar-el-repositorio-y-construir-el-sistema) | Clonar el `repositorio`, enlazar la configuración y ejecutar la primera construcción | 20–30 min |
| [Conectarse en internet](arquitectura/conectarse_en_internet.md) | Elegir una alternativa | 10 min |
| [Desplegar un VPS](replicación/vps.md) | Despliegue del punto de entrada público (Ruta A o B) | 30–60 min |
| [Crear un túnel ZeroTrust](cuidados/zero-trust.md) | Crear una cuenta en Cloudflare y configurar el túnel | 30 min |

**Tiempo total estimado para el proceso de `replicación`: 4-6 horas.**

Los pasos están diseñados para seguirse en esta secuencia. Hay dependencias entre ellos: no podemos cifrar secretos antes de tener la clave age, y no podemos construir el sistema antes de tener los secretos cifrados.

```mermaid
%%{init: {'theme': 'base', 'gitGraph': {'mainBranchName': 'replicacion'}, 'themeVariables': {'background': '#fbf1c7', 'primaryColor': '#f2e5bc', 'primaryBorderColor': '#3c3836', 'primaryTextColor': '#3c3836', 'lineColor': '#a89984', 'git0': '#458588', 'git1': '#8f3f71', 'git2': '#427b58', 'git3': '#b57614', 'git4': '#cc241d', 'git5': '#b57614', 'git6': '#d65d0e', 'git7': '#cc241d', 'gitBranchLabel0': '#fbf1c7', 'gitBranchLabel1': '#fbf1c7', 'gitBranchLabel2': '#fbf1c7', 'gitBranchLabel3': '#fbf1c7', 'gitBranchLabel4': '#fbf1c7', 'gitBranchLabel5': '#fbf1c7', 'gitBranchLabel6': '#fbf1c7', 'gitBranchLabel7': '#fbf1c7', 'gitInv0': '#fbf1c7', 'gitInv1': '#fbf1c7', 'gitInv2': '#fbf1c7', 'gitInv3': '#fbf1c7', 'gitInv4': '#fbf1c7', 'gitInv5': '#fbf1c7', 'gitInv6': '#fbf1c7', 'gitInv7': '#fbf1c7', 'commitLabelBackground': '#f2e5bc', 'commitLabelColor': '#3c3836'}}}%%
gitGraph
  commit id: "documentación"
  branch documentacion
  checkout replicacion
  commit id: "prepararse"
  checkout documentacion
  commit id: "hardware y herramientas"
  checkout replicacion
  commit id: "instalar NixOS"
  checkout documentacion
  commit id: "obstáculos encontrados"
  checkout replicacion
  commit id: "personalizar config.nix"
  checkout documentacion
  commit id: "decisiones de configuración"
  checkout replicacion
  commit id: "generar secretos"
  checkout documentacion
  commit id: "claves y estructura"
  checkout replicacion
  commit id: "construir sistema"
  checkout documentacion
  commit id: "errores y soluciones"
  checkout replicacion
  commit id: "conectarse en internet"
  merge documentacion
```

## Los objetos digitales de la replicación

El proceso de `replicación` tiene sus propios `objetos digitales`: los archivos con los que preparamos el medio de arranque desde el que instalamos la `midu`. Viven en `midu/nixos/replicate/` y este es su índice completo.

### Imágenes de arranque

Las ISOs que arrancan el instalador o un entorno de rescate:

- [nixos-minimal](../../midu/nixos/replicate/nixos-minimal-25.11.6495.e764fc9a4058-x86_64-linux.iso): imagen mínima de [NixOS](arquitectura/nixos.md) para la instalación por consola
- [nixos-graphical](../../midu/nixos/replicate/nixos-graphical-25.11.6495.e764fc9a4058-x86_64-linux.iso): imagen de NixOS con entorno gráfico
- [archlinux](../../midu/nixos/replicate/archlinux-2026.02.01-x86_64.iso): imagen de Arch Linux como entorno de rescate alternativo

### Objetos de diseño

Los archivos fuente de GIMP de los gráficos del arranque:

- [replicate-logo.xcf](../../midu/nixos/replicate/replicate-logo.xcf): el logo de la `replicación`
- [replicate-grub.xcf](../../midu/nixos/replicate/replicate-grub.xcf): el fondo del menú de arranque GRUB

### Ventoy: el USB multiarranque

Ventoy permite poner varias ISOs en un mismo USB y elegir cuál arrancar desde un menú con tema propio. La carpeta `ventoy/` se copia a la partición Ventoy del USB:

- [ventoy.json](../../midu/nixos/replicate/ventoy/ventoy.json): la configuración de Ventoy y sus plugins
- [README.md](../../midu/nixos/replicate/ventoy/README.md): las instrucciones para preparar el USB
- [theme.txt](../../midu/nixos/replicate/ventoy/theme/replicate/theme.txt): la definición del tema del menú de arranque
- [background.png](../../midu/nixos/replicate/ventoy/theme/replicate/background.png): el fondo del menú
- [ShureTechMonoNerdFont-Regular-32.pf2](../../midu/nixos/replicate/ventoy/theme/replicate/ShureTechMonoNerdFont-Regular-32.pf2): la tipografía del menú

El repertorio visual de íconos de las visualizaciones se cataloga aparte, en [objetos digitales](../lenguaje_común/objetos_digitales.md).

## La posibilidad del error

NixOS cuenta con una función para devolverse al último estado estable del sistema: el [rollback](../lenguaje_común/lenguaje_común.md#rollback). Si hacemos una modificación y la construcción falla o el sistema queda en un estado inesperado, podemos volver a la configuración anterior desde el menú de arranque (GRUB) o con:

```bash
nixos-rebuild switch --rollback
```

El sistema está diseñado para ser reversible.