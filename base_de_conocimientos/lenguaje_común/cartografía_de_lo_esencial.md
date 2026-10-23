# La cartografía de lo esencial

El [lenguaje común](lenguaje_común.md) también se dibuja. Reunimos tres formas de cartografía visual que acompañan a la `base de conocimientos`, cada una mira el mismo territorio desde una distancia distinta.

- **El grafo de `graphify`** es una vista amplia. El plugin `graphify` de `Claude Code` recorre las ideas, los textos y el código del `repositorio`, encuentra las relaciones semánticas entre ellos y produce un mapa que las personas y las máquinas podemos navegar.
- **Los diagramas de Excalidraw** son una vista en detalle. Son cinco mapas que narran, en orden, cómo entendemos el paso de la internet del presente hacia una red federada soberana. Cada diagrama es un `objeto digital` editable, y de cada uno exportamos una imagen fija.
- **Las presentaciones con Slideshow** son una vista en el tiempo. Cada diagrama tiene una animación que lo recorre poco a poco, primero las personas, luego sus `dispositivos`, sus `infraestructuras` y las conexiones que se van creando entre ellas. Cada animación vive en un archivo producido por un script de Python que la genera a partir del diagrama.

## El grafo de graphify

- [visualización interactiva](https://alfabeto.digital/assets/graph.html): el grafo navegable en el navegador.
- [grafo en texto](../graphify/graph.json): el mismo mapa como `contexto` para cualquier LLM.

## Los diagramas y sus presentaciones

Cada diagrama reúne cuatro archivos: la imagen fija, el diagrama editable de Excalidraw, su presentación animada y el script de Python que la genera. El script recorre el diagrama, resuelve sus elementos por nombre, texto y grupo, y arma la secuencia de frames con sus animaciones de aparición; el diagrama original nunca se toca, así que volver a correr el script recoge los últimos cambios del diagrama. Los cinco scripts comparten dependencias en [requirements.txt](visualizaciones/requirements.txt).

- **La internet del presente**: [imagen](visualizaciones/midu-la_internet_del_presente.png), [diagrama](visualizaciones/midu-la_internet_del_presente.excalidraw.md), [presentación](visualizaciones/midu-la_internet_del_presente-slideshow.excalidraw.md), [script](visualizaciones/midu-la_internet_del_presente-slideshow.py)
- **Una red local soberana**: [imagen](visualizaciones/midu-una_red_local_soberana.png), [diagrama](visualizaciones/midu-una_red_local_soberana.excalidraw.md), [presentación](visualizaciones/midu-una_red_local_soberana-slideshow.excalidraw.md), [script](visualizaciones/midu-una_red_local_soberana-slideshow.py)
- **Conectarse en internet**: [imagen](visualizaciones/midu-conectarse_en_internet.png), [diagrama](visualizaciones/midu-conectarse_en_internet.excalidraw.md), [presentación](visualizaciones/midu-conectarse_en_internet-slideshow.excalidraw.md), [script](visualizaciones/midu-conectarse_en_internet-slideshow.py)
- **Una red federada**: [imagen](visualizaciones/midu-una_red_federada.png), [diagrama](visualizaciones/midu-una_red_federada.excalidraw.md), [presentación](visualizaciones/midu-una_red_federada-slideshow.excalidraw.md), [script](visualizaciones/midu-una_red_federada-slideshow.py)
- **Una red federada soberana**: [imagen](visualizaciones/midu-una_red_federada_soberana.png), [diagrama](visualizaciones/midu-una_red_federada_soberana.excalidraw.md), [presentación](visualizaciones/midu-una_red_federada_soberana-slideshow.excalidraw.md), [script](visualizaciones/midu-una_red_federada_soberana-slideshow.py)

## Navegar y editar los mapas

Abrimos la carpeta `base_de_conocimientos` como una bóveda de [Obsidian](https://obsidian.md); desde ahí recorremos las tres cartografías y actualizamos cada una por su cuenta.

**El grafo** se explora en el navegador, abriendo la [visualización interactiva](https://alfabeto.digital/assets/graph.html). Se regenera con el plugin `graphify` de `Claude Code`, que vuelve a recorrer el `repositorio` cuando cambian las ideas o el código.

**Los diagramas** se abren con el plugin Excalidraw de Obsidian, que muestra cada `.excalidraw.md` como un lienzo y nos deja editarlo. Al terminar una edición exportamos de nuevo la imagen `.png` desde el mismo plugin. Para leerlos sin editar, basta con abrir la imagen.

**Las presentaciones** se reproducen con el script "Slideshow" de Obsidian desde el lienzo del archivo `-slideshow.excalidraw.md`, que avanza frame por frame. No las editamos a mano: cada una se regenera a partir de su diagrama con su script de Python. Instalamos las dependencias una vez con `pip install -r visualizaciones/requirements.txt` y después ejecutamos el script del diagrama, que reescribe la presentación con los últimos cambios.

## Ver también

- [el lenguaje común](lenguaje_común.md): semillas.
