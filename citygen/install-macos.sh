#conda activate project_ttc
pb_tool compile
rm -rf /System/Volumes/Data/Users/arthurrufhosangdacosta/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/citygen
cp -R ../citygen/ /System/Volumes/Data/Users/arthurrufhosangdacosta/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/citygen/
echo
echo Done!
