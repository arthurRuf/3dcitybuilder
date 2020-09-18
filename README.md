# 3dcitybuilder
This QGIS Plugin generates 3D Models of Urban Areas using Aerial Imagery (Satellite Image), DTM (Digital Terrain Model), DSM (Digital Surface Model) and a Footprint layer (the contour of the buildings) from both, files stored on your computer or online.

**Requirements**
1. QGIS 3.0 or superior

## Result Demo

**Vienna, Austria**
![Result in Vienna, Austria](https://github.com/arthurRuf/3dcitybuilder/blob/master/docs/austria_vienna.gif?raw=true)

**Cities of Itajaí and Navegantes, Santa Catarina, Brazil**
![Result in the cities of Itajaí and Navegantes, Santa Catarina, Brazil](https://github.com/arthurRuf/3dcitybuilder/blob/master/docs/brazil_itajai_and_navegantes.gif?raw=true)

 
## Installing

"Stable" releases are available through the official QGIS plugins repository.

1. In QGIS 3 select Plugins->Manage and Install Plugins...
2. On the sidebar go to `Settings` and check the `Show also experimental plugins` checkbox
3. Now, go to `All` on the sidebar and search for `3D City Generator`. Select the plugin and click `Install Plugin` 


## Using

To run the 3D City Generator, just follow this steps:
1. Go to the menu `Plugins >> citygen >> 3D City Generator` to open the plugin.
2. Fill the information on `Definitions` and `Advanced` tabs. Then click `Run`.
3. Close the Plugins' window, go to `View >> New 3D Map View`
4. Have fun :D

Animation demonstrating how to use this Plugin
![Image demonstrating how to use the plugin](https://github.com/arthurRuf/3dcitybuilder/blob/master/docs/how-to-use.gif?raw=true)


## Development

You can use `make` to assist you while developing.

The following rules can be useful:
* `make deploy`: will automatically copy the required files to your QGIS plugins' folder. **BEWARE:** *it only works out-of-the-box for macOS. For other operating systems you might have to change the `QGISDIR` variable in `Makefile`.*
* `make package VERSION=GIT_REF`: (where *GIT_REF* is a branch, tag or any other git ref) will make a zip package to be installed manually from QGIS or uploaded to the QGIS plugins' repository.
