from .bibliotecas import DotDict


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
        "crawler": {
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

    def updateContext(self, newContext):
        self.plugins = newContext.plugins
        self.user_parameters = newContext.user_parameters
        self.steps = newContext.steps
