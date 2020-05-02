import os
from qgis.core import QgsProcessingUtils, QgsRasterLayer, QgsProject


def configure(appResources, appContext):
    pass


def addLayer(filePath, baseName, provider="gdal"):
    layer = QgsRasterLayer(filePath, baseName, "gdal")

    if not layer.isValid():
        raise Exception("Error!")

    return layer


def execute(appResources, appContext):
    print(os.path)

    appResources.bibliotecas.logger.update_progress(step_current=1, step_maximum=5)
    raw_folder = f"{appContext.execution.raw_temp_folder}/dtm"
    raw_file = f"{raw_folder}/dtm.zip"
    appResources.bibliotecas.file_management.create_dirs(raw_folder)

    appResources.bibliotecas.logger.plugin_log(f"raw_file: {raw_file}")
    appResources.bibliotecas.logger.plugin_log(
        f"https://www.wien.gv.at/ma41datenviewer/downloads/ma41/geodaten/dgm_tif/35_4_dgm_tif.zip")

    appResources.bibliotecas.logger.update_progress(step_description="Downloading DTM...")
    appResources.bibliotecas.internet.download_file(
        # 'https://www.wien.gv.at/ma41datenviewer/downloads/ma41/geodaten/dgm_tif/35_4_dgm_tif.zip',
        'https://ttc-hosang.s3.amazonaws.com/test/34_4_dom_tif.zip',
        raw_file)

    # NORMALIZING
    appResources.bibliotecas.logger.update_progress(step_description="Uncompromising...")
    appResources.bibliotecas.file_management.unzip_file(raw_file, f"{appContext.execution.raw_temp_folder}/dtm/")

    normalized_folder = f"{appContext.execution.normalized_temp_folder}/dtm"
    normalized_file = appContext.user_parameters.dtm_output
    appResources.bibliotecas.file_management.create_dirs(normalized_folder)
    appResources.bibliotecas.logger.update_progress(step_description="Moving files...")
    appResources.bibliotecas.file_management.move_file(f"{appContext.execution.raw_temp_folder}/dtm/34_4_dom.tif",
                                                       normalized_file)

    appContext.steps.gis.dtm.input_file = normalized_file

    appResources.bibliotecas.logger.update_progress(step_current=1, step_maximum=1)
    appResources.bibliotecas.logger.plugin_log("Done!")
