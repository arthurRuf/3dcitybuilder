def configure(appResources, appContext):
    pass
    # appContext.steps.getters.dsm.parameters.input_layer = appContext.user_parameters.dsm_input


def execute(appResources, appContext):
    configure(appResources, appContext)

    appContext.update_layer_with_loaded(
        appContext,
        appContext.user_parameters.dsm_input,
        "dsm"
    )
