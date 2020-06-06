import os, processing
from qgis.core import QgsProcessingUtils, QgsRasterLayer, QgsProject


def configure(appResources, appContext):
    pass


def execute(appResources, appContext):
    print(os.path)

    appResources.bibliotecas.logger.update_progress(step_current=1, step_maximum=5)
    raw_folder = f"{appContext.execution.raw_temp_folder}/footprint"
    appResources.bibliotecas.file_management.create_dirs(raw_folder)

    appResources.bibliotecas.logger.update_progress(step_description="Downloading DTM...")

    zip_file_path = f"{raw_folder}/footprint.zip"
    uncompressed_file_path = f"{raw_folder}"
    appResources.bibliotecas.internet.download_file("http://download.geofabrik.de/europe/austria-latest-free.shp.zip", zip_file_path )

    # NORMALIZING
    appResources.bibliotecas.logger.update_progress(step_description="Uncompromising...")
    appResources.bibliotecas.file_management.unzip_file_list(zip_file_path, uncompressed_file_path)

    result = f"{uncompressed_file_path}/gis_osm_buildings_a_free_1.shp"


    appContext.update_layer(
        appContext,
        result,
        "dtm",
        "gdal",
        31256
    )
    # QgsProject.instance().addMapLayer(appContext.layers.dtm.layer)

    appResources.bibliotecas.logger.update_progress(step_current=1, step_maximum=1)
    appResources.bibliotecas.logger.plugin_log("Done!")
