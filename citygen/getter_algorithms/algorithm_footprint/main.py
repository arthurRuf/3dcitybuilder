import os, processing


def configure(appResources, appContext):
    pass


def execute(appResources, appContext):
    pass


def identify_footprint(appResources, appContext):
    appResources.bibliotecas.logger.plugin_log("Identifying footprint.infos")
    # appContext.steps.gis.footprint.input_file =
    # footprint_layer = appContext.update_layer(
    #     appContext,
    #     f"{appContext.layers.footprint.layer_path}|layername=footprint|geometrytype=Polygon",
    #     "footprint",
    #     "ogr"
    # )
    # footprint_layer = appContext.update_layer(
    #     appContext,
    #     f"/Users/arthurrufhosangdacosta/qgis_data/extrusion/footprintg.geojson",
    #     "footprint",
    #     "ogr",
    #     "vector"
    # )

    neighbors_path = f"{appContext.execution.raw_temp_folder}/footprint/neighbors.tif"
    pixelstopolygons_path = f"{appContext.execution.raw_temp_folder}/footprint/pixelstopolygons.tif"
    footprints_path = f"{appContext.execution.raw_temp_folder}/footprint/pixelstopolygons.shp"

    processing.run(
        "grass7:r.neighbors",
        {
            'input': appContext.layers.dsm.layer.dataProvider().dataSourceUri(),
            'selection': appContext.layers.dsm.layer.dataProvider().dataSourceUri(),
            'method': 7,
            # 'size': 5,
            'size': 3,
            'gauss': None,
            'quantile': '',
            '-c': False,
            '-a': False,
            'weight': '',
            'output': neighbors_path,
            'GRASS_REGION_PARAMETER': None,
            'GRASS_REGION_CELLSIZE_PARAMETER': 9,
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_RASTER_FORMAT_META': ''
        }
    )

    processing.run(
        "native:pixelstopolygons",
        {
            'INPUT_RASTER': neighbors_path,
            'RASTER_BAND': 1,
            'FIELD_NAME': 'VALUE',
            'OUTPUT': pixelstopolygons_path
        }
    )

    processing.run(
        "gdal:polygonize",
        {
            'INPUT': pixelstopolygons_path,
            'BAND': 1,
            'FIELD': 'DN',
            'EIGHT_CONNECTEDNESS': False,
            'OUTPUT': footprints_path
        }
    )
