# Descarga de datos de calles de Madrid (paso 1 de 2)

**Script:** `descargar\_datos\_madrid.py`
**Autoría:** Diana Damas / GargolaHost
**Contexto:** Ecomapeo de [ecomapa.org](https://ecomapa.org), 3 y 4 de octubre de 2026, municipio de Madrid

Este script es el **primero de dos**. Descarga y guarda en tu ordenador los datos de calles, barrios y distritos de Madrid capital. El segundo script, `teselas\_distritos\_madrid.py`, usa esos datos para dividir un distrito en zonas de trabajo (teselas) y repartirlas entre las personas voluntarias. Tiene su propia guía: `LEEME\_2\_teselas\_distritos\_madrid.md`.

Esta guía está pensada para personas que **nunca han usado Python** y trabajan con **Windows 10 u 11**.

\---

## Qué hace este script

Se conecta a OpenStreetMap, descarga los datos de todo el municipio de Madrid y los guarda en una carpeta de tu ordenador. Solo hay que ejecutarlo **una vez**, o cuando se quieran actualizar los datos (por ejemplo, cada pocos meses).

Una vez descargados, el segundo script trabaja con ellos sin volver a conectarse a internet, lo que es más rápido y garantiza que todas las teselas de todos los distritos parten exactamente de los mismos datos.

## Qué datos descarga y de dónde

Todos los datos proceden de **OpenStreetMap**, la base de datos cartográfica libre y colaborativa, a través de sus servicios públicos (Nominatim para localizar Madrid y Overpass para descargar los datos).

|Datos|Descripción|
|-|-|
|Distritos|Límites de los 21 distritos de Madrid|
|Barrios|Límites de los barrios, con el distrito al que pertenecen y un código de tres letras (Acacias: ACA)|
|Calles|Todas las calles del municipio, divididas en tramos de cruce a cruce y asignadas a su barrio|

Se incluyen las calles de tipo principal, secundario, terciario, residencial, peatonal y de coexistencia. Se excluyen autopistas, enlaces, túneles, vías de servicio y caminos peatonales sueltos (por ejemplo, los senderos dentro de los parques).

Los datos de OpenStreetMap se distribuyen bajo licencia ODbL. Si publicas o compartes resultados, incluye la atribución "© colaboradores de OpenStreetMap".

\---

## Instalación y uso paso a paso

### Paso 1. Descargar los scripts

1. Entra en el repositorio: https://github.com/UnseenGargoyle/teselas\_ecomapa\_madridoctubre2026
2. Pulsa el botón verde **Code** y después **Download ZIP**.
3. Busca el archivo ZIP en tu carpeta de Descargas, haz clic derecho sobre él y elige **Extraer todo**.
4. Mueve la carpeta extraída a un sitio cómodo, por ejemplo `Documentos\\teselas`.

Es importante **extraer** el ZIP: los scripts no funcionan si se ejecutan desde dentro del archivo comprimido.

### Paso 2. Instalar Python

Python es el lenguaje en el que están escritos los scripts. Hay que instalarlo una sola vez.

1. Entra en [python.org/downloads](https://www.python.org/downloads/) y pulsa el botón de descarga para Windows (cualquier versión 3.11 o superior sirve).
2. Abre el instalador descargado.
3. **Muy importante:** si en la primera pantalla aparece la casilla **"Add python.exe to PATH"**, márcala antes de continuar. Sin ella, Windows no encontrará Python.
4. Pulsa **Install Now** y espera a que termine.

Alternativa: también puedes instalarlo desde la **Microsoft Store** buscando "Python".

### Paso 3. Abrir PowerShell en la carpeta de los scripts

Los scripts se ejecutan desde **PowerShell**, una ventana de comandos que ya viene con Windows. No necesitas instalar ningún otro programa.

1. Abre el Explorador de archivos y entra en la carpeta donde están los scripts.
2. Haz clic en la **barra de direcciones** (donde aparece la ruta de la carpeta), borra lo que hay, escribe `powershell` y pulsa **Enter**.

Se abrirá una ventana azul o negra que ya está situada en esa carpeta. Para comprobar que Python funciona, escribe lo siguiente y pulsa Enter:

```
python --version
```

Debe aparecer algo como `Python 3.13.1`. Si aparece un error, consulta la sección de problemas frecuentes.

### Paso 4. Instalar las librerías necesarias

Las librerías son complementos de Python que los scripts necesitan. En la misma ventana de PowerShell, copia esta línea, pégala (con Ctrl+V o con clic derecho) y pulsa Enter:

```
python -m pip install geopandas osmnx folium mapclassify matplotlib openpyxl
```

Tardará uno o dos minutos. Esta línea instala también lo que necesita el segundo script, así que después no tendrás que repetirla.

### Paso 5. Ejecutar la descarga

En la misma ventana, escribe y pulsa Enter:

```
python descargar\_datos\_madrid.py
```

Verás cómo avanza en tres fases:

```
1/3 Descargando límites de los distritos...
2/3 Descargando barrios...
3/3 Descargando calles de todo Madrid (puede tardar varios minutos)...
```

La descarga de calles es grande y puede tardar **entre 5 y 15 minutos**, según la conexión y lo ocupados que estén los servidores. No cierres la ventana mientras tanto. Si un servidor corta la conexión, el script espera y lo reintenta automáticamente, incluso en servidores alternativos.

Al terminar, muestra un resumen con los kilómetros de calle y el número de barrios de cada distrito. **Comprueba que aparecen los 21 distritos** y que ninguno tiene 0 barrios.

\---

## Qué obtienes

Se crea una carpeta `datos\_madrid` junto a los scripts, con dos archivos:

|Archivo|Contenido|
|-|-|
|`madrid\_osm.gpkg`|Los datos descargados (distritos, barrios y tramos de calle). Ocupa unas decenas de MB. **No lo borres ni lo muevas**: el segundo script lo busca en esta carpeta|
|`info\_descarga.txt`|Fecha de la descarga y totales (distritos, barrios, tramos y kilómetros). Se puede abrir con el Bloc de notas|

El archivo `.gpkg` es un GeoPackage, un formato estándar para datos geográficos. Si tienes QGIS (programa gratuito de mapas), puedes abrirlo arrastrándolo a su ventana, pero no es necesario para nada.

## Cuándo volver a ejecutarlo

Solo si quieres datos más recientes, porque en OpenStreetMap se corrigen y añaden calles continuamente. Al volver a ejecutarlo, los datos anteriores se sustituyen por los nuevos, pero solo cuando la descarga ha terminado bien: si falla a mitad, se conservan los anteriores.

## Siguiente paso

Con los datos descargados, ya puedes crear las teselas de cualquier distrito con el segundo script. Sigue la guía `LEEME\_2\_teselas\_distritos\_madrid.md`.

\---

## Problemas frecuentes

|Síntoma|Causa|Solución|
|-|-|-|
|`python` no se reconoce como comando, o se abre la Microsoft Store|Python no está instalado o no se marcó "Add python.exe to PATH"|Reinstala Python marcando esa casilla. Cierra y vuelve a abrir PowerShell después|
|`can't open file ... No such file or directory`|PowerShell no está en la carpeta de los scripts|Repite el paso 3, abriendo PowerShell desde la barra de direcciones de la carpeta correcta|
|`ModuleNotFoundError: No module named '...'`|Faltan librerías|Repite el paso 4|
|Avisos de "El servidor ... ha fallado"|Servidor de OpenStreetMap saturado|No hagas nada: el script reintenta solo|
|`No se ha podido descargar de ningún servidor`|Sin conexión, VPN activa o servidores caídos|Comprueba la conexión, desactiva la VPN si usas una y prueba de nuevo más tarde|
|En el resumen faltan distritos o alguno tiene 0 barrios|Cambios en los datos de OpenStreetMap|Contacta con nosotras (ver abajo)|

## Contacto

Para dudas o aclaraciones, escríbenos a través del formulario de contacto de GargolaHost:

[**gargolahost.com/contacto**](https://gargolahost.com/contacto/)

Indica en el asunto **TESELAS ECOMAPEO** para que podamos identificar tu consulta. No publicamos una dirección de correo electrónico para evitar recibir spam.

Si nos escribes por un error, copia y pega el texto completo que aparece en PowerShell: nos ayuda mucho a encontrar la causa.

\---

*Herramienta desarrollada por Diana Damas / GargolaHost para el Ecomapeo de ecomapa.org (Madrid, 3 y 4 de octubre de 2026). Datos © colaboradores de OpenStreetMap, licencia ODbL.*

