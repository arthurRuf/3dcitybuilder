import sys, os, random, string
from qgis.core import QgsVectorLayer, QgsRasterLayer
from .bibliotecas import DotDict, logger


def add_layer(filePath, type="raster", layer_name="", provider="gdal"):
    layer = None

    if (type == "vector"):
        layer = QgsVectorLayer(filePath, layer_name, provider)
    else:
        layer = QgsRasterLayer(filePath, layer_name, provider)

    if not layer.isValid():
        raise Exception("Error!")

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
        "getter_dsm_list": []
    })

    user_parameters = DotDict.DotDict({
        "x1": 0,
        "y1": 0,
        "x2": 0,
        "y2": 0,

        "ortho_getter": None,
        "dtm_getter": None,
        "dsm_getter": None,

        "ortho_output": "",
        "dtm_output": "",
        "dsm_output": "",

        "building_height_method": ""
    })

    layers = DotDict.DotDict({
        "ortho": {
            "layer_name": None,
            "layer_path": None,
            "layer_data_provider": None,
            "layer_loaded": None
        },
        "dtm": {
            "layer_name": None,
            "layer_path": None,
            "layer_data_provider": None,
            "layer_loaded": None
        },
        "dsm": {
            "layer_name": None,
            "layer_path": None,
            "layer_data_provider": None,
            "layer_loaded": None
        },
        "footprint": {
            "layer_name": None,
            "layer_path": None,
            "layer_data_provider": None,
            "layer_loaded": None
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

    def update_layer(self, layer_path, layer_name, layer_data_provider="gdal", layer_type="raster"):
        self.layers[layer_name].layer_name = layer_name
        self.layers[layer_name].layer_path = layer_path
        self.layers[layer_name].layer_data_provider = layer_data_provider

        self.layers[layer_name].layer_loaded = add_layer(layer_path, layer_type, layer_name, layer_data_provider)

        return self.layers[layer_name].layer_loaded

    def update_layer_with_loaded(self, layer_loaded, layer_name):
        self.layers[layer_name].layer_name = layer_loaded.name()
        self.layers[layer_name].layer_path = layer_loaded.dataProvider().dataSourceUri()
        self.layers[layer_name].layer_data_provider = layer_loaded.dataProvider().name()
        self.layers[layer_name].layer_loaded = layer_loaded

        return self.layers[layer_name].layer_loaded
