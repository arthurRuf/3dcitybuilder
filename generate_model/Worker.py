# import some modules used in the example
from qgis.core import *
import traceback
import time
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from .main import start


class Worker(QtCore.QObject):
    '''Example worker for calculating the total area of all features in a layer'''

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.killed = False

    def run(self):
        ret = None
        try:
            start()

            if self.killed is False:
                self.change_value.emit(100)
                self.finished.emit()
                # self.progress.emit(100)
                # ret = (self.layer, total_area,)
        except Exception as e:
            # forward the exception upstream
            # self.error_method.emit(e, traceback.format_exc())
            # self.error_method.emit()
            pass
        # self.finished.emit(ret)

    def kill(self):
        self.killed = True

    change_value = pyqtSignal(int)
