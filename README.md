# automation with Python
Repository containing useful tools to equip the user when automating processes with Python.
<p align="center">
  <br>
  <img src="img/automation-robot.png">
  <br>
  <i>Why automation is important.</i>
</p>

## Module Breakdowns
Below you will find a short summary of each module and its specific use case.

### mongodb.py
Generic functions to assist the set up and use of PyMongo and Arctic library.

PyMongo, the python package for MongoDB.

https://pymongo.readthedocs.io/en/stable/

Arctic, a high performance database that sits atop MongoDB. Useful for time series and dataframe data.

https://arctic.readthedocs.io/en/latest/

Main function 'db_connect' expects your databases to be categorised as 'arctic' or 'non_arctic'(default mongodb). It returns an 'arctic connection' or 'pymongo collection' based on the defined parameters. The 2 parameters are 'is_arctic' to specify arctic/non arctic database and 'lib_name', which is the name of the library to connect to.

The function is passed onto other functions to manipulate the libraries such as creation/deletion of a library, append or write to a library or list the keys and symbols.
