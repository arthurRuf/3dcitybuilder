def configure(appResources, appContext):
    pass
    # appContext.steps.getters.dtm.parameters.input_layer = appContext.user_parameters.dtm_input


def execute(appResources, appContext):
    configure(appResources, appContext)

    appContext.update_layer_with_loaded(
        appContext,
        appContext.user_parameters.dtm_input,
        "dtm"
    )
