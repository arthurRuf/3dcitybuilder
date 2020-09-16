# 3dcitybuilder
QGIS Plugin that creates 3D Models of Urban Areas using online databases or files stored locally.

To generate the 3D Model, this plugin uses Aerial Imagery (Satellite Image), DTM (Digital Terrain Model), DSM (Digital Surface Model) and a Footprint layer (the contour of the buildings).

This plugin requires QGIS 3.0 or superior.

Vienna, Austria:
![Result in Vienna, Austria](https://github.com/arthurRuf/3dcitybuilder/blob/master/docs/austria_vienna.gif?raw=true)

Cities of Itajaí and Navegantes, Santa Catarina, Brazil
![Result in the cities of Itajaí and Navegantes, Santa Catarina, Brazil](https://github.com/arthurRuf/3dcitybuilder/blob/master/docs/brazil_itajai_and_navegantes.gif?raw=true)


## Instalation

After installing the plugin, please run these commands on the terminal
```shell script
brew reinstall libcapn
brew install capnp
brew install spatialindex
```

Then, on the QGIS Python, run these commands
```shell script
python3  -m pip install 
```


## Usage

Demonstration of using the Plugin
![Plugin Usage Demonstration](https://github.com/arthurRuf/3dcitybuilder/blob/master/docs/brazil_itajai_and_navegantes.gif?raw=true)



## ToDo
