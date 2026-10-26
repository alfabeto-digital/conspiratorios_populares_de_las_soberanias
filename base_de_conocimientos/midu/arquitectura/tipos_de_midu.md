# Tipos de midu

La [`midu`](../../midu.md) es viable en muchas escalas. La misma arquitectura puede darle vida a una `midu` en un `computador` reutilizado con un disco externo o en un gabinete especialmente diseñado para utilizar cuatro tarjetas gráficas (GPU). En cada configuración obtenemos distintas capacidades de cómputo, de almacenamiento y un grado diferente de resiliencia.

Tomamos el **gabinete de 8 Unidades (8U) como referencia**: es la configuración mínima que incorpora las tres [capas de resiliencia](almacenamiento_federado.md) completas (capa operativa en NVMe y capa local en RAID1, más su cuota en la capa federada). En algunas configuraciones hay ventajas y desventajas respecto de la configuración de 8U. Más detalles sobre los costos, el consumo de energía y las horas de trabajo están en [estimaciones](estimaciones.md).

El diseño sigue un principio de **crecimiento modular**, cada configuración de gabinete incorpora los componentes de la anterior y agrega capacidad.

## Computador reutilizado + disco duro externo

La `midu` más accesible. Un `computador` que ya tenemos aporta la capa operativa en su disco interno, y un disco duro externo aporta una capa local para las `memorias` que deben sobrevivir. Esta `replicación` es suficiente para correr los servicios esenciales y poder dialogar con otras `midu` de la federación. No puede participar de la red de almacenamiento federado.

**Ventajas, respecto del 8U**: costo cercano a cero, reutiliza hardware existente, bajo consumo de energía y puesta en marcha inmediata.

**Desventajas, respecto del 8U**: un solo disco externo no ofrece réplica en espejo para las `memorias`, así que la capa local de resiliencia es parcial (la pérdida del disco duro compromete todos los `datos`); sin UPS queda expuesta a cortes de energía; el hardware diseñado para usos más generales es menos fiable en operación continua; la expansión y la cuota federada son limitadas.

## Gabinete 8U: configuración base (referencia)

El punto de comparación. Integra un mini PC con puerto OCuLink (por ejemplo GMKtec G9 Plus), una pantalla táctil HDMI de 7", una carcasa de 4 bahías para HDD y una UPS. La carcasa divide sus discos en dos pares RAID1 independientes: uno para `datos` propios (capa local) y uno para fragmentos de la federación (capa federada).

```text
1U  mini PC (bandeja universal)
1U  pantalla táctil HDMI 7"
2U  carcasa 4 bahías HDD
1U  UPS 750 VA
1U  panel ventiladores
1U  gestión cables y accesorios
1U  espacio libre
══
8U
```

Almacenamiento de referencia: 2 TB RAID1 local y 2 TB RAID1 federado. La pantalla táctil se monta en el gabinete y se conecta al mini PC por HDMI y USB, de modo que podemos monitorear y controlar la `midu` sin necesidad de un monitor externo.

## Gabinete 10U de servicios

Añade capacidades de enrutamiento al 8U: conmutador (switch) gestionado, enrutador (router) y panel de conexiones ethernet (patch panel).

```text
8U  base
1U  conmutador 8 puertos
1U  enrutador + panel de conexiones ethernet
══
10U
```

**Ventajas, respecto del 8U**: puede crear una red local para otros dispositivos y personas usuarias.

**Desventajas, respecto del 8U**: dos unidades de gabinete extras y consumos adicionales de energía por el equipo de red.

## Gabinete 10U con GPU

Reemplaza el espacio libre del 8U por un carcasa eGPU de 2U y actualiza la UPS. El mini PC se conecta a la GPU por OCuLink (equivalente a PCIe x4 Gen 4).

```text
1U  mini PC (bandeja)
1U  pantalla táctil HDMI 7"
2U  carcasa eGPU (perfil completo)
2U  carcasa 4 bahías HDD
2U  UPS 1500 VA
1U  panel ventiladores
1U  gestión cables
══
10U
```

**Ventajas, respecto del 8U**: suma una GPU para inferencia y entrenamiento ligero de modelos de inteligencia artificial.

**Desventajas, respecto del 8U**: mayor consumo de energía y una UPS más grande; sin capacidades de enrutamiento local para otras personas o dispositivos.

## Gabinete 12U: IA con capacidades de enrutamiento

Combina el 10U con GPU y añade capacidades de enrutamiento completo.

```text
1U  mini PC (bandeja)
1U  pantalla táctil HDMI 7"
2U  carcasa eGPU
2U  carcasa 4 bahías HDD
2U  UPS 1500 VA
1U  conmutador 8 puertos
1U  enrutador
1U  panel de conexiones ethernet + gestión cables
══
12U (11U hardware · 1U libre)
```

**Ventajas, respecto del 8U**: primera configuración con capacidad completa de IA,  contribución activa a la federación, con enrutamiento propio.

**Desventajas, respecto del 8U**: más componentes que mantener y mayor consumo de energía.

## Transición de plataforma: de 1 GPU a 2 o más

El mini PC con OCuLink soporta **una GPU** a través del conector externo. Para configuraciones de 2, 3 o 4 GPU reemplazamos el conjunto mini PC + eGPU por un **workstation de 4U** con ranuras PCIe internas. La pantalla, el capacidades de enrutamiento, el almacenamiento y la UPS se mantienen; sólo cambia la unidad de cómputo.

## Gabinete 14U: dos GPU

Plataforma workstation 4U en formato ATX, con dos GPU en ranuras PCIe internas.

```text
4U  workstation ATX (2× GPU PCIe)
2U  carcasa 4 bahías HDD
2U  UPS 2000 VA
1U  pantalla táctil HDMI 7"
1U  conmutador 8 puertos
1U  enrutador
1U  panel de conexiones ethernet
1U  gestión cables
══
13U → gabinete 14U
```

**Ventajas, respecto del 8U**: duplica la capacidad de cómputo de IA; el almacenamiento local y federado crece a 6 TB RAID1 cada uno.

**Desventajas, respecto del 8U**: el peso y el consumo justifican un chasis más robusto y una UPS mayor; el costo sube de forma considerable.

## Gabinete 16U: tres GPU

Para una tercera GPU la plataforma cambia al formato EATX, que permite más ranuras PCIe y mayor capacidad de alimentación.

```text
4U  workstation EATX (3× GPU PCIe)
2U  carcasa 4 bahías HDD
3U  UPS 3000 VA
1U  pantalla táctil HDMI 7"
1U  conmutador 8 puertos
1U  enrutador
1U  panel de conexiones ethernet
1U  gestión cables
══
15U → gabinete 16U (1U libre)
```

**Ventajas, respecto del 8U**: datasets extensos y modelos de IA de mayor tamaño; capa local y federada de 8 TB RAID1 cada una.

**Desventajas, respecto del 8U**: requiere memoria ECC, doble fuente de alimentación y una UPS de 3000 VA; es una inversión inicial alta.

## Gabinete 18U: cuatro GPU

La capacidad máxima considerada por ahora, con dos carcasas de almacenamiento.

```text
4U  workstation EATX (4× GPU PCIe)
2U  carcasa 4 bahías HDD primario
2U  carcasa 4 bahías HDD secundario
4U  2× UPS 2000 VA
1U  pantalla táctil HDMI 7"
1U  conmutador 8 puertos
1U  enrutador
1U  panel de conexiones ethernet
1U  gestión cables
══
17U → gabinete 18U (1U libre)
```

**Ventajas, respecto del 8U**: capacidad máxima para el ciclo completo de entrenamiento de IA local (datasets activos, checkpoints, modelos y respaldo distribuido); 16 TB RAID1 local y 16 TB RAID1 federado repartidos entre dos carcasas de 4 discos duros cada una.

**Desventajas, respecto del 8U**: la configuración más cara, pesada y demandante de energía; necesita alimentación redundante y un plan de refrigeración.

## Alternativas compatibles

Estas opciones reemplazan al workstation en configuraciones de 2 a 4 GPU. No forman parte de la progresión modular, pero son compatibles con el resto de la infraestructura de gabinetes.

- **Computador de sobremesa (1 a 4 GPU)**: una torre ATX o EATX junto a un gabinete de 10U a 12U que aloja capacidades de enrutamiento, almacenamiento y UPS. Separa el cómputo del gabinete.
- **Bandeja de 19": servidor 2U o 4U**: un servidor estándar de datacenter, pensado para entornos de producción con mantenimiento remoto. Para 3 o 4 GPU en 2U se requiere un chasis especializado con conexiones PCIe.

## De los tipos por rol a las configuraciones

Los cuatro tipos de `midu` del modelo de [almacenamiento federado](almacenamiento_federado.md) contemplan el uso de estas configuraciones:

| Tipo de `midu` | Configuración típica |
|---|---|
| Servicios | Gabinete 10U de servicios, con mayor capacidad de HDD local |
| IA compacta | Equipo de escritorio con memoria unificada CPU + GPU (por ejemplo una NVIDIA DGX Spark), sin gabinete |
| IA de alta capacidad | Gabinete 18U con cuatro GPU |
| Redundancia | Gabinete 10U de servicios, con la mayor cuota de HDD federado |

## Ver también

- [almacenamiento federado](almacenamiento_federado.md): el modelo de tres capas de resiliencia y la cuota federada de cada tipo.
- [estimaciones](estimaciones.md): costos, consumo de energía y horas de trabajo de cada configuración.
