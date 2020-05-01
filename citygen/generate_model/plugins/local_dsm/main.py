import time, shutil, logging, os, sys, requests
from ...bibliotecas import progress_bar, inputa, getter, file_menagement



def configure(appResources, appContext):
    pass


def execute(appResources, appContext):
    logging.info("Getting file...")

    file_destination = f"{appResources.constants.temp_raw_folder}/dsm/dsm.zip"
    url = 'https://www.wien.gv.at/ma41datenviewer/downloads/ma41/geodaten/dom_tif/34_4_dom_tif.zip'
    getter.download_file(url, file_destination)

    # NORMALIZING
    file_menagement.unzip(file_destination, f"{appResources.constants.temp_raw_folder}/dsm/")

    normalized_file = f"{appResources.constants.temp_normalizer_folder}/dsm/dsm.tif"
    file_menagement.copy(f"{appResources.constants.temp_raw_folder}/dsm/34_4_dom.tif", normalized_file)

    appContext.steps.gis.dsm.input_file = normalized_file

    logging.info("Done!")
