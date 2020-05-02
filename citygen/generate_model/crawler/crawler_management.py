from ..appCtx import appContext
from ..bibliotecas import progress_bar, plugin_management, logger



def execute_crawlers():
    # Ortho
    logger.increase_overall_current("Data Retrieve")
    logger.update_progress(step_current=1, step_description="Satellite Image (Ortho)", step_maximum=100)
    # plugin_management.execute_plugin(appContext.steps.crawler.ortho.id)
    logger.plugin_log("Done!")

    # DSM
    logger.increase_overall_current()
    logger.update_progress(step_current=1, step_description="Digital Surface Model (DSM)", step_maximum=100)
    # plugin_management.execute_plugin(appContext.steps.crawler.dsm.id)
    logger.plugin_log("Done!")

    # DTM
    logger.increase_overall_current()
    logger.update_progress(step_current=1, step_description="Digital Terrain Model (DTM)", step_maximum=100)
    # plugin_management.execute_plugin(appContext.steps.crawler.dtm.id)
    logger.plugin_log("Done!")