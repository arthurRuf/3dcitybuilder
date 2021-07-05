from ..appCtx import appContext
from ..bibliotecas import progress_bar, extension_manager, logger
from ..normalizer.normalizer import normalize_layer



def execute_getters():
    # Ortho
    logger.increase_overall_current("Data Retrieve")
    logger.update_progress(step_current=1, step_description="Satellite Image (Ortho)", step_maximum=100)
    extension_manager.execute_plugin(appContext.user_parameters.ortho_getter.id)
    normalize_layer("ortho", "raster")
    logger.plugin_log("Done!", "SUCCESS")

    # DTM
    logger.increase_overall_current()
    logger.update_progress(step_current=1, step_description="Digital Terrain Model (DTM)", step_maximum=100)
    extension_manager.execute_plugin(appContext.user_parameters.dtm_getter.id)
    normalize_layer("dtm", "raster")
    logger.plugin_log("Done!", "SUCCESS")

    # DSM
    logger.increase_overall_current()
    logger.update_progress(step_current=1, step_description="Digital Surface Model (DSM)", step_maximum=100)
    extension_manager.execute_plugin(appContext.user_parameters.dsm_getter.id)
    normalize_layer("dsm", "raster")
    logger.plugin_log("Done!", "SUCCESS")


    # Footprint
    logger.increase_overall_current()
    logger.update_progress(step_current=1, step_description="Footprint", step_maximum=100)
    # if appContext.user_parameters.footprint_getter.format == "algorithm":
        # extension_management.run_plugin_method(appContext.user_parameters.footprint_getter.id, "identify_footprint")
    extension_manager.execute_plugin(appContext.user_parameters.footprint_getter.id)
    logger.plugin_log("Done!", "SUCCESS")

    # Street
    if appContext.user_parameters.street_getter is not None:
        logger.increase_overall_current()
        logger.update_progress(step_current=1, step_description="Street", step_maximum=100)
        # if appContext.user_parameters.street_getter.format == "algorithm":
            # extension_management.run_plugin_method(appContext.user_parameters.street_getter.id, "identify_street")
        extension_manager.execute_plugin(appContext.user_parameters.street_getter.id)
        logger.plugin_log("Done!", "SUCCESS")


    # Tree
    if appContext.user_parameters.tree_getter is not None:
        logger.increase_overall_current()
        logger.update_progress(step_current=1, step_description="Tree", step_maximum=100)
        # if appContext.user_parameters.tree_getter.format == "algorithm":
            # extension_management.run_plugin_method(appContext.user_parameters.tree_getter.id, "identify_tree")
        extension_manager.execute_plugin(appContext.user_parameters.tree_getter.id)
        logger.plugin_log("Done!", "SUCCESS")


    # Water
    if appContext.user_parameters.water_getter is not None:
        logger.increase_overall_current()
        logger.update_progress(step_current=1, step_description="Water", step_maximum=100)
        # if appContext.user_parameters.water_getter.format == "algorithm":
            # extension_management.run_plugin_method(appContext.user_parameters.water_getter.id, "identify_water")
        extension_manager.execute_plugin(appContext.user_parameters.water_getter.id)
        logger.plugin_log("Done!", "SUCCESS")
    