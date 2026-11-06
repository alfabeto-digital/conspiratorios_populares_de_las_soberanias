# ROADMAP — alfabeto.digital

## Semillas

- [x] NixOS + patrón dendrítico (import-tree)
- [x] Base de conocimiento

## Comunicaciones

- [x] Servidor principal + VPS con túnel WireGuard (Pangolin/Gerbil/Newt)
- [ ] Investigación: WireGuard dentro del túnel ZeroTrust — cloudflared opera sobre TCP/HTTP; WireGuard necesita UDP. Requiere envolver UDP en TCP (udp2raw, wstunnel u otro adaptador) o usar Cloudflare WARP Gateway (capa de pago) que soporta UDP nativamente
- [x] Cifrado en reposo (LUKS) + gestión de secretos (sops-nix/age)
- [x] Stalwart — email (SMTP/IMAP)
- [x] Dendrite — mensajería Matrix
- [x] ntfy — notificaciones push
- [x] Vaultwarden — gestor de contraseñas
- [x] Syncthing — sincronización de archivos
- [x] AdGuard Home — DNS con bloqueo de rastreadores
- [x] Authelia — SSO + 2FA (TOTP)
- [x] Caddy — reverse proxy con HTTPS automático
- [ ] Hugo — base de conocimientos como sitio web navegable (`info.alfabeto.digital`)
- [ ] Hugo — migración del sitio principal (`alfabeto.digital`) desde HTML artesanal

## Observabilidad

- [ ] Prometheus — métricas (node, systemd, postgres, podman, caddy, authelia)
- [ ] Loki + Promtail — agregación de logs desde journald
- [ ] Grafana — dashboards de métricas y logs
- [ ] Alertmanager — alertas → ntfy
- [ ] Homepage — portal de servicios (punto de entrada unificado)
- [ ] Cockpit — gestión web del servidor (terminal SSH + Podman)
- [ ] Forgejo — repositorio git auto-hospedado

## Operaciones

- [ ] Backups automatizados (restic)
- [ ] Runbooks de recuperación ante desastre
- [ ] CI/CD para el flake NixOS (Woodpecker CI, integrado con Forgejo)
- [ ] Automatización de flujos de trabajo (n8n)

## Servicios

### Descubribilidad
- [ ] Motor de búsqueda interno (SearXNG)
- [ ] Gestor de marcadores y conocimiento (Karakeep)
- [ ] Automatización de series de TV (Sonarr)
- [ ] Automatización de películas (Radarr)
- [ ] Automatización de música (Lidarr)
- [ ] Automatización de libros y audiolibros (Readarr)
- [ ] Gestor de indexadores (Prowlarr)
- [ ] Automatización de subtítulos (Bazarr)
- [ ] Cliente de torrents (qBittorrent)
- [ ] Cliente de Usenet (SABnzbd)

### Transferencias
- [ ] Transferencia de archivos efímera (Pairdrop)

### Navegación
- [ ] Gestión documental (Paperless-ngx)
- [ ] Archivado web (Archivebox)
- [ ] Finanzas personales (Firefly III)
- [ ] Fotos y videos (Immich)
- [ ] Servidor de video y TV (Jellyfin)
- [ ] Streaming de música (Navidrome)
- [ ] Audiolibros y podcasts (Audiobookshelf)
- [ ] Biblioteca de libros (Calibre)

### Procesamiento
- [ ] LLM local (Ollama + Open WebUI)
- [ ] Procesamiento con modelos de IA (Hermes)
- [ ] Coordinación de agentes (Paperclip)

### Colaboración
- [ ] Plataforma colaborativa (NextCloud)
- [ ] Suite ofimática (EuroOffice)
- [ ] Wiki / gestión del conocimiento (FrankMD)
- [ ] Gestión de proyectos (OpenProject)

### Participación (Red Federada)
- [ ] Microblogging federado (Mastodon)
- [ ] Fotos federadas (Pixelfed)
- [ ] Video federado (PeerTube)
- [ ] Foro federado (Lemmy)
- [ ] Eventos y grupos federados (Mobilizon)
- [ ] Lectura social federada (Bookwyrm)
- [ ] Podcast federado (Castopod)
