

def configure(appResources, appContext):
    appContext.steps.getters.dsm.parameters.input_layer = appContext.user_parameters.dsm_input


def execute(appResources, appContext):
    configure(appResources, appContext)
    appContext.steps.gis.dsm.input_layer = appContext.steps.getters.dsm.parameters.input_layer
