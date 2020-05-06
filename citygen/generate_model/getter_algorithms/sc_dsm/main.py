import os
import processing
from qgis.core import QgsProcessingUtils, QgsRasterLayer, QgsProject

def configure(appResources, appContext):
    pass


def execute(appResources, appContext):
    print(os.path)

    appResources.bibliotecas.logger.update_progress(step_current=1, step_maximum=100)
    raw_folder = f"{appContext.execution.raw_temp_folder}/dsm"
    raw_file = f"{raw_folder}/dsm.zip"
    appResources.bibliotecas.file_management.create_dirs(raw_folder)

    appResources.bibliotecas.logger.plugin_log(f"raw_file: {raw_file}")

    appResources.bibliotecas.logger.update_progress(step_description="Downloading DSM...")
    appResources.bibliotecas.internet.download_file(
        # 'https://www.wien.gv.at/ma41datenviewer/downloads/ma41/geodaten/dom_tif/34_4_dom_tif.zip',
        'https://ttc-hosang.s3.amazonaws.com/test/sc_dsm.zip',
        raw_file)

    # NORMALIZING
    appResources.bibliotecas.logger.update_progress(step_description="Uncompromising...")
    appResources.bibliotecas.file_management.unzip_file(raw_file, f"{appContext.execution.raw_temp_folder}/dsm/")
    result = f"{appContext.execution.raw_temp_folder}/dsm/dsm.tif"

    appContext.update_layer(
        appContext,
        result,
        "dsm",
        "gdal"
    )

    appResources.bibliotecas.logger.update_progress(step_current=1, step_maximum=1)
    appResources.bibliotecas.logger.plugin_log("Done!")
