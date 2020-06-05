import sys, os, processing
import qgis
from qgis.core import QgsRasterLayer, QgsProject, QgsCoordinateReferenceSystem
from ..appCtx import appContext
from ..bibliotecas import logger


def equalize_layer(layer_name, loaded_layer, layer_type):
    project_csr = QgsProject.instance().crs()
    layer_crs = loaded_layer.crs()

    result_path = loaded_layer.dataProvider().dataSourceUri()

    if project_csr != layer_crs and loaded_layer.dataProvider().name() != 'wms':
        logger.plugin_log(f"Converting layer {loaded_layer.name()} CRS...")

        project_epsg = f'EPSG:{project_csr.postgisSrid()}'
        layer_epsg = f'EPSG:{layer_crs.postgisSrid() or appContext.user_parameters.dtm_getter.epsg_code}'

        if layer_type == "raster":
            result_path = f"{appContext.execution.raw_temp_folder}/{layer_name}/{layer_name}_epsg.tif"

            processing.run(
                "grass7:r.proj",
                {
                    'input': loaded_layer.dataProvider().dataSourceUri(),
                    'crs': QgsCoordinateReferenceSystem(project_epsg),
                    'method': 0,
                    'memory': 300,
                    'resolution': None,
                    '-n': False,
                    'output': result_path,
                    'GRASS_REGION_PARAMETER': None,
                    'GRASS_REGION_CELLSIZE_PARAMETER': 0,
                    'GRASS_RASTER_FORMAT_OPT': '',
                    'GRASS_RASTER_FORMAT_META': ''
                }
            )

            # processing.run(
            #     "gdal:warpreproject",
            #     {
            #         'INPUT': loaded_layer.dataProvider().dataSourceUri(),
            #         'SOURCE_CRS': QgsCoordinateReferenceSystem(layer_epsg),
            #         'TARGET_CRS': QgsCoordinateReferenceSystem(project_epsg),
            #         'RESAMPLING': 0,
            #         'NODATA': None,
            #         'TARGET_RESOLUTION': None,
            #         'OPTIONS': '',
            #         'DATA_TYPE': 0,
            #         'TARGET_EXTENT': None,
            #         'TARGET_EXTENT_CRS': None,
            #         'MULTITHREADING': False,
            #         'EXTRA': '',
            #         'OUTPUT': result_path
            #     }
            # )
        else:
            result_path = f"{appContext.execution.raw_temp_folder}/{layer_name}/{layer_name}_epsg.shp"
            processing.run(
                'qgis:reprojectlayer',
                {
                    'INPUT': loaded_layer.dataProvider().dataSourceUri(),
                    'TARGET_CRS': project_epsg,
                    'OUTPUT': result_path
                }
            )

        appContext.update_layer(
            appContext,
            result_path,
            layer_name,
            crs=project_csr.postgisSrid()
        )

    return result_path


def clip_layer(layer_name, loaded_layer, layer_type):
    result_path = loaded_layer.dataProvider().dataSourceUri()

    if True and \
            appContext.user_parameters.clip_layer != None:
        logger.plugin_log(f"Cropping layer {loaded_layer.name()}...")

        layer_path = loaded_layer.dataProvider().dataSourceUri()
        polygon_path = appContext.user_parameters.clip_layer.dataProvider().dataSourceUri()

        if layer_type == "raster":
            result_path = f"{appContext.execution.raw_temp_folder}/{layer_name}/{layer_name}_croped.tif"

            processing.run(
                "gdal:cliprasterbymasklayer",
                {
                    'INPUT': layer_path,
                    'MASK': polygon_path,
                    'SOURCE_CRS': None,
                    'TARGET_CRS': None,
                    'NODATA': None,
                    'ALPHA_BAND': False,
                    'CROP_TO_CUTLINE': True,
                    'KEEP_RESOLUTION': False,
                    'SET_RESOLUTION': False,
                    'X_RESOLUTION': None,
                    'Y_RESOLUTION': None,
                    'MULTITHREADING': False,
                    'OPTIONS': '',
                    'DATA_TYPE': 0,
                    'OUTPUT': result_path
                }
            )
        else:
            result_path = f"{appContext.execution.raw_temp_folder}/{layer_name}/{layer_name}_croped.shp"
            processing.run(
                "native:clip",
                {
                    'INPUT': layer_path,
                    'OVERLAY': polygon_path,
                    'OUTPUT': result_path
                }
            )

        appContext.update_layer(
            appContext,
            result_path,
            layer_name
        )

    return result_path



def normalize_layer(layer_name, layer_type):
    layer = appContext.layers[layer_name]

    if layer.data_provider != "wms":
        equalize_layer(layer_name, layer.layer, layer_type)
        layer_final_path = clip_layer(layer_name, layer.layer, layer_type)

        appContext.update_layer(appContext, layer_final_path, layer_name, layer.data_provider)


def normalize_layers():
    normalize_layer("ortho", "raster")
    normalize_layer("dtm", "raster")
    normalize_layer("dsm", "raster")
