"""
Model exported as python.
Name : Extrude_Footprint
Group : TTC
With QGIS : 31201
"""

import processing
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterLayer


class Extrude_footprint(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('footprint', 'footprint_layer', types=[QgsProcessing.TypeVector], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('DSM', 'DSM', defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'default_height',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': '99',
            'INPUT': parameters['footprint'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # v.rast.stats
        alg_params = {
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
            'GRASS_REGION_CELLSIZE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'column_prefix': 'calculated_height',
            'map': outputs['FieldCalculator']['OUTPUT'],
            'method': [0,1,2,3,4,5,6,7,8,9,10,11,12],
            'percentile': 90,
            'raster': parameters['DSM'],
            'output': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Vraststats'] = processing.run('grass7:v.rast.stats', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'Extrude_Footprint'

    def displayName(self):
        return 'Extrude_Footprint'

    def group(self):
        return 'TTC'

    def groupId(self):
        return ''

    def createInstance(self):
        return Extrude_footprint()

if __name__ == '__main__':
    Extrude_footprint()