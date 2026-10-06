# Authelia

← [Servicios](servicios.md)

## ¿Qué es esto?

Authelia verifica la identidad de quien solicita acceso antes de que cualquier petición llegue a un servicio de la `interfaz`. Lo hace de dos formas: primero comprueba la contraseña, y si es correcta, pide un segundo código que solo quien tiene el `dispositivo` registrado puede generar en ese momento.

## ¿Para qué sirve?

Authelia implementa dos conceptos que vale la pena entender por separado:

**SSO (Single Sign-On, inicio de sesión único):** una sola autenticación da acceso a todos los servicios del sistema. No necesitas una contraseña distinta para el correo, otra para el gestor de archivos y otra para el chat. Te autenticas una vez con Authelia y todas las puertas quedan abiertas durante tu sesión.

**2FA (autenticación de dos factores):** además de la contraseña (algo que sabes), Authelia pide un código TOTP (algo que tienes). TOTP significa *Time-based One-Time Password*: un código de seis dígitos que cambia cada 30 segundos y que genera una aplicación en tu teléfono (como Aegis en Android o Raivo en iOS). Un atacante que robe tu contraseña no puede entrar sin también tener tu teléfono físico.

**Forward auth:** este es el mecanismo técnico que conecta Authelia con Caddy. Cuando alguien pide acceso a un servicio protegido, Caddy no lo manda directamente al servicio, primero le pregunta a Authelia: "¿tiene este usuario una sesión válida?". Si la respuesta es sí, el tráfico pasa. Si no, Authelia redirige al usuario a la pantalla de inicio de sesión. El servicio protegido nunca ve tráfico no autenticado.

## ¿Por qué Authelia específicamente?

Hay alternativas como Keycloak (más potente pero más pesado) o simplemente contraseñas individuales en cada servicio. Authelia se eligió porque:

- Es ligero y está pensado exactamente para este caso de uso: proteger servicios auto-hospedados con forward auth.
- El soporte para Caddy está bien documentado y probado.
- Implementa 2FA sin necesidad de servicios externos, los códigos TOTP se generan localmente.
- Tiene un panel de usuario donde se puede gestionar los `dispositivo`s 2FA registrados.

## ¿Cómo funciona en alfabeto.digital?

Authelia corre en el `computador` local y usa PostgreSQL como base de `datos` para guardar la información de sesiones y usuarios.

El flujo de autenticación es:

```
Usuario pide acceso a mail.alfabeto.digital
    ↓
Caddy consulta a Authelia: ¿está autenticado?
    ↓
Si no: Authelia muestra el formulario de login (contraseña + TOTP)
Si sí: Caddy pasa el tráfico a Stalwart (el servidor de correo)
```

**Módulo NixOS:** `nixos/modules/nixos/security/authelia.nix`

## La decisión ética: un solo punto de autenticación

Concentrar toda la autenticación en un sistema tiene ventajas y riesgos que vale la pena nombrar explícitamente.

**Ventajas:** si alguien roba o compromete una contraseña, basta con cambiarla en un solo lugar. Si se quiere revocar el acceso a un usuario, se desactiva en Authelia y pierde acceso a todo. Es más fácil auditar quién entró cuándo.

**Riesgo:** Authelia es un punto único de fallo. Si Authelia cae o es comprometida, todos los servicios quedan inaccesibles o desprotegidos. Por eso es especialmente importante que la contraseña de Authelia sea fuerte (Vaultwarden ayuda con eso) y que el 2FA esté siempre activo.

La alternativa, no tener SSO y manejar contraseñas separadas por servicio, parece más descentralizada pero en la práctica es más débil: la gente reutiliza contraseñas, olvida cambiarlas en todos los servicios cuando hay un compromiso, y los servicios individuales tienen protecciones de autenticación más básicas.

## Ver también

- [Caddy](caddy.md): el proxy que consulta a Authelia mediante forward auth
- [Vaultwarden](vaultwarden.md): donde se guarda la contraseña maestra de Authelia
- [PostgreSQL](postgresql.md): la base de `datos` de Authelia
- [`cuidados`](../../`cuidados`/modelo_de_`cuidados`.md): el modelo de `cuidados` general del sistema
