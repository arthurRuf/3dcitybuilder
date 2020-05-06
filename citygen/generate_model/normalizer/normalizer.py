import sys, os, processing
import qgis
from qgis.core import QgsRasterLayer, QgsProject, QgsCoordinateReferenceSystem
from ..appCtx import appContext
from ..bibliotecas import logger


def equalize_layer(layer_name, loaded_layer, layer_type):
    project_epsg = QgsProject.instance().crs()
    layer_epsg = loaded_layer.crs()

    result_path = loaded_layer.dataProvider().dataSourceUri()

    if project_epsg != layer_epsg and loaded_layer.dataProvider().name() != 'wms':
        logger.plugin_log(f"Converting layer {loaded_layer.name()} CRS...")

        if layer_type == "raster":
            result_path = f"{appContext.execution.raw_temp_folder}/{layer_name}/{layer_name}_ready.tif"

            processing.run(
                "gdal:warpreproject",
                {
                    'INPUT': loaded_layer.dataProvider().dataSourceUri(),
                    'SOURCE_CRS': QgsCoordinateReferenceSystem(f'EPSG:{layer_epsg.postgisSrid()}'),
                    'TARGET_CRS': QgsCoordinateReferenceSystem(f'EPSG:{project_epsg.postgisSrid()}'),
                    'RESAMPLING': 0,
                    'NODATA': None,
                    'TARGET_RESOLUTION': None,
                    'OPTIONS': '',
                    'DATA_TYPE': 0,
                    'TARGET_EXTENT': None,
                    'TARGET_EXTENT_CRS': None,
                    'MULTITHREADING': False,
                    'EXTRA': '',
                    'OUTPUT': result_path
                }
            )
        else:
            result_path = f"{appContext.execution.raw_temp_folder}/{layer_name}/{layer_name}_ready.shp"
            processing.run(
                'qgis:reprojectlayer',
                {
                    'INPUT': loaded_layer.dataProvider().dataSourceUri(),
                    'TARGET_CRS': f'EPSG:{project_epsg.postgisSrid()}',
                    'OUTPUT': result_path
                }
            )

        appContext.update_layer(
            appContext,
            result_path,
            layer_name
        )

    return result_path


def clip_layer():
    pass


def equalize_crs():
    ortho = equalize_layer("ortho", appContext.layers.ortho.layer, "raster")
    dtm = equalize_layer("dtm", appContext.layers.dtm.layer, "raster")
    dsm = equalize_layer("dsm", appContext.layers.dsm.layer, "raster")

    clip_layer()

    appContext.update_layer(appContext, ortho, "ortho", appContext.layers.ortho.data_provider)
    appContext.update_layer(appContext, dtm, "dtm", appContext.layers.dtm.data_provider)
    appContext.update_layer(appContext, dsm, "dsm", appContext.layers.dsm.data_provider)
