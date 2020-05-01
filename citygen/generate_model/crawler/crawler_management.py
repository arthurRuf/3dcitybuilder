from ..appCtx import appContext
from ..bibliotecas import progress_bar, plugin_management, logger



def execute_crawlers():
    # logging.info("Retrieving Satellite Imagery...")
    # plugin_management.execute_plugin(appContext.steps.crawler.ortho.id)
    # logging.info("Done!")

    logger.plugin_log("Retrieving Surface Digital Model...")
    plugin_management.execute_plugin(appContext.steps.crawler.dsm.id)
    logger.plugin_log("Done!")

    # logging.info("Retrieving Terrain Digital Model...")
    # plugin_management.execute_plugin(appContext.steps.crawler.dtm.id)
    # logging.info("Done")