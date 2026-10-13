# Los servicios

← [la `midu`](../midu.md#servicios)

Los servicios son los programas que corren continuamente en el `computador` local y responden cuando los necesitamos. La diferencia con los servicios externos es el control: cuando los servicios corren en `infraestructuras` propias, las reglas de acceso, las `memorias` y las decisiones sobre cómo funcionan las tomamos nosotros.

Los servicios de la `midu` se organizan según las [capas de la memoria](arquitectura/capas_de_la_memoria.md): los estratos funcionales donde cada capa sostiene lo que puede existir en las capas superiores.

## El enrutamiento

Antes de llegar a cualquier servicio, el tráfico pasa por una secuencia de puertas. Esta secuencia es la superficie de ataque mínima descrita en los [`cuidados`](cuidados.md): el único camino hacia la `midu`, y un camino que requiere autenticación en cada paso.

| Servicio | Función |
|---|---|
| [Pangolin](servicios/pangolin.md) | El stack del `computador` desechable: gestiona los pares WireGuard y enruta el tráfico hacia el `computador` local |
| [Túnel cifrado](servicios/túnel_cifrado.md) | Cómo el `computador` local establece la conexión con el `computador` desechable: Newt con WireGuard o Cloudflare |
| [Caddy](servicios/caddy.md) | Proxy inverso HTTPS; recibe todo el tráfico entrante y lo distribuye al servicio correcto |
| [AdGuard](servicios/adguard.md) | Servidor DNS local; resuelve consultas sin salir a proveedores externos y bloquea dominios de rastreo |
| [Authelia](servicios/authelia.md) | Inicio de sesión único con segundo factor; ningún servicio es accesible sin pasar por aquí |

## Las comunicaciones

La capa más inmediata: el intercambio de mensajes, documentos y notificaciones entre personas. Los metadatos de comunicación pueden revelar nuestra identidad incluso cuando el contenido está cifrado. Por eso todos estos servicios corren en el `computador` local: los metadatos no salen del sistema.

| Servicio | Función |
|---|---|
| [Stalwart](servicios/stalwart.md) | Servidor de correo electrónico (SMTP/IMAP) |
| [Dendrite](servicios/dendrite.md) | Homeserver de Matrix; mensajería instantánea federada e interoperable con otros servidores |
| [ntfy](servicios/ntfy.md) | Notificaciones push sin pasar por los servidores de Google ni Apple |

## La observabilidad

Sin observabilidad, la `midu` existe pero no puede examinarse. Esta capa permite reflexionar sobre el sistema: qué recursos consume, qué errores produce, qué patrones emergen. Las métricas es permiten auditar y administrar el funcionamiento interno.

| Servicio | Función |
|---|---|
| [Prometheus](../../ROADMAP.md) | Recopilación de métricas del sistema: node, systemd, PostgreSQL, Podman, Caddy, Authelia |
| [Loki + Promtail](../../ROADMAP.md) | Agregación de logs desde journald |
| [Grafana](../../ROADMAP.md) | Visualización de métricas y logs |
| [Alertmanager](../../ROADMAP.md) | Alertas automáticas enviadas a ntfy |
| [Homepage](../../ROADMAP.md) | Portal de servicios; punto de entrada unificado a todos los servicios de la `midu` |
| [Cockpit](../../ROADMAP.md) | Gestión web del `computador` local: terminal SSH y administración de contenedores |

## El almacenamiento

Las `memorias` tienen viven en un lugar físico. Esta capa facilita el almacenamiento estructurado que usan los servicios internamente, la sincronización de archivos entre `dispositivos`, las gestión de credenciales de acceso y los archivos de trabajo.

| Servicio | Función |
|---|---|
| [PostgreSQL](servicios/postgresql.md) | Base de `datos` compartida por Authelia, Dendrite, Stalwart y Vaultwarden |
| [Syncthing](servicios/syncthing.md) | Sincronización de archivos entre `dispositivos` sin pasar por servidores externos |
| [Vaultwarden](servicios/vaultwarden.md) | Gestor de contraseñas cifrado, compatible con Bitwarden |
| [Paperless-ngx](../../ROADMAP.md) | Gestión documental con OCR; digitalización y organización de documentos |
| [Immich](../../ROADMAP.md) | Gestión de fotos y videos con sincronización automática desde el `dispositivo` |
| [Archivebox](../../ROADMAP.md) | Archivo web; guarda copias locales de páginas y recursos de internet |
| [Send / Pairdrop](../../ROADMAP.md) | Transferencia efímera de archivos entre `dispositivos` |

## El procesamiento

El procesamiento es la capa de las transformaciones: extraer texto de un documento, resumir conversaciones, generar nuevas representaciones a partir de las existentes. Los modelos que hacen ese trabajo inscriben subjetividades en sus salidas; tenerlos en el `computador` local los hace auditables y reemplazables.

| Servicio | Función |
|---|---|
| [Ollama](../../ROADMAP.md) | Ejecución de modelos de lenguaje en el `computador` local |
| [Open WebUI](../../ROADMAP.md) | `Interfaz` web para interactuar con los modelos de Ollama |

## La descubribilidad

La capa de descubribilidad nos permite encontrar personas y `memorias` en la red. No basta con que algo exista: tiene que poder ser encontrado. Esta capa incluye tanto la publicación como las herramientas para navegar lo que ya guardamos.

| Servicio | Función |
|---|---|
| [Publicación](servicios/publicación.md) | Hugo convierte los archivos Markdown en un sitio navegable; Pagefind genera el índice de búsqueda en tiempo de ejecución |
| [SearXNG](../../ROADMAP.md) | Motor de búsqueda federado que agrega resultados sin identificar a quien busca |
| [Linkding / Hoarder](../../ROADMAP.md) | Gestión de bookmarks y artículos guardados |

## La colaboración

La colaboración es la capa donde múltiples personas trabajan sobre las mismas `memorias`. Estos servicios cubren la producción conjunta de documentos, la organización del conocimiento compartido y la coordinación del trabajo.

| Servicio | Función |
|---|---|
| [Collabora Online](../../ROADMAP.md) | Suite ofimática en el navegador; edición colaborativa de documentos |
| [Wiki.js](../../ROADMAP.md) | Gestión del conocimiento colaborativa con editor visual |
| [Plane](../../ROADMAP.md) | Gestión de proyectos |

## La participación

La participación es la capa de la presencia pública federada: cómo la `midu` se relaciona con otras `midu`s y con el Fediverso. Cada servicio federado amplía la red de reciprocidad sin ceder el control de las `memorias` a una plataforma centralizada.

| Servicio | Función |
|---|---|
| [GoToSocial / Mastodon](../../ROADMAP.md) | Microblogging federado en el Fediverso |
| [PeerTube](../../ROADMAP.md) | Publicación y distribución de video federado |
| [WriteFreely](../../ROADMAP.md) | Blog federado; publicación de textos largos |
| [Lemmy](../../ROADMAP.md) | Foro federado |
| [Castopod](../../ROADMAP.md) | Publicación de podcasts federada |

## La reproducibilidad

La reproducibilidad es la condición de que el sistema pueda replicarse en nuevos `contextos`. Esta capa incluye las herramientas que permiten construir, mantener, versionar y recuperar la `interfaz`.

| Servicio | Función |
|---|---|
| [Virtualización](servicios/virtualización.md) | Docker y Podman: cómo se despliegan los servicios del `computador` desechable en contenedores |
| [Terminal](servicios/terminal.md) | Herramientas de terminal para administrar el `computador` local: git, SSH, neovim, nix |
| [Forgejo](../../ROADMAP.md) | Repositorio git auto-hospedado |
| [Woodpecker CI](../../ROADMAP.md) | Integración y despliegue continuos para el flake NixOS, integrado con Forgejo |
| [Restic](../../ROADMAP.md) | Backups automatizados y cifrados con política de retención configurable |

## Ver también

- [Capas de la memoria](arquitectura/capas_de_la_memoria.md): la arquitectura conceptual detrás de esta organización
- [la `midu`](../midu.md): las `infraestructuras` que integran los servicios
- [Arquitectura](arquitectura.md): los componentes técnicos del sistema
- [`cuidados`](cuidados.md): cómo protegemos nuestras `memorias`
