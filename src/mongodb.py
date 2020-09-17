"""
MongoDB functions using PyMongo and Arctic library.
"""

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from arctic import Arctic, VERSION_STORE, CHUNK_STORE, TICK_STORE
import pandas as pd
from json import load

# Location to jsonified credentials
credentials = load(open(r""))
MONGO_USER = credentials["personal_db"]["username"]
MONGO_PASSWORD = credentials["personal_db"]["password"]
MONGO_DB_NAME = "personal"
MONGO_CONNECTION = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.m7iwb.azure.mongodb.net/{MONGO_DB_NAME}?retryWrites=true&w=majority"


def db_connect(is_arctic=True, lib_name=None):
    """Function to connect to mongodb database, arctic/non_arctic

    Args:
        is_arctic (bool): Specify arctic or non_arctic database.
        lib_name (str or optional): Name of library within database, defaults to None.

    Returns:
        lib_store (arctic.store.version_store.VersionStore)
        lib_collection (pymongo.collection.Collection)
        db_connection (arctic.arctic.Arctic or pymongo.database.Database): If lib_name is None.

    Notes:
        Returns arctic connection and lists available arctic libraries
            >>> db_connect(is_arctic=True, lib_name=None)
        Returns arctic versionStore
            >>> db_connect(is_arctic=True, lib_name="something")
        Returns pymongo connection and lists available non_arctic collections
            >>> db_connect(is_arctic=False, lib_name=None)
        Returns pymongo collection
            >>> db_connect(is_arctic=False, lib_name="something_else")

    Documentation:
        https://arctic.readthedocs.io/en/latest/
    """

    client = MongoClient(MONGO_CONNECTION)

    # Check connection to mongodb
    try:
        client["non_arctic"].list_collection_names()
    except ServerSelectionTimeoutError:
        raise ServerSelectionTimeoutError("MongoDB not hosted.")

    # 'arctic' connection
    if is_arctic is True:
        db_connection = Arctic(MONGO_CONNECTION)
        lib_lst = db_connection.list_libraries()

        if lib_name is not None:
            # Raise error if library does not exist in database
            assert lib_name in lib_lst, f"\nLibrary '{lib_name}' does not exist in 'arctic' database."
            lib_store = db_connection[lib_name]
            return lib_store

        else:
            print(f"\nList of libraries in 'arctic' database: ")
            print(lib_lst)
            return db_connection

    # 'non_arctic' connection
    elif is_arctic is False:
        db = "non_arctic"
        db_connection = client[db]
        lib_lst = db_connection.list_collection_names()

        if lib_name is not None:
            # Raise error if library does not exist in non_arctic database
            assert lib_name in lib_lst, f"\nLibrary '{lib_name}' does not exist in 'non_arctic' database."
            lib_collection = db_connection[lib_name]
            return lib_collection

        else:
            print(f"\nList of libraries in 'non_arctic' database: ")
            print(lib_lst)
            return db_connection

    else:
        raise TypeError("Specify bool for arctic/non_arctic database")


def db_keys_and_symbols(is_arctic, lib_name):
    """
    Returns list of keys in collection (arctic/non-arctic database).

    Parameters
    ----------
    is_arctic : bool
        True for arctic symbols, False for non_arctic keys
    lib_name : str
        Library name

    Returns
    -------
    keys / symbols : list
        List of symbols or keys depending on arctic/non-arctic database
    """

    # Non arctic keys
    if is_arctic is False:
        cl = db_connect(is_arctic=False, lib_name=lib_name)
        try:
            docs = cl.find_one()
            keys = []
            for x in docs:
                keys.append(x)
            return keys

        except AttributeError:
            print('\nIncorrect data type, mongodb collection should be the only acceptable type.')

    # Arctic symbols
    else:
        lib = db_connect(is_arctic=True, lib_name=lib_name)
        symbols = lib.list_symbols()
        return symbols


def db_arctic_new_library(name_library: str, lib_type=VERSION_STORE):
    """To initialise new arctic library."""
    if lib_type not in [VERSION_STORE, CHUNK_STORE, TICK_STORE]:
        raise KeyError(f"Library store must be an arctic store type: {VERSION_STORE}, {CHUNK_STORE}, "
                       f"{TICK_STORE}")
    c = db_connect(is_arctic=True, lib_name=None)
    c.initialize_library(library=name_library, lib_type=lib_type)
    # This is important because arctic will not show the existing libraries upon creation of a new library.
    Arctic.reload_cache(c)


def db_arctic_delete_library(name_library: str):
    """To delete existing arctic library."""
    c = db_connect(is_arctic=True, lib_name=None)
    confirm = input(f"Are you sure you want to delete arctic library {name_library}? (Y/N)")
    if confirm == "Y":
        print(f"Deleting library: '{name_library}'")
        c.delete_library(library=name_library)
        Arctic.reload_cache(c)
        print(f"'{name_library}' deleted.")
    else:
        print(f"Not deleting library: '{name_library}'.")


def db_arctic_amend(lib_name: str, df: pd.DataFrame, symbol: str, append: bool) -> None:
    """
    Make changes to an arctic library.

    Parameters
    ----------
    lib_name : str
        Name of arctic library to amend.
    df : pd.DataFrame
        Pandas dataframe to store in library.
    symbol : str
        Specify symbol for arctic library.
    append : bool
        True to *append* to library with existing symbol, False to *write* to library with new symbol.

    Returns
    -------
    None
    """

    lib = db_connect(is_arctic=True, lib_name=lib_name)
    if append:
        print(f"Appending {lib_name} library to symbol {symbol}.")
        lib.append(symbol, df, upsert=True)
    else:
        print(f"Writing {lib_name} library. Created new symbol {symbol}.")
        lib.write(symbol, df)


def db_non_arctic_read(lib_name: str, no_id: bool = True) -> pd.DataFrame:
    """
    Reading of non arctic data.

    Parameters
    ----------
    lib_name
        Only acceptable type.
    no_id : bool
        Specify if mongodb _id to be included in pd.dataframe

    Returns
    -------
    pd.DataFrame

    """

    cl = db_connect(is_arctic=False, lib_name=lib_name)

    # Make a query to the specific DB and Collection
    cursor = cl.find()

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor))

    # If no_id is True, delete _id column
    if no_id:
        del df['_id']

        return df


