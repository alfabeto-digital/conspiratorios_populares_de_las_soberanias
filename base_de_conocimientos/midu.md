# La `midu`

← [Inicio](../README.md#la-midu)

Una `midu` (Mínima `Interfaz` Digital Viable) es un **conjunto posible de `infraestructuras` físicas, digitales y humanas** que permiten a una persona o comunidad `gobernar` sus `memorias`, individuales y colectivas, con un criterio de [`soberanía digital`](subjetividades/`soberanía`_digital.md).

La noción de la *viabilidad* proviene de la biología. Un organismo viable es el que tiene los componentes mínimos para existir de forma autónoma y replicarse en nuevos `contextos`. **Cada `midu` configura su propio conjunto de `infraestructuras`**, las que decide que necesita para su existencia `soberana` y su [`replicación`](subjetividades/`replicación`.md) en otro lugar.

## El `dispositivo`

`alfabeto.digital` es un [`dispositivo`](subjetividades/`dispositivo`.md) con tres dimensiones simultáneas:

- Como `dispositivo tecnológico` es una `midu`: un conjunto de `infraestructuras` configurado con herramientas que permiten la `gobernanza` de las `memorias` con un criterio de `soberanía` digital.
- Como `dispositivo pedagógico` es una propuesta de [`alfabetización digital popular`](subjetividades/alfabetización_digital_popular.md): documentar el `desarrollo` del `dispositivo` permite compartir el proceso y poder transferirlo a otra persona o comunidad.
- Como `dispositivo político` es una narrativa sobre el presente que busca introducir unas `subjetividades` en las `infraestructuras` sobre las que nos imaginamos el futuro. Cada decisión técnica encarna valores sobre la privacidad, la `soberanía`, la participación. **Esa subjetividad se transfiere a quien usa el `dispositivo` y, en cada `replicación`, tiene la oportunidad de ser cuestionada, modificada, adaptada**.

## Los principios

Para `alfabeto.digital`, el conjunto mínimo viable está organizado en cuatro principios:

- **Autenticación**: un sistema de verificación de identidad en el que podamos confiar.
- **Comunicaciones** privadas y seguras: correo electrónico propio, chat, notificaciones.
- **Almacenamiento** encriptado y resiliente: un modo de guardar, sincronizar y recuperar `objetos digitales`.
- **Red de `gobernanza` participativa**: herramientas que le permiten a cada persona o comunidad, a través de una `midu`, participar de una red de construcción, custodia y administración de las `memorias` individuales y colectivas.

## Los valores

La `midu` está construida sobre valores concretos:

- **Transparencia**: código abierto y de libre acceso
- **Reproducibilidad**: `infraestructuras` como código, descentralización, `gobernanza` distribuida y federada, servicios que dialogan con `interfaces` compatibles.
- **Privacidad** por diseño: los `datos` son de quien los genera y estas personas deciden cómo, por qué, para qué y con quién compartirlos.

## La arquitectura

La `midu` imita el funcionamiento de un organismo vivo. El `computador` local es el núcleo: almacena las `memorias` y ejecuta todos los servicios. El `computador` desechable (un VPS arrendado o una cuenta de Cloudflare) es la membrana: filtra el tráfico entrante, puede destruirse y reconstruirse sin perder ningún `dato`. El túnel cifrado conecta la membrana con el núcleo sin exponer el núcleo a internet.

NixOS es el genoma del sistema: describe el estado completo de cada máquina como código. Modificar el genoma reconstruye el sistema; revertir el genoma lo restaura. El `flake.nix` es el punto de entrada que declara las dependencias exactas y cómo ensamblarlas; el `flake.lock` fija la secuencia precisa para que dos máquinas construidas desde el mismo repositorio produzcan el mismo sistema.

El patrón dendrítico organiza la configuración: añadir un servicio nuevo es crear un archivo nuevo en el directorio correcto, sin modificar ningún archivo central. Los secretos (contraseñas, tokens, claves) viven cifrados en el repositorio; `age` los cifra para la máquina que los necesita y `sops-nix` los descifra durante la construcción del sistema.

La [visualización de una red local soberana](lenguaje_común/visualizaciones/midu-una_red_local_soberana.png) muestra esta arquitectura completa; su [presentación animada](lenguaje_común/visualizaciones/midu-una_red_local_soberana-slideshow.excalidraw.md) la recorre paso a paso.

- [El `computador` local y el `computador` desechable](midu/arquitectura/computadores.md)
- [NixOS](midu/arquitectura/nixos.md)
- [El Nix Flake](midu/arquitectura/flake.md)
- [El patrón dendrítico](midu/arquitectura/patrón_dendrítico.md)
- [Gestión de secretos](midu/arquitectura/secretos.md)
- [Las capas de la memoria](midu/arquitectura/capas_de_la_memoria.md)
- [Almacenamiento federado](midu/arquitectura/almacenamiento_federado.md)
- [Tipos de midu](midu/arquitectura/tipos_de_midu.md)
- [Estimaciones](midu/arquitectura/estimaciones.md)

### Conectarse en internet

El `computador` local vive en una red privada sin IP pública fija. Un intermediario público recibe el tráfico desde internet y lo reenvía al `computador` local. Antes de llegar a la `midu`, toda solicitud pasa por el Proveedor de internet ISP, el DNS y el registrador de dominio; la ruta que decidamos usar determina qué información se expone y a quién.

Hay tres rutas posibles. Las Rutas A y B usan un VPS arrendado como `computador` desechable que expone un `túnel cifrado`. La Ruta C usa la red de Cloudflare y un tunel ZeroTrust; la configuración es más simple pero Cloudflare se dedica explícitamente a monitorear patrones de tráfico en internet con propósitos comerciales. La `soberanía` sobre el tráfico en las tres rutas depende de la combinación del tunel cifrado y la naturaleza desechable de estas opciones para conectarse en internet. 

La [visualización de la conexión a internet](lenguaje_común/visualizaciones/midu-conectarse_en_internet.png) traza las rutas y los actores; su [presentación animada](lenguaje_común/visualizaciones/midu-conectarse_en_internet-slideshow.excalidraw.md) las recorre paso a paso.

- [Conectarse en internet](midu/arquitectura/conectarse_en_internet.md)
- [Ruta A: VPS con NixOS](midu/replicación/rutas/ruta_A-vps+nixos.md)
- [Ruta B: VPS con Podman](midu/replicación/rutas/ruta_B-vps+podman.md)
- [Ruta C: túnel de Cloudflare](midu/replicación/rutas/ruta_C-cloudflare.md)

## Los cuidados

Los `cuidados` son el conjunto de decisiones que protegen la `midu`: las personas, las `memorias` y las `infraestructuras` que las sostienen.

Cinco principios articulan el modelo: 
- **Defensa en profundidad**: ninguna capa es la última línea de defensa.
- **Menor privilegio**: cada componente tiene exactamente los permisos que necesita.
- **Separación de responsabilidades**: el `computador` local no está expuesto a internet; el `computador` desechable no almacena `datos`.
- **Desconfiar de los intermediarios**: asumir por diseño que no podemos confiar en los proveedores del `computador` desechable y exponer de manera controlada los recursos locales a internet.
- **Superficie de ataque mínima**: existe un único camino hacia cualquier servicio de la `midu` y es necesario autenticarse para poder acceder a ellos.

- [`cuidados`](midu/cuidados.md)
- [Zero Trust](midu/cuidados/zero-trust.md)
- [Cifrado](midu/cuidados/cifrado.md)
- [Privacidad](midu/cuidados/privacidad.md)

## Los servicios

Los servicios son los programas que corren continuamente en el `computador` local y responden cuando los necesitamos. Se organizan según las [capas de la memoria](midu/arquitectura/capas_de_la_memoria.md): los estratos funcionales donde cada capa sostiene lo que puede existir en las capas superiores.

- **Enrutamiento**: el único camino hacia cualquier servicio. Pangolin en el `computador` desechable, Caddy como proxy inverso, AdGuard como DNS local, Authelia como autenticación de dos factores.
- **Comunicaciones**: correo con Stalwart, chat federado con Dendrite, notificaciones con ntfy.
- **Observabilidad**: métricas con Prometheus, logs con Loki, visualización con Grafana, alertas con Alertmanager.
- **Almacenamiento**: base de `datos` con PostgreSQL, archivos con Syncthing, contraseñas con Vaultwarden, documentos con Paperless-ngx, fotos con Immich.
- **Procesamiento**: modelos de lenguaje locales con Ollama.
- **Descubribilidad**: base de conocimientos navegable con Hugo, búsqueda federada con SearXNG.
- **Colaboración**: documentos con Collabora Online, gestión del conocimiento con Wiki.js.
- **Participación**: microblogging federado con GoToSocial, video con PeerTube, blog con WriteFreely.
- **Reproducibilidad**: repositorio git con Forgejo, CI/CD con Woodpecker, backups con Restic.

- [Todos los servicios](midu/servicios.md)

## La replicación

Replicar una `midu` requiere tiempo y trabajo. Reconocemos que existe una curva de aprendizaje para toda persona o comunidad que decida configurar la `interfaz` con la que interactúa con sus `memorias`. La documentación del proceso es una práctica pedagógica: registrar las decisiones que tomamos, los obstáculos que encontramos y las adaptaciones que hacemos convierte cada `replicación` en una experiencia transferible.

La secuencia sigue un orden con dependencias: 
- Preparativos,
- instalación de NixOS y cifrado de discos,
- personalización del sistema: `config.nix`,
- generación de secretos,
- construcción del sistema y
- conexión a internet. 

El tiempo estimado para la `replicación` es de unas 6 horas. NixOS incluye la opción `rollback`, es como un `Ctrl + Z`: si algo sale mal, podemos volver al último estado estable desde el menú de arranque.

- [Documentar el proceso](midu/replicación/documentación.md)
- [Preparativos](midu/replicación/preparativos.md)
- [Instalar NixOS y cifrar discos](midu/replicación/nixos.md)
- [Personalizar `config.nix`](midu/replicación/configuración.md)
- [Generar secretos](midu/replicación/secretos.md)
- [Desplegar el `computador` desechable](midu/replicación/vps.md)

## Ver también

- [Subjetividades](subjetividades.md): las ideas que articulan las decisiones de la `midu`
- [Lenguaje común](lenguaje_común/lenguaje_común.md): definiciones del vocabulario usado en la documentación
- [Cartografía de lo esencial](lenguaje_común/cartografía_de_lo_esencial.md): las visualizaciones de las `infraestructuras` y sus presentaciones animadas
