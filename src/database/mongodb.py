"""
Generic MongoDB set up architecture.

"""

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from arctic import Arctic
from arctic import VERSION_STORE
from arctic import CHUNK_STORE
from arctic import TICK_STORE
import pandas as pd

# This can be hidden in an encrypted file
mongodb_host = "mongo host details"
mongodb_port = 12345
arctic_connection = "some arctic connection string"


# Database navigation
# -------------------
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

    client = MongoClient(mongodb_host, mongodb_port)

    # Check connection to mongodb
    try:
        client["non_arctic"].list_collection_names()
    except ServerSelectionTimeoutError:
        raise ServerSelectionTimeoutError("MongoDB not hosted.")

    # 'arctic' connection
    if is_arctic is True:
        db_connection = Arctic(arctic_connection)
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


# Symbol (arctic) or Key (non-arctic)
# ------------------------------------
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
        collection = db_connect(is_arctic=False, lib_name=lib_name)

        try:
            docs = collection.find_one()
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


# -----------------
# Arctic functions
# -----------------
def db_arctic_library(library=None):
    """
    Quick function to return arctic store or list of library names in arctic database.

    Parameter
    ---------
        library : str, None
            If None, returns lists of available library names

    Returns
    --------
        arctic store

    """

    store = db_connect(is_arctic=True, lib_name=library)

    if library is None:
        return store.list_libraries()

    else:
        return store


# ------------------------
# Arctic helper functions
# ------------------------
def db_arctic_initialise(lib_name: str, lib_type: str):
    """
    To initialise new arctic library.

    Parameters
    ----------
    lib_name
        Name of the new library to create.
    lib_type
        Acceptable types ["VERSION_STORE", "CHUNK_STORE", "TICK_STORE"]

    """
    arctic_stores = [VERSION_STORE, CHUNK_STORE, TICK_STORE]

    if lib_type not in arctic_stores:
        raise KeyError(f"Library store must be an arctic store type: {VERSION_STORE}, {CHUNK_STORE}, "
                       f"{TICK_STORE}")

    lib = db_connect(is_arctic=True, lib_name=None)

    lib.initialize_library(lib_name, lib_type=lib_type)

    # This is important because arctic will not show the existing libraries upon creation of a new library.
    Arctic.reload_cache(lib)


def db_arctic_write(df, symbol, lib_name=None):
    """
    Writing to existing arctic library.

    Parameters
    ----------
        df : df
            Dataframe to write into library
        symbol : str
            Name of symbol
        lib_name : str
            Name of arctic library to write on

    """

    assert lib_name is not None, "lib_name must be passed in to specify library to write."

    lib = db_connect(is_arctic=True, lib_name=lib_name)
    lib.write(symbol, df)


def db_arctic_append(df, symbol, lib_name=None):
    """
    Appending existing arctic library.

    Parameters
    ----------
        df : pd.DataFrame
        symbol : str
            Name of symbol
        lib_name : str
            Name of arctic library to append on

    """

    assert lib_name is not None, "lib_name must be passed in to specify library to append."
    lib = db_connect(is_arctic=True, lib_name=lib_name)
    lib.append(symbol, df, upsert=True)


# --------------------
# Non_arctic functions
# --------------------
def db_non_arctic_library(lib_name: str = None):
    """
    Return pymongo collection or list of collection names in non_arctic database.

    Parameters
    ----------
    lib_name
        If None, returns list of available collection names

    Returns
    --------
    Collection
    """
    cl = db_connect(is_arctic=False, lib_name=lib_name)

    if lib_name is None:
        return cl.list_collection_names()
    else:
        return cl


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


