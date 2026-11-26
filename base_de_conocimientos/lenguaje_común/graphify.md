---
title: graphify
tipo: índice
estado: borrador
tags: [memorias, infraestructuras]
relaciones:
  parte_de: lenguaje_común/lenguaje_común.md
  relacionado:
    - lenguaje_común/cartografía_de_lo_esencial.md
---

# graphify

← [Lenguaje común](lenguaje_común.md)

graphify convierte la `base_de_conocimientos/` en un grafo de conocimiento navegable: lee los archivos (notas, código, documentos, imágenes), extrae entidades y relaciones, detecta comunidades y deja un rastro auditable de qué relación fue extraída, inferida o es ambigua. Donde la [cartografía de lo esencial](cartografía_de_lo_esencial.md) reúne las visualizaciones que hacemos a mano, graphify produce un mapa automático que podemos consultar y contrastar.

El grafo actual reúne 528 nodos, 752 aristas y 44 comunidades, con un 96% de relaciones extraídas directamente del texto y un 4% inferidas. Todos los artefactos viven en `graphify/`.

## Los artefactos del grafo

| Artefacto | Qué es |
|---|---|
| [graph.html: el grafo interactivo](../graphify/graph.html) | Visualización navegable en el navegador; cada nodo usa su icono de `objetos_digitales/` |
| [GRAPH_REPORT.md: el reporte en lenguaje llano](../graphify/GRAPH_REPORT.md) | Resumen de comunidades, nodos centrales y rastro de auditoría |
| [graph.json: los datos del grafo](../graphify/graph.json) | El grafo completo en JSON, listo para consultas |
| [manifest.json: el manifiesto de la corrida](../graphify/manifest.json) | Qué archivos se procesaron y con qué parámetros |
| [cost.json: el costo de extracción](../graphify/cost.json) | Tokens consumidos en la extracción semántica |
| [cache.md: el índice del cache](../graphify/cache/cache.md) | Conecta cada archivo del cache con su fuente (ver abajo) |

## El cache y su índice

La extracción es costosa, así que graphify guarda en `graphify/cache/` el resultado por archivo, indexado por el hash de su contenido: la estructura del código en `cache/ast/` y la extracción semántica en `cache/semantic/`. Cuando volvemos a producir el grafo, solo se re-extraen los archivos que cambiaron.

El [índice del cache](../graphify/cache/cache.md) enlaza cada entrada con el archivo fuente que representa. Lo genera [build_cache_index.py](../graphify/build_cache_index.py), que recorre el cache y lo cruza con [stat-index.json](../graphify/cache/stat-index.json), el mapa de cada archivo fuente a su hash de contenido:

```bash
cd base_de_conocimientos/graphify
python build_cache_index.py      # reescribe cache.md
```

Lo corremos a mano cada vez que regeneramos el grafo, para que `cache.md` refleje el estado del cache.

## Ver también

- [Cartografía de lo esencial](cartografía_de_lo_esencial.md): las visualizaciones hechas a mano de las `infraestructuras`
- [Lenguaje común](lenguaje_común.md): el índice de las definiciones del vocabulario
