import sys, os
from qgis.core import QgsRasterLayer, QgsProject
from ..appCtx import appContext
from ..bibliotecas import logger



def addLayer(filePath, baseName, provider="gdal"):
    logger.plugin_log(f"filePath: {filePath}")
    logger.plugin_log(f"baseName: {baseName}")
    logger.plugin_log(f"provider: {provider}")
    layer = QgsRasterLayer(filePath, baseName, provider)

    if not layer.isValid():
        raise Exception("Error!")

    return layer


def load_layers():
    if appContext.steps.gis.ortho.input_file != "":
        ortho_layer = addLayer(appContext.steps.gis.ortho.input_file, "ortho", appContext.steps.gis.ortho.provider)
        QgsProject.instance().addMapLayer(ortho_layer)
    else:
        ortho_layer = appContext.steps.gis.ortho.input_layer

    if appContext.steps.gis.dsm.input_file != "":
        dsm_layer = addLayer(appContext.steps.gis.dsm.input_file, "dsm")
        QgsProject.instance().addMapLayer(dsm_layer)
    else:
        dsm_layer = appContext.steps.gis.dsm.input_layer

    if appContext.steps.gis.dtm.input_file != "":
        dtm_layer = addLayer(appContext.steps.gis.dtm.input_file, "dtm")
        QgsProject.instance().addMapLayer(dtm_layer)
    else:
        dtm_layer = appContext.steps.gis.dtm.input_layer

    # footprint_layer = addLayer("/Users/arthurrufhosangdacosta/qgis_data/rasters/Image1.tif", "footprint")
    # QgsProject.instance().addMapLayer(footprint_layer)


def identify_footprint():
    # logger.plugin_log("Identifying footprint.infos")
    pass


def extrude_footprint():
    # logger.plugin_log("Extruding footprint.infos")

    """
        { '-t' : False, 'GRASS_MIN_AREA_PARAMETER' : 0.0001, 'GRASS_OUTPUT_TYPE_PARAMETER' : 0, 'GRASS_REGION_CELLSIZE_PARAMETER' : 0, 'GRASS_REGION_PARAMETER' : None, 'GRASS_SNAP_TOLERANCE_PARAMETER' : -1, 'GRASS_VECTOR_DSCO' : '', 'GRASS_VECTOR_EXPORT_NOCAT' : False, 'GRASS_VECTOR_LCO' : '', 'elevation' : None, 'height' : 99999, 'height_column' : '', 'input' : '/Users/arthurrufhosangdacosta/qgis_data/footprint.geojson|layername=footprint|geometrytype=Polygon', 'method' : 0, 'null_value' : None, 'output' : 'TEMPORARY_OUTPUT', 'scale' : 1, 'type' : [0,1,2], 'where' : '', 'zshift' : 0 }

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


def generate_3d_model():
    load_layers()
    identify_footprint()
    extrude_footprint()
    join_layers()
