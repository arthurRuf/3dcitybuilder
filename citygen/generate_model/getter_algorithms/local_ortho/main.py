

def configure(appResources, appContext):
    appContext.steps.getters.ortho.parameters.input_layer = appContext.user_parameters.ortho_input


def execute(appResources, appContext):
    configure(appResources, appContext)
    appContext.steps.gis.ortho.input_layer = appContext.steps.getters.ortho.parameters.input_layer
