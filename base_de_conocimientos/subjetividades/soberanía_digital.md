---
title: Soberanía digital
tipo: subjetividad
estado: revisado
tags: [soberanía, datos, gobernanza]
referencias:
  - "Principios CARE (Carroll et al.)"
  - "Tahu Kukutai y Te Mana Raraunga"
  - "Linda Tuhiwai Smith"
  - "Abeba Birhane"
  - "Kemly Camacho (Sulá Batsú)"
  - "Paz Peña y Joana Varon (Coding Rights)"
  - "Principios Feministas de Internet (APC)"
  - "Lorena Cabnal (cuerpo-territorio)"
relaciones:
  parte_de: subjetividades.md
  relacionado:
    - subjetividades/interfaces.md
    - midu.md
    - subjetividades/pluriverso.md
    - subjetividades/alfabetización_digital_popular.md
    - midu/servicios.md
    - midu/arquitectura.md
---

﻿# `soberanía` digital

← [Subjetividades](../subjetividades.md)

## ¿Qué es la `soberanía` digital?

La `soberanía` digital es el derecho, tanto de las personas individualmente como de las comunidades, a controlar su infraestructura digital, sus `datos` y las herramientas que usan para comunicarse y organizarse. Es la capacidad de decidir qué tecnología usar, cómo usarla, dónde guardar la información y quién puede acceder a ella, sin depender de que una corporación o un gobierno lo permita. Esa `soberanía` es personal: la de quien controla su propia bandeja de correo, sus contraseñas, sus archivos. Y es también colectiva: la de una comunidad que gestiona su propia infraestructura compartida y toma decisiones sobre ella.

El concepto surge como respuesta a algo concreto: la concentración de poder digital en muy pocas manos. Hoy, unas pocas empresas controlan los sistemas operativos que usamos, las aplicaciones con las que nos comunicamos, los servidores donde guardamos nuestros archivos y los algoritmos que deciden qué vemos. Y cuando esas empresas cambian sus condiciones de uso, aumentan sus precios o simplemente desaparecen, las comunidades que dependían de ellas quedan sin herramientas.

## El problema de la dependencia

Depender de servicios de terceros no siempre parece un problema. Hay servicios que son gratuitos y funcionan bien, que sincronizan tus archivos entre `dispositivo`s y te conectan con todas las personas que conoces. ¿Por qué construir algo propio?

La respuesta tiene varias capas:

**Privacidad.** Los servicios gratuitos suelen financiarse con `datos`. Los servicios de correo que no controlamos pueden analizar nuestros mensajes. Los servicios de mensajería que no controlamos registran con quién hablamos, cuándo y desde dónde, aunque no puedan leer el contenido.

**Control.** Quien provee el servicio puede cambiar sus condiciones, cerrar el servicio o cerrar tu cuenta sin darte explicaciones. ¿Qué pasa con tus contactos, tus archivos, tu historial de comunicaciones? Si está en sus servidores, es su decisión.

**Dependencia estructural.** Las plataformas están diseñadas para que sea difícil salirse de ellas. Tus contactos están ahí, tus archivos están ahí, tu historial está ahí. Cambiar tiene un costo alto, y eso no es accidental.

## ¿Qué se necesita para la `soberanía`?

La `soberanía` digital no se reduce a tener un servidor propio. Requiere un conjunto de condiciones:

1. **Infraestructura propia**: un lugar donde corre el software, bajo tu control
2. **Software libre y de código abierto**: que puedas auditar, modificar y compartir
3. **Documentación**: que permita entender el sistema, no solo instalarlo
4. **Conocimiento distribuido**: que más de una persona sepa cómo funciona y pueda mantenerlo
5. **Confianza**: que quienes usan el sistema puedan confiar en la información que les llega a través de él

La última condición es quizás la más importante. ¿Cómo se diseña un sistema que nos habilite para ser soberanos y nos permita confiar en la información que usamos para tomar decisiones, para leer el mundo, para vivir? Esa pregunta guía cada decisión de diseño en alfabeto.digital.

## `soberanía` tecnológica vs. `soberanía` digital

A veces se usa "`soberanía` tecnológica" para hablar de algo parecido pero más amplio: el derecho de los pueblos a definir sus propias políticas tecnológicas, a desarrollar tecnología propia, a no quedar atrapados en dependencias geopolíticas. La `soberanía` digital es más acotada, se refiere específicamente al dominio digital, a la infraestructura de comunicación e información.

Ambos conceptos comparten la idea central: la tecnología no es neutral, y quién la controla importa.

## El túnel como decisión de `soberanía`

Un ejemplo concreto de cómo la `soberanía` digital se traduce en decisiones técnicas: el túnel.

Para que un servidor doméstico sea accesible desde internet sin tener que abrir puertos en el router ni depender de una dirección IP fija, se pueden usar varias soluciones. Una opción popular es Cloudflare Tunnel, funciona bien, es gratis y es fácil de configurar. El problema: todo el tráfico pasa por los servidores de Cloudflare, lo que significa que Cloudflare puede ver (y en teoría leer) cada solicitud que llega a tu servidor.

alfabeto.digital usa Newt, un cliente de código abierto que funciona con Pangolin, un stack de túnel que corre en un VPS arrendado. El tráfico no pasa por un tercero: pasa por infraestructura que controlas. Es más trabajo configurar, pero es `soberanía` real: no estás dependiendo de que Cloudflare decida que tu tráfico no viola sus políticas de uso.

Esa diferencia, Cloudflare vs. Newt, es la diferencia entre conveniencia y `soberanía`.

## Cómo se relaciona con alfabeto.digital

alfabeto.digital es una implementación técnica de la `soberanía` digital. La MIDV (Mínima `interfaz` Digital Viable) es el conjunto mínimo de herramientas que permite a una persona o a una comunidad funcionar de manera soberana: comunicarse, almacenar información, autenticarse y publicar, sin depender de `infraestructuras` que no controlamos.

Cada servicio del sistema fue elegido porque puede correr bajo control propio, con código abierto, y porque respeta la privacidad de quienes lo usan. Esa no es una lista de requisitos técnicos, es una lista de valores.

## Ver también

- [las `interfaces`](interfaces.md): las herramientas que determinan la experiencia digital
- [la `midu`](../midu.md): el conjunto mínimo de herramientas para la `soberanía`
- [Pluriverso](pluriverso.md): diversidad epistémica como fundamento político
- [Alfabetización digital popular](alfabetización_digital_popular.md): cómo apropiarse de las herramientas
- [Servicios](../midu/servicios.md): los servicios que componen el sistema
- [Arquitectura](../midu/arquitectura.md): cómo está construida la infraestructura
