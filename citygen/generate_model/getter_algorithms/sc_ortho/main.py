import os, processing
from qgis.core import QgsProcessingUtils, QgsRasterLayer, QgsProject


def configure(appResources, appContext):
    pass


def execute(appResources, appContext):
    print(os.path)

    appResources.bibliotecas.logger.update_progress(step_current=1, step_maximum=5)
    raw_folder = f"{appContext.execution.raw_temp_folder}/ortho"
    raw_file = f"{raw_folder}/ortho.zip"
    appResources.bibliotecas.file_management.create_dirs(raw_folder)

    appResources.bibliotecas.logger.plugin_log(f"raw_file: {raw_file}")

    appResources.bibliotecas.logger.update_progress(step_description="Downloading DTM...")
    appResources.bibliotecas.internet.download_file(
        # 'https://www.wien.gv.at/ma41datenviewer/downloads/ma41/geodaten/dgm_tif/35_4_dgm_tif.zip',
        "https://ttc-hosang.s3.amazonaws.com/test/sc_ortho.zip",
        raw_file)

    # NORMALIZING
    appResources.bibliotecas.logger.update_progress(step_description="Uncompromising...")
    appResources.bibliotecas.file_management.unzip_file(raw_file, f"{appContext.execution.raw_temp_folder}/ortho/")
    result = f"{appContext.execution.raw_temp_folder}/ortho/ortho.tif"

    appContext.update_layer(
        appContext,
        result,
        "ortho",
        "gdal"
    )

    appResources.bibliotecas.logger.update_progress(step_current=1, step_maximum=1)
    appResources.bibliotecas.logger.plugin_log("Done!")
