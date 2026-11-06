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

Las fuentes y las familias de archivos de cada visualización se colapsan para hacer el árbol legible.

---

```
.
├── .gitattributes
├── .gitignore
├── LICENSE
├── README.md
├── ROADMAP.md
├── TREE.md
├── base_de_conocimientos/
│   ├── graphify/
│   │   ├── .graphify_labels.json        (gitignored)
│   │   ├── .graphify_python             (gitignored)
│   │   ├── .graphify_root               (gitignored)
│   │   ├── GRAPH_REPORT.md              (gitignored)
│   │   ├── cost.json                    (gitignored)
│   │   ├── graph.html
│   │   ├── graph.json
│   │   └── manifest.json                (gitignored)
│   ├── lenguaje_común/
│   │   ├── cartografía_de_lo_esencial.md
│   │   ├── lenguaje_común.md
│   │   └── visualizaciones/   (cada diagrama: .excalidraw.md + imagen; las 5 redes suman -slideshow.excalidraw.md y -slideshow.py)
│   │       ├── midu-la_internet_del_presente
│   │       ├── midu-una_red_local_soberana
│   │       ├── midu-conectarse_en_internet
│   │       ├── midu-una_red_federada
│   │       ├── midu-una_red_federada_soberana
│   │       ├── midu-las_capas_de_las_memorias
│   │       ├── midu-las_memorias-comunicaciones
│   │       ├── midu-las_memorias-observabilidad
│   │       ├── midu-las_memorias-procesamiento
│   │       ├── midu-las_memorias-descubribilidad
│   │       ├── midu-las_memorias-reproducibilidad
│   │       ├── midu-las_memorias-navegación
│   │       └── requirements.txt
│   ├── midu/
│   │   ├── arquitectura/
│   │   │   ├── almacenamiento_federado.md
│   │   │   ├── capas_de_la_memoria.md
│   │   │   ├── computadores.md
│   │   │   ├── conectarse_en_internet.md
│   │   │   ├── estimaciones.md
│   │   │   ├── flake.md
│   │   │   ├── nixos.md
│   │   │   ├── patrón_dendrítico.md
│   │   │   ├── secretos.md
│   │   │   └── tipos_de_midu.md
│   │   ├── arquitectura.md
│   │   ├── cuidados/
│   │   │   ├── cifrado.md
│   │   │   ├── privacidad.md
│   │   │   └── zero-trust.md
│   │   ├── cuidados.md
│   │   ├── replicación/
│   │   │   ├── configuración.md
│   │   │   ├── documentación.md
│   │   │   ├── nixos.md
│   │   │   ├── preparativos.md
│   │   │   ├── rutas/
│   │   │   │   ├── ruta_A-vps+nixos.md
│   │   │   │   ├── ruta_B-vps+podman.md
│   │   │   │   └── ruta_C-cloudflare.md
│   │   │   ├── secretos.md
│   │   │   └── vps.md
│   │   ├── replicación.md
│   │   ├── servicios/
│   │   │   ├── adguard.md
│   │   │   ├── authelia.md
│   │   │   ├── caddy.md
│   │   │   ├── dendrite.md
│   │   │   ├── hugo.md
│   │   │   ├── ntfy.md
│   │   │   ├── pangolin.md
│   │   │   ├── postgresql.md
│   │   │   ├── stalwart.md
│   │   │   ├── syncthing.md
│   │   │   ├── terminal.md
│   │   │   ├── túnel_cifrado.md
│   │   │   └── vaultwarden.md
│   │   └── servicios.md
│   ├── midu.md
│   ├── notas_de_desarrollo.md            (gitignored)
│   ├── referencias.md
│   ├── subjetividades/                   (gitignored)
│   │   ├── alfabetización_digital_popular.md
│   │   ├── conspiratorios.md
│   │   ├── contexto.md
│   │   ├── desarrollo.md
│   │   ├── dispositivo.md
│   │   ├── ecologías_queer.md
│   │   ├── gobernanza.md
│   │   ├── imaginación_moral.md
│   │   ├── infraestructuras.md
│   │   ├── interfaces.md
│   │   ├── memorias_colectivas.md
│   │   ├── pluriverso.md
│   │   ├── replicación.md
│   │   ├── soberanía_digital.md
│   │   └── transdisciplinariedad.md
│   └── subjetividades.md
├── midu/
│   ├── conectarse_a_internet/
│   │   ├── ruta_A-vps+nixos/
│   │   │   ├── .sops-vps.yaml.template
│   │   │   └── README.md
│   │   ├── ruta_B-vps+podman/
│   │   │   ├── .gitignore
│   │   │   ├── README.md
│   │   │   ├── config/
│   │   │   │   ├── dynamic/
│   │   │   │   │   └── routes.toml
│   │   │   │   ├── gerbil.yaml
│   │   │   │   ├── pangolin.yaml
│   │   │   │   └── traefik.toml
│   │   │   ├── docker-compose.yml
│   │   │   ├── secrets.env.template
│   │   │   └── setup.sh
│   │   └── ruta_C-cloudflare/
│   │       └── README.md
│   ├── nixos/
│   │   ├── .config/
│   │   ├── .sops.yaml.template
│   │   ├── config-vps.nix.template
│   │   ├── config.nix.template
│   │   ├── flake.nix
│   │   ├── home/
│   │   │   └── default.nix
│   │   ├── modules/
│   │   │   ├── hosts/
│   │   │   │   ├── alfabeto.digital/
│   │   │   │   │   └── default.nix
│   │   │   │   └── vps/
│   │   │   │       └── default.nix
│   │   │   └── nixos/
│   │   │       ├── admin.nix
│   │   │       ├── base.nix
│   │   │       ├── communications/
│   │   │       │   ├── dendrite.nix
│   │   │       │   ├── ntfy.nix
│   │   │       │   └── stalwart.nix
│   │   │       ├── database.nix
│   │   │       ├── network/
│   │   │       │   ├── caddy.nix
│   │   │       │   ├── cloudflare.nix
│   │   │       │   ├── newt.nix
│   │   │       │   └── pangolin-server.nix
│   │   │       ├── security/
│   │   │       │   ├── adguard.nix
│   │   │       │   └── authelia.nix
│   │   │       ├── services/
│   │   │       │   ├── syncthing.nix
│   │   │       │   └── vaultwarden.nix
│   │   │       └── storage.nix
│   │   ├── replicate/
│   │   │   ├── archlinux-2026.02.01-x86_64.iso                              (gitignored)
│   │   │   ├── nixos-graphical-25.11.6495.e764fc9a4058-x86_64-linux.iso     (gitignored)
│   │   │   ├── nixos-minimal-25.11.6495.e764fc9a4058-x86_64-linux.iso       (gitignored)
│   │   │   ├── replicate-grub.xcf                                           (gitignored)
│   │   │   ├── replicate-logo.xcf                                           (gitignored)
│   │   │   └── ventoy/
│   │   │       ├── README.md
│   │   │       ├── theme/replicate/   (ShureTechMono .pf2, background.png, theme.txt)
│   │   │       └── ventoy.json
│   │   └── secrets/
│   │       ├── secrets-vps.plain.template
│   │       └── secrets.plain.template
│   └── página_web/
│       ├── assets/
│       │   ├── css/
│       │   │   ├── about.css
│       │   │   ├── header.css
│       │   │   ├── landing.css
│       │   │   ├── menu.css
│       │   │   └── styles.css
│       │   ├── fonts/   (Gohu, Monofur, OpenDyslexic, ShareTechMono)
│       │   ├── images/
│       │   │   └── bg-texture.jpg
│       │   ├── js/
│       │   │   ├── landing.js
│       │   │   └── scripts.js
│       │   └── library/
│       │       └── transdisciplinariedad-martin-barbero.pdf
│       ├── components/
│       │   ├── about.html
│       │   ├── header.html
│       │   ├── landing.html
│       │   ├── landing.old.html          (gitignored)
│       │   └── menu.html
│       ├── index.html
│       └── pages/
│           ├── about.html
│           ├── search.html
│           ├── social.html
│           ├── soon.html
│           └── terminal.html
└── upgrade_notes/
    └── 26.05.md
```
