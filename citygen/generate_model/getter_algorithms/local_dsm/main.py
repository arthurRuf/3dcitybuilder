import time, shutil, logging, os, sys, requests
from ...bibliotecas import progress_bar, inputa, internet, plugin_management



def configure(appResources, appContext):
    pass


def execute(appResources, appContext):
    logging.info("Getting file...")

    file_destination = f"{appResources.constants.temp_raw_folder}/dsm/dsm.zip"
    url = 'https://www.wien.gv.at/ma41datenviewer/downloads/ma41/geodaten/dom_tif/34_4_dom_tif.zip'
    internet.download_file(url, file_destination)

    # NORMALIZING
    plugin_management.unzip(file_destination, f"{appResources.constants.temp_raw_folder}/dsm/")

    normalized_file = f"{appResources.constants.temp_normalizer_folder}/dsm/dsm.tif"
    plugin_management.copy(f"{appResources.constants.temp_raw_folder}/dsm/34_4_dom.tif", normalized_file)

    appContext.steps.gis.dsm.input_file = normalized_file

    logging.info("Done!")
