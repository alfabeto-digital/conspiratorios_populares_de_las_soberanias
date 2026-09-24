# Árbol del repositorio

Para regenerar este árbol desde la raíz del repositorio:

**PowerShell:**
```powershell
Get-ChildItem -Recurse -Force | `
  Where-Object {
    $_.FullName -notmatch '\\\.git\\' -and `
    $_.FullName -notmatch '\\website($|\\)' -and `
    $_.FullName -notmatch '\\00-hallucinations($|\\)' -and `
    $_.FullName -notmatch '\\\.claude($|\\)' -and `
    $_.FullName -notmatch 'graphify\\cache'
  } | Resolve-Path -Relative | Sort-Object
```

**Bash:**
```bash
find . \
  -not -path './.git/*' \
  -not -path './website/*' \
  -not -path './00-hallucinations/*' \
  -not -path './.claude/*' \
  -not -path '*/graphify/cache*' | sort
```

---

```
.
├── .gitattributes
├── .gitignore
├── .sops-vps.yaml.template
├── .sops.yaml.template
├── LICENSE
├── README.md
├── ROADMAP.md
├── TREE.md
├── base_de_conocimientos/
│   ├── alfabeto.digital.md              (gitignored)
│   ├── graphify/
│   │   ├── .graphify_labels.json        (gitignored)
│   │   ├── .graphify_python             (gitignored)
│   │   ├── .graphify_root               (gitignored)
│   │   ├── GRAPH_REPORT.md              (gitignored)
│   │   ├── cache/                       (gitignored)
│   │   ├── cost.json                    (gitignored)
│   │   ├── graph.html
│   │   ├── graph.json
│   │   └── manifest.json                (gitignored)
│   ├── init/                            (gitignored)
│   │   ├── almacenamiento_federado.md
│   │   ├── arquitectura.md
│   │   ├── cuidados.md
│   │   ├── lenguaje_común.md
│   │   ├── midv.md
│   │   ├── referencias.md
│   │   ├── replicación.md
│   │   ├── servicios.md
│   │   └── subjetividades.md
│   ├── midv/                            (gitignored)
│   │   ├── arquitectura/
│   │   │   ├── dos_hosts.md
│   │   │   ├── flake.md
│   │   │   ├── nixos.md
│   │   │   ├── patrón_dendrítico.md
│   │   │   ├── secretos.md
│   │   │   └── visión_general.md
│   │   ├── cuidados/
│   │   │   ├── cifrado.md
│   │   │   ├── modelo.md
│   │   │   ├── privacidad.md
│   │   │   └── zero-trust.md
│   │   ├── replicación/
│   │   │   ├── configuración.md
│   │   │   ├── nixos.md
│   │   │   ├── requisitos.md
│   │   │   ├── secretos.md
│   │   │   └── vps.md
│   │   └── servicios/
│   │       ├── adguard.md
│   │       ├── authelia.md
│   │       ├── caddy.md
│   │       ├── dendrite.md
│   │       ├── ntfy.md
│   │       ├── pangolin.md
│   │       ├── postgresql.md
│   │       ├── stalwart.md
│   │       ├── syncthing.md
│   │       ├── túnel.md
│   │       └── vaultwarden.md
│   └── subjetividades/                  (gitignored)
│       ├── alfabetización-digital-popular.md
│       ├── conspiratorios.md
│       ├── contexto.md
│       ├── desarrollo.md
│       ├── dispositivo.md
│       ├── gobernanza.md
│       ├── imaginación-moral.md
│       ├── infraestructuras.md
│       ├── interfaces.md
│       ├── la-interfaz.md
│       ├── memorias-colectivas.md
│       ├── pluriverso.md
│       ├── replicación.md
│       ├── soberanía-digital.md
│       └── transdisciplinariedad.md
└── midu/
    ├── conectarse_a_internet/
    │   ├── ruta_A-cloudflare/
    │   ├── ruta_B-vps+nixos/
    │   └── ruta_C-vps+podman/
    │       ├── .gitignore
    │       ├── config/
    │       │   ├── dynamic/
    │       │   │   └── routes.toml
    │       │   ├── gerbil.yaml
    │       │   ├── pangolin.yaml
    │       │   └── traefik.toml
    │       ├── docker-compose.yml
    │       ├── secrets.env.template
    │       └── setup.sh
    └── nixos/
        ├── .config/
        ├── config-vps.nix.template
        ├── config.nix.template
        ├── flake.nix
        ├── home/
        │   └── default.nix
        ├── modules/
        │   ├── hosts/
        │   │   ├── alfabeto.digital/
        │   │   │   └── default.nix
        │   │   └── vps/
        │   │       └── default.nix
        │   └── nixos/
        │       ├── admin.nix
        │       ├── base.nix
        │       ├── communications/
        │       │   ├── dendrite.nix
        │       │   ├── ntfy.nix
        │       │   └── stalwart.nix
        │       ├── database.nix
        │       ├── network/
        │       │   ├── caddy.nix
        │       │   ├── cloudflare.nix
        │       │   ├── newt.nix
        │       │   └── pangolin-server.nix
        │       ├── security/
        │       │   ├── adguard.nix
        │       │   └── authelia.nix
        │       ├── services/
        │       │   ├── syncthing.nix
        │       │   └── vaultwarden.nix
        │       └── storage.nix
        ├── replicate/
        │   ├── archlinux-2026.02.01-x86_64.iso                              (gitignored)
        │   ├── nixos-graphical-25.11.6495.e764fc9a4058-x86_64-linux.iso     (gitignored)
        │   ├── nixos-minimal-25.11.6495.e764fc9a4058-x86_64-linux.iso       (gitignored)
        │   ├── replicate-grub.xcf                                           (gitignored)
        │   ├── replicate-logo.xcf                                           (gitignored)
        │   └── ventoy/
        │       ├── README.md
        │       ├── theme/
        │       │   └── replicate/
        │       │       ├── ShureTechMonoNerdFont-Regular-32.pf2
        │       │       ├── background.png
        │       │       └── theme.txt
        │       └── ventoy.json
        └── secrets/
            ├── secrets-vps.plain.template
            └── secrets.plain.template
```
