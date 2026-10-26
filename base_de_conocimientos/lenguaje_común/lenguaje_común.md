# Lenguaje común

← [Inicio](../../README.md#el-lenguaje-común)

Definiciones de los términos técnicos usados en esta documentación. Si encuentras una palabra que no entiendes, probablemente está aquí.

## A

**ACME** (Automatic Certificate Management Environment)
Protocolo estándar para obtener certificados [TLS](#tls) de manera automática. [Let's Encrypt](#lets-encrypt) lo implementa: en lugar de configurar manualmente el certificado cada vez, el servidor demuestra que controla el dominio (respondiendo a un desafío HTTP o DNS) y recibe el certificado sin intervención manual. [Caddy](#caddy) usa ACME para que todos los servicios tengan HTTPS desde el primer arranque. Ver [Instalación → Configuración](../midu/`replicación`/configuración.md#red-y-dominio).

**age**
Herramienta moderna de cifrado de archivos. Funciona con clave pública y privada: cada máquina o persona tiene una clave pública (que puede compartirse libremente) y una clave privada (que nunca se comparte). Lo que se cifra con la clave pública solo puede descifrarse con la clave privada correspondiente. En esta `interfaz`, cada servidor tiene su propia clave age para descifrar sus secretos. Ver [Instalación → Secretos](../midu/`replicación`/secretos.md).

**Authelia**
Servidor de autenticación [SSO](#sso) y [2FA](#totp). Actúa como portero central: todos los servicios que requieren login pasan primero por Authelia, que verifica la identidad del usuario. Si Authelia dice que sí, el servicio permite el acceso. Implementa el modelo [Zero Trust](#zero-trust). Ver [Servicios → Authelia](../midu/servicios/authelia.md).

## C

**Caddy**
Servidor web y [reverse proxy](#reverse-proxy) con renovación automática de certificados [TLS](#tls). Recibe las solicitudes HTTPS entrantes y las reenvía al servicio correspondiente según el subdominio. La ventaja de Caddy frente a alternativas como nginx: gestiona los certificados Let's Encrypt automáticamente, sin configuración adicional. Ver [Servicios → Caddy](../midu/servicios/caddy.md).

**Certificado TLS**
Documento digital que certifica la identidad de un servidor y habilita la comunicación cifrada (HTTPS). El equivalente a un DNI para un sitio web. Lo emite una autoridad certificadora de confianza (como [Let's Encrypt](#lets-encrypt)) después de verificar que el solicitante controla el dominio. Sin certificado válido, los navegadores muestran la advertencia "conexión no segura". Ver [TLS](#tls).

## D

**DNS** (Domain Name System)
El "directorio telefónico" de internet. Convierte nombres de dominio legibles por humanos (`alfabeto.digital`, `mail.tusitio.com`) en direcciones [IP](#ip) numéricas que las computadoras usan para comunicarse. Cuando escribes una URL en el navegador, tu computadora primero consulta un servidor DNS para saber a qué IP dirigirse.

**Docker**
Plataforma para ejecutar aplicaciones en [contenedores](#podman): entornos aislados que incluyen todo lo que necesita una aplicación para correr (código, dependencias, configuración). Docker gestiona el ciclo de vida de esos contenedores. En esta `interfaz`, el VPS Path B usa Docker Compose para orquestar varios servicios. Ver también [Podman](#podman).

## F

**Federación** (servicios federados)
Capacidad de dos servidores independientes de comunicarse entre sí usando un protocolo estándar abierto, sin que ninguno controle al otro. El correo electrónico es el ejemplo más antiguo: puedes enviar un email desde Gmail a Outlook, a un servidor propio, o a cualquier otro servidor de correo, todos hablan el mismo protocolo ([SMTP](#smtp)/[IMAP](#imap)). [Matrix](#matrix) es federado de la misma forma: puedes chatear desde tu servidor con usuarios de otros servidores Matrix. Lo contrario de federado es una plataforma centralizada (WhatsApp, Instagram): solo funciona entre usuarios del mismo silo.

**Flake** (Nix Flake)
Sistema de gestión de configuración y dependencias para [NixOS](#nixos). El archivo `flake.nix` define las entradas (qué versiones de paquetes usar, desde dónde obtenerlos) y las salidas (los sistemas a construir: el servidor principal, el VPS, etc.). El archivo `flake.lock` fija las versiones exactas de todas las dependencias, garantizando que el sistema construido hoy sea idéntico al construido en seis meses. Ver [Instalación → VPS](../midu/`replicación`/vps.md#actualizar-nixpkgs).

## I

**IMAP** (Internet Message Access Protocol)
Protocolo para recibir y sincronizar correo electrónico entre el servidor de correo y los clientes (Thunderbird, Apple Mail, K-9 Mail, etc.). A diferencia de POP3 (que descarga y elimina), IMAP mantiene los correos en el servidor y sincroniza el estado entre varios `dispositivo`s, si marcas un correo como leído en el teléfono, aparece leído también en el ordenador.

**initrd** (initial RAM disk)
Sistema de archivos mínimo que NixOS carga en memoria durante los primeros segundos del arranque, antes de que los discos reales estén disponibles. El initrd contiene lo mínimo necesario para montar el sistema de archivos principal. En esta `interfaz`, se añade un servidor [SSH](#ssh) al initrd para poder desbloquear remotamente el disco cifrado ([LUKS](#luks)) de `nvme0` después de un reinicio, sin necesidad de acceso físico al servidor. Ver [Instalación → NixOS](../midu/`replicación`/nixos.md#paso-3-ssh-en-initrd--desbloqueo-remoto-de-nvme0).

**IP** (Internet Protocol address)
Dirección numérica única que identifica un `dispositivo` en internet. Dos formatos coexisten actualmente: IPv4 (cuatro grupos de números, ej: `203.0.113.42`) e IPv6 (ocho grupos hexadecimales, ej: `2001:db8::1`). Los servidores necesitan una IP pública fija para ser accesibles desde internet. Los routers domésticos suelen asignar IPs privadas (192.168.x.x, 10.x.x.x) que no son accesibles directamente desde el exterior, por eso la `interfaz` usa un [VPS](#vps) con IP pública.

**ISP** (Internet Service Provider / Proveedor de acceso a internet)
Empresa que conecta hogares u oficinas con internet. Asigna una dirección [IP](#ip) al router; en contratos residenciales esa IP es dinámica y puede cambiar sin previo aviso. Los ISP residenciales también suelen bloquear los puertos de entrada estándar (80 y 443), lo que impide recibir conexiones externas directas. Por eso la `midu` usa un intermediario con IP pública fija, Cloudflare o un [VPS](#vps), en lugar de exponer el `computador` local directamente a internet. Ver [conectarse en internet](../midu/arquitectura/conectarse_en_internet.md).

## L

**Let's Encrypt**
Autoridad de certificación gratuita, automática y abierta. Emite certificados [TLS](#tls) válidos usando el protocolo [ACME](#acme), que los servidores web como [Caddy](#caddy) implementan nativamente. El certificado se renueva automáticamente cada 90 días. Antes de Let's Encrypt, obtener un certificado TLS costaba dinero y requería proceso manual; desde 2016, cualquier servidor puede tener HTTPS gratuito.

**LUKS** (Linux Unified Key Setup)
Estándar de cifrado de disco completo para Linux. Cifra todos los `datos` del disco a nivel de bloque: no importa qué sistema de archivos esté dentro, todos los `datos` se cifran antes de escribirse en el disco físico. Sin la clave correcta, el contenido del disco es ruido aleatorio ilegible. Admite hasta 8 "key slots", múltiples contraseñas o claves que abren el mismo disco, lo que permite tener una clave de emergencia y una clave gestionada automáticamente. Ver [Instalación → NixOS](../midu/`replicación`/nixos.md#por-qué-ciframos-los-discos) y [Instalación → Secretos](../midu/`replicación`/secretos.md#f-enrollar-luks_data_key-en-el-header-luks-de-nvme1).

## M

**MIDV** (Mínima `interfaz` Digital Viable)
Una configuración particular de elementos de infraestructura (física, digital y humana) que permite a una persona o una comunidad gobernar su memoria individual y colectiva con criterio de `soberanía` digital. "Viable" en sentido biológico: una `interfaz` viable es aquella que tiene los componentes mínimos para existir de forma autónoma y replicarse en otros `contexto`s. Ver [la `midu`](../midu/midu.md).

**Matrix**
Protocolo abierto y [federado](#federación-servicios-federados) de mensajería instantánea. Permite comunicación en tiempo real (chat, llamadas, videollamadas) entre servidores independientes. Dendrite es la implementación de servidor Matrix que usa esta `interfaz`. Ver [Servicios → Dendrite](../midu/servicios/dendrite.md).

**MITM** (Man In The Middle)
Tipo de ataque (o configuración intencional) donde un tercero se interpone entre dos partes en comunicación, pudiendo leer o modificar los mensajes. En seguridad, es un vector de ataque a evitar. En esta `interfaz`, Cloudflare Tunnel es técnicamente un MITM benigno: el tráfico HTTPS llega a Cloudflare, que lo descifra, lo reenvía al servidor, y cifra de nuevo. Esto significa que Cloudflare puede ver el contenido. La alternativa sin MITM es usar WireGuard/Newt ([VPS](../midu/`replicación`/vps.md)).

**Módulo NixOS**
Archivo `.nix` que describe una parte del sistema: un servicio, una configuración de red, un conjunto de paquetes, etc. Los módulos se combinan (importan unos a otros) para construir la configuración completa del sistema. La arquitectura modular permite activar o desactivar servicios con una sola línea y mantener cada parte del sistema organizada en su propio archivo.

**MVP** (Minimum Viable Product)
Versión más simple de un producto que ya es útil para sus usuarios. Concepto del mundo del desarrollo de software y startups que prioriza entregar valor rápidamente sobre construir algo perfecto. Origen conceptual del [MIDV](#midv).

## N

**NixOS**
Distribución Linux con configuración declarativa y reproducible. En lugar de instalar paquetes con comandos que modifican el sistema de forma incremental, NixOS describe el estado completo del sistema en archivos de configuración (`.nix`). Luego "construye" ese estado, si algo falla, vuelve al estado anterior ([rollback](#rollback)). El mismo archivo de configuración produce el mismo sistema en cualquier hardware. Ver [Arquitectura → NixOS](../midu/arquitectura/nixos.md).

**NVMe** (Non-Volatile Memory Express)
Tipo de disco de estado sólido (SSD) de alta velocidad que se conecta directamente al bus PCIe del ordenador, a diferencia de los discos SATA que usan una `interfaz` más lenta. Los discos NVMe son significativamente más rápidos en operaciones de lectura/escritura aleatoria, lo que beneficia a bases de `datos` como [PostgreSQL](#postgresql). Se identifican como `/dev/nvme0n1`, `/dev/nvme1n1`, etc. Ver [Instalación → NixOS](../midu/`replicación`/nixos.md#paso-0-prerequisitos-de-disco).

## P

**P2P** (Peer-to-Peer)
Comunicación directa entre `dispositivo`s sin un servidor central intermediario. Syncthing, que sincroniza archivos entre `dispositivo`s, usa P2P: los archivos van directamente de una máquina a otra sin pasar por un servidor de terceros.

**Podman**
Alternativa a [Docker](#docker) para ejecutar contenedores. Compatible con los mismos formatos de imagen y comandos, pero con diferencias importantes: Podman puede correr sin privilegios de root (rootless), lo que reduce la superficie de ataque. En esta `interfaz`, el VPS Path B puede usar Podman en lugar de Docker, con la consideración de que WireGuard requiere permisos de red (NET_ADMIN) que en Podman rootless no están disponibles. Ver [Instalación → VPS](../midu/`replicación`/vps.md#path-b--dockerpodman-en-cualquier-linux).

**PostgreSQL**
Sistema de gestión de bases de `datos` relacionales de código abierto. Los servicios de esta `interfaz` (correo, mensajería, autenticación, etc.) guardan sus `datos` estructurados en PostgreSQL. Es conocido por su robustez, cumplimiento de estándares SQL, y capacidades avanzadas para `datos` JSON. Ver [Servicios → PostgreSQL](../midu/servicios/postgresql.md).

**Principio de menor privilegio**
Dar a cada componente del sistema solo los permisos que necesita para funcionar, y nada más. Un servicio de correo no necesita acceso a la base de `datos` de mensajería; un proceso de usuario no necesita permisos de root. Limita el daño potencial si un componente es comprometido: un atacante que compromete un servicio solo obtiene los permisos de ese servicio.

## R

**Registrador de dominio** (DNS Registrar)
Empresa acreditada para vender y gestionar nombres de dominio. Mantiene el registro oficial del propietario y controla qué servidores de nombres (nameservers) son autoritativos para ese dominio: es decir, decide qué servidor [DNS](#dns) responde las consultas sobre ese nombre. Cambiar los nameservers en el registrador redirige todas las consultas hacia otro proveedor. Registradores comunes: Namecheap, Porkbun, Gandi, Cloudflare Registrar. Ver [conectarse en internet: ISP, DNS y registrador de dominio](../midu/arquitectura/conectarse_en_internet.md#isp-dns-y-registrador-de-dominio).

**Reverse proxy** (proxy inverso)
Servidor intermediario que recibe solicitudes de los clientes y las reenvía al servicio interno apropiado. Permite tener múltiples servicios en el mismo servidor usando el mismo puerto (443/HTTPS): el reverse proxy decide a cuál servicio reenviar cada solicitud según el subdominio (`mail.tusitio.com` va al servidor de correo, `chat.tusitio.com` va al servidor de mensajería). [Caddy](#caddy) actúa como reverse proxy en esta `interfaz`. Traefik cumple el mismo rol en el [VPS](#vps).

**Rollback**
En [NixOS](#nixos), la capacidad de volver instantáneamente a una configuración anterior del sistema. NixOS guarda automáticamente cada "generación" del sistema construido. Si una actualización rompe algo, se puede volver a la generación anterior desde el menú de arranque (GRUB) o con `nixos-rebuild switch --rollback`, sin pérdida de `datos`.

## S

**SMTP** (Simple Mail Transfer Protocol)
Protocolo para enviar correo electrónico entre servidores y desde clientes hacia el servidor. Cuando envías un correo, tu cliente contacta al servidor SMTP saliente, que lo entrega al servidor SMTP del destinatario. [Stalwart](servicios.md) implementa SMTP en esta `interfaz`.

**sops** (Secrets OPerationS)
Herramienta de gestión de secretos que integra cifrado ([age](#age), PGP, AWS KMS, etc.) con repositorios git. Permite guardar archivos cifrados en git de manera segura: `sops` cifra los valores pero preserva la estructura del archivo (YAML, JSON, etc.), de modo que es visible qué claves existen sin revelar sus valores. Se configura con `.sops.yaml`, que indica con qué claves cifrar cada archivo. Ver [Instalación → Secretos](../midu/`replicación`/secretos.md).

**SSH** (Secure Shell)
Protocolo para acceder remotamente a un servidor de manera cifrada. Permite ejecutar comandos en un servidor como si estuvieras sentado frente a él. Más seguro que las contraseñas cuando se usa con pares de claves criptográficas: la clave privada queda en tu máquina, la clave pública se instala en el servidor. Solo quien tiene la clave privada puede conectarse. Ver [Instalación → NixOS](../midu/`replicación`/nixos.md#paso-3-ssh-en-initrd--desbloqueo-remoto-de-nvme0).

**SSO** (Single Sign-On)
Sistema de autenticación donde una sola cuenta y contraseña da acceso a múltiples servicios. En lugar de recordar credenciales distintas para el correo, la mensajería, el almacenamiento de archivos, etc., el usuario se autentica una vez con [Authelia](#authelia) y accede a todos los servicios del sistema.

## T

**TLS** (Transport Layer Security)
Protocolo de cifrado para comunicaciones en internet. HTTPS es HTTP sobre TLS. TLS garantiza dos cosas: que la comunicación entre el cliente y el servidor está cifrada (nadie puede interceptarla), y que el servidor es quien dice ser (autenticación mediante [certificado TLS](#certificado-tls)). Sustituye al protocolo SSL (que está obsoleto y es inseguro).

**TOTP** (Time-based One-Time Password)
Código de 6 dígitos que cambia cada 30 segundos, generado por una app de autenticación (Aegis, Authy, Google Authenticator, etc.). Es el segundo factor de autenticación (2FA) más común. La clave secreta compartida entre el servidor y la app genera el mismo código en el mismo instante, lo que permite verificar la identidad sin transmitir la contraseña. Si alguien roba tu contraseña, todavía necesita acceso físico a tu `dispositivo` con la app de TOTP.

## U

**UPS** (Uninterruptible Power Supply / Sistema de alimentación ininterrumpida)
`Dispositivo` que combina batería y regulador de voltaje. Mantiene el suministro eléctrico durante cortes breves y, cuando la batería se agota, envía señal al `computador` para que se apague de forma ordenada antes de perder energía definitivamente. Un apagado abrupto puede corromper los `datos` que estaban siendo escritos en disco en ese momento. Para el `computador` local de la `midu`, que está encendido de forma continua, se recomienda un UPS de 600–1000 VA, suficiente para un mini-PC de bajo consumo.

**UUID** (Universally Unique Identifier)
Identificador único de 128 bits, representado como 32 dígitos hexadecimales en formato `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`. Los discos de almacenamiento tienen UUIDs asignados al formatearse. La ventaja del UUID sobre el nombre del `dispositivo` (`/dev/nvme1n1`): el nombre puede cambiar si se conectan nuevos discos o se cambia el orden de arranque, pero el UUID identifica el disco específico sin importar dónde esté conectado. Ver [Instalación → NixOS](../midu/`replicación`/nixos.md#b-obtener-el-uuid-del-disco) y [Instalación → Configuración](../midu/`replicación`/configuración.md#discos-y-puntos-de-montaje).

## V

**VPS** (Virtual Private Server)
Servidor virtual alquilado en un proveedor de nube (Hetzner, DigitalOcean, Vultr, OVH, etc.). Es una porción de un servidor físico particionada con virtualización. En esta `interfaz`, el VPS tiene una IP pública fija y actúa como punto de entrada del tráfico, reenviándolo al servidor principal que puede estar detrás de una red doméstica. Los proveedores ofrecen VPS desde pocos euros al mes. Ver [Instalación → VPS](../midu/`replicación`/vps.md).

## W

**WireGuard**
Protocolo VPN moderno, eficiente y con código pequeño (auditado). Crea túneles cifrados entre `dispositivo`s usando criptografía de clave pública. En esta `interfaz`, WireGuard conecta el VPS con el servidor principal: el tráfico público llega al VPS y viaja por el túnel WireGuard hasta el servidor, sin que el VPS pueda ver el contenido de las comunicaciones cifradas de extremo a extremo. Gerbil (parte de la pila Pangolin) gestiona las interfaces WireGuard. Ver [Instalación → VPS](../midu/`replicación`/vps.md).

## Z

**Zero Trust**
Modelo de seguridad que no confía en ningún componente por defecto, independientemente de su posición en la red ("dentro" o "fuera" del perímetro). Cada solicitud debe ser autenticada y autorizada explícitamente. Contrasta con el modelo perimetral tradicional donde todo lo que está "dentro de la red" se considera de confianza. En esta `interfaz`, [Authelia](#authelia) implementa Zero Trust: todos los servicios requieren autenticación, incluso desde la red local. Ver [`cuidados` → Zero Trust](../midu/`cuidados`/zero-trust.md).
