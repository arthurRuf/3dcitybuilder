import sys, os, processing
import qgis
from qgis.core import QgsRasterLayer, QgsProject, QgsCoordinateReferenceSystem
import qgis._3d as d
from PyQt5.QtGui import QColor
from ..appCtx import appContext
from ..bibliotecas import logger, file_management, plugin_management
from ..normalizer import normalizer


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

    # processing.run("grass7:v.rast.stats", {
    #     'map': vectorlayer.dataProvider().dataSourceUri(),
    #     'raster': rasterfile.dataProvider().dataSourceUri(),
    #     'column_prefix': 'citygen',
    #     'method': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    #     'percentile': 90,
    #     'output': output,
    #     'GRASS_REGION_PARAMETER': None,
    #     'GRASS_REGION_CELLSIZE_PARAMETER': 0,
    #     'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
    #     'GRASS_MIN_AREA_PARAMETER': 0.000001,
    #     'GRASS_OUTPUT_TYPE_PARAMETER': 3,
    #     'GRASS_VECTOR_DSCO': '',
    #     'GRASS_VECTOR_LCO': '',
    #     'GRASS_VECTOR_EXPORT_NOCAT': True
    # })

    output = f"{appContext.execution.raw_temp_folder}/footprint/footprint_height.shp"

    processing.run(
        "saga:addrastervaluestofeatures",
        {
            'SHAPES': appContext.layers.footprint.layer.dataProvider().dataSourceUri(),
            # '/Users/arthurrufhosangdacosta/qgis_data/extrusion/footprintshp.shp|layername=footprintshp',
            'GRIDS': [
                appContext.layers.dsm.layer.dataProvider().dataSourceUri()
                # '/Users/arthurrufhosangdacosta/qgis_data/extrusion/dsm.tif'
            ],
            'RESAMPLING': 3,
            'RESULT': output
        }
    )

    footprint = appContext.update_layer(appContext, output, "footprint", "ogr", "vector")

    findex = footprint.dataProvider().fieldNameIndex("dsm")
    if findex != -1:
        footprint.dataProvider().renameAttributes({findex: "building_heigth"})
        footprint.updateFields()

    normalizer.equalize_layer("footprint", footprint, "vector")


def run_footprint():
    if appContext.user_parameters.footprint_getter.format == "algorithm":
        identify_footprint()
    extrude_footprint()


def save_files():
    if (appContext.user_parameters.ortho_output != ""):
        file_management.move_file(
            file_management.path_cleanup(appContext.layers.ortho.layer.dataProvider().dataSourceUri()),
            file_management.path_cleanup(appContext.user_parameters.ortho_output),
        )

    if (appContext.user_parameters.dtm_output != ""):
        file_management.move_file(
            file_management.path_cleanup(appContext.layers.dtm.layer.dataProvider().dataSourceUri()),
            file_management.path_cleanup(appContext.user_parameters.dtm_output),
        )

    if (appContext.user_parameters.dsm_output != ""):
        file_management.move_file(
            file_management.path_cleanup(appContext.layers.dsm.layer.dataProvider().dataSourceUri()),
            file_management.path_cleanup(appContext.user_parameters.dsm_output),
        )

    if (appContext.user_parameters.footprint_output != ""):
        file_management.move_file(
            file_management.path_cleanup(appContext.layers.footprint.layer.dataProvider().dataSourceUri()),
            file_management.path_cleanup(appContext.user_parameters.footprint_output),
        )


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

    renderer = d.QgsVectorLayer3DRenderer()
    renderer.setSymbol(symbol)

    materialSettings = d.QgsPhongMaterialSettings()
    materialSettings.setAmbient(QColor(255, 0, 0))
    materialSettings.setDiffuse(QColor(255, 0, 0))
    materialSettings.setSpecular(QColor(255, 0, 0))
    symbol.setMaterial(materialSettings)

    appContext.layers.footprint.layer.setRenderer3D(renderer)
    # renderer.setLayer(appContext.layers.footprint.layer)
    QgsProject.instance().addMapLayer(appContext.layers.footprint.layer)


def generate_3d_model():
    run_footprint()
    save_files()
    load_layers_to_project()
