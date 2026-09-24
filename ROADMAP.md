# ROADMAP — alfabeto.digital

## Semillas

- [x] NixOS + patrón dendrítico (import-tree)
- [x] Base de conocimiento

## Comunicaciones

- [x] Servidor principal + VPS con túnel WireGuard (Pangolin/Gerbil/Newt)
- [x] Cifrado en reposo (LUKS) + gestión de secretos (sops-nix/age)
- [x] Stalwart — email (SMTP/IMAP)
- [x] Dendrite — mensajería Matrix
- [x] ntfy — notificaciones push
- [x] Vaultwarden — gestor de contraseñas
- [x] Syncthing — sincronización de archivos
- [x] AdGuard Home — DNS con bloqueo de rastreadores
- [x] Authelia — SSO + 2FA (TOTP)
- [x] Caddy — reverse proxy con HTTPS automático

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

## Servicios

### Descubribilidad
- [ ] Motor de búsqueda interno (SearXNG)
- [ ] Gestor de bookmarks y conocimiento (Linkding o Hoarder)

### Transferencias
- [ ] Transferencia de archivos efímera (Send o Pairdrop)

### Almacenamiento
- [ ] Gestión documental (Paperless-ngx)
- [ ] Fotos (Immich)
- [ ] Archivado web (Archivebox)

### Procesamiento
- [ ] LLM local (Ollama + Open WebUI)

### Colaboración
- [ ] Suite ofimática (Collabora Online)
- [ ] Wiki / gestión del conocimiento (Wiki.js)
- [ ] Gestión de proyectos (Plane)

### Participación (Red Federada)
- [ ] Microblogging federado (GoToSocial o Mastodon)
- [ ] Video federado (PeerTube)
- [ ] Blog / publicación (WriteFreely)
- [ ] Foro federado (Lemmy)
- [ ] Podcast (Castopod)
