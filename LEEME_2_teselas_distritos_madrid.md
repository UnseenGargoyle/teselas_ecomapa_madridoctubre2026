# Teselas de trabajo por distrito de Madrid (paso 2 de 2)

**Script:** `teselas\_distritos\_madrid.py`
**Autoría:** Diana Damas / GargolaHost
**Contexto:** Ecomapeo de [ecomapa.org](https://ecomapa.org), 3 y 4 de octubre de 2026, municipio de Madrid

Este script divide un distrito de Madrid en **teselas**: zonas de trabajo de unos **3 km de acera** cada una, numeradas y con la lista de calles que incluyen. Sirve para repartir el territorio entre las personas voluntarias del ecomapeo.

> \*\*Importante: este script depende de los datos que genera el primero\*\* (`descargar\_datos\_madrid.py`), que deben estar en la carpeta `datos\_madrid`. El repositorio \*\*ya incluye esos datos\*\*, así que si lo has descargado completo no tienes que ejecutar el primer script. Solo necesitas la guía `LEEME\_1\_descargar\_datos\_madrid.md` si quieres actualizar los datos.

Esta guía está pensada para personas que **nunca han usado Python** y trabajan con **Windows 10 u 11**.

\---

## Qué hace este script

1. Te pregunta para qué distrito quieres crear las teselas.
2. Lee de tu ordenador los barrios y calles de ese distrito (no necesita internet).
3. Divide cada barrio en teselas de unos 3 km de acera.
4. Genera un mapa interactivo, un Excel con los listados y un archivo de capas para QGIS.

### Qué es una tesela y cómo se forma

Una tesela es un conjunto de calles **contiguas** (que se tocan entre sí) dentro de un mismo barrio, pensado para que una persona o un pequeño grupo lo recorra en una jornada.

* **Tamaño:** unos 3 km de acera. Como cada calle tiene dos aceras y hay que recorrer ambas, cada tesela tiene aproximadamente **1,5 km de calle**.
* **Límites:** las teselas nunca cruzan el límite de un barrio.
* **Calles largas:** se parten por tramos entre cruces, de modo que una avenida larga puede repartirse entre varias teselas.
* **Forma:** el script empieza cada tesela por el borde del barrio y va añadiendo los tramos conectados más cercanos, para que salgan zonas compactas y fáciles de recorrer.
* **Numeración:** por barrio, con el código de tres letras del barrio y un número (ACA-01, ACA-02... para Acacias). Dentro de cada barrio se numeran de norte a sur y de oeste a este, como se lee un texto.

\---

## Requisitos

Si ya seguiste la guía del primer script, **lo tienes todo** y puedes pasar a **Cómo se usa**. Si no, no pasa nada: estos son los pasos, y el primer script no es necesario porque los datos ya vienen incluidos.

Si no, necesitas, en este orden:

1. **Los scripts descargados y extraídos.** Entra en https://github.com/UnseenGargoyle/teselas\_ecomapa\_madridoctubre2026, pulsa el botón verde **Code**, después **Download ZIP**, y en tu carpeta de Descargas haz clic derecho sobre el ZIP y elige **Extraer todo**. Los dos scripts deben estar en la misma carpeta.
2. **Python instalado.** Descárgalo desde [python.org/downloads](https://www.python.org/downloads/) (versión 3.11 o superior) y, al instalarlo, marca la casilla **"Add python.exe to PATH"**.
3. **Las librerías.** Abre PowerShell en la carpeta de los scripts (ver abajo) y ejecuta:

```
   python -m pip install geopandas osmnx folium mapclassify matplotlib openpyxl
   ```

4. **Los datos de Madrid.** Vienen incluidos en el repositorio: comprueba que junto a los scripts está la carpeta `datos\_madrid` con el archivo `madrid\_osm.gpkg` dentro. Si quieres datos más recientes, puedes volver a descargarlos con `python descargar\_datos\_madrid.py`.

La guía `LEEME\_1\_descargar\_datos\_madrid.md` explica los pasos 1 a 3 con más detalle.

\---

## Cómo se usa

### 1\. Abrir PowerShell en la carpeta de los scripts

PowerShell es la ventana de comandos que viene con Windows; no hace falta instalar ningún otro programa.

1. Abre el Explorador de archivos y entra en la carpeta donde están los scripts (la que contiene la carpeta `datos\_madrid`).
2. Haz clic en la **barra de direcciones**, borra lo que hay, escribe `powershell` y pulsa **Enter**.

### 2\. Ejecutar el script

Escribe lo siguiente y pulsa Enter:

```
python teselas\_distritos\_madrid.py
```

El script te indicará la fecha de los datos que está usando y te mostrará un menú:

```
¿Para qué distrito de Madrid quieres crear las teselas?
   1. Centro
   2. Arganzuela
   3. Retiro
   ...
Escribe el número y pulsa Enter:
```

Escribe el número del distrito y pulsa Enter. En pocos segundos mostrará el resultado: kilómetros del distrito, número de teselas creadas, el tamaño mínimo y máximo de las teselas y un resumen por barrio.

Puedes ejecutarlo tantas veces como quieras y para tantos distritos como necesites. Cada ejecución crea archivos nuevos sin borrar los anteriores.

\---

## Qué archivos se generan

Tres archivos en la carpeta de los scripts. Todos llevan en el nombre el distrito y la **fecha y hora** de creación (año, mes, día, hora y minuto), por ejemplo `20260928\_09\_01` para el 28 de septiembre de 2026 a las 9:01.

### Mapa interactivo: `mapa\_arganzuela\_20260928\_09\_01.html`

Se abre con **doble clic** en cualquier navegador (Edge, Chrome, Firefox). Necesita conexión a internet solo para cargar el fondo del mapa.

* Cada tesela tiene su color, y sus calles se pintan de ese color.
* Cada tesela lleva una etiqueta con su código (ACA-01...).
* Al pasar el ratón sobre una calle, se resalta y muestra su tesela, nombre, barrio y metros de calle y de acera.
* Con el icono de capas (arriba a la derecha) puedes mostrar u ocultar los límites de barrio, los códigos de tesela y los nombres de los barrios.

Es un único archivo, así que se puede enviar por correo o compartir con otras coordinadoras.

### Listados: `teselas\_arganzuela\_20260928\_09\_01.xlsx`

Se abre con Excel o LibreOffice Calc. Tiene cuatro hojas:

|Hoja|Contenido|
|-|-|
|Teselas|Una fila por tesela: código, barrio, km de calle, km de acera, número de calles y lista de calles. Es la hoja para asignar teselas a las personas voluntarias|
|Calles por tesela|Cada calle de cada tesela, con sus metros de calle y de acera|
|Por barrio|Kilómetros y número de teselas de cada barrio|
|Todas las calles|Metros totales de cada calle en el distrito|

### Capas para QGIS: `teselas\_arganzuela\_20260928\_09\_01.gpkg`

Archivo geográfico con tres capas (tramos, teselas y barrios) para quien quiera revisar o editar las teselas en QGIS, un programa de mapas gratuito. Basta con arrastrar el archivo a la ventana de QGIS. No es necesario para el uso normal.

\---

## Cambiar el tamaño de las teselas

Si quieres teselas más grandes o más pequeñas:

1. Haz clic derecho sobre `teselas\_distritos\_madrid.py` y elige **Abrir con** > **Bloc de notas**.
2. Busca la línea:

```
   KM\_ACERA\_POR\_TESELA = 3.0
   ```

3. Cambia el número (usa punto para los decimales, por ejemplo `2.5`), guarda el archivo y vuelve a ejecutar el script.

## Limitaciones a tener en cuenta

* **Tamaño aproximado.** Las teselas se ajustan a los tramos entre cruces, así que no miden exactamente 3 km: la consola indica el rango real (mínimo y máximo).
* **Zonas aisladas.** Si un barrio tiene calles separadas por vías de tren, grandes avenidas o parques, alguna tesela puede quedar algo dispersa. Se ve fácilmente en el mapa.
* **Calles frontera.** Muchos límites de barrio siguen el eje de una calle; esos tramos se asignan a uno u otro barrio de forma algo arbitraria. Conviene revisarlos al hacer el reparto.
* **Bulevares y avenidas con dos calzadas separadas** cuentan como dos líneas, por lo que su longitud sale aproximadamente doble. Suele ser razonable, porque cada calzada tiene sus propias aceras.
* **Aceras estimadas.** Los metros de acera se calculan como el doble de la longitud de la calle. Las calles peatonales o con una sola acera tendrán en realidad menos recorrido.
* **Parques y zonas verdes** no se incluyen como calles. Si también se censan, hay que organizarlos aparte.
* **Datos colaborativos.** OpenStreetMap puede no coincidir exactamente con el callejero oficial del Ayuntamiento, aunque en Madrid su calidad es alta.

\---

## Problemas frecuentes

|Síntoma|Causa|Solución|
|-|-|-|
|`No se encuentran los datos en ...madrid\_osm.gpkg`|La carpeta `datos\_madrid` no está junto a este script|Comprueba que has extraído el ZIP completo y que `datos\_madrid` está en la misma carpeta que el script. Si falta, descárgala del repositorio o genera los datos con `python descargar\_datos\_madrid.py`|
|`python` no se reconoce como comando|Python no está instalado o falta la casilla "Add python.exe to PATH"|Reinstala Python marcando esa casilla y vuelve a abrir PowerShell|
|`can't open file ... No such file or directory`|PowerShell no está en la carpeta de los scripts|Ábrelo desde la barra de direcciones de la carpeta correcta|
|`ModuleNotFoundError: No module named '...'`|Faltan librerías|Ejecuta la línea de instalación de librerías del apartado Requisitos|
|`Número no válido` en el menú|Se ha escrito algo que no es un número de la lista|Escribe solo el número y pulsa Enter|
|El mapa se abre pero sin fondo|No hay conexión a internet|Las calles y teselas se ven igual; el fondo aparece al conectarse|
|Una tesela sale muy grande, muy pequeña o dispersa|Calles poco conectadas en esa zona|Revísala en el mapa y ajústala a mano en el reparto, o contacta con nosotras|

## Contacto

Para dudas o aclaraciones, escríbenos a través del formulario de contacto de GargolaHost:

[**gargolahost.com/contacto**](https://gargolahost.com/contacto/)

Indica en el asunto **TESELAS ECOMAPEO** para que pueda identificar tu consulta. No publico una dirección de correo electrónico para evitar recibir spam, que ya me llega bastante. :)

Si me escribes por un error, copia y pega el texto completo que aparece en PowerShell: ayuda mucho a encontrar la causa.

\---

*Herramienta desarrollada por Diana Damas / GargolaHost para el Ecomapeo de ecomapa.org (Madrid, 3 y 4 de octubre de 2026). Datos © colaboradores de OpenStreetMap, licencia ODbL.*

