---
title: NextCloud
tipo: servicio
estado: revisado
codigo: abierto
capa_memoria: procesamiento
tags: [datos, memorias, procesamiento]
nix:
  - midu/nixos/modules/nixos/services/nextcloud.nix
icono: lenguaje_común/objetos_digitales/midu/digital_infrastructures/nextcloud.png
relaciones:
  parte_de: midu/servicios.md
  requiere:
    - midu/servicios/postgresql.md
    - midu/servicios/caddy.md
    - midu/arquitectura/almacenamiento_federado.md
  implementa:
    - subjetividades/soberanía_digital.md
    - subjetividades/memorias_colectivas.md
  relacionado:
    - midu/servicios/syncthing.md
  reemplaza_a:
    - lenguaje_común/definiciones/servicios_no_soberanos/dropbox.md
    - lenguaje_común/definiciones/servicios_no_soberanos/googlesuite.md
    - lenguaje_común/definiciones/servicios_no_soberanos/microsoftoffice.md
    - lenguaje_común/definiciones/servicios_no_soberanos/evernote.md
    - lenguaje_común/definiciones/servicios_no_soberanos/notion.md
---

# NextCloud

← [Servicios](../servicios.md)

## ¿Qué es esto?

NextCloud es una plataforma de colaboración que corre en el `computador` local: archivos compartidos, edición de documentos en el navegador, calendario y contactos. Es la capa donde varias personas trabajan sobre las mismas `memorias` sin que esas `memorias` salgan del sistema.

## ¿Para qué sirve?

**Archivos compartidos.** Carpetas que un grupo guarda, organiza y comparte, con control de versiones y enlaces de descarga, sobre `infraestructuras` propias.

**Documentos colaborativos.** Con Collabora Online integrado, editamos textos, hojas de cálculo y presentaciones en el navegador, varias personas a la vez, sin enviar el documento a un tercero.

**Calendario y contactos.** Agenda y libreta de direcciones sincronizadas entre `dispositivo`s mediante estándares abiertos (CalDAV y CardDAV).

**Estación de migración.** NextCloud también sirve para ingresar `memorias` por lotes y organizarlas antes de llevarlas al almacenamiento definitivo, montando discos externos como almacenamiento dentro de la `interfaz`.

## ¿Cómo funciona en alfabeto.digital?

NextCloud corre detrás de [Caddy](caddy.md), igual que el resto de servicios: su servidor web escucha solo en localhost y Caddy termina el TLS. Guarda sus `datos` estructurados en [PostgreSQL](postgresql.md) y sus archivos en el disco `data`. El [almacenamiento federado](../arquitectura/almacenamiento_federado.md) se monta como almacenamiento externo de lectura y escritura dentro de NextCloud, de modo que podemos mover `memorias` entre el disco de trabajo y la capa de almacenamiento sin salir de la `interfaz`.

La edición de documentos la provee un servidor Collabora Online propio, también detrás de Caddy, para que ningún documento pase por un servicio de terceros.

**Módulo NixOS:** [`nixos/modules/nixos/services/nextcloud.nix`](../../../midu/nixos/modules/nixos/services/nextcloud.nix)

## Ver también

- [Syncthing](syncthing.md): sincronización de archivos entre `dispositivo`s, complementaria a NextCloud
- [PostgreSQL](postgresql.md): la base de `datos` que NextCloud comparte con el resto del sistema
- [el almacenamiento federado](../arquitectura/almacenamiento_federado.md): las capas donde viven las `memorias`
