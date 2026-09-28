"""
Crea teselas de unos 3 km de acera para el distrito de Madrid que se elija,
a partir de los datos guardados por descargar_datos_madrid.py
(datos_madrid/madrid_osm.gpkg). No necesita conexión a internet, salvo
para ver el fondo del mapa.

Genera, con fecha y hora en el nombre:
  - mapa_<distrito>_<fecha>.html     mapa interactivo
  - teselas_<distrito>_<fecha>.xlsx  listados de teselas y calles
  - teselas_<distrito>_<fecha>.gpkg  capas para QGIS
"""
import heapq
import sys
import unicodedata
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import folium
import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.ops import nearest_points

CARPETA = Path(__file__).parent
ARCHIVO_DATOS = CARPETA / "datos_madrid" / "madrid_osm.gpkg"
INFO_DESCARGA = CARPETA / "datos_madrid" / "info_descarga.txt"

# Tamaño de cada tesela en kilómetros de ACERA (se cuentan las dos aceras de cada calle,
# así que cada tesela tendrá aproximadamente la mitad de kilómetros de calle)
KM_ACERA_POR_TESELA = 3.0
OBJETIVO_M_CALLE = KM_ACERA_POR_TESELA * 1000 / 2

# Orden en que se muestran los distritos en el menú
DISTRITOS_MADRID = [
    "Centro", "Arganzuela", "Retiro", "Salamanca", "Chamartín", "Tetuán",
    "Chamberí", "Fuencarral-El Pardo", "Moncloa-Aravaca", "Latina",
    "Carabanchel", "Usera", "Puente de Vallecas", "Moratalaz", "Ciudad Lineal",
    "Hortaleza", "Villaverde", "Villa de Vallecas", "Vicálvaro",
    "San Blas-Canillejas", "Barajas",
]

# Colores bien distintos para diferenciar teselas vecinas en el mapa
PALETA = [
    "#e6194b", "#3cb44b", "#4363d8", "#f58231", "#911eb4", "#42d4f4",
    "#f032e6", "#9a6324", "#469990", "#800000", "#808000", "#000075",
]


# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------

def nombre_archivo(texto):
    """Fuencarral-El Pardo -> fuencarral_el_pardo"""
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    limpio = "".join(c if c.isalnum() else "_" for c in sin_tildes.lower())
    return "_".join(p for p in limpio.split("_") if p)


def preguntar_opcion(pregunta, opciones):
    """Muestra un menú numerado y devuelve la opción elegida."""
    print(pregunta)
    for i, opcion in enumerate(opciones, start=1):
        print(f"  {i:2d}. {opcion}")
    while True:
        respuesta = input("Escribe el número y pulsa Enter: ").strip()
        if respuesta.isdigit() and 1 <= int(respuesta) <= len(opciones):
            return opciones[int(respuesta) - 1]
        print("  Número no válido, prueba otra vez.")


def teselar(u, v, longitudes, cx, cy, objetivo_m):
    """
    Reparte los tramos de un barrio en teselas contiguas de longitud parecida.
    Crece cada tesela desde el tramo más exterior que queda libre, añadiendo
    tramos conectados (que comparten un cruce), empezando por los más cercanos,
    hasta alcanzar la longitud objetivo. Devuelve el número de tesela de cada tramo.
    """
    n = len(longitudes)
    total = longitudes.sum()
    num_teselas = max(1, round(total / objetivo_m))

    por_nodo = defaultdict(list)
    for i in range(n):
        por_nodo[u[i]].append(i)
        por_nodo[v[i]].append(i)
    vecinos = [set() for _ in range(n)]
    for lista in por_nodo.values():
        for i in lista:
            vecinos[i].update(lista)
    for i in range(n):
        vecinos[i].discard(i)

    asignado = np.full(n, -1)
    restante = total

    for t in range(num_teselas):
        libres = np.where(asignado == -1)[0]
        if len(libres) == 0:
            break
        if t == num_teselas - 1:  # la última tesela se queda con lo que falte
            asignado[libres] = t
            break

        objetivo = restante / (num_teselas - t)
        mx, my = cx[libres].mean(), cy[libres].mean()
        semilla = libres[np.argmax((cx[libres] - mx) ** 2 + (cy[libres] - my) ** 2)]
        sx, sy = cx[semilla], cy[semilla]

        acumulado = 0.0
        cola = [(0.0, semilla)]
        en_cola = {semilla}
        while acumulado < objetivo:
            if not cola:
                libres = np.where(asignado == -1)[0]
                if len(libres) == 0:
                    break
                d = (cx[libres] - sx) ** 2 + (cy[libres] - sy) ** 2
                j = libres[np.argmin(d)]
                cola = [(d.min(), j)]
                en_cola.add(j)
            _, i = heapq.heappop(cola)
            if asignado[i] != -1:
                continue
            asignado[i] = t
            acumulado += longitudes[i]
            for j in vecinos[i]:
                if asignado[j] == -1 and j not in en_cola:
                    heapq.heappush(cola, ((cx[j] - sx) ** 2 + (cy[j] - sy) ** 2, j))
                    en_cola.add(j)
        restante -= acumulado

    return asignado


def orden_de_lectura(teselas, cx, cy, banda_m=500):
    """Renumera las teselas de norte a sur y de oeste a este, como se lee un texto."""
    df = pd.DataFrame({"t": teselas, "x": cx, "y": cy})
    centros = df.groupby("t")[["x", "y"]].mean()
    centros["banda"] = ((centros["y"].max() - centros["y"]) // banda_m).astype(int)
    orden = centros.sort_values(["banda", "x"]).index
    nuevo = {t: n + 1 for n, t in enumerate(orden)}
    return np.array([nuevo[t] for t in teselas])


# ---------------------------------------------------------------------------
# 1. Comprobar que existen los datos descargados
# ---------------------------------------------------------------------------
if not ARCHIVO_DATOS.exists():
    print(f"No se encuentran los datos en {ARCHIVO_DATOS}.")
    print("Ejecuta primero:  python descargar_datos_madrid.py")
    sys.exit(1)

if INFO_DESCARGA.exists():
    fecha_datos = INFO_DESCARGA.read_text(encoding="utf-8").splitlines()[1]
else:
    fecha_datos = "Descargados el " + datetime.fromtimestamp(
        ARCHIVO_DATOS.stat().st_mtime).strftime("%d/%m/%Y %H:%M")
print(f"Datos de OpenStreetMap: {fecha_datos.lower()}")

# ---------------------------------------------------------------------------
# 2. Elegir distrito y cargar sus datos
# ---------------------------------------------------------------------------
disponibles = gpd.read_file(ARCHIVO_DATOS, layer="distritos", ignore_geometry=True)["distrito"]
opciones = [d for d in DISTRITOS_MADRID if d in set(disponibles)]
distrito = preguntar_opcion("\n¿Para qué distrito de Madrid quieres crear las teselas?", opciones)
clave = nombre_archivo(distrito)
marca = datetime.now().strftime("%Y%m%d_%H_%M")
print(f"\nDistrito elegido: {distrito}")

filtro = "distrito = '" + distrito.replace("'", "''") + "'"
barrios = gpd.read_file(ARCHIVO_DATOS, layer="barrios", where=filtro)
tramos = gpd.read_file(ARCHIVO_DATOS, layer="tramos_base", where=filtro)
print(f"Barrios ({len(barrios)}): "
      + ", ".join(f"{b} ({c})" for b, c in zip(barrios["barrio"], barrios["codigo"])))

# ---------------------------------------------------------------------------
# 3. Dividir cada barrio en teselas
# ---------------------------------------------------------------------------
print(f"\nCreando teselas de unos {KM_ACERA_POR_TESELA} km de acera...")
tramos["metros_calle"] = tramos.geometry.length
tramos["tesela"] = ""
for codigo, grupo in tramos.groupby("codigo"):
    centro = grupo.geometry.centroid
    cx, cy = centro.x.to_numpy(), centro.y.to_numpy()
    numeros = teselar(
        grupo["u"].to_numpy(), grupo["v"].to_numpy(),
        grupo["metros_calle"].to_numpy(), cx, cy, OBJETIVO_M_CALLE,
    )
    numeros = orden_de_lectura(numeros, cx, cy)
    tramos.loc[grupo.index, "tesela"] = [f"{codigo}-{n:02d}" for n in numeros]

tramos["metros_calle"] = tramos["metros_calle"].round(0).astype(int)
tramos["metros_acera"] = tramos["metros_calle"] * 2

# ---------------------------------------------------------------------------
# 4. Tablas de resumen y Excel
# ---------------------------------------------------------------------------
calles_por_tesela = (
    tramos.groupby(["tesela", "barrio", "nombre"])
    .agg(metros_calle=("metros_calle", "sum"), metros_acera=("metros_acera", "sum"))
    .reset_index()
    .sort_values(["tesela", "metros_calle"], ascending=[True, False])
)

teselas = (
    tramos.groupby(["tesela", "barrio"])
    .agg(km_calle=("metros_calle", "sum"), km_acera=("metros_acera", "sum"))
    .reset_index()
)
teselas["km_calle"] = (teselas["km_calle"] / 1000).round(2)
teselas["km_acera"] = (teselas["km_acera"] / 1000).round(2)
teselas["num_calles"] = teselas["tesela"].map(calles_por_tesela.groupby("tesela").size())
teselas["calles"] = teselas["tesela"].map(
    calles_por_tesela.groupby("tesela")["nombre"].apply(lambda s: ", ".join(s)))
teselas = teselas.sort_values("tesela")

por_barrio = (
    teselas.groupby("barrio")
    .agg(km_calle=("km_calle", "sum"), km_acera=("km_acera", "sum"), num_teselas=("tesela", "count"))
    .reset_index()
    .sort_values("barrio")
)

todas_las_calles = (
    tramos.groupby("nombre")
    .agg(metros_calle=("metros_calle", "sum"), metros_acera=("metros_acera", "sum"))
    .reset_index()
    .sort_values("metros_calle", ascending=False)
)

salida_excel = CARPETA / f"teselas_{clave}_{marca}.xlsx"
with pd.ExcelWriter(salida_excel) as excel:
    teselas.to_excel(excel, sheet_name="Teselas", index=False)
    calles_por_tesela.to_excel(excel, sheet_name="Calles por tesela", index=False)
    por_barrio.to_excel(excel, sheet_name="Por barrio", index=False)
    todas_las_calles.to_excel(excel, sheet_name="Todas las calles", index=False)

# ---------------------------------------------------------------------------
# 5. Mapa interactivo
# ---------------------------------------------------------------------------
lista_teselas = sorted(tramos["tesela"].unique())
color_tesela = {t: PALETA[(i * 5) % len(PALETA)] for i, t in enumerate(lista_teselas)}
tramos["color"] = tramos["tesela"].map(color_tesela)

mapa = barrios.explore(
    color="black",
    style_kwds={"fill": False, "weight": 3},
    tooltip="barrio",
    name="Límites de barrios",
    tiles="Esri.WorldGrayCanvas",
)

# Calles pintadas con el color de su tesela
tramos_mapa = tramos[["tesela", "nombre", "barrio", "metros_calle", "metros_acera", "color", "geometry"]]
folium.GeoJson(
    tramos_mapa.to_crs(epsg=4326).to_json(),
    name="Calles por tesela",
    style_function=lambda f: {"color": f["properties"]["color"], "weight": 5, "opacity": 0.9},
    highlight_function=lambda f: {"weight": 9, "opacity": 1},
    tooltip=folium.GeoJsonTooltip(
        fields=["tesela", "nombre", "barrio", "metros_calle", "metros_acera"],
        aliases=["Tesela", "Calle", "Barrio", "Metros de calle", "Metros de acera"],
    ),
).add_to(mapa)

# Etiquetas con el código de cada tesela, colocadas sobre una de sus calles
teselas_geo = tramos.dissolve(by="tesela", as_index=False)[["tesela", "geometry"]]
teselas_geo["geometry"] = [nearest_points(g, g.centroid)[0] for g in teselas_geo.geometry]
teselas_geo = teselas_geo.to_crs(epsg=4326)
capa_teselas = folium.FeatureGroup(name="Códigos de teselas")
for _, fila in teselas_geo.iterrows():
    folium.Marker(
        location=[fila.geometry.y, fila.geometry.x],
        tooltip=fila["tesela"],
        icon=folium.DivIcon(
            icon_size=(60, 18),
            icon_anchor=(30, 9),
            html=(
                '<div style="text-align:center; font-size:11px; font-weight:bold; '
                f'color:#fff; background:{color_tesela[fila["tesela"]]}; '
                'border:1px solid #fff; border-radius:4px; padding:1px 3px; '
                'box-shadow:0 0 2px #000;">'
                f'{fila["tesela"]}</div>'
            ),
        ),
    ).add_to(capa_teselas)
capa_teselas.add_to(mapa)

# Etiquetas con el nombre de cada barrio (desactivadas al abrir el mapa)
capa_barrios = folium.FeatureGroup(name="Nombres de barrios", show=False)
puntos = barrios.copy()
puntos["geometry"] = barrios.representative_point()
puntos = puntos.to_crs(epsg=4326)
for _, fila in puntos.iterrows():
    folium.Marker(
        location=[fila.geometry.y, fila.geometry.x],
        icon=folium.DivIcon(
            icon_size=(160, 20),
            icon_anchor=(80, 10),
            html=(
                '<div style="text-align:center; font-size:14px; font-weight:bold; '
                'color:#222; white-space:nowrap; '
                'text-shadow: 1px 1px 2px #fff, -1px -1px 2px #fff, 1px -1px 2px #fff, -1px 1px 2px #fff;">'
                f'{fila["barrio"]}</div>'
            ),
        ),
    ).add_to(capa_barrios)
capa_barrios.add_to(mapa)

folium.LayerControl().add_to(mapa)
salida_mapa = CARPETA / f"mapa_{clave}_{marca}.html"
mapa.save(salida_mapa)

# ---------------------------------------------------------------------------
# 6. Capas para QGIS
# ---------------------------------------------------------------------------
salida_gpkg = CARPETA / f"teselas_{clave}_{marca}.gpkg"
tramos.drop(columns=["color"]).to_file(salida_gpkg, layer="tramos", driver="GPKG")
tramos.dissolve(by="tesela", as_index=False)[["tesela", "barrio", "geometry"]].to_file(
    salida_gpkg, layer="teselas", driver="GPKG")
barrios.to_file(salida_gpkg, layer="barrios", driver="GPKG")

# ---------------------------------------------------------------------------
# 7. Resultados
# ---------------------------------------------------------------------------
print(f"\nKilómetros de calle en {distrito}: {teselas['km_calle'].sum():.2f} km "
      f"({teselas['km_acera'].sum():.2f} km de acera)")
print(f"Teselas creadas: {len(teselas)} "
      f"(entre {teselas['km_acera'].min():.2f} y {teselas['km_acera'].max():.2f} km de acera)")
print("\nPor barrio:")
for _, fila in por_barrio.iterrows():
    print(f"  {fila['barrio']:<25} {fila['km_acera']:7.2f} km de acera  {fila['num_teselas']:3d} teselas")
print(f"\nExcel: {salida_excel.name}")
print(f"Mapa:  {salida_mapa.name}")
print(f"Capas: {salida_gpkg.name}")
