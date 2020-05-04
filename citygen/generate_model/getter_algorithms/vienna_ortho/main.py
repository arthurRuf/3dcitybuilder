import time, shutil, os, sys, requests
from qgis.core import QgsRasterLayer


def configure(appResources, appContext):
    pass


def execute(appResources, appContext):
    # WMS Server: https://maps.wien.gv.at/wmts/1.0.0/WMTSCapabilities-arcmap.xml

    appContext.update_layer(
        appContext,
        'crs=EPSG:3857&dpiMode=7&format=image/jpeg&layers=lb&styles=farbe&tileMatrixSet=google3857&url=https://maps.wien.gv.at/wmts/1.0.0/WMTSCapabilities-arcmap.xml',
        "ortho",
        "wms"
    )

    appResources.bibliotecas.logger.update_progress(step_current=1, step_maximum=1)
    appResources.bibliotecas.logger.plugin_log("Done!")
