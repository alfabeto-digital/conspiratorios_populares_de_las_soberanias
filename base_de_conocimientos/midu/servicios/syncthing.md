---
title: Syncthing
tipo: servicio
estado: revisado
codigo: abierto
capa_memoria: navegación
tags: [navegación, datos, soberanía]
nix:
  - midu/nixos/modules/nixos/services/syncthing.nix
icono: lenguaje_común/objetos_digitales/midu/digital_infrastructures/syncthing.png
relaciones:
  parte_de: midu/servicios.md
  implementa:
    - subjetividades/soberanía_digital.md
  relacionado:
    - midu/servicios/vaultwarden.md
    - midu/servicios/caddy.md
    - midu/servicios/authelia.md
  reemplaza_a:
    - lenguaje_común/definiciones/servicios_no_soberanos/mega.md
---

﻿# Syncthing

← [Servicios](../servicios.md)

## ¿Qué es esto?

Syncthing es como Google Drive o Dropbox, pero sin intermediarios. Los archivos se sincronizan entre nuestros `dispositivo`s sin pasar por servidores de terceros: cuando el teléfono y la computadora están en la misma red, se comunican directamente. Cuando están en redes distintas, el servidor hace de punto de encuentro, pero los archivos son nuestros y solo nuestros.

## ¿Para qué sirve?

- **Sincronización de archivos** entre `dispositivo`s: lo que guardamos en una carpeta de Syncthing en un `dispositivo` aparece en los demás y en el servidor automáticamente.
- **Backup distribuido**: si un `dispositivo` se daña, los archivos siguen existiendo en los otros.
- **Acceso desde cualquier lugar**: el servidor actúa como nodo siempre encendido, de modo que cuando volvemos a casa y conectamos un `dispositivo`, recibe las actualizaciones aunque haya estado apagado mientras estábamos fuera.
- **Sin cuota de almacenamiento**: el límite es el espacio en disco de nuestros propios `dispositivo`s, no el plan que paguemos a una empresa.

## ¿Por qué Syncthing específicamente?

Syncthing es P2P (peer-to-peer): los `dispositivo`s se conectan directamente entre sí cuando pueden, sin necesidad de que los archivos pasen por un servidor central. Esto tiene ventajas importantes:

- **Privacidad real**: los archivos no pasan por servidores de Syncthing Inc. ni de ningún otro tercero. La empresa detrás de Syncthing no tiene acceso a nuestros `datos`.
- **Sin vendor lock-in**: Syncthing es software libre. El protocolo es abierto y documentado.
- **Funciona offline**: la sincronización local (entre `dispositivo`s en la misma red) funciona sin acceso a internet.

La alternativa más conocida, Nextcloud, es más completa (incluye editor de documentos, calendario, contactos) pero también más pesada. Para el caso de uso de sincronización de archivos pura, Syncthing es más eficiente y más simple de mantener.

## ¿Cómo funciona en alfabeto.digital?

Syncthing corre en el `computador` local con un usuario de sistema dedicado. Ese usuario pertenece al grupo `storage`, junto con el usuario administrador y el usuario de Vaultwarden, lo que define exactamente qué partes del sistema de archivos pueden acceder los servicios de almacenamiento.

Los `dispositivo`s externos (teléfono, laptop) se configuran una vez como "pares" del servidor. A partir de entonces, la sincronización es automática y continua.

**Módulo NixOS:** [`nixos/modules/nixos/services/syncthing.nix`](../../../midu/nixos/modules/nixos/services/syncthing.nix)

## La decisión ética: nuestros archivos son nuestros

Google Drive analiza el contenido de los archivos para mejorar sus productos y personalizar publicidad. Dropbox ha tenido incidentes de privacidad conocidos. Los servicios en la nube de las grandes empresas son convenientes, pero el precio no siempre es dinero: a veces es acceso a los `datos`.

Con Syncthing, los archivos nunca salen de nuestros `dispositivo`s y nuestro servidor. No hay un servicio de terceros que indexe el contenido, no hay análisis de comportamiento, no hay publicidad. Es más trabajo de configuración inicial, pero el resultado es que los archivos son efectivamente privados.

## Ver también

- [Vaultwarden](vaultwarden.md): otro servicio de almacenamiento, para contraseñas
- [Caddy](caddy.md): gestiona el acceso HTTPS al panel de Syncthing
- [Authelia](authelia.md): protege el acceso al panel de administración
- [`soberanía` digital](../../subjetividades/soberanía_digital.md): el concepto detrás de estas decisiones
