import sys, os, processing
import qgis
from qgis.core import QgsRasterLayer, QgsProject, QgsCoordinateReferenceSystem
from ..appCtx import appContext
from ..bibliotecas import logger


def equalize_layer(layer_loaded, layer_name, layer_type="raster"):
    project_postgis_id = QgsProject.instance().crs().postgisSrid()

    result_path = layer_loaded.dataProvider().dataSourceUri()

    if layer_loaded.crs() != QgsProject.instance().crs() and layer_loaded.dataProvider().name() != 'wms':
        logger.plugin_log(f"Converting layer {layer_loaded.name()} CRS...")
        if layer_type == "raster":
            f"{appContext.user_parameters[f'{layer_name}_output']}"
            f"{appContext.user_parameters[f'{layer_name}_output']}/{layer_name}.tif"
        else:
            f"{appContext.user_parameters[f'{layer_name}_output']}"
            f"{appContext.user_parameters[f'{layer_name}_output']}/{layer_name}.shp"

        source_epsg = layer_loaded.crs().postgisSrid()

        if layer_type == "raster":
            result_path = f"{appContext.execution.raw_temp_folder}/{layer_name}/{layer_name}_ready.tif"

            processing.run(
                "gdal:warpreproject",
                {
                    'INPUT': layer_loaded.dataProvider().dataSourceUri(),
                    'SOURCE_CRS': QgsCoordinateReferenceSystem(f'EPSG:{source_epsg}'),
                    'TARGET_CRS': QgsCoordinateReferenceSystem(f'EPSG:{project_postgis_id}'),
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
            processing.run('qgis:reprojectlayer', layer_loaded.dataProvider().dataSourceUri(),
                           f'EPSG:{project_postgis_id}',
                           result_path)

    return result_path


def equalize_crs():
    ortho = equalize_layer(appContext.layers.ortho.layer_loaded, "ortho")
    dtm = equalize_layer(appContext.layers.dtm.layer_loaded, "dtm")
    dsm = equalize_layer(appContext.layers.dsm.layer_loaded, "dsm")

    appContext.update_layer(appContext, ortho, "ortho", appContext.layers.ortho.layer_data_provider)
    appContext.update_layer(appContext, dtm, "dtm", appContext.layers.dtm.layer_data_provider)
    appContext.update_layer(appContext, dsm, "dsm", appContext.layers.dsm.layer_data_provider)
