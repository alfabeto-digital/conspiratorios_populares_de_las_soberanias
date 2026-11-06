# Los servicios

← [la `midu`](../midu.md#servicios)

Los servicios son los programas que corren continuamente en el `computador` local y responden cuando los necesitamos. La diferencia con los servicios externos es el control: cuando los servicios corren en `infraestructuras` propias, las reglas de acceso, las `memorias` y las decisiones sobre cómo funcionan las tomamos nosotros.

Los servicios se organizan según las [capas de la memoria](arquitectura/capas_de_la_memoria.md): seis capas que funcionan como la red de activación de una red neuronal, donde cada una participa en los procesos de las demás. Dos tienen subcapas (comunicaciones y procesamiento). La `resiliencia` es una propiedad transversal que existe como principio fundamental en todas las capas, descrita en los [`cuidados`](cuidados.md).

```text
1. Comunicaciones
   1.1 Enrutamiento
2. Observabilidad
3. Procesamiento
   3.1 Colaboración
   3.2 Participación
4. Descubribilidad
5. Reproducibilidad
6. Navegación
```

## 1. Comunicaciones

La capa más inmediata: el intercambio de mensajes, documentos y notificaciones entre personas. Los metadatos de comunicación pueden revelar nuestra identidad incluso cuando el contenido está cifrado. Por eso todos estos servicios corren en el `computador` local: los metadatos no salen del sistema.

| Servicio | Función |
|---|---|
| [Stalwart](servicios/stalwart.md) | Servidor de correo electrónico (SMTP/IMAP) |
| [Dendrite](servicios/dendrite.md) | Homeserver de Matrix; mensajería instantánea federada e interoperable con otros servidores |
| [ntfy](servicios/ntfy.md) | Notificaciones push sin pasar por los servidores de Google ni Apple |

### 1.1 Enrutamiento

Subcapa de las comunicaciones. Antes de llegar a cualquier servicio, el tráfico pasa por una secuencia de puertas: la superficie de ataque mínima descrita en los [`cuidados`](cuidados.md), el único camino hacia la `midu` y un camino que requiere autenticación en cada paso.

| Servicio | Función |
|---|---|
| [Pangolin](servicios/pangolin.md) | El stack del `computador` desechable: gestiona los pares WireGuard y enruta el tráfico hacia el `computador` local |
| [Túnel cifrado](servicios/túnel_cifrado.md) | Cómo el `computador` local establece la conexión con el `computador` desechable: Newt con WireGuard o Cloudflare |
| [Caddy](servicios/caddy.md) | Proxy inverso HTTPS; recibe todo el tráfico entrante y lo distribuye al servicio correcto |
| [AdGuard](servicios/adguard.md) | Servidor DNS local; resuelve consultas sin salir a proveedores externos y bloquea dominios de rastreo |
| [Authelia](servicios/authelia.md) | Inicio de sesión único con segundo factor; ningún servicio es accesible sin pasar por aquí |

## 2. Observabilidad

Sin observabilidad, la `midu` existe pero no puede examinarse. Esta capa permite reflexionar sobre el sistema: qué recursos consume, qué errores produce, qué patrones emergen. Las métricas permiten auditar y administrar el funcionamiento interno.

| Servicio | Función |
|---|---|
| [Prometheus](../../ROADMAP.md) | Recopilación de métricas del sistema: node, systemd, PostgreSQL, Podman, Caddy, Authelia |
| [Loki + Promtail](../../ROADMAP.md) | Agregación de logs desde journald |
| [Grafana](../../ROADMAP.md) | Visualización de métricas y logs |
| [Alertmanager](../../ROADMAP.md) | Alertas automáticas enviadas a ntfy |
| [Homepage](../../ROADMAP.md) | Portal de servicios; punto de entrada unificado a todos los servicios de la `midu` |
| [Cockpit](../../ROADMAP.md) | Gestión web del `computador` local: terminal SSH y administración de contenedores |

## 3. Procesamiento

El procesamiento es la capa de las transformaciones: extraer texto de un documento, resumir conversaciones, generar nuevas representaciones a partir de las existentes. Los modelos que hacen ese trabajo inscriben subjetividades en sus salidas; tenerlos en el `computador` local los hace auditables y reemplazables.

| Servicio | Función |
|---|---|
| [Ollama](../../ROADMAP.md) | Ejecución de modelos de lenguaje en el `computador` local |
| [Open WebUI](../../ROADMAP.md) | `Interfaz` web para interactuar con los modelos de Ollama |
| [Hermes](../../ROADMAP.md) | Procesamiento de `objetos digitales` con modelos de IA |
| [Paperclip](../../ROADMAP.md) | Coordinación de los agentes de Hermes |

### 3.1 Colaboración

Subcapa del procesamiento: donde varias personas trabajan sobre las mismas `memorias`. Estos servicios cubren la producción conjunta de documentos, la organización del conocimiento compartido y la coordinación del trabajo.

| Servicio | Función |
|---|---|
| [NextCloud](../../ROADMAP.md) | Plataforma colaborativa: archivos, documentos, calendario y contactos compartidos |
| [EuroOffice](../../ROADMAP.md) | Suite ofimática: documentos, hojas de cálculo y presentaciones |
| [FrankMD](../../ROADMAP.md) | Gestión del conocimiento en Markdown con notas enlazadas |
| [OpenProject](../../ROADMAP.md) | Gestión de proyectos |

### 3.2 Participación

Subcapa del procesamiento: la presencia pública federada, cómo la `midu` se relaciona con otras `midu` y con el `Fediverso`. Cada servicio federado amplía la red de reciprocidad sin ceder el control de las `memorias` a una plataforma centralizada.

| Servicio | Función |
|---|---|
| [Mastodon](../../ROADMAP.md) | Microblogging federado en el `Fediverso` |
| [Pixelfed](../../ROADMAP.md) | Publicación de fotos federada |
| [PeerTube](../../ROADMAP.md) | Publicación y distribución de video federado |
| [Lemmy](../../ROADMAP.md) | Foro federado |
| [Mobilizon](../../ROADMAP.md) | Eventos y grupos federados |
| [Bookwyrm](../../ROADMAP.md) | Lectura social federada: reseñas y seguimiento de libros |
| [Castopod](../../ROADMAP.md) | Publicación de podcasts federada |

## 4. Descubribilidad

La capa de descubribilidad nos permite encontrar personas y `memorias` en la red. No basta con que algo exista: tiene que poder ser encontrado. Esta capa incluye tanto la publicación como las herramientas para navegar lo que ya guardamos.

| Servicio | Función |
|---|---|
| [Hugo](servicios/hugo.md) | Convierte los archivos Markdown en un sitio navegable; Pagefind genera el índice de búsqueda en tiempo de ejecución |
| [SearXNG](../../ROADMAP.md) | Motor de búsqueda federado que agrega resultados sin identificar a quien busca |
| [Karakeep](../../ROADMAP.md) | Gestión de marcadores y artículos guardados |
| [Sonarr](../../ROADMAP.md) | Automatización de series de TV: episodios, temporadas y series |
| [Radarr](../../ROADMAP.md) | Automatización de películas por perfil de calidad |
| [Lidarr](../../ROADMAP.md) | Automatización de música: álbumes, artistas y pistas |
| [Readarr](../../ROADMAP.md) | Automatización de libros y audiolibros |
| [Prowlarr](../../ROADMAP.md) | Gestor de indexadores para todas las apps \*arr |
| [Bazarr](../../ROADMAP.md) | Automatización de subtítulos para las bibliotecas de Sonarr y Radarr |
| [qBittorrent](../../ROADMAP.md) | Cliente de torrents; gestión de descargas |
| [SABnzbd](../../ROADMAP.md) | Cliente de Usenet; gestión de descargas NZB |

## 5. Reproducibilidad

La reproducibilidad es la condición de que el sistema pueda replicarse en nuevos `contextos`. Esta capa incluye las herramientas que permiten construir, mantener, versionar y recuperar la `interfaz`.

| Servicio | Función |
|---|---|
| [Virtualización](servicios/virtualización.md) | Docker y Podman: cómo se despliegan los servicios del `computador` desechable en contenedores |
| [Terminal](servicios/terminal.md) | Herramientas de terminal para administrar el `computador` local: git, SSH, neovim, nix |
| [Forgejo](../../ROADMAP.md) | Repositorio git auto-hospedado |
| [Woodpecker CI](../../ROADMAP.md) | Integración y despliegue continuos para el flake NixOS, integrado con Forgejo |
| [Restic](../../ROADMAP.md) | Backups automatizados y cifrados con política de retención configurable |
| [n8n](../../ROADMAP.md) | Automatización de flujos de trabajo |

## 6. Navegación

Recorrer las memorias: la navegación es la capa donde las `memorias` y los `datos` viven físicamente y donde los consultamos, recorremos y servimos. Reúne el almacenamiento estructurado, la sincronización de archivos entre `dispositivos`, la gestión de credenciales, los archivos de trabajo y las bibliotecas de medios. La `resiliencia` que protege todo esto es una propiedad transversal, descrita en los [`cuidados`](cuidados.md) y en el [almacenamiento federado](arquitectura/almacenamiento_federado.md); el stack \*arr de la capa de descubribilidad alimenta las bibliotecas con nuevo contenido.

| Servicio | Función |
|---|---|
| [PostgreSQL](servicios/postgresql.md) | Base de `datos` compartida por Authelia, Dendrite, Stalwart y Vaultwarden |
| [Syncthing](servicios/syncthing.md) | Sincronización de archivos entre `dispositivos` sin pasar por servidores externos |
| [Vaultwarden](servicios/vaultwarden.md) | Gestor de contraseñas cifrado, compatible con Bitwarden |
| [Paperless-ngx](../../ROADMAP.md) | Gestión documental con OCR; digitalización y organización de documentos |
| [Archivebox](../../ROADMAP.md) | Archivo web; guarda copias locales de páginas y recursos de internet |
| [Pairdrop](../../ROADMAP.md) | Transferencia efímera de archivos entre `dispositivos` |
| [Firefly III](../../ROADMAP.md) | Gestión de finanzas personales |
| [Immich](../../ROADMAP.md) | Galería de fotos y videos con sincronización automática desde el `dispositivo` |
| [Jellyfin](../../ROADMAP.md) | Servidor de medios para video, series y películas |
| [Navidrome](../../ROADMAP.md) | Servidor de streaming de música |
| [Audiobookshelf](../../ROADMAP.md) | Servidor de audiolibros y podcasts |
| [Calibre](../../ROADMAP.md) | Gestión y servidor de libros electrónicos |

## Ver también

- [Capas de la memoria](arquitectura/capas_de_la_memoria.md): la arquitectura conceptual detrás de esta organización
- [la `midu`](../midu.md): las `infraestructuras` que integran los servicios
- [Arquitectura](arquitectura.md): los componentes técnicos del sistema
- [`cuidados`](cuidados.md): cómo protegemos nuestras `memorias`
