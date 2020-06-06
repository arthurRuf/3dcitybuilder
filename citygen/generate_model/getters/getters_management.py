from ..appCtx import appContext
from ..bibliotecas import progress_bar, extension_manager, logger
from ..normalizer.normalizer import normalize_layer



def execute_getters():
    # Ortho
    logger.increase_overall_current("Data Retrieve")
    logger.update_progress(step_current=1, step_description="Satellite Image (Ortho)", step_maximum=100)
    extension_manager.execute_plugin(appContext.user_parameters.ortho_getter.id)
    normalize_layer("ortho", "raster")
    logger.plugin_log("Done!")

    # DTM
    # logger.increase_overall_current()
    # logger.update_progress(step_current=1, step_description="Digital Terrain Model (DTM)", step_maximum=100)
    # extension_manager.execute_plugin(appContext.user_parameters.dtm_getter.id)
    # normalize_layer("dtm", "raster")
    # logger.plugin_log("Done!")

    # DSM
    logger.increase_overall_current()
    logger.update_progress(step_current=1, step_description="Digital Surface Model (DSM)", step_maximum=100)
    extension_manager.execute_plugin(appContext.user_parameters.dsm_getter.id)
    normalize_layer("dsm", "raster")
    logger.plugin_log("Done!")


    # Footprint
    logger.increase_overall_current()
    logger.update_progress(step_current=1, step_description="Footprint", step_maximum=100)
    # if appContext.user_parameters.footprint_getter.format == "algorithm":
        # extension_management.run_plugin_method(appContext.user_parameters.footprint_getter.id, "identify_footprint")
    extension_manager.execute_plugin(appContext.user_parameters.footprint_getter.id)
    logger.plugin_log("Done!")
