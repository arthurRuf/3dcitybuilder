import time, shutil, logging, os, sys, requests
from ...bibliotecas import progress_bar, inputa, getter,file_menagement


def configure(appResources, appContext):
    pass


def execute(appResources, appContext):
    logging.info("Getting file...")

    raw_file = f"{appResources.constants.temp_raw_folder}/dsm/dsm.zip"
    url = 'https://www.wien.gv.at/ma41datenviewer/downloads/ma41/geodaten/dgm_tif/35_4_dgm_tif.zip'

    getter.download_file(url, raw_file)

    # NORMALIZING
    file_menagement.unzip(raw_file, f"{appResources.constants.temp_raw_folder}/dtm/")

    normalized_file = f"{appResources.constants.temp_normalizer_folder}/dtm/dtm.tif"
    file_menagement.copy(f"{appResources.constants.temp_raw_folder}/dtm/35_4_dgm.tif", normalized_file)

    appContext.steps.gis.dtm.input_file = normalized_file

    logging.info("Done!")
