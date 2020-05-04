import os, importlib, json, pathlib

from . import DotDict, logger
from .. import bibliotecas
from ..appCtx import appContext


def get_list():
    plugin_list = load_plugin_list()
    return list(filter(lambda x: "getter" in x["type"], plugin_list))


def load_plugin_list():
    logger.plugin_log("Loading Plugins... ")

    file_re = os.path.dirname(os.path.realpath(__file__))
    path = pathlib.Path(file_re)
    plugins_path = str(path.parent) + "/getter_algorithms"

    appContext.plugins.path = plugins_path

    logger.plugin_log("Loading getters from: " + plugins_path)

    directory_list = os.listdir(plugins_path)

    plugin_list = []
    for index, directory_name in enumerate(directory_list):
        try:
            with open(rf'{plugins_path}/{directory_name}/config.json') as file:

                plugin_configuration_file = json.load(file)

                if "features" not in plugin_configuration_file \
                        or len(plugin_configuration_file["features"]) != 1 \
                        or "properties" not in plugin_configuration_file["features"][0] \
                        or "geometry" not in plugin_configuration_file["features"][0]:
                    logger.plugin_log(
                        f"Invalid config.json file for plugin {directory_name}.")
                    raise Exception()

                plugin_feature = plugin_configuration_file["features"][0]
                plugin_properties = plugin_feature["properties"]
                plugin_geometry = plugin_feature["geometry"]

                if "type" not in plugin_properties:
                    logger.plugin_log(
                        f"Invalid config.json file for plugin {directory_name}.\n Property 'type' is mandatory on features[0].properties.")
                    raise Exception()
                if "layer" not in plugin_properties:
                    logger.plugin_log(
                        f"Invalid config.json file for plugin {directory_name}.\n Property 'layer' is mandatory on features[0].properties.")
                    raise Exception()

                plugin_list.append({
                    "id": directory_name,
                    "position": 0 if directory_name in ["local_ortho", "local_dtm", "local_dsm"] else index + 1,
                    "name": plugin_properties.get("name", directory_name),
                    "type": plugin_properties["type"],
                    "format": plugin_properties["format"],
                    "layer": plugin_properties["layer"],
                    "invocation": plugin_properties.get("invocation", "python3"),
                    "datum": plugin_properties.get("datum", "????"),
                    "cropIncluded": plugin_properties.get("cropIncluded", True),
                    "requirements": plugin_properties.get("requirements", []),
                    "normalizer": plugin_properties.get("normalizer", {"id": "none"}),
                    "parameters": plugin_properties.get("parameters", {}),
                    "geometry": plugin_geometry
                })
        except FileExistsError:
            logger.plugin_log(f"Fail to load {directory_name} plugin! The plugin does not have a config.yml file")
        except Exception:
            logger.plugin_log(f"Fail to load {directory_name} plugin!")

            plugin_list = sorted(plugin_list, key=lambda k: k['position'])

            logger.plugin_log("Done!")
    return plugin_list


def run_plugin_method(plugin_id, method_name):

    logger.plugin_log(f"plugin_id: {plugin_id}")
    path = f"{appContext.plugins.path}/{plugin_id}"
    plugin_main_module = importlib.machinery.SourceFileLoader('main', f'{path}/main.py').load_module()



    appResources = DotDict.DotDict({
        "configure_plugin": configure_plugin,
        "execute_plugin": execute_plugin,
        "bibliotecas": bibliotecas
    })

    method = getattr(plugin_main_module, method_name)
    method(appResources, appContext)



def configure_plugin(plugin_id):
    run_plugin_method(plugin_id, "configure")


def execute_plugin(plugin_id):
    run_plugin_method(plugin_id, "execute")
