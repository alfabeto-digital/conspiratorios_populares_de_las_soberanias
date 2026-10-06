# Cuidados

← [Inicio](../../README.md#los-cuidados)

Los `cuidados` son el conjunto de decisiones que protegen la `midu`: las personas, los `datos` y las `infraestructuras` que los sostienen. Son la condición de posibilidad de que el sistema cumpla su promesa de `soberanía`, integrados en el diseño desde el primer componente.

Cinco principios articulan el modelo de `cuidados`:

**Defensa en profundidad.** Ninguna capa de seguridad es la última línea de defensa: disco cifrado, secretos cifrados, tráfico cifrado, autenticación de dos factores. Un fallo en cualquiera de ellas no compromete el sistema completo.

**Menor privilegio.** Cada componente tiene exactamente los permisos que necesita para funcionar, nada más. El usuario de base de `datos` de Authelia no puede leer la base de `datos` de Dendrite; el VPS reenvía tráfico cifrado pero no tiene acceso a los `datos`.

**Separación de responsabilidades.** El `computador` local no está expuesto directamente a internet; el VPS no almacena `datos`. Comprometer el VPS no da acceso a los `datos`: el VPS solo ve tráfico cifrado que no puede descifrar.

**Asumir compromiso.** El sistema está diseñado asumiendo que cualquier componente puede ser comprometido en algún momento. Si el VPS cae o es tomado, los `datos` siguen cifrados en el `computador` local. Si alguien roba físicamente el servidor, el disco es ilegible sin la clave LUKS.

**Superficie de ataque mínima.** El único camino para llegar a cualquier servicio pasa por cinco puertas en serie: VPS, túnel WireGuard, Caddy, Authelia, servicio solicitado. No en paralelo.

## Documentos de esta sección

| Documento | Qué explica |
|---|---|
| [Modelo de cuidados](cuidados/modelo_de_cuidados.md) | Los principios que guían las decisiones de seguridad: defensa en profundidad, menor privilegio, aislamiento |
| [Zero Trust](cuidados/zero-trust.md) | El modelo de confianza cero: ningún componente confía en otro sin verificación |
| [Cifrado](cuidados/cifrado.md) | Las cuatro capas de cifrado de la `midu`: disco, secretos, tráfico y autenticación |
| [Privacidad](cuidados/privacidad.md) | Qué información sale del sistema, qué no sale, y por qué |

## Ver también

- [Arquitectura](arquitectura.md): los componentes técnicos que los `cuidados` protegen
- [la `midu`](../midu.md): la filosofía detrás del conjunto
- [Subjetividades](subjetividades.md): los fundamentos conceptuales de las decisiones de diseño
