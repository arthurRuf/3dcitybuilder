import sys, os, processing
import qgis
from qgis.core import QgsRasterLayer, QgsProject, QgsCoordinateReferenceSystem, QgsProperty, QgsVectorLayer, QgsFeature, \
    QgsGeometry, QgsPointXY, QgsVectorFileWriter, QgsFields
import qgis._3d as d
from PyQt5.QtGui import QColor
from ..appCtx import appContext, add_layer
from ..bibliotecas import logger, file_management, plugin_management
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


def identify_footprint():
    plugin_management.run_plugin_method(appContext.user_parameters.footprint_getter.id, "identify_footprint")


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

    # QGIS Analysis -> Supports only SUM, MEAN and COUNT
    # zonalstats = qgis.analysis.QgsZonalStatistics(vectorlayer, rasterfile, "d")
    # zonalstats.calculateStatistics(None)

    output = ""

    if appContext.user_parameters.building_height_method.algorithm == "grass7:v.rast.stats":
        output = f"{appContext.execution.raw_temp_folder}/footprint/footprint_height.gpkg"

        processing.run(
            "grass7:v.rast.stats",
            {
                'map': appContext.layers.footprint.layer.dataProvider().dataSourceUri(),
                'raster': appContext.layers.dsm.layer.dataProvider().dataSourceUri(),
                'column_prefix': 'cbuilding',
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

    footprint = appContext.update_layer(appContext, output, "footprint", "ogr", "vector")

    normalizer.normalize_layer("footprint", "vector")

    findex = len(footprint.dataProvider().fields()) - 1
    if findex != -1:
        footprint.dataProvider().renameAttributes({findex: "building_height"})
        footprint.updateFields()


def run_footprint():
    if appContext.user_parameters.footprint_getter.format == "algorithm":
        identify_footprint()
    extrude_footprint()


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
    materialSettings.setDiffuse(QColor(179, 179, 179))
    materialSettings.setSpecular(QColor(255, 0, 0))
    symbol.setMaterial(materialSettings)

    appContext.layers.footprint.layer.setRenderer3D(renderer)
    # renderer.setLayer(appContext.layers.footprint.layer)
    QgsProject.instance().addMapLayer(appContext.layers.footprint.layer)


def generate_3d_model():
    run_footprint()
    save_files()
    load_layers_to_project()
