import os, processing
from qgis.core import QgsProcessingUtils, QgsRasterLayer, QgsProject


def configure(appResources, appContext):
    pass


def execute(appResources, appContext):
    print(os.path)

    appResources.bibliotecas.logger.update_progress(step_current=1, step_maximum=5)
    raw_folder = f'{appContext.execution.raw_temp_folder}/street'
    result_file = f'{raw_folder}/street.shp'

    appResources.bibliotecas.logger.update_progress(step_description="Downloading Street Network...")

    try:
        import osmnx as ox
        import geopandas as gpd
    except:
        appResources.bibliotecas.logger.plugin_log("Unable to Download Street Networks")
        appResources.bibliotecas.logger.plugin_log(
            "You need to install geopandas and osmnx python library into QGIS Python in order to use this functionality")

    ox.config(log_console=True, use_cache=True)

    calif = gpd.read_file(
        '/Volumes/TarDisk/ruf/workspace/ttc/test/osmnx-examples/notebooks/input_data/ZillowNeighborhoods-CA/ZillowNeighborhoods-CA.shp')
    # appContext.user_parameters.clip_layer.dataProvider().dataSourceUri()

    mission_district = calif
    polygon = mission_district['geometry'].iloc[0]

    G = ox.graph_from_polygon(polygon, network_type='drive_service')

    ox.save_graph_shapefile(G, folder=raw_folder, filename='drive')

    appResources.bibliotecas.copy_file(f'{raw_folder}/drive/edges/edges.shp', result_file)
    appResources.bibliotecas.copy_file(f'{raw_folder}/drive/edges/edges.cpg', f'{raw_folder}/street.cpg')
    appResources.bibliotecas.copy_file(f'{raw_folder}/drive/edges/edges.dbf', f'{raw_folder}/street.dbf')
    appResources.bibliotecas.copy_file(f'{raw_folder}/drive/edges/edges.prj', f'{raw_folder}/street.prj')
    appResources.bibliotecas.copy_file(f'{raw_folder}/drive/edges/edges.shp', f'{raw_folder}/street.shp')
    appResources.bibliotecas.copy_file(f'{raw_folder}/drive/edges/edges.shx', f'{raw_folder}/street.shx')


    appContext.update_layer(
        appContext,
        result_file,
        "street",
        "ogr",
        "vector",
        4326
    )
    # QgsProject.instance().addMapLayer(appContext.layers.dtm.layer)

    appResources.bibliotecas.logger.update_progress(step_current=1, step_maximum=1)
    appResources.bibliotecas.logger.plugin_log("Done!")
