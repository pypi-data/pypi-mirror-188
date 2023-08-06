# Dozer
Flattens unstructured data into a relation format

## Installation 
```commandline
pip install pybulldozer
```

## Features
pybulldozer aims to make working with non-relation data files as easy as possible

#### Explore the structure of the file
- statistics
- structure
- attributes

#### Flatten the file to record-arrays
Returns a dictionary that contains a {name: record-array} for all layers in the file


## File formats
Currenty pybulldozer only works with xml

## Future development
 - Parse more data formats
 - Speed optimization
 - Create SQL insert statements