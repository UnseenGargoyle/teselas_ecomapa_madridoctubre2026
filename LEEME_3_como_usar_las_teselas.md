# Cómo usar las teselas: guía para coordinadoras y voluntariado

**Ecomapeo de** [**ecomapa.org**](https://ecomapa.org) · Madrid, 3 y 4 de octubre de 2026

> \*\*ATENCIÓN:\*\* esta documentación y el script de teselas que genera los mapas se pueden descargar en \[https://github.com/UnseenGargoyle/teselas\_ecomapa\_madridoctubre2026](https://github.com/UnseenGargoyle/teselas\_ecomapa\_madridoctubre2026). Son una propuesta para ayudar a realizar el Ecomapeo de ecomapa.org · Madrid, 3 y 4 de octubre de 2026, \*\*Y NO SON OFICIALES\*\*. Si hay algún error u omisión, toda la responsabilidad es de la autora del script y en ningún caso de las organizaciones convocantes.

**Autoría:** Diana Damas / GargolaHost

Esta guía explica cómo leer el **Excel** y el **mapa** que genera el script `teselas\_distritos\_madrid.py`, y cómo usarlos para repartir el territorio y seguir el avance del mapeo. Usamos como ejemplo el distrito de **Arganzuela**, pero todo funciona igual para cualquier distrito de Madrid.

No hace falta instalar nada para usar esta guía: basta con abrir el Excel y el mapa que te hayan pasado.

\---

## 1\. Qué es una tesela

Una tesela es la **unidad de trabajo** del ecomapeo: un grupo de calles contiguas, dentro de un mismo barrio, pensado para que una persona lo recorra en **aproximadamente una hora**.

* Cada tesela suma unos **3 km de recorrido a pie por acera**. Como hay que mapear **las dos aceras** de cada calle, eso equivale a unos 1,5 km de calle.
* La hora es **orientativa**. Cada persona tiene su ritmo y sus circunstancias, y no es lo mismo una calle con pocos árboles que un paseo arbolado. Lo importante es que todas las teselas tienen un tamaño parecido, así que sirven para repartir el trabajo de forma equilibrada.
* Las teselas **no cruzan el límite de un barrio**. Una calle larga puede repartirse entre varias teselas, siempre cortada en un cruce.

## 2\. Cómo se nombran las teselas

Cada tesela tiene un código con **las tres primeras letras de su barrio** y un número:

**LAS-01** = tesela número 1 del barrio de **Las Acacias**

Las letras se toman del nombre del barrio tal como figura en OpenStreetMap, incluido el artículo si lo tiene: por eso Las Acacias es LAS y no ACA.

Dentro de cada barrio, las teselas se numeran de norte a sur y de oeste a este, como se lee un texto. En la hoja *Por barrio* del Excel puedes ver qué barrios tiene el distrito y, en la hoja *Teselas*, el código de cada uno.

\---

## 3\. La hoja de cálculo (el Excel, vaya)

El archivo se llama, por ejemplo, `teselas\_arganzuela\_20260928\_09\_01.xlsx`: distrito, fecha (año, mes, día) y hora de creación. Tiene cuatro hojas.

### Hoja "Teselas": la principal para el reparto

Una fila por tesela.

|Columna|Qué significa|
|-|-|
|tesela|Código de la tesela (LAS-01)|
|barrio|Barrio al que pertenece|
|km\_calle|Kilómetros de calle que incluye|
|km\_acera|Kilómetros de acera que hay que recorrer (el doble de km\_calle). Unos 3 km, aproximadamente una hora|
|num\_calles|Cuántas calles distintas incluye|
|calles|Lista de las calles, de la más larga a la más corta dentro de la tesela|

Es la hoja que se usa para **asignar teselas** y para decirle a cada persona qué calles le tocan.

### Hoja "Calles por tesela"

Una fila por cada calle de cada tesela, con sus metros de calle y de acera. Sirve para ver cuánto de cada calle entra en una tesela: una avenida larga puede aparecer en varias teselas, cada una con su tramo.

### Hoja "Por barrio"

Una fila por barrio, con sus kilómetros totales y su número de teselas. Sirve para hacerse una idea del volumen de trabajo: **cada tesela es aproximadamente una hora de una persona**.

### Hoja "Todas las calles"

Todas las calles del distrito con sus metros totales. Útil para buscar una calle concreta.

### Ejemplo: Arganzuela

En Arganzuela salen **73 teselas**, repartidas en los siete barrios del distrito:

|Barrio|Código|Teselas|Km de acera|
|-|-|-|-|
|Las Acacias|LAS|7|21,57|
|Atocha|ATO|8|24,67|
|Chopera|CHO|12|35,32|
|Delicias|DEL|11|32,94|
|Imperial|IMP|13|40,24|
|Legazpi|LEG|13|40,27|
|Palos de Moguer|PAL|9|28,41|

Es decir, cubrir todo el distrito supone unas **73 horas de mapeo** en total, que pueden repartirse entre muchas personas.

\---

## 4\. El mapa y cómo se corresponde con el Excel

El mapa se llama, por ejemplo, `mapa\_arganzuela\_20260928\_09\_01.html`, con la misma fecha y hora que el Excel generado en la misma ejecución. Se abre con **doble clic** en cualquier navegador y necesita conexión a internet para cargar el fondo.

**Qué se ve:**

* Cada tesela tiene **un color**, y todas sus calles están pintadas de ese color.
* **ATENCIÓN:** en algunas calles pueden superponerse los colores de dos teselas y no apreciarse a simple vista. Pasa sobre todo cuando la calle hace de límite entre dos barrios o cuando tiene dos calzadas separadas. Para evitar confusiones, consulta la hoja de cálculo y, sobre todo, **PONTE DE ACUERDO CON LA GENTE DE LAS TESELAS VECINAS**. Las teselas son una ayuda para organizarse: no sustituyen el sentido común ni la coordinación entre personas.
* Cada tesela lleva una **etiqueta con su código** (LAS-01), el mismo que en el Excel.
* Los **límites de los barrios** aparecen en negro.
* Al **pasar el ratón** por una calle, se resalta y muestra su tesela, su nombre, su barrio y sus metros.

**Capas que se pueden activar y desactivar**

Arriba a la derecha hay un icono de capas. Al pulsarlo aparecen casillas para mostrar u ocultar:

|Capa|Para qué|
|-|-|
|Límites de barrios|Líneas negras de los barrios|
|Calles por tesela|Las calles coloreadas|
|Códigos de teselas|Las etiquetas LAS-01, LAS-02...|
|Nombres de barrios|El nombre de cada barrio (desactivada al abrir)|

Si **desactivas "Calles por tesela" y "Códigos de teselas"**, verás debajo el mapa de fondo con el **nombre de las calles**, lo que ayuda a orientarse. Vuelve a activarlas para ver de nuevo las teselas.

**Cómo pasar del Excel al mapa y al revés**

* **Del Excel al mapa:** busca el código de la tesela (por ejemplo LAS-03) en el mapa; la etiqueta está sobre una de sus calles.
* **Del mapa al Excel:** pasa el ratón por una calle para ver su tesela y busca ese código en la hoja *Teselas*.
* **Para localizar una calle:** en el Excel pulsa **Ctrl+B** (o Ctrl+F), escribe el nombre de la calle y verás en qué tesela o teselas está.

\---

## 5\. Cómo organizar el reparto

**1. Cada persona indica cuántas horas puede dedicar.** Como cada tesela es aproximadamente una hora, las horas disponibles indican cuántas teselas puede asumir: una persona con dos horas puede llevar dos teselas, a ser posible vecinas.

**2. Primero, donde mejor le venga a cada persona.** En la asignación inicial conviene dar a cada persona teselas cerca de su casa o de donde se mueva habitualmente. Así se aprovecha mejor el tiempo y es más fácil que se completen.

**3. Seguimiento de las teselas completadas.** Cada persona informa a su coordinadora cuando termina una tesela. Para llevar el control, lo más práctico es una copia compartida de la hoja *Teselas* con tres columnas añadidas a mano:

|Columna|Ejemplo|
|-|-|
|Asignada a|Nombre de pila de la persona|
|Estado|Pendiente / En curso / Completada|
|Fecha|Día en que se completó|

Así se ve de un vistazo qué queda por hacer en cada barrio.

**4. Después, cubrir las que falten.** Cuando las teselas cercanas a las personas participantes estén completadas, quedarán zonas sin cubrir. En esa segunda fase, quien pueda se desplaza a completarlas. La hoja *Por barrio* y el estado de cada tesela ayudan a decidir dónde hace más falta.

\---

## 6\. Qué no incluyen las teselas

* **Parques y zonas verdes** (en Arganzuela, por ejemplo, Madrid Río o el parque Tierno Galván). Sus caminos interiores no se incluyen como calles. Si se quieren mapear, hay que **repartirlos a mano**, aparte de las teselas.
* **Autopistas, túneles, enlaces y vías de servicio**, que no tienen aceras que recorrer.

Otros detalles a tener en cuenta:

* Los **km de acera** se calculan como el doble de la longitud de la calle. Las calles peatonales o con acera solo en un lado tendrán en realidad menos recorrido.
* Muchos **límites de barrio siguen el centro de una calle**, así que esa calle puede quedar asignada a uno u otro barrio. Conviene revisarlo al repartir.
* Las **avenidas con dos calzadas separadas** cuentan como dos líneas, porque cada calzada tiene sus propias aceras.

## 7\. Sobre los datos

Las calles, barrios y distritos proceden de **OpenStreetMap**, una base de datos cartográfica pública, libre y colaborativa. No son datos oficiales del Ayuntamiento, aunque en Madrid su calidad es alta. Si detectas una calle que falta o que no existe, avisa a tu coordinadora.

La fecha de los datos aparece en el `README.md` del repositorio. Datos © colaboradores de OpenStreetMap, licencia ODbL.

## 8\. Otros distritos

Todo lo anterior vale para **cualquier distrito de Madrid**. Al ejecutar el script se elige el distrito, y el Excel y el mapa salen con su nombre y con los códigos de sus propios barrios. Las instrucciones para generarlos están en `LEEME\_2\_teselas\_distritos\_madrid.md`.

\---

## Contacto

Para dudas o aclaraciones, escríbeme a través del formulario de contacto de GargolaHost:

[**gargolahost.com/contacto**](https://gargolahost.com/contacto/)

Indica en el asunto **TESELAS ECOMAPEO** para que pueda identificar tu consulta. No publico una dirección de correo electrónico para evitar recibir spam.

\---

*Diana Damas / GargolaHost para el Ecomapeo de ecomapa.org (Madrid, 3 y 4 de octubre de 2026). Datos © colaboradores de OpenStreetMap, licencia ODbL.

Licencia. Esta documentación y los scripts descargar\_datos\_madrid.py y teselas\_distritos\_madrid.py se dedican al dominio público mediante CC0 1.0 Universal. Puedes usarlos, copiarlos, modificarlos y compartirlos libremente, incluso con fines comerciales, sin pedir permiso ni citar la autoría. Los datos geográficos incluidos y los que generan los scripts proceden de OpenStreetMap y mantienen su propia licencia, la Open Database License (ODbL): si los compartes o publicas, debes incluir la atribución "© colaboradores de OpenStreetMap".*

