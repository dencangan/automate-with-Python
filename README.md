# automate with Python
This repository contains useful tools to equip the user when automating processes with Python. The tools in the repository relies heavily on the use of NumPy and Pandas when dealing with data. The readme can be split into three parts: general introduction, module breakdowns and conclusion.

## Introduction
<p align="center">
  <br>
  <img src="img/automation-robot.png">
  <br>
  <i>Why automation is important.</i>
</p>

## Module Breakdowns
Below you will find a short summary of each module and its specific use case.

### excel.py
Quick and easy automation with the use of some excel functions. With the use of pandas we can read excel files and output them into dictionary with the keys as the sheet name and values as 2D dataframes. There is also a function that helps with running inbuilt excel macros automatically.

### files.py
Generic functions to read, write, copy, or arrange your local files. The class object 'Files' contains class instances for path of folder directory (folder_directory) and name of the file (file_name). 

### decorators.py
Decorators: 'timer' to time function run time in seconds and 'deprecated' to warn users of a deprecated function.

### mongodb.py
MongoDB is a popular noSQL database for modern apps using cloud technologies. In this module you will find generic functions to assist the set up and use of modules PyMongo and Arctic library.

[PyMongo](https://pymongo.readthedocs.io/en/stable/), the python package for MongoDB.  
[Arctic](https://arctic.readthedocs.io/en/latest/), a high performance database that sits atop MongoDB. This is catered to the storage of time series and dataframe data.

Main function 'db_connect' expects your databases to be categorised as 'arctic' or 'non_arctic'(default mongodb). It returns an 'arctic connection' or 'pymongo collection' based on the defined parameters. The 2 parameters are 'is_arctic' to specify arctic/non arctic database and 'lib_name', which is the name of the library to connect to.

The function is passed onto other functions to manipulate the libraries such as creation/deletion of a library, append or write to a library or list the keys and symbols.
