import sys, os, processing
import qgis
from qgis.core import QgsRasterLayer, QgsProject, QgsCoordinateReferenceSystem, QgsProperty
import qgis._3d as d
from PyQt5.QtGui import QColor
from ..appCtx import appContext
from ..bibliotecas import logger, file_management, plugin_management
from ..normalizer import normalizer


def identify_footprint():
    plugin_management.run_plugin_method(appContext.user_parameters.footprint_getter.id, "identify_footprint")


def extrude_footprint():
    logger.plugin_log("Extruding footprint.infos")
    # vectorlayer = qgis.utils.iface.mapCanvas().currentLayer()
    # rasterfile = qgis.utils.iface.mapCanvas().currentLayer()

    logger.plugin_log(
        f"appContext.user_parameters.building_height_method: {appContext.user_parameters.building_height_method}")

    building_height_method = 2
    if appContext.user_parameters.building_height_method == 0:
        building_height_method = 1
    elif appContext.user_parameters.building_height_method == 1:
        building_height_method = 2
    elif appContext.user_parameters.building_height_method == 2:
        building_height_method = 4
    elif appContext.user_parameters.building_height_method == 3:
        building_height_method = 9
    elif appContext.user_parameters.building_height_method == 4:
        building_height_method = 10
    elif appContext.user_parameters.building_height_method == 5:
        building_height_method = 11
    elif appContext.user_parameters.building_height_method == 6:
        building_height_method = 12

    logger.plugin_log(f"building_height_method: {building_height_method}")

    # QGIS Analysis -> Supports only SUM, MEAN and COUNT
    # zonalstats = qgis.analysis.QgsZonalStatistics(vectorlayer, rasterfile, "d")
    # zonalstats.calculateStatistics(None)

    # processing.run("grass7:v.rast.stats", {
    #     'map': vectorlayer.dataProvider().dataSourceUri(),
    #     'raster': rasterfile.dataProvider().dataSourceUri(),
    #     'column_prefix': 'citygen',
    #     'method': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    #     'percentile': 90,
    #     'output': output,
    #     'GRASS_REGION_PARAMETER': None,
    #     'GRASS_REGION_CELLSIZE_PARAMETER': 0,
    #     'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
    #     'GRASS_MIN_AREA_PARAMETER': 0.000001,
    #     'GRASS_OUTPUT_TYPE_PARAMETER': 3,
    #     'GRASS_VECTOR_DSCO': '',
    #     'GRASS_VECTOR_LCO': '',
    #     'GRASS_VECTOR_EXPORT_NOCAT': True
    # })

    output = f"{appContext.execution.raw_temp_folder}/footprint/footprint_height.shp"

    processing.run(
        "saga:addrastervaluestofeatures",
        {
            'SHAPES': appContext.layers.footprint.layer.dataProvider().dataSourceUri(),
            # '/Users/arthurrufhosangdacosta/qgis_data/extrusion/footprintshp.shp|layername=footprintshp',
            'GRIDS': [
                appContext.layers.dsm.layer.dataProvider().dataSourceUri()
                # '/Users/arthurrufhosangdacosta/qgis_data/extrusion/dsm.tif'
            ],
            'RESAMPLING': 3,
            'RESULT': output
        }
    )

    footprint = appContext.update_layer(appContext, output, "footprint", "ogr", "vector")

    findex = footprint.dataProvider().fieldNameIndex("dsm")
    if findex != -1:
        footprint.dataProvider().renameAttributes({findex: "building_heigth"})
        footprint.updateFields()

    normalizer.equalize_layer("footprint", footprint, "vector")


def run_footprint():
    if appContext.user_parameters.footprint_getter.format == "algorithm":
        identify_footprint()
    extrude_footprint()


def save_files():
    if (appContext.user_parameters.ortho_output != ""):
        file_management.move_file(
            file_management.path_cleanup(appContext.layers.ortho.layer.dataProvider().dataSourceUri()),
            file_management.path_cleanup(appContext.user_parameters.ortho_output),
        )

    if (appContext.user_parameters.dtm_output != ""):
        file_management.move_file(
            file_management.path_cleanup(appContext.layers.dtm.layer.dataProvider().dataSourceUri()),
            file_management.path_cleanup(appContext.user_parameters.dtm_output),
        )

    if (appContext.user_parameters.dsm_output != ""):
        file_management.move_file(
            file_management.path_cleanup(appContext.layers.dsm.layer.dataProvider().dataSourceUri()),
            file_management.path_cleanup(appContext.user_parameters.dsm_output),
        )

    if (appContext.user_parameters.footprint_output != ""):
        file_management.move_file(
            file_management.path_cleanup(appContext.layers.footprint.layer.dataProvider().dataSourceUri()),
            file_management.path_cleanup(appContext.user_parameters.footprint_output),
        )


def load_layers_to_project():
    QgsProject.instance().addMapLayer(appContext.layers.ortho.layer)
    QgsProject.instance().addMapLayer(appContext.layers.dtm.layer)
    QgsProject.instance().addMapLayer(appContext.layers.dsm.layer)

    # Footprint
    symbol = d.QgsPolygon3DSymbol()
    symbol.setAddBackFaces(False)
    symbol.setAltitudeBinding(1)
    symbol.setAltitudeClamping(0)
    symbol.setCullingMode(0)

    symbol.setEdgesEnabled(True)
    symbol.setEdgeWidth(0.4)

    # symbol.setExtrusionHeight(QgsProperty.fromExpression('"dsm"'))

    renderer = d.QgsVectorLayer3DRenderer()
    renderer.setSymbol(symbol)

    materialSettings = d.QgsPhongMaterialSettings()
    materialSettings.setAmbient(QColor(246, 141, 131))
    materialSettings.setDiffuse(QColor(179, 179, 179))
    materialSettings.setSpecular(QColor(255, 0, 0))
    symbol.setMaterial(materialSettings)

    appContext.layers.footprint.layer.setRenderer3D(renderer)
    # renderer.setLayer(appContext.layers.footprint.layer)
    QgsProject.instance().addMapLayer(appContext.layers.footprint.layer)


def generate_3d_model():
    run_footprint()
    save_files()
    load_layers_to_project()


# a = ['Actions', 'AddToSelection', 'AllStyleCategories', 'AttributeTable', 'Cross', 'CustomProperties', 'Diagrams',
#      'EditFailed', 'EditResult', 'EmptyGeometry', 'FastInsert', 'FeatureAvailability', 'FeaturesAvailable',
#      'FeaturesMaybeAvailable', 'FetchFeatureFailed', 'Fields', 'Flag', 'Flags', 'Forms', 'GeometryOptions',
#      'Identifiable', 'IntersectSelection', 'InvalidLayer', 'Labeling', 'LayerConfiguration', 'LayerFlag', 'LayerFlags',
#      'LayerOptions', 'LayerType', 'MapTips', 'MeshLayer', 'Metadata', 'NoFeaturesAvailable', 'NoMarker', 'PluginLayer',
#      'PropertyType', 'RasterLayer', 'RegeneratePrimaryKey', 'Removable', 'RemoveFromSelection', 'Rendering',
#      'Searchable', 'SelectBehavior', 'SemiTransparentCircle', 'SetSelection', 'SinkFlag', 'SinkFlags', 'Style',
#      'StyleCategories', 'StyleCategory', 'Success', 'Symbology', 'Symbology3D', 'VectorLayer', 'VertexMarkerType',
#      '__bool__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
#      '__getattr__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__len__',
#      '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
#      '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'abstract', 'actions', 'addAttribute', 'addCurvedPart',
#      'addCurvedRing', 'addExpressionField', 'addFeature', 'addFeatures', 'addJoin', 'addPart', 'addPartV2', 'addRing',
#      'addTopologicalPoints', 'afterRollBack', 'aggregate', 'allFeatureIds', 'allowCommitChanged', 'appendError',
#      'attributeAdded', 'attributeAlias', 'attributeAliases', 'attributeDeleted', 'attributeDisplayName',
#      'attributeList', 'attributeTableConfig', 'attributeValueChanged', 'attribution', 'attributionUrl',
#      'autoRefreshInterval', 'autoRefreshIntervalChanged', 'auxiliaryLayer', 'beforeAddingExpressionField',
#      'beforeCommitChanges', 'beforeEditingStarted', 'beforeModifiedCheck', 'beforeRemovingExpressionField',
#      'beforeRollBack', 'beginEditCommand', 'blendMode', 'blendModeChanged', 'blockSignals', 'boundingBoxOfSelected',
#      'capabilitiesString', 'changeAttributeValue', 'changeAttributeValues', 'changeGeometry', 'childEvent', 'children',
#      'clone', 'commitChanges', 'commitErrors', 'committedAttributeValuesChanges', 'committedAttributesAdded',
#      'committedAttributesDeleted', 'committedFeaturesAdded', 'committedFeaturesRemoved', 'committedGeometriesChanges',
#      'conditionalStyles', 'configChanged', 'connectNotify', 'constraintDescription', 'constraintExpression',
#      'countSymbolFeatures', 'createExpressionContext', 'createExpressionContextScope', 'createMapRenderer', 'crs',
#      'crsChanged', 'customEvent', 'customProperty', 'customPropertyKeys', 'dataChanged', 'dataComment', 'dataProvider',
#      'dataSourceChanged', 'dataUrl', 'dataUrlFormat', 'decodedSource', 'defaultValue', 'defaultValueDefinition',
#      'deleteAttribute', 'deleteAttributes', 'deleteFeature', 'deleteFeatures', 'deleteLater', 'deleteSelectedFeatures',
#      'deleteStyleFromDatabase', 'deleteVertex', 'dependencies', 'dependenciesChanged', 'deselect', 'destroyEditCommand',
#      'destroyed', 'diagramLayerSettings', 'diagramRenderer', 'diagramsEnabled', 'disconnect', 'disconnectNotify',
#      'displayExpression', 'displayExpressionChanged', 'displayField', 'drawVertexMarker', 'dumpObjectInfo',
#      'dumpObjectTree', 'dynamicPropertyNames', 'editBuffer', 'editCommandDestroyed', 'editCommandEnded',
#      'editCommandStarted', 'editFormConfig', 'editFormConfigChanged', 'editingStarted', 'editingStopped',
#      'editorWidgetSetup', 'emitStyleChanged', 'encodedSource', 'endEditCommand', 'error', 'event', 'eventFilter',
#      'excludeAttributesWfs', 'excludeAttributesWms', 'exportNamedMetadata', 'exportNamedStyle', 'exportSldStyle',
#      'expressionField', 'extensionPropertyType', 'extent', 'featureAdded', 'featureBlendMode',
#      'featureBlendModeChanged', 'featureCount', 'featureDeleted', 'featuresDeleted', 'fieldConstraints',
#      'fieldConstraintsAndStrength', 'fields', 'findChild', 'findChildren', 'flags', 'flagsChanged', 'flushBuffer',
#      'formatLayerName', 'generateId', 'geometryChanged', 'geometryOptions', 'geometryType', 'getFeature', 'getFeatures',
#      'getGeometry', 'getSelectedFeatures', 'getStyleFromDatabase', 'hasAutoRefreshEnabled', 'hasDependencyCycle',
#      'hasFeatures', 'hasScaleBasedVisibility', 'htmlMetadata', 'id', 'importNamedMetadata', 'importNamedStyle',
#      'inherits', 'insertVertex', 'installEventFilter', 'invertSelection', 'invertSelectionInRectangle',
#      'isAuxiliaryField', 'isEditCommandActive', 'isEditable', 'isInScaleRange', 'isModified',
#      'isRefreshOnNotifyEnabled', 'isSignalConnected', 'isSpatial', 'isValid', 'isWidgetType', 'isWindowType',
#      'joinBuffer', 'keywordList', 'killTimer', 'labeling', 'labelingFontNotFound', 'labelsEnabled', 'layerModified',
#      'legend', 'legendChanged', 'legendUrl', 'legendUrlFormat', 'listStylesInDatabase', 'loadAuxiliaryLayer',
#      'loadDefaultMetadata', 'loadDefaultStyle', 'loadNamedMetadata', 'loadNamedMetadataFromDatabase', 'loadNamedStyle',
#      'loadNamedStyleFromDatabase', 'loadSldStyle', 'mapTipTemplate', 'mapTipTemplateChanged', 'materialize',
#      'maximumScale', 'maximumValue', 'metaObject', 'metadata', 'metadataChanged', 'metadataUri', 'metadataUrl',
#      'metadataUrlFormat', 'metadataUrlType', 'minimumScale', 'minimumValue', 'modifySelection', 'moveToThread',
#      'moveVertex', 'moveVertexV2', 'name', 'nameChanged', 'objectName', 'objectNameChanged', 'opacity',
#      'opacityChanged', 'originalXmlProperties', 'parent', 'primaryKeyAttributes', 'property', 'providerType',
#      'publicSource', 'pyqtConfigure', 'raiseError', 'readCommonStyle', 'readCustomProperties', 'readCustomSymbology',
#      'readExtentFromXml', 'readLayerXml', 'readOnly', 'readOnlyChanged', 'readSld', 'readStyle', 'readStyleManager',
#      'readSymbology', 'readXml', 'recalculateExtents', 'receivers', 'referencingRelations', 'refreshOnNotifyMessage',
#      'reload', 'removeCustomProperty', 'removeEventFilter', 'removeExpressionField', 'removeFieldAlias',
#      'removeFieldConstraint', 'removeJoin', 'removeSelection', 'renameAttribute', 'renderer', 'renderer3D',
#      'renderer3DChanged', 'rendererChanged', 'repaintRequested', 'resolveReferences', 'rollBack', 'saveDefaultMetadata',
#      'saveDefaultStyle', 'saveNamedMetadata', 'saveNamedStyle', 'saveSldStyle', 'saveStyleToDatabase', 'select',
#      'selectAll', 'selectByExpression', 'selectByIds', 'selectByRect', 'selectedFeatureCount', 'selectedFeatureIds',
#      'selectedFeatures', 'selectionChanged', 'sender', 'senderSignalIndex', 'setAbstract', 'setAttributeTableConfig',
#      'setAttribution', 'setAttributionUrl', 'setAutoRefreshEnabled', 'setAutoRefreshInterval', 'setAuxiliaryLayer',
#      'setBlendMode', 'setConstraintExpression', 'setCoordinateSystem', 'setCrs', 'setCustomProperties',
#      'setCustomProperty', 'setDataSource', 'setDataUrl', 'setDataUrlFormat', 'setDefaultValueDefinition',
#      'setDependencies', 'setDiagramLayerSettings', 'setDiagramRenderer', 'setDisplayExpression', 'setEditFormConfig',
#      'setEditorWidgetSetup', 'setError', 'setExcludeAttributesWfs', 'setExcludeAttributesWms', 'setExtent',
#      'setFeatureBlendMode', 'setFieldAlias', 'setFieldConstraint', 'setFlags', 'setKeywordList', 'setLabeling',
#      'setLabelsEnabled', 'setLayerOrder', 'setLegend', 'setLegendUrl', 'setLegendUrlFormat', 'setMapTipTemplate',
#      'setMaximumScale', 'setMetadata', 'setMetadataUrl', 'setMetadataUrlFormat', 'setMetadataUrlType',
#      'setMinimumScale', 'setName', 'setObjectName', 'setOpacity', 'setOriginalXmlProperties', 'setParent',
#      'setProperty', 'setProviderEncoding', 'setProviderType', 'setReadExtentFromXml', 'setReadOnly',
#      'setRefreshOnNofifyMessage', 'setRefreshOnNotifyEnabled', 'setRenderer', 'setRenderer3D',
#      'setScaleBasedVisibility', 'setShortName', 'setSimplifyMethod', 'setSubLayerVisibility', 'setSubsetString',
#      'setTitle', 'setTransformContext', 'setValid', 'shortName', 'signalsBlocked', 'simplifyDrawingCanbeApplied',
#      'simplifyMethod', 'source', 'sourceCrs', 'sourceExtent', 'sourceName', 'splitFeatures', 'splitParts',
#      'startEditing', 'startTimer', 'staticMetaObject', 'statusChanged', 'storageType', 'styleChanged', 'styleManager',
#      'styleURI', 'subLayers', 'subsetString', 'subsetStringChanged', 'symbolFeatureCountMapChanged', 'thread',
#      'timerEvent', 'timestamp', 'title', 'tr', 'transformContext', 'translateFeature', 'triggerRepaint', 'type',
#      'undoStack', 'undoStackStyles', 'uniqueStringsMatching', 'uniqueValues', 'updateExpressionField', 'updateExtents',
#      'updateFeature', 'updateFields', 'updatedFields', 'vectorJoins', 'willBeDeleted', 'wkbType', 'writeCommonStyle',
#      'writeCustomProperties', 'writeCustomSymbology', 'writeLayerXml', 'writeSld', 'writeStyle', 'writeStyleManager',
#      'writeSymbology', 'writeXml']
