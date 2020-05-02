from qgis.core import Qgis, QgsMessageLog
from ..appCtx import appContext


def general_log(message):
    QgsMessageLog.logMessage(message)


def message_bar_log(title, message="", level=Qgis.Success):
    appContext.qgis.iface.messageBar().pushMessage(title, message, level=level, duration=3)


def plugin_log(message=""):
    appContext.qgis.segf.dlg.txtLog.append(message)


def update_progress(step_current=None, step_description=None, step_maximum=None,
                    overall_current=None,overall_description=None, overall_maximum=None):
    if step_current is not None:
        appContext.execution.step.current = step_current
        plugin_log(step_description)
    if step_description is not None:
        appContext.execution.step.description = step_description
    if step_maximum is not None:
        appContext.execution.step.maximum = step_maximum
    if overall_current is not None:
        appContext.execution.overall.current = overall_current
    if overall_description is not None:
        appContext.execution.overall.description = overall_description
    if overall_maximum is not None:
        appContext.execution.overall.maximum = overall_maximum

    appContext.qgis.segf.dlg.lblStepDescription.setText(f"{appContext.execution.overall.description} - {appContext.execution.step.description}")
    appContext.qgis.dlg.prgStepProgress.setValue(appContext.execution.step.current)
    appContext.qgis.dlg.prgStepProgress.setMaximum(appContext.execution.step.maximum)

    appContext.qgis.dlg.prgOverallProgress.setValue(appContext.execution.overall.current)
    appContext.qgis.dlg.prgOverallProgress.setMaximum(appContext.execution.overall.maximum)


def increase_step_current(step_description=appContext.execution.step.description):
    update_progress(step_current=appContext.execution.step.current + 1, step_description=step_description)


def increase_overall_current(overall_description=appContext.execution.overall.description):
    update_progress(overall_current=appContext.execution.overall.current + 1, overall_description=overall_description)
