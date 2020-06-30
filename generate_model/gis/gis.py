import sys

# sys.path.append("/Volumes/TarDisk/ruf/workspace/ttc/3dcitybuilder/citygen/generate_model/gis/dependencies/")
# sys.path.append("/Volumes/TarDisk/ruf/workspace/ttc/3dcitybuilder/citygen/generate_model/gis/dependencies/osmnx/")
# sys.path.append("/Volumes/TarDisk/ruf/workspace/ttc/3dcitybuilder/citygen/generate_model/gis/dependencies/geopandas/")

import os, processing
import qgis

from qgis.core import QgsRasterLayer, QgsProject, QgsCoordinateReferenceSystem, QgsProperty, QgsVectorLayer, QgsFeature, \
    QgsGeometry, QgsPointXY, QgsVectorFileWriter, QgsFields, QgsSimpleLineSymbolLayer
from qgis.core.additions.edit import edit
import qgis._3d as d
from PyQt5.QtGui import QColor
from ..appCtx import appContext, add_layer
from ..bibliotecas import logger, file_management, extension_manager
from ..normalizer import normalizer


def create_viewport_polygon():
    extent = appContext.qgis.iface.mapCanvas().extent()

    layer = QgsVectorLayer(f"Polygon?crs={QgsProject.instance().crs().toWkt()}", 'polygon', "memory")
    feature = QgsFeature()
    points = [
        QgsPointXY(
            extent.xMinimum(),
            extent.yMaximum()
        ),
        QgsPointXY(
            extent.xMaximum(),
            extent.yMaximum()
        ),
        QgsPointXY(
            extent.xMaximum(),
            extent.yMinimum()
        ),
        QgsPointXY(
            extent.xMinimum(),
            extent.yMinimum()
        )
    ]
    # or points = [QgsPointXY(50,50),QgsPointXY(50,150),QgsPointXY(100,150),QgsPointXY(100,50)]
    feature.setGeometry(QgsGeometry.fromPolygonXY([points]))
    layer.dataProvider().addFeatures([feature])
    layer.updateExtents()
    QgsProject.instance().addMapLayers([layer])

    path = f"{appContext.execution.raw_temp_folder}/viewport.geojson"
    error, error_string = QgsVectorFileWriter.writeAsVectorFormat(
        layer,
        path,
        'utf-8',
        # destCRS=QgsProject.instance().crs(),
        driverName="GeoJSON"
    )

    if error != QgsVectorFileWriter.NoError:
        raise Exception('Error on creating Clipping Polygon: {details}'.format(details=error_string))

    loaded_layer = add_layer(path, "vector", "clipping_polygon", "ogr", layer.crs().postgisSrid())

    return loaded_layer


def extrude_footprint():
    logger.plugin_log("Extruding footprint.infos")
    # vectorlayer = qgis.utils.iface.mapCanvas().currentLayer()
    # rasterfile = qgis.utils.iface.mapCanvas().currentLayer()

    logger.plugin_log(
        f"appContext.user_parameters.building_height_method: {appContext.user_parameters.building_height_method}")

    building_height_method = 2
    if appContext.user_parameters.building_height_method == 0:
        building_height_method = 1
    elif appContext.user_parameters.building_height_method == 1:
        building_height_method = 2
    elif appContext.user_parameters.building_height_method == 2:
        building_height_method = 4
    elif appContext.user_parameters.building_height_method == 3:
        building_height_method = 9
    elif appContext.user_parameters.building_height_method == 4:
        building_height_method = 10
    elif appContext.user_parameters.building_height_method == 5:
        building_height_method = 11
    elif appContext.user_parameters.building_height_method == 6:
        building_height_method = 12

    logger.plugin_log(f"building_height_method: {building_height_method}")

    output = ""

    if appContext.user_parameters.building_height_method.algorithm == "grass7:v.rast.stats":
        output = f"{appContext.execution.raw_temp_folder}/footprint/footprint_height.gpkg"
        output = f"{appContext.execution.raw_temp_folder}/footprint/footprint_height.geojson"

        processing.run(
            "grass7:v.rast.stats",
            {
                'map': appContext.layers.footprint.layer.dataProvider().dataSourceUri(),
                'raster': appContext.layers.dsm.layer.dataProvider().dataSourceUri(),
                'column_prefix': "cb_heigh",
                'method': [appContext.user_parameters.building_height_method.method_id],
                'percentile': 90,
                'output': output,
                'GRASS_REGION_PARAMETER': None,
                'GRASS_REGION_CELLSIZE_PARAMETER': 0,
                'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
                'GRASS_MIN_AREA_PARAMETER': 0.0001,
                'GRASS_OUTPUT_TYPE_PARAMETER': 3,
                'GRASS_VECTOR_DSCO': '',
                'GRASS_VECTOR_LCO': '',
                'GRASS_VECTOR_EXPORT_NOCAT': False
            }
        )
    elif appContext.user_parameters.building_height_method.algorithm == "saga:addrastervaluestofeatures":
        output = f"{appContext.execution.raw_temp_folder}/footprint/footprint_height.shp"

        processing.run(
            "saga:addrastervaluestofeatures",
            {
                'SHAPES': appContext.layers.footprint.layer.dataProvider().dataSourceUri(),
                'GRIDS': [
                    appContext.layers.dsm.layer.dataProvider().dataSourceUri()
                ],
                'RESAMPLING': appContext.user_parameters.building_height_method.method_id,
                'RESULT': output
            }
        )
    elif appContext.user_parameters.building_height_method.algorithm == "native:zonalstatistics":
        output = appContext.layers.footprint.layer.dataProvider().dataSourceUri()

        processing.run(
            "native:zonalstatistics",
                       {
                           'INPUT_RASTER':appContext.layers.dsm.layer.dataProvider().dataSourceUri(),
                           'RASTER_BAND':1,
                           'INPUT_VECTOR':appContext.layers.footprint.layer.dataProvider().dataSourceUri(),
                           'COLUMN_PREFIX':'cg_',
                           'STATISTICS':[
                               appContext.user_parameters.building_height_method.method_id
                           ]})

    footprint = appContext.update_layer(appContext, output, "footprint", "ogr", "vector")

    normalizer.normalize_layer("footprint", "vector")

    findex = len(footprint.dataProvider().fields()) - 1
    if findex != -1:
        with edit(footprint):
            footprint.dataProvider().renameAttributes({findex: "cb_heigh"})
            footprint.updateFields()
    else:
        loggeer.log("It was not possible to rename Buildings Height Variable.")


def move(source, destination, layer_name):
    file_management.copy_file(file_management.path_cleanup(source), destination)

    if "|" in source:
        destination = f"{destination}|{source.split('|')[1]}"

    appContext.update_layer(appContext, destination, layer_name)


def save_files():
    if (appContext.user_parameters.ortho_output != ""):
        move(appContext.layers.ortho.layer.dataProvider().dataSourceUri(), appContext.user_parameters.ortho_output,
             "ortho")

    if (appContext.user_parameters.dtm_output != ""):
        move(appContext.layers.dtm.layer.dataProvider().dataSourceUri(), appContext.user_parameters.dtm_output, "dtm")

    if (appContext.user_parameters.dsm_output != ""):
        move(appContext.layers.dsm.layer.dataProvider().dataSourceUri(), appContext.user_parameters.dsm_output, "dsm")

    if (appContext.user_parameters.footprint_output != ""):
        move(appContext.layers.footprint.layer.dataProvider().dataSourceUri(),
             appContext.user_parameters.footprint_output, "footprint")


    if (appContext.user_parameters.street_output != ""):
        move(appContext.layers.street.layer.dataProvider().dataSourceUri(),
             appContext.user_parameters.street_output, "street")


    if (appContext.user_parameters.tree_output != ""):
        move(appContext.layers.tree.layer.dataProvider().dataSourceUri(),
             appContext.user_parameters.tree_output, "tree")


    if (appContext.user_parameters.water_output != ""):
        move(appContext.layers.water.layer.dataProvider().dataSourceUri(),
             appContext.user_parameters.water_output, "water")


def load_layers_to_project():
    QgsProject.instance().addMapLayer(appContext.layers.ortho.layer)
    QgsProject.instance().addMapLayer(appContext.layers.dtm.layer)
    QgsProject.instance().addMapLayer(appContext.layers.dsm.layer)

    # Footprint
    symbol = d.QgsPolygon3DSymbol()
    symbol.setAddBackFaces(False)
    symbol.setAltitudeBinding(1)
    symbol.setAltitudeClamping(0)
    symbol.setCullingMode(0)

    symbol.setEdgesEnabled(True)
    symbol.setEdgeWidth(0.4)

    # symbol.setExtrusionHeight(QgsProperty.fromExpression('"dsm"'))

    renderer = d.QgsVectorLayer3DRenderer()
    renderer.setSymbol(symbol)

    materialSettings = d.QgsPhongMaterialSettings()
    materialSettings.setAmbient(QColor(246, 141, 131))
    materialSettings.setDiffuse(QColor(192, 173, 159))
    materialSettings.setSpecular(QColor(255, 0, 0))
    symbol.setMaterial(materialSettings)

    appContext.layers.footprint.layer.setRenderer3D(renderer)
    # renderer.setLayer(appContext.layers.footprint.layer)
    QgsProject.instance().addMapLayer(appContext.layers.footprint.layer)

    # Street
    if appContext.user_parameters.street_getter is not None:
        appContext.layers.street.layer.renderer().symbol().setWidth(10.50000)
        appContext.layers.street.layer.renderer().symbol().setColor(QColor("#000000"))

        symbol_layer = [None, None, None]

        symbol_layer[0] = QgsSimpleLineSymbolLayer()
        symbol_layer[0].setWidth(0.4)
        symbol_layer[0].setColor(QColor("#cdd31b"))
        symbol_layer[0].setPenJoinStyle(1)
        symbol_layer[0].setPenCapStyle(0)

        symbol_layer[1] = QgsSimpleLineSymbolLayer()
        symbol_layer[1].setWidth(10)
        symbol_layer[1].setColor(QColor("#3b3b3b"))
        symbol_layer[1].setPenJoinStyle(1)
        symbol_layer[1].setPenCapStyle(0)

        symbol_layer[2] = QgsSimpleLineSymbolLayer()
        symbol_layer[2].setWidth(10.5)
        symbol_layer[2].setColor(QColor("#000000"))
        symbol_layer[2].setPenJoinStyle(1)
        symbol_layer[2].setPenCapStyle(0)

        appContext.layers.street.layer.renderer().symbol().appendSymbolLayer(symbol_layer[0])
        appContext.layers.street.layer.renderer().symbol().appendSymbolLayer(symbol_layer[1])
        appContext.layers.street.layer.renderer().symbol().appendSymbolLayer(symbol_layer[2])

        QgsProject.instance().addMapLayer(appContext.layers.street.layer)


    # Tree
    if appContext.user_parameters.tree_getter is not None:
        QgsProject.instance().addMapLayer(appContext.layers.tree.layer)

    # Water
    if appContext.user_parameters.water_getter is not None:
        QgsProject.instance().addMapLayer(appContext.layers.water.layer)




def generate_3d_model():
    extrude_footprint()
    save_files()
    load_layers_to_project()
