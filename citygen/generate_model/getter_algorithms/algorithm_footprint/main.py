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
    footprint_layer = appContext.update_layer(
        appContext,
        f"/Users/arthurrufhosangdacosta/qgis_data/extrusion/footprintg.geojson",
        "footprint",
        "ogr",
        "vector"
    )
