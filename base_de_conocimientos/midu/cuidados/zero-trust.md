# Arquitectura Zero Trust

## El problema del castillo con foso

El modelo tradicional de seguridad de redes se parece a un castillo medieval: hay un perímetro (el foso, las murallas) que separa el "interior seguro" del "exterior peligroso". Todo lo que está dentro de las murallas se considera confiable. Si eres parte del personal del castillo, puedes moverte libremente por los pasillos.

El problema con este modelo es que asume que el perímetro es impenetrable. Pero ¿qué pasa cuando alguien con malas intenciones ya está dentro? ¿O cuando el perímetro tiene una grieta que no se detectó? Una vez dentro del castillo, ese alguien tiene acceso a todo.

En el mundo actual, este modelo tiene otra debilidad: el "interior" ya no existe de manera clara. Los servicios están en la nube, los usuarios acceden desde casa, los `dispositivo`s se conectan desde redes distintas. No hay un perímetro definido que defender.

## Zero Trust: no confíes en nada, verifica todo

Zero Trust invierte la lógica completamente: **ningún componente confía en ningún otro por defecto**, sin importar si está "dentro" o "fuera" de la red. Cada solicitud, venga de donde venga, debe ser autenticada y autorizada antes de recibir respuesta.

El nombre puede sonar paranoico. Pero la lógica es sólida: si asumes que algo puede estar comprometido —un `dispositivo`, una contraseña, una cuenta— y diseñas el sistema para eso, un compromiso real tiene consecuencias mucho más limitadas.

## Cómo funciona Zero Trust en alfabeto.digital

**Caddy como portero**

Caddy es el proxy inverso: el componente que recibe todo el tráfico de internet antes de que llegue a cualquier servicio. No importa si alguien pide acceso a Nextcloud, al correo, al chat o al gestor de contraseñas: la solicitud pasa primero por Caddy.

Caddy no deja pasar nada sin consultar a Authelia.

**Authelia como verificador de identidad**

Antes de reenviar cualquier solicitud a un servicio, Caddy le pregunta a Authelia: "¿está autenticado este usuario y tiene permiso para acceder a esto?"

Este mecanismo se llama **forward auth** (autenticación hacia adelante): Caddy delega la verificación de identidad a Authelia antes de decidir si pasa la solicitud o no.

Si Authelia dice que no hay sesión válida, Caddy redirige al usuario a la pantalla de login. El servicio destino nunca ve la solicitud no autenticada.

Si Authelia confirma la identidad, Caddy reenvía la solicitud al servicio y añade cabeceras con la información del usuario (nombre, correo, grupos). El servicio puede usar esas cabeceras para tomar decisiones adicionales de autorización.

**La excepción necesaria**

Solo hay un endpoint que está exento de la verificación de Authelia: `auth.{dominio}`, el propio dominio de Authelia. Tiene que estarlo por necesidad lógica: si Authelia tuviera que autenticarse a sí misma para funcionar, el sistema quedaría en un bucle imposible. El usuario no puede autenticarse porque Authelia no responde, y Authelia no responde porque el usuario no está autenticado.

Esta excepción es la única. Todos los demás servicios pasan por Authelia sin excepción.

**Aislamiento dentro del servidor**

Zero Trust no termina en la puerta de entrada. Dentro del `computador` local, cada servicio vive en su propio espacio:

- Cada servicio tiene su propio usuario de sistema con permisos mínimos.
- Cada servicio tiene su propia base de `datos`. El usuario de base de `datos` de Authelia no puede leer la base de `datos` de Dendrite, ni al revés.
- Los directorios de `datos` de cada servicio tienen permisos que solo permiten el acceso al usuario correspondiente.

Esto significa que incluso si un atacante lograra comprometer un servicio concreto —por ejemplo, encontrar una vulnerabilidad en Nextcloud— no obtendría acceso automático al correo, al chat ni a las contraseñas almacenadas en Vaultwarden. Cada servicio es un compartimento separado.

## Una decisión ética, no solo técnica

Adoptar Zero Trust es también una postura honesta sobre la naturaleza de la seguridad.

El modelo del castillo con foso implica decir "somos seguros porque nadie ha entrado". Zero Trust implica decir "en algún momento algo va a fallar, y hemos diseñado el sistema para que ese fallo tenga consecuencias limitadas".

La segunda postura es más honesta. No promete seguridad perfecta —que no existe— sino **contención del daño** cuando algo sale mal.

En términos prácticos: si mañana hay una vulnerabilidad crítica en uno de los servicios y un atacante la explota, los `datos` de los demás servicios siguen protegidos. El disco sigue cifrado. Los secretos siguen cifrados. El atacante tiene acceso a ese servicio, no al sistema completo.

Ver también: [Modelo de `cuidados`](modelo.md) · [Cifrado en capas](cifrado.md) · [Privacidad por diseño](privacidad.md) · [Arquitectura general](../arquitectura/)
