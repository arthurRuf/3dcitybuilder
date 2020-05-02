import sys, os, random, string
from .bibliotecas import DotDict, logger


class appContext:
    plugins = DotDict.DotDict({
        "getter_ortho_list": [],
        "getter_dsm_list": [],
        "getter_dtm_list": []
    })

    user_parameters = DotDict.DotDict({
        "x1": 0,
        "y1": 0,
        "x2": 0,
        "y2": 0,
        "output": "",
    })

    steps = DotDict.DotDict({
        "getters": {
            "ortho": {
                "id": "",
                "parameters": {
                    "input_file": ""
                }
            },
            "dsm": {
                "id": "",
                "parameters": {
                    "input_file": ""
                }
            },
            "dtm": {
                "id": "",
                "parameters": {
                    "input_file": ""
                }
            },
        },
        "gis": {
            "ortho": {
                "input_file": ""
            },
            "dsm": {
                "input_file": ""
            },
            "dtm": {
                "input_file": ""
            }
        }
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

    def updateContext(self, newContext):
        self.plugins = newContext.plugins
        self.user_parameters = newContext.user_parameters
        self.steps = newContext.steps
