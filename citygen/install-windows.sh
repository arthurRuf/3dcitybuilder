#conda activate project_ttc
pb_tool compile
rmdir C:\Users\USER\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\citygen
Xcopy /E /I ..\citygen\ C:\Users\USER\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\citygen\
echo
echo Done!


# export PYTHONPATH="$PYTHONPATH:/Applications/QGIS3.12.app/Contents/MacOS/bin/python3"

