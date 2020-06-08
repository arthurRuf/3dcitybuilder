layer = QgsVectorLayer('Point', 'points', "memory")
pr = layer.dataProvider()
# add the first point
pt = QgsFeature()
point1 = QgsPointXY(extent.xMaximum(), extent.yMaximum())
pt.setGeometry(QgsGeometry.fromPoint(point1))
pr.addFeatures([pt])
# update extent of the layer
layer.updateExtents()
# add the second point
pt = QgsFeature()
point2 = QgsPointXY(extent.xMinimum(), extent.yMinimum())
pt.setGeometry(QgsGeometry.fromPoint(point2))
pr.addFeatures([pt])
# update extent
layer.updateExtents()
# add the layer to the canvas
QgsProject.instance().addMapLayers([layer])

layer = QgsVectorLayer('Polygon', 'poly', "memory")
pr = layer.dataProvider()
poly = QgsFeature()
points = [
    QgsPointXY(
        extent.xMinimum(),
        extent.yMaximum()
    ),
    QgsPointXY(
        extent.xMaximum(),
        extent.yMaximum()
    ),
    QgsPointXY(
        extent.xMaximum(),
        extent.yMinimum()
    ),
    QgsPointXY(
        extent.xMinimum(),
        extent.yMinimum()
    )
]
# or points = [QgsPointXY(50,50),QgsPointXY(50,150),QgsPointXY(100,150),QgsPointXY(100,50)]
poly.setGeometry(QgsGeometry.fromPolygon([points]))
pr.addFeatures([poly])
layer.updateExtents()
QgsProject.instance().addMapLayers([layer])



##############################################

viewport_memory_layer = QgsVectorLayer(f"Polygon?crs={QgsProject.instance().crs().toWkt()}", "viewport", "memory")
# viewport_memory_layer = QgsVectorFileWriter(f"{appContext.execution.raw_temp_folder}/viewport.shp", "viewport", "ogr")

# if viewport_memory_layer.isValid():
#     raise Exception("Error!")

extent = appContext.qgis.iface.mapCanvas().extent()

# viewport_memory_layer.startEditing()
feature = QgsFeature()
feature.setGeometry(QgsGeometry.fromPolygonXY([
    [
        QgsPointXY(
            extent.xMinimum(),
            extent.yMaximum()
        ),
        QgsPointXY(
            extent.xMaximum(),
            extent.yMaximum()
        ),
        QgsPointXY(
            extent.xMaximum(),
            extent.yMinimum()
        ),
        QgsPointXY(
            extent.xMinimum(),
            extent.yMinimum()
        ),
    ]
]))
viewport_memory_layer.addFeature(feature)
viewport_memory_layer.commitChanges()

QgsProject.instance().addMapLayer(viewport_memory_layer)

return viewport_memory_layer



