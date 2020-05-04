import sys, os, processing
import qgis
from qgis.core import QgsRasterLayer, QgsProject, QgsCoordinateReferenceSystem
from ..appCtx import appContext
from ..bibliotecas import logger
from ..normalizer import normalizer


def load_layers():
    QgsProject.instance().addMapLayer(appContext.layers.ortho.layer_loaded)
    QgsProject.instance().addMapLayer(appContext.layers.dtm.layer_loaded)
    QgsProject.instance().addMapLayer(appContext.layers.dsm.layer_loaded)


def identify_footprint():
    logger.plugin_log("Identifying footprint.infos")
    # appContext.steps.gis.footprint.input_file =
    # footprint_layer = appContext.update_layer(
    #     appContext,
    #     f"{appContext.layers.footprint.layer_path}|layername=footprint|geometrytype=Polygon",
    #     "footprint",
    #     "ogr"
    # )
    footprint_layer = appContext.update_layer(
        appContext,
        f"/Users/arthurrufhosangdacosta/qgis_data/extrusion/footprintg.geojson",
        "footprint",
        "ogr",
        "vector"
    )


def extrude_footprint():
    logger.plugin_log("Extruding footprint.infos")
    # vectorlayer = qgis.utils.iface.mapCanvas().currentLayer()
    # rasterfile = qgis.utils.iface.mapCanvas().currentLayer()

    vectorlayer = appContext.layers.footprint.layer_loaded
    rasterfile = appContext.layers.dsm.layer_loaded

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
            'SHAPES': vectorlayer.dataProvider().dataSourceUri(), # '/Users/arthurrufhosangdacosta/qgis_data/extrusion/footprintshp.shp|layername=footprintshp',
            'GRIDS': [
                rasterfile.dataProvider().dataSourceUri(), # '/Users/arthurrufhosangdacosta/qgis_data/extrusion/dsm.tif'
            ],
            'RESAMPLING': 3,
            'RESULT': output
        }
    )

    footprint = appContext.update_layer(appContext, output, "footprint", "ogr", "vector")
    footprint = normalizer.equalize_layer(footprint, "footprint", "vector")
    footprint = appContext.update_layer(appContext, footprint, "footprint", "ogr", "vector")
    QgsProject.instance().addMapLayer(footprint)

    """
        { '-t' : False, 'GRASS_MIN_AREA_PARAMETER' : 0.0001, 'GRASS_OUTPUT_TYPE_PARAMETER' : 0, 'GRASS_REGION_CELLSIZE_PARAMETER' : 0, 'GRASS_REGION_PARAMETER' : None, 'GRASS_SNAP_TOLERANCE_PARAMETER' : -1, 'GRASS_VECTOR_DSCO' : '', 'GRASS_VECTOR_EXPORT_NOCAT' : False, 'GRASS_VECTOR_LCO' : '', 'elevation' : None, 'height' : 99999, 'height_column' : '', 'input' : '/Users/arthurrufhosangdacosta/qgis_data/extrusion/footprintg.geojson|layername=footprint|geometrytype=Polygon', 'method' : 0, 'null_value' : None, 'output' : 'TEMPORARY_OUTPUT', 'scale' : 1, 'type' : [0,1,2], 'where' : '', 'zshift' : 0 }

        g.proj -c proj4="+proj=longlat +datum=WGS84 +no_defs"
        v.in.ogr min_area=0.0001 snap=-1.0 input="/Users/arthurrufhosangdacosta/qgis_data/footprint.geojson" layer="footprint" output="vector_5e99e857c69b23" --overwrite -o
        g.region n=-26.9003043 s=-27.014627 e=-48.5893986 w=-48.7151464 res=100.0
        v.extrude input=vector_5e99e857c69b23 type="point,line,area" zshift=0 height=99999 method="nearest" scale=1 output=outputb6f924da998943208ddbe68621dbf0cd --overwrite
        v.out.ogr type="auto" input="outputb6f924da998943208ddbe68621dbf0cd" output="/private/var/folders/6k/gwc2zlsd7tl7ph27q44pcm0w0000gn/T/processing_DsnlEY/1fbe88153eac46d284f78212695de208/output.gpkg" format="GPKG" --overwrite

    """
    pass


def join_layers():
    pass
    # logger.plugin_log("Applying Satellite Image on Terrain Digital Model")
    # logger.plugin_log("Placing 3D buildings model into CityModel")
    # logger.plugin_log("Generating output file")
    # f = open(os.path.expanduser(appContext.user_parameters.output), "w+")

def configure_layers_layout():
    pass

def generate_3d_model():
    load_layers()
    identify_footprint()
    extrude_footprint()
    join_layers()
    configure_layers_layout()
