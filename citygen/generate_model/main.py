import logging, sys, os
from generate_model.appContext import appContext
from generate_model.bibliotecas import plugin_management, progress_bar

from generate_model.cli import cli_controler
from generate_model.crawler import crawler_management
from generate_model.normalizer import normalizer_management
from generate_model.gis import gis


def configure_logging():
    format = "%(asctime)s:%(levelname)s: %(message)s"
    logging.basicConfig(filename='logs.log', level=logging.DEBUG, format=format)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(format))
    logging.getLogger().addHandler(stream_handler)


def cleanup_temp():
    os.rmdir("temp")

    os.mkdir("temp")

    os.mkdir("temp/raw")
    os.mkdir("temp/raw/ortho")
    os.mkdir("temp/raw/dtm")
    os.mkdir("temp/raw/dsm")

    os.mkdir("temp/normalized")
    os.mkdir("temp/normalized/ortho")
    os.mkdir("temp/normalized/dtm")
    os.mkdir("temp/normalized/dsm")


def start():
    configure_logging()

    logging.info("Getting files...")
    crawler_management.execute_crawlers()

    gis.generate_3d_model()
    # logging.info("Process complete without errors!")
    # logging.info(f"Output file is at \n{user_parameters['output']}")
