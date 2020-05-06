import os, processing
from qgis.core import QgsProcessingUtils, QgsRasterLayer, QgsProject


def configure(appResources, appContext):
    pass


def execute(appResources, appContext):
    print(os.path)

    appResources.bibliotecas.logger.update_progress(step_current=1, step_maximum=5)
    raw_folder = f"{appContext.execution.raw_temp_folder}/dtm"
    raw_file = f"{raw_folder}/dtm.zip"
    appResources.bibliotecas.file_management.create_dirs(raw_folder)

    appResources.bibliotecas.logger.plugin_log(f"raw_file: {raw_file}")

    appResources.bibliotecas.logger.update_progress(step_description="Downloading DTM...")
    appResources.bibliotecas.internet.download_file(
        # 'https://www.wien.gv.at/ma41datenviewer/downloads/ma41/geodaten/dgm_tif/35_4_dgm_tif.zip',
        "https://ttc-hosang.s3.amazonaws.com/test/35_4_dgm_tif.zip",
        raw_file)

    # NORMALIZING
    appResources.bibliotecas.logger.update_progress(step_description="Uncompromising...")
    appResources.bibliotecas.file_management.unzip_file(raw_file, f"{appContext.execution.raw_temp_folder}/dtm/")

    normalized_folder = f"{appContext.execution.normalized_temp_folder}/dtm"
    normalized_file = f"{appContext.execution.raw_temp_folder}/dtm/dtm_ready.tif"
    appResources.bibliotecas.file_management.create_dirs(normalized_folder)
    appResources.bibliotecas.logger.update_progress(step_description="Moving files...")

    postgis_id = QgsProject.instance().crs().postgisSrid()
    processing.run("qgis:reprojectlayer", f"{appContext.execution.raw_temp_folder}/dtm/35_4_dgm.tif",
                      f"EPSG:{postgis_id}", normalized_file)

    # appResources.bibliotecas.file_management.move_file(f"{appContext.execution.raw_temp_folder}/dtm/35_4_dgm.tif",
    #                                                    normalized_file)


    appContext.update_layer(
        appContext,
        normalized_file,
        "dtm",
        "gdal"
    )

    appResources.bibliotecas.logger.update_progress(step_current=1, step_maximum=1)
    appResources.bibliotecas.logger.plugin_log("Done!")
