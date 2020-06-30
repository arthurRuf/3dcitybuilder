def configure(appResources, appContext):
    pass
    # appContext.steps.getters.water.parameters.input_layer = appContext.user_parameters.water_input


def execute(appResources, appContext):
    configure(appResources, appContext)

    appContext.update_layer_with_loaded(
        appContext,
        appContext.user_parameters.water_input,
        "water"
    )
