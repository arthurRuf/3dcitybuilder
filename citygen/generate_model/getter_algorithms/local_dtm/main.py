
def configure(appResources, appContext):
    appContext.steps.getters.dtm.parameters.input_layer = appContext.user_parameters.dtm_input


def execute(appResources, appContext):
    configure(appResources, appContext)
    appContext.steps.gis.dtm.input_layer = appContext.steps.getters.dtm.parameters.input_layer
