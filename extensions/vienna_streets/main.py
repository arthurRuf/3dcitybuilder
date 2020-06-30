import os, processing
from qgis.core import QgsProcessingUtils, QgsRasterLayer, QgsProject


def configure(appResources, appContext):
    pass


def execute(appResources, appContext):
    print(os.path)

    appResources.bibliotecas.logger.update_progress(step_current=1, step_maximum=5)
    raw_folder = f"{appContext.execution.raw_temp_folder}/water"
    appResources.bibliotecas.file_management.create_dirs(raw_folder)

    appResources.bibliotecas.logger.update_progress(step_description="Downloading Water...")

    zip_file_path = f"{raw_folder}/water.zip"

    # zip_file_path = f"/private/var/folders/6k/gwc2zlsd7tl7ph27q44pcm0w0000gn/T/processing_c9b8c5d3c16e439fb67a0bbb40d8904e/citygen/W6FSUo5EqeZuqURU/raw/water/water.zip"

    zip_file_path = f"{appContext.execution.raw_temp_folder}/downolads/osm.zip"
    # zip_file_path = f"/private/var/folders/6k/gwc2zlsd7tl7ph27q44pcm0w0000gn/T/processing_c9b8c5d3c16e439fb67a0bbb40d8904e/citygen/W6FSUo5EqeZuqURU/raw/tree/tree.zip"
    uncompressed_file_path = f"{raw_folder}"

    if os.path.exists(zip_file_path) == False:
        appResources.bibliotecas.internet.download_file(
            "http://download.geofabrik.de/europe/austria-latest-free.shp.zip",
            zip_file_path)

    # NORMALIZING
    appResources.bibliotecas.logger.update_progress(step_description="Uncompressing...")
    appResources.bibliotecas.file_management.unzip_file(zip_file_path, uncompressed_file_path)

    result = f"{uncompressed_file_path}/gis_osm_water_a_free_1.shp"

    appContext.update_layer(
        appContext,
        path=result,
        name="water",
        data_provider="ogr",
        type="vector",
        crs=4626
    )

    appResources.bibliotecas.logger.update_progress(step_current=1, step_maximum=1)
    appResources.bibliotecas.logger.plugin_log("Done!")
