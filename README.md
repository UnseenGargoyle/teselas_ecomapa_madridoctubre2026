Script Teselas para el Ecomapeo de Madrid

Esctructura y contenido
===



teselas-ecomapeo-madrid/

├── README.md

├── LEEME\_1\_descargar\_datos\_madrid.md

├── LEEME\_2\_teselas\_distritos\_madrid.md

├── descargar\_datos\_madrid.py

├── teselas\_distritos\_madrid.py

└── datos\_madrid/

&#x20;   ├── madrid\_osm.gpkg

&#x20;   └── info\_descarga.txt



Herramientas para dividir los distritos de Madrid en **teselas**: zonas de trabajo de unos **3 km de acera**, numeradas y con la lista de calles que incluyen, para repartir el territorio entre las personas voluntarias.

Preparadas para el **Ecomapeo de** [**ecomapa.org**](https://ecomapa.org) de los días **3 y 4 de octubre de 2026** en el municipio de Madrid.

**Autoría:** Diana Damas / GargolaHost

\---

## Archivos generados por el script

Para el distrito que elijas, se generan tres archivos:

* Un **mapa interactivo** (se abre en el navegador) con cada tesela en un color, su código (por ejemplo ACA-01 en el barrio de Acacias) y la información de cada calle al pasar el ratón.
* Un **Excel** con la lista de teselas, sus kilómetros y las calles que incluye cada una, listo para asignar teselas a las personas voluntarias.
* Un archivo de **capas para QGIS**, por si se quieren revisar o editar las teselas.


## Contenido del repositorio

|Archivo o carpeta|Qué es|
|-|-|
|`teselas\_distritos\_madrid.py`|Script que crea las teselas de un distrito|
|`descargar\_datos\_madrid.py`|Script que descarga de OpenStreetMap los datos de calles, barrios y distritos de Madrid|
|`datos\_madrid/`|**Datos de Madrid ya descargados**, listos para usar|
|`LEEME\_1\_descargar\_datos\_madrid.md`|Guía del script de descarga|
|`LEEME\_2\_teselas\_distritos\_madrid.md`|Guía del script de teselas|

## Datos incluidos

Para que no tengas que descargarlos tú, el repositorio incluye los datos de Madrid capital en la carpeta `datos\_madrid`:

* **Fecha de descarga:** 28 de septiembre de 2026
* **Contenido:** límites de los 21 distritos, barrios y todos los tramos de calle del municipio.
* **Fuente:** OpenStreetMap. El archivo `datos\_madrid/info\_descarga.txt` indica la fecha exacta y los totales.

Todas las teselas creadas con estos datos parten exactamente de la misma información, así que son coherentes entre distritos y entre coordinadoras.

## Por dónde empezar

**Opción A. Usar los datos incluidos (recomendado)**

Es el camino más rápido y no necesita descargar nada de OpenStreetMap.

1. Descarga el repositorio: botón verde **Code** > **Download ZIP**, y extrae el ZIP (clic derecho > **Extraer todo**). Mantén la carpeta `datos\_madrid` junto a los scripts.
2. Sigue la guía [**LEEME\_2\_teselas\_distritos\_madrid.md**](LEEME_2_teselas_distritos_madrid.md), que explica desde cero cómo instalar Python en Windows 10 u 11 y cómo usar el script.

**Opción B. Actualizar los datos**

Solo si necesitas datos más recientes que los incluidos (OpenStreetMap se actualiza continuamente).

1. Sigue la guía [**LEEME\_1\_descargar\_datos\_madrid.md**](LEEME_1_descargar_datos_madrid.md) para descargar los datos de nuevo. Sustituirán a los de la carpeta `datos\_madrid`.
2. Después, sigue la guía [**LEEME\_2\_teselas\_distritos\_madrid.md**](LEEME_2_teselas_distritos_madrid.md).

Si te coordinas con otras personas, es preferible que todas uséis los mismos datos (los incluidos), para que las teselas coincidan.

## Requisitos

* Ordenador con **Windows 10 u 11**.
* **Python 3.11 o superior** (gratuito; las guías explican cómo instalarlo).
* Conexión a internet para instalar Python y sus librerías, y para ver el fondo del mapa. Crear las teselas no necesita conexión.

No hace falta saber programar ni instalar ningún otro programa: todo se hace desde PowerShell, que ya viene con Windows.

## Contacto

Para dudas o aclaraciones, escríbeme a través del formulario de contacto de GargolaHost:

[**gargolahost.com/contacto**](https://gargolahost.com/contacto/)

Indica en el asunto **TESELAS ECOMAPEO** para que pueda identificar tu consulta. No publico una dirección de correo electrónico para evitar recibir spam, que ya recibo suficiente. :)

## Licencias y atribución

* **Datos:** © colaboradores de OpenStreetMap, disponibles bajo la licencia [ODbL](https://opendatacommons.org/licenses/odbl/). Si publicas o compartes mapas o listados generados con estas herramientas, incluye la atribución "© colaboradores de OpenStreetMap".
* **Fondo del mapa interactivo:** Esri World Gray Canvas.
* **Scripts:** Diana Damas / GargolaHost.

