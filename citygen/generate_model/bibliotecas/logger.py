from qgis.core import Qgis, QgsMessageLog
from ..appCtx import appContext

def general_log(message):
    QgsMessageLog.logMessage(message)

def message_bar_log(title, message="", level=Qgis.Success):
    appContext.qgis.iface.messageBar().pushMessage(title, message, level=level, duration=3)

def plugin_log(message=""):
    appContext.qgis.segf.dlg.txtLog.append(message)
    # appContext.qgis.iface.messageBar().pushMessage(title, message, level=level, duration=3)

