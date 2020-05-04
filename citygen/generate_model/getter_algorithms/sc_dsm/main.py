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
    appResources.bibliotecas.logger.plugin_log(
        f"https://www.wien.gv.at/ma41datenviewer/downloads/ma41/geodaten/dom_tif/dsmsc_dtm.zip")

    appResources.bibliotecas.logger.update_progress(step_description="Downloading DSM...")
    appResources.bibliotecas.internet.download_file(
        # 'https://www.wien.gv.at/ma41datenviewer/downloads/ma41/geodaten/dom_tif/34_4_dom_tif.zip',
        'https://ttc-hosang.s3.amazonaws.com/test/sc_dsm.zip',
        raw_file)

    # NORMALIZING
    appResources.bibliotecas.logger.update_progress(step_description="Uncompromising...")
    appResources.bibliotecas.file_management.unzip_file(raw_file, f"{appContext.execution.raw_temp_folder}/dsm/")

    normalized_folder = f"{appContext.execution.normalized_temp_folder}/dsm"
    normalized_file = f"{appContext.execution.raw_temp_folder}/dsm/dsm_ready.tif"
    appResources.bibliotecas.file_management.create_dirs(normalized_folder)
    appResources.bibliotecas.logger.update_progress(step_description="Moving files...")

    # postgis_id = QgsProject.instance().crs().postgisSrid()
    # processing.run("qgis:reprojectlayer", f"{appContext.execution.raw_temp_folder}/dsm/dsm.tif", f"EPSG:{postgis_id}", normalized_file)

    # appResources.bibliotecas.file_management.move_file(f"{appContext.execution.raw_temp_folder}/dsm/34_4_dom.tif",
    #                                               normalized_file)

    appContext.update_layer(
        appContext,
        f"{appContext.execution.raw_temp_folder}/dsm/dsm.tif",
        "dsm",
        "gdal"
    )

    appResources.bibliotecas.logger.update_progress(step_current=1, step_maximum=1)
    appResources.bibliotecas.logger.plugin_log("Done!")
