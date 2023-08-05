Python CLI wrapper for Maastricht's json avu.
Takes a JSON file and annotates an iRODS object accordingly.


## Usage


On the command line you can use the module with the following command:

schema2avu [-h] -j JSON d|C|R file

positional arguments:\
&emsp; d|C|R &emsp;&emsp;&emsp;&emsp; the irods resource type [d=data objects (file), C=collection (directory), R=resources]\
&emsp;  file &emsp;&emsp;&emsp;&emsp;&emsp; path to data object, collection or resource

Defining input Files:\
&emsp;-j JSON, --json &emsp;JSON  defines json schema input


## Acknowledgments
A lot of thanks to Christian Meesters who provided the initial script and who will publish an improved 
version later.