"""
File handling type functions.
"""
import os
import shutil
import zipfile


def read_zip(zip_file, file_name):
    """Opens contents of zip file without extraction, can be read using pandas if dataframe like"""
    zip_extraction = zipfile.ZipFile(zip_file, 'r')
    file = zip_extraction.open(file_name)
    return file


def check_file_exists(files):

    if isinstance(files, list):
        # Testing all directories
        for file in files:
            assert os.path.exists(file), f"{file} not found"

    else:
        assert os.path.exists(files), f"{files} not found"


def copy_file(src, des, src_name=None, des_name=None):
    """
    Basic copy function

    Parameters
    ----------
        src : str
            Source to file to copy
        des : str
            Destination to copy file to
        src_name : str
            Specify file name if needed (for loop runs)
        des_name : str
            New file name
    """
    if src_name is not None:
        src = os.path.join(src, src_name)

    if des_name is not None:
        des = os.path.join(des, des_name)

    shutil.copy(src, des)

