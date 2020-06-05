import sys, os, random, string
from qgis.core import QgsProcessingUtils, QgsRasterLayer, QgsProject
from .bibliotecas import logger, file_management, install_python_package
from .appCtx import appContext

from .getters import getters_management
from .normalizer import normalizer
from .gis import gis


# def cleanup_temp():
#     os.rmdir("temp")
#
#     os.mkdir("temp")
#
#     os.mkdir("temp/raw")
#     os.mkdir("temp/raw/ortho")
#     os.mkdir("temp/raw/dtm")
#     os.mkdir("temp/raw/dsm")
#
#     os.mkdir("temp/normalized")
#     os.mkdir("temp/normalized/ortho")
#     os.mkdir("temp/normalized/dtm")
#     os.mkdir("temp/normalized/dsm")

def appContext_setup():
    logger.update_progress(step_current=0, step_description="Loading...", step_maximum=27,
                           overall_current=1, overall_description="Initialization", overall_maximum=12)

    appContext.execution.id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    logger.plugin_log("")
    logger.plugin_log("==============================================")
    logger.plugin_log(f"EXECUTION ID: {appContext.execution.id}")
    logger.plugin_log("==============================================")
    logger.plugin_log("")

    # temp_folder = QgsProcessingUtils.tempFolder()
    # appContext.execution.temp_folder = f"{temp_folder}"
    # appContext.execution.raw_temp_folder = f"{appContext.execution.temp_folder}/raw"
    # appContext.execution.normalized_temp_folder = f"{appContext.execution.temp_folder}/normalized"

    appContext.execution.id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    temp_folder = os.path.join(QgsProcessingUtils.tempFolder(), "citygen", appContext.execution.id)
    appContext.execution.temp_folder = f"{temp_folder}"
    appContext.execution.raw_temp_folder = os.path.join(appContext.execution.temp_folder, "raw")
    appContext.execution.normalized_temp_folder = os.path.join(appContext.execution.temp_folder, "normalized")

    file_management.create_temp_dirs(appContext.execution.raw_temp_folder)
    file_management.create_temp_dirs(appContext.execution.normalized_temp_folder)

    # if appContext.user_parameters.ortho_output == "" and \
    #         appContext.user_parameters.ortho_getter.format == "file":
    #     appContext.user_parameters.ortho_output = f"{appContext.execution.normalized_temp_folder}/ortho.tif"
    # if appContext.user_parameters.dtm_output == "" and \
    #         appContext.user_parameters.dtm_getter.format == "file":
    #     appContext.user_parameters.dtm_output = f"{appContext.execution.normalized_temp_folder}/dtm.tif"
    # if appContext.user_parameters.dsm_output == "" and \
    #         appContext.user_parameters.dsm_getter.format == "file":
    #     appContext.user_parameters.dsm_output = f"{appContext.execution.normalized_temp_folder}/dsm.tif"
    # if appContext.user_parameters.footprint_output == "" and \
    #         (appContext.user_parameters.footprint_getter.format == "file" or
    #          appContext.user_parameters.footprint_getter.format == "algorithm"
    #         ):
    #     appContext.user_parameters.footprint_output = f"{appContext.execution.normalized_temp_folder}/footprint.shp"

    logger.plugin_log(f"Plugin Temp folder: {appContext.execution.temp_folder}")

    logger.update_progress(step_current=100, overall_current=2)

    if appContext.user_parameters.clip_layer == "viewport":
        appContext.user_parameters.clip_layer = gis.create_viewport_polygon()

    install_python_package.install_package("geopandas")
    install_python_package.install_package("numpy")
    install_python_package.install_package("osmnx")


def start():
    logger.plugin_log("OUTPUT LOCATION: " + appContext.user_parameters.ortho_output)

    appContext_setup()

    logger.plugin_log("Getting files...")
    getters_management.execute_getters()

    gis.generate_3d_model()

    logger.plugin_log("Process complete without errors!")

    logger.plugin_log("OUTPUT LOCATION: " + appContext.user_parameters.ortho_output)

    logger.update_progress(step_current=1, step_description="Done!", step_maximum=1,
                           overall_current=1, overall_description="", overall_maximum=1)
