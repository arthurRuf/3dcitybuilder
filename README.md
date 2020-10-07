# 3D City Builder
This QGIS Plugin generates 3D Models of Urban Areas using Aerial Imagery (Satellite Image), DTM (Digital Terrain Model), DSM (Digital Surface Model) and a Footprint layer (the contour of the buildings) from both, files stored on your computer and online.

This plugin requires QGIS 3.0 or superior

To see it on QGIS Plugin Repository, go to: https://plugins.qgis.org/plugins/citygen/

If you want to help in this project I'll be glad :D
Plus, if you have any suggestins, please, let me know :D

I appreciate any help to make this code compliant with PEP8. 

**Vienna, Austria**
![Result in Vienna, Austria](https://github.com/arthurRuf/3dcitybuilder/blob/main/docs/austria_vienna.gif?raw=true)

**Cities of Itajaí and Navegantes, Santa Catarina, Brazil**
![Result in the cities of Itajaí and Navegantes, Santa Catarina, Brazil](https://github.com/arthurRuf/3dcitybuilder/blob/main/docs/brazil_itajai_and_navegantes.gif?raw=true)

 
## Installing

"Stable" releases are available through the official QGIS plugins repository.

1. In QGIS 3 select Plugins->Manage and Install Plugins...
2. On the sidebar go to `Settings` and check the `Show also experimental plugins` checkbox
3. Now, go to `All` on the sidebar and search for `3D City Generator`. Select the plugin and click `Install Plugin` 

After installing the plugin, please run these commands on the terminal
```shell script
brew reinstall libcapn
brew install capnp
brew install spatialindex
```

Opitionally, you can run these commands on the QGIS Python
```shell script
python3 -m pip install geopandas numpy osmnx
```
Opitionally, you can follow the steps under https://landscapearchaeology.org/2018/installing-python-packages-in-qgis-3-for-windows/ to install the following libraries on QGIS Python: geopandas numpy osmnx.

## Using

To run the 3D City Generator, just follow this steps:
1. Go to the menu `Plugins >> citygen >> 3D City Generator` to open the plugin.
2. Fill the information on `Definitions` and `Advanced` tabs. Then click `Run`.
3. Close the Plugins' window, go to `View >> New 3D Map View`
4. Have fun :D

Animation demonstrating how to use this Plugin
![Image demonstrating how to use the plugin](https://github.com/arthurRuf/3dcitybuilder/blob/main/docs/how-to-use.gif?raw=true)


A sample dataset is available to:
To make it easier for you to test this plugin, we've made available a sample dataset: 
 * Vienna, Austria: https://3dcitygen-test-dataset.s3.amazonaws.com/test-dataset-vienna.zip


## Development

You can use `make` to assist you while developing.

The following rules can be useful:
* `make deploy`: will automatically copy the required files to your QGIS plugins' folder. **BEWARE:** *it only works out-of-the-box for macOS. For other operating systems you might have to change the `QGISDIR` variable in `Makefile`.*
* `make package VERSION=GIT_REF`: (where *GIT_REF* is a branch, tag or any other git ref) will make a zip package to be installed manually from QGIS or uploaded to the QGIS plugins' repository.

## License
The project is licensed under the GNU GPLv2 license.

You are free to download, modify and redistribute this plugin, since you reference this repo ;D


**Third Party Licences**
  * geopandas: © GeoPandas - BSD Licence (https://geopandas.org/)
  * numpy: © NumPy - BSD Licence (https://www.numpy.org)
  * osmnx: © OSMnx - MIT Licence (https://github.com/gboeing/osmnx)

