import sys, os
from .bibliotecas import logger
# from .generate_model.appContext import appContext
# from .generate_model.bibliotecas import plugin_management, progress_bar

from .crawler import crawler_management
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


def start():
    logger.plugin_log("Getting files...")
    # crawler_management.execute_crawlers()

    gis.generate_3d_model()
    logger.plugin_log("Process complete without errors!")
