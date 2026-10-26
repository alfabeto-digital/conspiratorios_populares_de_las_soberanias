# Las capas de la memoria

← [Arquitectura](../arquitectura.md)

La `midu` no gestiona `datos` abstractos: gestiona `memorias`. Las `memorias` no son monolíticas; se organizan en estratos funcionales donde cada capa sostiene lo que puede existir en las capas superiores.

Esta organización no es nueva. La imprenta organizó la memoria escrita en capas: quién podía producir tipos, quién podía costear una edición, quién tenía acceso a redes de distribución, quién sabía leer. La web comercial organizó la memoria digital en capas similares: quién controla los servidores de búsqueda, quién decide qué permanece almacenado, quién puede pagar por visibilidad. En ambos casos, las decisiones sobre cada capa determinan qué sobrevive.

La `midu` articula seis capas, cada una esta bajo nuestro control. La `soberanía` se traduce en la capacidad técnica de determinar el comportamiento de estas capas.

## Las seis capas

| Capa | Función | Riesgo si no es sobearana |
|---|---|---|
| Comunicaciones | Intercambio de mensajes, documentos y notificaciones | Los metadatos de quién habla con quién quedan en manos de terceros |
| Observabilidad | Capacidad de examinar el propio sistema | El sistema existe pero no puede leerse ni auditarse |
| Procesamiento | Transformación de `objetos digitales`; nuevas representaciones | Las herramientas de procesamiento inscriben subjetividades ajenas |
| Descubribilidad | Visibilidad recíproca entre nodos y personas | Los algoritmos de recomendación determinan qué existe para quién |
| Reproducibilidad | Adaptación, mutación y `replicación` en nuevos `contextos` | El sistema no puede sobrevivir fuera del entorno en que fue creado |
| Resiliencia | Recuperación ante fallos y eventos catastróficos | La recuperación depende de la disponibilidad de terceros |

## Comunicaciones

La capa de comunicaciones es la más inmediata: el intercambio de mensajes, documentos y notificaciones entre personas. Es también la más vigilada. Los metadatos de comunicación, quién envió qué a quién, cuándo, con qué frecuencia, tienen valor informacional incluso cuando el contenido está cifrado.

En la `midu`, la capa de comunicaciones incluye el correo electrónico ([Stalwart](../servicios/stalwart.md)), la mensajería instantánea federada ([Dendrite](../servicios/dendrite.md)) y las notificaciones push ([ntfy](../servicios/ntfy.md)). Cada servicio corre en el `computador` local: los metadatos no salen del sistema.

La federación agrega una consideración extra: cuando un servicio interactúa con participantes en otros servicios federados (Matrix), los metadatos de esas interacciones existen en todos los actores federados. Esta es una decisión consciente, la interoperabilidad tiene un costo en términos de control centralizado de los metadatos.

## Observabilidad

Sin observabilidad, la memoria existe pero no puede examinarse. Una biblioteca sin catálogo, un sistema sin métricas: los `datos` están ahí pero no podemos verlos.

La capa de observabilidad permite reflexionar sobre el sistema: qué recursos consume, qué errores produce, qué patrones emergen. En la `midu` esto incluye métricas (Prometheus), logs (Loki), visualización (Grafana) y alertas (Alertmanager).

La observabilidad también es una capa política. Quién puede ver las métricas del sistema determina quién puede auditarlo. En `infraestructuras` delegadas, la observabilidad está disponible para el proveedor, no para la comunidad que usa el servicio. La `soberanía` sobre los `datos` incluye la `soberanía` sobre la información de cómo esos `datos` se mueven.

## Procesamiento

El procesamiento es la capa de las transformaciones: extraer texto de un documento, resumir conversaciones, identificar patrones, generar nuevas representaciones a partir de las existentes.

Esta capa concentra el debate sobre inteligencia artificial porque los modelos de lenguaje inscriben subjetividades en sus salidas. Un modelo entrenado sobre ciertos contenidos, con ciertos criterios de filtrado, produce ciertos tipos de textos y no otros. Delegar el procesamiento a servicios externos es delegar la producción de conocimiento a quien diseñó esos modelos.

En la `midu`, el procesamiento incluye herramientas de gestión documental, ofimática y modelos de lenguaje locales (Ollama). Ninguna de estas herramientas es neutral, pero podemos decidir sobre su presencia en el `computador` local.

## Descubribilidad

La descubribilidad responde a la pregunta de cómo encuentrar personas y memorias en la red. No basta con que algo exista: tiene que poder ser encontrado.

Esta capa es donde las diferencias entre federación y centralización son más visibles. La web centralizada resolvió la descubribilidad con motores de búsqueda que indexan todo y deciden qué aparece primero. La federación redistribuye el almacenamiento pero no resuelve automáticamente la descubribilidad: un nodo que nadie conoce no puede ser contactado.

La descubribilidad también tiene una dimensión de exclusión. Los estudios sobre el fediverso documentan cómo las dinámicas de instancias pequeñas y grandes replican las exclusiones de la web centralizada: personas negras, trans y del sur global encuentran sus cuentas bloqueadas, defederadas o silenciadas por administradores de instancias grandes que actúan como guardianes informales del espacio.

Gobernar la descubribilidad requiere decisiones explícitas: con quién se federa, qué instancias se bloquean, qué criterios de moderación se aplican. Estas decisiones son ejercicios de `gobernanza` participativa y producirán reglas distintas para comunidades distintas.

## Reproducibilidad

La reproducibilidad es la condición de que el sistema pueda sobrevivir fuera del entorno en que fue creado: adaptarse, mutar, replicarse en nuevos `contextos` con personas y dispositivos distintos.

La imprenta no fue viable porque una persona construyó una prensa y la distribuyó uniformemente. Fue viable porque el conocimiento de cómo construir una prensa, operar un taller tipográfico y distribuir textos se diseminó de maneras que permitieron que otros lo adaptaran a sus condiciones. Cada taller incorporó las subjetividades del lugar donde se instalaba.

En la `midu`, la reproducibilidad descansa en infraestructura como código (NixOS), documentación transferible y el [patrón dendrítico](patrón_dendrítico.md). Lo que se replica no es la configuración exacta sino la capacidad: el conocimiento de cómo construir y mantener la `interfaz`, transferible a otra persona, otra comunidad, y otro `contexto`.

## Resiliencia

La resiliencia es la capacidad de recuperarse ante fallos: hardware que se daña, desastres naturales, ataques físicos y digitales, y ausencia de personas capaces de cuidar la `midu`.

Los sistemas de archivo alternativos, emergentes en todo el Sur Global, han propuesto prácticas de resiliencia que van más allá de los copias de seguridad. El Archivo de la Memoria Trans Argentina distribuye copias físicas entre personas de confianza en distintas ciudades. Los archivos de comunidades indígenas mantienen copias en múltiples formatos y lenguas para sobrevivir a la pérdida de cualquier soporte.

La resiliencia requiere infraestructura humana: personas que saben restaurar el sistema, que conocen las claves, que pueden responder cuando algo falla. Sin esa capa humana, la resiliencia técnica es frágil. Un disco de respaldo que nadie sabe restaurar no agrega capacidades de resiliencia.

En la `midu`, la resiliencia técnica incluye: cifrado LUKS con dos slots (passphrase de emergencia y clave de sops-nix), backups periódicos en Syncthing, rollbacks automáticos de NixOS y documentación del proceso de restauración. La resiliencia humana requiere que al menos dos personas en una comunidad entiendan el sistema y puedan mantenerlo.

## La soberanía

Cada capa puede estar bajo control soberano o delegada a `infraestructuras` externas. Los niveles de `soberanía` pueden variar según las capacidades y necesidades: una persona o comunidad pueden controlar sus comunicaciones y delegar el procesamiento, o controlar la reproducibilidad y delegar la descubribilidad.

La `midu` propone que todas las capas estén bajo nuestro control en todo momento. Sin embargo, reconocemos que en algunos casos debemos hacer concesiones de acuerdo a nuestros recursos; en ese caso la `midu` facilita las herramientas conceptuales para que esa decisión sea consciente y susceptible de ser revisada en el tiempo: que las comunidades sepan qué capas controlan, qué capas delegan, a quién las delegan y bajo qué condiciones pueden recuperar ese control.

Entendemos la `soberanía`, en este caso la `soberanía digital`, como la capacidad de tomar decisiones sobre nuestras representaciones digitales y sobre nuestras `memorias` individuales y colectivas en todo momento, y de resistirse a que otros tomen decisiones por nosotros.

## La base de conocimientos

Los servicios de comunicación de la `midu` permiten el intercambio entre personas que ya están conectadas a la red. Publicar la base de conocimientos como sitio web extiende esa capa hacia afuera: hace accesible el conocimiento a quien todavía no tiene una `midu`.

[Hugo](../servicios/publicación.md) convierte los archivos Markdown de `base_de_conocimientos/` en un sitio navegable servido por [Caddy](../servicios/caddy.md) en [info.alfabeto.digital](https://info.alfabeto.digital).

## Ver también

- [la `midu`](../../midu.md): la interfaz que integra las seis capas
- [`memorias` colectivas](../../subjetividades/memorias_colectivas.md): qué se conserva y quién decide
- [`infraestructuras`](../../subjetividades/infraestructuras.md): las tres capas de toda infraestructuras: físicas, digitales y humanas