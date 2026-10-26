# Estimaciones

Reunimos aquí los valores de referencia para dimensionar una [`midu`](../../midu.md) y una federación de ejemplo: el costo del hardware de cada configuración, el consumo de energía, las horas de trabajo humano y los costos fijos recurrentes. Las configuraciones están descritas en [tipos de `midu`](tipos_de_midu.md) y el modelo de almacenamiento en [almacenamiento federado](almacenamiento_federado.md).

Todas las cifras son estimaciones en USD, pensadas para comparar opciones y planear una `replicación`. Los precios de hardware fluctúan y las tarifas de energía, internet y soporte dependen del lugar, así que las tarifas se declaran como supuestos con un rango.

## Precios de referencia

| Componente | USD unitario |
|---|---:|
| RTX 5090 32 GB | $4,300 |
| DGX Spark (GB10) | $4,679 |
| HDD 2 TB | $114 |
| HDD 4 TB | $179 |
| HDD 6 TB | $200 |
| HDD 8 TB | $249 |
| HDD 16 TB | $579 |
| NVMe 1 TB | $179 |
| Mini PC (GMKtec G9 Plus) | $800 |
| RAM DDR5 128 GB (4×32 GB) | $1,800 |
| RAM DDR5 ECC 256 GB (8×32 GB) | $3,600 |

Precio de referencia de RAM: $450 por módulo DDR5 de 32 GB.

## Componentes base

Presentes en todas las configuraciones de gabinete:

| Componente | Modelo de referencia | USD |
|---|---|---:|
| Mini PC con OCuLink | GMKtec G9 Plus (Ryzen 9 8945HS) | $800 |
| NVMe 1 TB | Samsung 990 Pro | $179 |
| Pantalla táctil HDMI 7" | gabinete 1U, HDMI + USB | $100 |
| UPS 750 VA | APC BX750 | $130 |
| Carcasa 4 bahías HDD | ICY BOX IB-3640SU3 | $180 |
| Panel de ventiladores 2×120 mm | Pure Wings 3 | $60 |
| Cables y accesorios | | $50 |
| **Subtotal base (sin gabinete ni HDD)** | | **$1,499** |

## Gabinetes

Todos los gabinetes son de aluminio: perfiles de extrusión de 19" estándar, con la rigidez necesaria para cualquier tamaño de 8U a 18U. La impresión 3D cubre las piezas de adaptación interna: el gabinete de la pantalla táctil, las bandejas para el mini PC o la DGX Spark, las retenciones de cables y los paneles frontales.

| Concepto | USD |
|---|---:|
| Perfil de aluminio 19" + tornillería estructural | $80–$150 |
| Diseño CAD (piezas de adaptación) | $150–$300 |
| Impresión 3D PETG/ASA (gabinetes, bandejas, paneles) | $40–$120 |
| **Total gabinete 8U a 12U armado** | **$270–$570** |

Para gabinetes de 14U a 18U, el peso acumulado de la workstation EATX y las UPS justifica un chasis prefabricado:

| Gabinete | Chasis prefabricado de aluminio | USD |
|---|---|---:|
| 14U | perfil 19" + paneles laterales | $220 |
| 16U | perfil 19" + paneles laterales | $280 |
| 18U | perfil 19" + paneles laterales | $350 |

## Costo por configuración de gabinete

El crecimiento es modular: cada configuración incorpora los componentes de la anterior y agrega capacidad.

### Gabinete 8U: configuración base

| Componente | USD |
|---|---:|
| Subtotal base | $1,499 |
| Gabinete 8U (aluminio + piezas 3D) | $120 |
| HDD local: 2× 2 TB RAID1 | $228 |
| HDD federado: 2× 2 TB RAID1 | $228 |
| **Total 8U** | **$2,075** |

### Gabinete 10U de servicios (añade capacidades de enrutamiento)

| Componente adicional | USD |
|---|---:|
| Conmutador 8p gestionado (TP-Link TL-SG108E) | $45 |
| Enrutador (GL.iNet GL-MT6000) | $90 |
| Panel de conexiones ethernet 24p 1U | $60 |
| Gabinete diferencia (+2U) | $30 |
| HDD local: 2× 4 TB RAID1 (upgrade +$130 vs 8U) | $130 |
| HDD federado: 2× 4 TB RAID1 | $358 |
| **Subtotal adicional** | **$713** |
| **Total 10U servicios** | **$2,560** |

### Gabinete 10U con GPU (sin capacidades de enrutamiento)

| Componente adicional vs 8U | USD |
|---|---:|
| Carcasa eGPU OCuLink 2U | $160 |
| GPU (RTX 5090 32 GB) | $4,300 |
| UPS upgrade: 750 VA a 1500 VA | $70 |
| Gabinete diferencia (+2U) | $30 |
| HDD local: 2× 4 TB RAID1 (upgrade +$130 vs 8U) | $130 |
| HDD federado: 2× 4 TB RAID1 | $358 |
| **Subtotal adicional** | **$5,048** |
| **Total 10U GPU** | **$6,895** |

### Gabinete 12U: IA con capacidades de enrutamiento

| Componente adicional vs 10U GPU | USD |
|---|---:|
| Conmutador 8p gestionado | $45 |
| Enrutador | $90 |
| Panel de conexiones ethernet 24p 1U | $60 |
| Gabinete diferencia (+2U) | $30 |
| **Subtotal adicional** | **$225** |
| **Total 12U** | **$7,120** |

### Plataforma workstation para 2 o más GPU

El mini PC con OCuLink soporta una GPU. Para 2, 3 o 4 GPU reemplazamos el conjunto mini PC + eGPU por un workstation de 4U.

| Reemplaza | Por | Diferencia |
|---|---|---:|
| Mini PC $800 + eGPU carcasa $160 | Workstation 4U $3,280 | +$2,320 |

Plataforma 4U ATX (1 a 2 GPU):

| Componente | USD |
|---|---:|
| Chasis 4U ATX (IStarUSA E4M10) | $380 |
| Placa madre Z790 (ASUS ROG Strix Z790-E) | $380 |
| CPU Intel Core i9-14900K | $420 |
| Cooler AIO 240 mm | $100 |
| 128 GB DDR5 (4×32 GB) | $1,800 |
| PSU 1200 W 80+ Gold | $200 |
| **Subtotal plataforma 4U ATX** | **$3,280** |

Plataforma 4U EATX (3 a 4 GPU):

| Componente | USD | vs ATX |
|---|---:|---:|
| Chasis 4U E-ATX | $500 | +$120 |
| Placa madre EATX (ASUS Pro WS W790E-SAGE) | $800 | +$420 |
| CPU Intel Xeon W7-3455 | $800 | +$380 |
| Cooler industrial AIO 360 mm | $200 | +$100 |
| 256 GB DDR5 ECC (8×32 GB) | $3,600 | +$1,800 |
| 2× PSU 1600 W 80+ Platinum | $700 | +$500 |
| **Subtotal plataforma 4U EATX** | **$6,600** | **+$3,320** |

### Gabinete 14U: dos GPU

| Presupuesto completo 14U | USD |
|---|---:|
| Plataforma 4U ATX | $3,280 |
| 2× RTX 5090 32 GB | $8,600 |
| NVMe 2 TB (upgrade) | $300 |
| Carcasa 4 bahías HDD | $180 |
| UPS 2000 VA | $300 |
| Pantalla táctil HDMI 7" | $100 |
| Conmutador 8p + Enrutador + Panel de conexiones ethernet | $195 |
| Gestión de cables | $50 |
| Gabinete 14U (aluminio prefabricado) | $220 |
| HDD local: 2× 6 TB RAID1 | $400 |
| HDD federado: 2× 6 TB RAID1 | $400 |
| **Total 14U** | **$14,025** |

### Gabinete 16U: tres GPU

| Diferencia desde 14U | USD |
|---|---:|
| Upgrade plataforma ATX a EATX (case, MB, CPU, PSU×2, RAM) | +$3,320 |
| 3ª RTX 5090 32 GB | +$4,300 |
| UPS upgrade: 2000 VA a 3000 VA | +$150 |
| Gabinete diferencia (14U a 16U) | +$60 |
| HDD local: upgrade 2× 6 TB a 2× 8 TB | +$98 |
| HDD federado: upgrade 2× 6 TB a 2× 8 TB | +$98 |
| **Diferencia total desde 14U** | **+$8,026** |
| **Total 16U** | **$22,051** |

### Gabinete 18U: cuatro GPU

| Diferencia desde 16U | USD |
|---|---:|
| 4ª RTX 5090 32 GB | +$4,300 |
| 2º carcasa 4 bahías HDD | +$180 |
| UPS upgrade: 3000 VA a 2× 2000 VA | +$150 |
| Gabinete diferencia (16U a 18U) | +$70 |
| HDD local enc2: 2× 8 TB RAID1 | +$498 |
| HDD federado enc2: 2× 8 TB RAID1 | +$498 |
| **Diferencia total desde 16U** | **+$5,696** |
| **Total 18U** | **$27,747** |

### Alternativas para múltiples GPU

Variantes al workstation para 2 a 4 GPU, compatibles con el resto de la infraestructura de gabinete.

Computador de sobremesa (1 a 4 GPU), junto a un gabinete de 10U a 12U que aloja capacidades de enrutamiento, almacenamiento y UPS:

| Configuración | Plataforma | GPU | Solo cómputo |
|---|---:|---:|---:|
| 1 GPU (ATX) | $2,740 | $4,300 | $7,040 |
| 2 GPU (ATX) | $2,740 | $8,600 | $11,340 |
| 3 GPU (EATX) | $6,480 | $12,900 | $19,380 |
| 4 GPU (EATX) | $6,480 | $17,200 | $23,680 |

Bandeja de 19" (servidor 2U o 4U de datacenter), para entornos de producción con mantenimiento remoto:

| Configuración | Chasis | GPU | Solo cómputo |
|---|---:|---:|---:|
| 1 a 2 GPU (2U) | $2,300 | $4,300–$8,600 | $6,600–$10,900 |
| 3 a 4 GPU (2U especializado) | $5,700 | $12,900–$17,200 | $18,600–$22,900 |

## Costo por tipo de `midu`

La federación de ejemplo del modelo de [almacenamiento federado](almacenamiento_federado.md) se compone de cuatro tipos de `midu`:

| Tipo de `midu` | Gabinete | CPU | RAM | vRAM | HDD local | HDD federado | Total |
|---|---|---|---:|---:|---:|---:|---:|
| **IA de alta capacidad** | 18U | Xeon W7-3455 | 256 GB DDR5 ECC | 128 GB (4× RTX 5090) | 16 TB | 8 TB | **$27,467** |
| **Servicios** | 10U servicios | Ryzen 9 8945HS | 32 GB | sin GPU | 8 TB | 6 TB | **$2,921** |
| **IA compacta** | equipo DGX Spark | GB10 (72c Arm) | 128 GB LPDDR5X | 128 GB | 2 TB | 4 TB | **$5,935** |
| **Redundancia** | 10U servicios | Ryzen 9 8945HS | 32 GB | sin GPU | 2 TB | 8 TB | **$2,570** |
| **Total** | | | | | **28 TB** | **26 TB** | **$38,893** |

La `midu` de IA compacta usa memoria unificada CPU + GPU: los 128 GB se comparten entre cómputo e inferencia.

**IA de alta capacidad (18U, 4× RTX 5090):** workstation EATX con dos carcasas de 4 bahías. Cada carcasa: 2× 8 TB local RAID1 + 2× 4 TB federado RAID1. Total: 16 TB local + 8 TB federado. Los `datos` críticos propios (≈4 TB) se distribuyen a las demás `midu`; los 4 TB federados restantes alojan fragmentos de otras `midu`.

**Servicios (10U servicios):** mini PC con carcasa de 4 bahías. Bahías 1 y 2: 2× 8 TB local RAID1. Bahías 3 y 4: 2× 6 TB federado RAID1. NVMe adicional de 1 TB para el sistema de servicios.

**IA compacta (DGX Spark):** la DGX Spark es una computadora completa, no usa mini PC. Carcasa de 4 bahías: 2× 2 TB local RAID1 + 2× 4 TB federado RAID1.

**Redundancia (10U servicios):** mini PC con carcasa de 4 bahías. Bahías 1 y 2: 2× 2 TB local RAID1. Bahías 3 y 4: 2× 8 TB federado RAID1 (mayor cuota por su rol de redundancia y failover).

### Resumen consolidado

$$
\text{Total federación} = \underbrace{27{,}467}_{\text{IA alta capacidad}} + \underbrace{2{,}921}_{\text{servicios}} + \underbrace{5{,}935}_{\text{IA compacta}} + \underbrace{2{,}570}_{\text{redundancia}} = \$38{,}893
$$

La federación completa suma 28 TB de almacenamiento local útil (`datos` propios de cada `midu` en RAID1) y 26 TB de almacenamiento federado (fragmentos cifrados de otras `midu` almacenados localmente).

### Rango de estimación ±10 %

| Tipo de `midu` | −10 % | Estimación central | +10 % |
|---|---:|---:|---:|
| IA de alta capacidad | $24,720 | $27,467 | $30,214 |
| Servicios | $2,629 | $2,921 | $3,213 |
| IA compacta | $5,342 | $5,935 | $6,529 |
| Redundancia | $2,313 | $2,570 | $2,827 |
| **Total federación** | **$35,004** | **$38,893** | **$42,783** |

| Gabinete | −10 % | Estimación central | +10 % |
|---|---:|---:|---:|
| 8U | $1,868 | $2,075 | $2,283 |
| 10U servicios | $2,304 | $2,560 | $2,816 |
| 10U GPU | $6,206 | $6,895 | $7,585 |
| 12U IA + capacidades de enrutamiento | $6,408 | $7,120 | $7,832 |
| 14U (2× GPU) | $12,623 | $14,025 | $15,428 |
| 16U (3× GPU) | $19,846 | $22,051 | $24,256 |
| 18U (4× GPU) | $24,972 | $27,747 | $30,522 |

## Consumo de energía

Estimamos el consumo con la potencia media de cada configuración en operación continua (24 horas, 30 días). La potencia media es un supuesto de carga mixta; en las configuraciones con GPU, los picos bajo entrenamiento intensivo son bastante más potentes (una RTX 5090 llega a 575 W por unidad). El costo usa una tarifa supuesta de electricidad de $0.10 a $0.25 por kWh.

$$
\text{kWh/mes} = \frac{P_{\text{media}} \times 24 \times 30}{1000}
$$

| Configuración | Potencia media | kWh/mes | Costo/mes ($0.10–$0.25) |
|---|---:|---:|---:|
| Computador reutilizado + disco externo | 55 W | 40 | $4–$10 |
| Gabinete 8U | 100 W | 72 | $7–$18 |
| Gabinete 10U servicios | 120 W | 86 | $9–$22 |
| IA compacta (DGX Spark) | 200 W | 144 | $14–$36 |
| Gabinete 10U / 12U (1 GPU) | 350 W | 252 | $25–$63 |
| Gabinete 14U (2 GPU) | 630 W | 454 | $45–$113 |
| Gabinete 16U (3 GPU) | 910 W | 655 | $66–$164 |
| Gabinete 18U (4 GPU) | 1180 W | 850 | $85–$212 |

Potencia de referencia usada: RTX 5090 ≈ 575 W de pico y ≈ 250 W en carga mixta sostenida; mini PC Ryzen 9 ≈ 55 a 120 W; DGX Spark ≈ 170 a 240 W; HDD ≈ 6 a 9 W cada uno; NVMe ≈ 7 W; switch y router ≈ 10 a 20 W; sobrecosto de la UPS ≈ 5 %.

## Horas de trabajo humano

La puesta en marcha presencial de una `midu` tiene tres fases: el ensamblaje del hardware, la instalación del sistema base y la configuración inicial de los servicios. El ensamblaje escala con la configuración; la instalación del sistema y la configuración de servicios son casi independientes del hardware. El costo usa una tarifa por hora de referencia de $20 a $40 (supuesto).

### Ensamblaje presencial del hardware

| Configuración | Horas |
|---|---:|
| Computador reutilizado + disco externo | 1–2 |
| Gabinete 8U | 3–5 |
| Gabinete 10U servicios | 5–7 |
| Gabinete 10U / 12U (1 GPU) | 6–9 |
| Gabinete 14U (2 GPU) | 8–12 |
| Gabinete 16U (3 GPU) | 9–14 |
| Gabinete 18U (4 GPU) | 10–16 |

### Sistema base

Instalación de [NixOS](nixos.md), cifrado en reposo (LUKS), gestión de secretos (sops-nix y age) y arranque del patrón dendrítico: **4 a 8 horas**, casi constante entre configuraciones.

### Configuración inicial de los servicios

Estimación de la primera configuración de cada servicio, incluyendo pruebas, para el conjunto completo del [ROADMAP](../../../ROADMAP.md) y los [servicios](../servicios.md) ya implementados. Es un esfuerzo de una sola vez, casi independiente del hardware.

| Capa | Servicios | Horas |
|---|---|---:|
| Enrutamiento | Pangolin, túnel cifrado, Caddy, AdGuard, Authelia | 10–17 |
| Comunicaciones | Stalwart, Dendrite, ntfy | 8–15 |
| Observabilidad | Prometheus, Loki + Promtail, Grafana, Alertmanager, Homepage, Cockpit | 9–16 |
| Almacenamiento | PostgreSQL, Syncthing, Vaultwarden, Paperless-ngx, Immich, Archivebox, Send / Pairdrop | 10–17 |
| Procesamiento | Ollama, Open WebUI | 2–4 |
| Descubribilidad | Publicación (Hugo + Pagefind), SearXNG, Linkding / Hoarder | 5–9 |
| Colaboración | Collabora Online, Wiki.js, Plane | 5–9 |
| Participación | GoToSocial / Mastodon, PeerTube, WriteFreely, Lemmy, Castopod | 10–17 |
| Reproducibilidad y operaciones | Terminal, Forgejo, Woodpecker CI, Restic, runbooks de recuperación | 10–18 |
| **Total servicios** | | **79–122** |

### Total por `midu`

Para un gabinete 8U, el total es la suma de las tres fases:

| Fase | Horas | Costo ($20–$40/h) |
|---|---:|---:|
| Ensamblaje (8U) | 3–5 | $60–$200 |
| Sistema base | 4–8 | $80–$320 |
| Configuración de servicios | 79–122 | $1,580–$4,880 |
| **Total** | **86–135** | **$1,720–$5,400** |

En configuraciones más potentes sólo cambia el ensamblaje; la configuración de servicios se mantiene, porque el conjunto de servicios es el mismo.

## Costos fijos recurrentes

Más allá de la inversión inicial, una `midu` tiene costos mensuales. Las tarifas son supuestos en USD con rango y dependen del lugar y del nivel de servicio.

| Concepto | USD/mes | USD/año |
|---|---:|---:|
| Plan de internet (buena capacidad de subida) | $20–$60 | $240–$720 |
| Mantenimiento y soporte remoto | $30–$120 | $360–$1,440 |
| VPS arrendado (`computador` desechable, rutas A y B) | $5–$20 | $60–$240 |
| Electricidad (gabinete 8U de referencia) | $7–$18 | $84–$216 |
| **Total (gabinete 8U de referencia)** | **$62–$218** | **$744–$2,616** |

La electricidad escala con la configuración (ver la tabla de consumo de energía): una `midu` de IA de alta capacidad en 18U puede sumar de $85 a $212 al mes sólo en electricidad, mientras que un `computador` reutilizado suma de $4 a $10. El plan de internet, el mantenimiento y el VPS arrendado se mantienen parecidos entre configuraciones.

## Ver también

- [tipos de `midu`](tipos_de_midu.md): distintas configuraciones de hardware de la `midu`.
- [almacenamiento federado](almacenamiento_federado.md): las capas de resiliencia y la cuota federada de almacenamiento.
