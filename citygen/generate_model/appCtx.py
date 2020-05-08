import sys, os, random, string
from qgis.core import QgsVectorLayer, QgsRasterLayer
from .bibliotecas import DotDict, logger


def add_layer(filePath, type="raster", layer_name="", provider="gdal", crs_id=None):
    layer = None

    if type == "vector":
        layer = QgsVectorLayer(filePath, layer_name, provider)
    else:
        layer = QgsRasterLayer(filePath, layer_name, provider)

    if not layer.isValid():
        raise Exception("Error!")

    if crs_id != None:
        crs = layer.crs()
        crs.createFromId(crs_id)

    return layer


class appContext:
    BUILDING_HEIGHT_METHODS = [
        {
            "title": "Minimum",
            "grassGIS_method_id": 1
        },
        {
            "title": "Maximum",
            "grassGIS_method_id": 2
        },
        {
            "title": "Average",
            "grassGIS_method_id": 4
        },
        {
            "title": "First Quartile",
            "grassGIS_method_id": 9
        },
        {
            "title": "Median",
            "grassGIS_method_id": 10
        },
        {
            "title": "Third Quartile",
            "grassGIS_method_id": 11
        },
        {
            "title": "Percentile",
            "grassGIS_method_id": 12
        }
    ]

    plugins = DotDict.DotDict({
        "getter_ortho_list": [],
        "getter_dtm_list": [],
        "getter_dsm_list": [],
        "getter_footprint_list": [],
        "footprint_algorithm":[],
    })

    user_parameters = DotDict.DotDict({
        "x1": 0,
        "y1": 0,
        "x2": 0,
        "y2": 0,

        "ortho_getter": None,
        "dtm_getter": None,
        "dsm_getter": None,
        "footprint_getter": None,

        "ortho_output": "",
        "dtm_output": "",
        "dsm_output": "",
        "footprint_output": "",

        "building_height_method": "",
        "clip_layer": None
    })

    layers = DotDict.DotDict({
        "ortho": {
            "layer": None,
            "data_provider": None,
            "type": "raster",
            "crs": None
        },
        "dtm": {
            "layer": None,
            "data_provider": None,
            "type": "raster",
            "crs": None
        },
        "dsm": {
            "layer": None,
            "data_provider": None,
            "type": "raster",
            "crs": None
        },
        "footprint": {
            "layer": None,
            "data_provider": None,
            "type": "vector",
            "crs": None
        },
    })

    qgis = DotDict.DotDict({
        "iface": None,
        "dlg": None
    })

    execution = DotDict.DotDict({
        "id": "",
        "temp_folder": "",
        "raw_temp_folder": "",
        "normalized_temp_folder": "",
        "overall": {
            "description": "",
            "current": 0,
            "maximum": 100

        },
        "step": {
            "description": "",
            "current": 0,
            "maximum": 100
        }
    })

    def update_layer(self, path, name, data_provider=None, type=None, crs=None):
        data_provider = data_provider or self.layers[name].data_provider
        type = type or self.layers[name].type
        crs = crs or self.layers[name].crs or None

        self.layers[name].data_provider = data_provider
        self.layers[name].type = type
        self.layers[name].crs = crs

        layer = add_layer(path, type, name, data_provider, crs)

        self.layers[name].layer = layer

        return layer

    def update_layer_with_loaded(self, layer, layer_name):
        self.layers[layer_name].layer = layer
        self.layers[layer_name].data_provider = layer.dataProvider().name()

        return layer
