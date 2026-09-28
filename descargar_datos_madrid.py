"""
Descarga de OpenStreetMap todo lo necesario para crear teselas en Madrid capital
y lo guarda en datos_madrid/madrid_osm.gpkg:
  - distritos: límites de los 21 distritos
  - barrios: límites de los barrios, con su distrito y un código de tres letras
  - tramos_base: calles divididas en tramos de cruce a cruce, cortadas por barrio

Solo hace falta ejecutarlo una vez, o cuando se quieran actualizar los datos.
"""
import time
import unicodedata
from datetime import datetime
from pathlib import Path

import geopandas as gpd
import osmnx as ox
import pandas as pd
import requests

CARPETA = Path(__file__).parent
CARPETA_DATOS = CARPETA / "datos_madrid"
ARCHIVO_DATOS = CARPETA_DATOS / "madrid_osm.gpkg"
CRS_METROS = 25830  # ETRS89 / UTM 30N, mide en metros

DISTRITOS_MADRID = [
    "Centro", "Arganzuela", "Retiro", "Salamanca", "Chamartín", "Tetuán",
    "Chamberí", "Fuencarral-El Pardo", "Moncloa-Aravaca", "Latina",
    "Carabanchel", "Usera", "Puente de Vallecas", "Moratalaz", "Ciudad Lineal",
    "Hortaleza", "Villaverde", "Villa de Vallecas", "Vicálvaro",
    "San Blas-Canillejas", "Barajas",
]

# Tipos de vía que nos interesan para el censo de arbolado
# (se excluyen autopistas, enlaces, caminos peatonales sueltos y vías de servicio)
TIPOS_CALLE = [
    "primary", "secondary", "tertiary", "residential",
    "living_street", "pedestrian", "unclassified",
]

# Servidores de Overpass (OpenStreetMap). Si uno falla, se prueba el siguiente.
SERVIDORES_OVERPASS = [
    "https://overpass-api.de/api",
    "https://overpass.kumi.systems/api",
    "https://overpass.private.coffee/api",
]
INTENTOS_POR_SERVIDOR = 2
ESPERA_SEGUNDOS = 30

# La consulta de calles de todo Madrid es grande: damos más tiempo al servidor
ox.settings.requests_timeout = 900
ox.settings.use_cache = True


def sin_tildes(texto):
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()


def normalizar(texto):
    """Para comparar nombres: sin tildes, minúsculas, solo letras y números."""
    return "".join(c for c in sin_tildes(str(texto)).lower() if c.isalnum())


def texto_de(valor):
    """OSM a veces guarda varios valores en una lista; los une en un texto."""
    if isinstance(valor, list):
        valores = [str(v) for v in dict.fromkeys(valor) if pd.notna(v)]
        return " / ".join(valores) if valores else None
    return valor


def codigo_barrio(nombre, usados):
    """Código de tres letras sin tildes: Acacias -> ACA. Evita repetidos."""
    letras = "".join(c for c in sin_tildes(nombre).upper() if c.isalpha())
    codigo = letras[:3]
    extra = 3
    while codigo in usados and extra < len(letras):
        codigo = letras[:2] + letras[extra]
        extra += 1
    usados.add(codigo)
    return codigo


def con_reintentos(funcion, *args, **kwargs):
    """Si el servidor corta la conexión, espera y reintenta, pasando a otros servidores."""
    for servidor in SERVIDORES_OVERPASS:
        ox.settings.overpass_url = servidor        # osmnx 2.x
        ox.settings.overpass_endpoint = servidor   # osmnx 1.x
        ox.settings.overpass_rate_limit = servidor == SERVIDORES_OVERPASS[0]
        for intento in range(1, INTENTOS_POR_SERVIDOR + 1):
            try:
                return funcion(*args, **kwargs)
            except (requests.exceptions.RequestException, ConnectionError) as error:
                print(f"  El servidor {servidor} ha fallado (intento {intento}): {type(error).__name__}")
                print(f"  Esperando {ESPERA_SEGUNDOS} segundos antes de reintentar...")
                time.sleep(ESPERA_SEGUNDOS)
    raise RuntimeError(
        "No se ha podido descargar de ningún servidor de OpenStreetMap. "
        "Comprueba la conexión (o desactiva la VPN si usas una) y prueba más tarde."
    )


inicio = time.time()
CARPETA_DATOS.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Distritos (en OSM, los distritos de Madrid son admin_level 9)
# ---------------------------------------------------------------------------
print("1/3 Descargando límites de los distritos...")
distritos = con_reintentos(
    ox.features_from_place, "Madrid, Comunidad de Madrid, España", tags={"admin_level": "9"})
distritos = distritos[distritos.geom_type.isin(["Polygon", "MultiPolygon"])]
distritos = distritos[distritos["name"].notna()]

nombre_oficial = {normalizar(d): d for d in DISTRITOS_MADRID}
distritos["distrito"] = distritos["name"].map(lambda n: nombre_oficial.get(normalizar(n)))
distritos = (distritos[distritos["distrito"].notna()]
             .drop_duplicates("distrito")[["distrito", "geometry"]]
             .reset_index(drop=True))
faltan = sorted(set(DISTRITOS_MADRID) - set(distritos["distrito"]))
print(f"    Distritos encontrados: {len(distritos)} de {len(DISTRITOS_MADRID)}")
if faltan:
    print(f"    AVISO: no se han encontrado: {', '.join(faltan)}")

madrid_gps = distritos.geometry.union_all()      # todo el municipio, en coordenadas GPS
distritos = distritos.to_crs(epsg=CRS_METROS)

# ---------------------------------------------------------------------------
# 2. Barrios (en OSM, los barrios de Madrid son admin_level 10)
# ---------------------------------------------------------------------------
print("2/3 Descargando barrios...")
barrios = con_reintentos(ox.features_from_polygon, madrid_gps, tags={"admin_level": "10"})
barrios = barrios[barrios.geom_type.isin(["Polygon", "MultiPolygon"])]
barrios = barrios[barrios["name"].notna()].to_crs(epsg=CRS_METROS)
barrios = barrios[["name", "geometry"]].rename(columns={"name": "barrio"}).reset_index(drop=True)

# Asignar cada barrio a su distrito (por un punto interior del barrio)
puntos = barrios.copy()
puntos["geometry"] = barrios.representative_point()
puntos = gpd.sjoin(puntos, distritos, how="inner", predicate="within")
barrios = barrios.loc[puntos.index].copy()
barrios["distrito"] = puntos["distrito"]
barrios = barrios.drop_duplicates(["distrito", "barrio"])
barrios = barrios.sort_values(["distrito", "barrio"]).reset_index(drop=True)

# Códigos de barrio únicos dentro de cada distrito
codigos = []
for _, grupo in barrios.groupby("distrito", sort=False):
    usados = set()
    codigos += [codigo_barrio(b, usados) for b in grupo["barrio"]]
barrios["codigo"] = codigos
barrios = barrios[["distrito", "barrio", "codigo", "geometry"]]
print(f"    Barrios encontrados: {len(barrios)}")

# ---------------------------------------------------------------------------
# 3. Calles de todo Madrid, divididas en tramos de cruce a cruce
# ---------------------------------------------------------------------------
print("3/3 Descargando calles de todo Madrid (puede tardar varios minutos)...")
filtro = (
    f'["highway"~"^({"|".join(TIPOS_CALLE)})$"]'
    '["tunnel"!="yes"]["area"!="yes"]'
)
red = con_reintentos(
    ox.graph_from_polygon,
    madrid_gps, custom_filter=filtro,
    simplify=True, retain_all=True, truncate_by_edge=True,
)
# Red sin sentidos de circulación, para no contar dos veces las calles de doble sentido
try:
    red = ox.convert.to_undirected(red)
except AttributeError:  # versiones antiguas de osmnx
    red = ox.utils_graph.get_undirected(red)

print("    Procesando tramos...")
tramos = ox.graph_to_gdfs(red, nodes=False).reset_index().to_crs(epsg=CRS_METROS)
if "name" in tramos.columns:
    tramos["nombre"] = tramos["name"].apply(texto_de).fillna("Sin nombre")
else:
    tramos["nombre"] = "Sin nombre"
tramos["tipo"] = tramos["highway"].apply(texto_de)
tramos = tramos[["u", "v", "nombre", "tipo", "geometry"]]

print("    Cortando tramos por barrio...")
tramos = gpd.overlay(tramos, barrios, how="intersection", keep_geom_type=True)
tramos = tramos[tramos.geometry.length > 1].reset_index(drop=True)
tramos = tramos[["distrito", "barrio", "codigo", "u", "v", "nombre", "tipo", "geometry"]]
print(f"    Tramos: {len(tramos)}")

# ---------------------------------------------------------------------------
# 4. Guardar (primero en un archivo temporal, para no perder los datos
#    anteriores si algo falla a mitad)
# ---------------------------------------------------------------------------
print("Guardando datos...")
temporal = CARPETA_DATOS / "madrid_osm_temporal.gpkg"
if temporal.exists():
    temporal.unlink()
distritos.to_file(temporal, layer="distritos", driver="GPKG")
barrios.to_file(temporal, layer="barrios", driver="GPKG")
tramos.to_file(temporal, layer="tramos_base", driver="GPKG")
temporal.replace(ARCHIVO_DATOS)

fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
(CARPETA_DATOS / "info_descarga.txt").write_text(
    f"Datos de OpenStreetMap (© colaboradores de OpenStreetMap, licencia ODbL)\n"
    f"Descargados el {fecha}\n"
    f"Distritos: {len(distritos)}\n"
    f"Barrios: {len(barrios)}\n"
    f"Tramos de calle: {len(tramos)}\n"
    f"Kilómetros de calle: {tramos.geometry.length.sum() / 1000:.1f}\n",
    encoding="utf-8",
)

tamano_mb = ARCHIVO_DATOS.stat().st_size / 1_000_000
minutos = (time.time() - inicio) / 60
print(f"\nListo en {minutos:.1f} minutos.")
print(f"Datos guardados en {ARCHIVO_DATOS} ({tamano_mb:.0f} MB)")
print(f"Kilómetros de calle en Madrid: {tramos.geometry.length.sum() / 1000:.0f} km")
print("\nResumen por distrito:")
resumen = tramos.assign(km=tramos.geometry.length / 1000).groupby("distrito")["km"].sum()
num_barrios = barrios.groupby("distrito").size()
for d in DISTRITOS_MADRID:
    if d in resumen.index:
        print(f"  {d:<22} {num_barrios.get(d, 0):3d} barrios  {resumen[d]:7.1f} km de calle")
