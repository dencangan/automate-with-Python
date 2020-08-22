import unittest
import os
import re
import pandas as pd
from time import time


def unit_test_analysis(src_dir, test_file_prefix='test_', test_def_prefix='test_', ignore_modules=None,
                       ignore_packages=None):
    """
    Checks packages for unittests and looks for test files corresponding for each module.

    Parameters
    ----------
    src_dir : str
        Directory containing packages (src folder).
    test_file_prefix: str, defaults to 'test_' so it will look for 'test_{module.py}'.
        Prefix for unit test file, default 'test_' - e.g. look for 'test_' + module.py.
    test_def_prefix : str
        Prefix for unit test def, default 'test_' - e.g. will count lines '^def test_.*'.
    ignore_modules : list
        Package files to ignore, default None.
    ignore_packages : list
        Packages to ignore, default None.

    Return
    -------
    df : pd.DataFrame
        Summary of unit tests in the library.
    """
    print('-' * 40)
    print(f"\n\nRunning unit test analysis.\n\n")
    print('-' * 40)

    # Getting list of packages from src
    pkg_dirs = [os.path.join(src_dir, i)
                for i in os.listdir(src_dir)
                if os.path.isdir(os.path.join(src_dir, i))]

    # Check if there is a subpackage called 'tests' in each package
    have_test_dir = {os.path.basename(i): 'tests' in os.listdir(i) for i in pkg_dirs}

    pkg_and_modules = dict()
    for i in pkg_dirs:
        pkg_and_modules[os.path.basename(i)] = [j for j in os.listdir(i) if bool(re.search('\.py$', j))]

    # package -> modules -> test details
    full_dict = dict()
    for pkg_name, lst_of_modules in pkg_and_modules.items():
        # Packages containing subpackages 'tests'
        if have_test_dir[pkg_name]:
            ut_dir = os.path.join(src_dir, pkg_name, 'tests')
            # Listing test modules within the subpackage
            ut_files = os.listdir(ut_dir)
            # To nest dictionary
            full_dict[pkg_name] = {}
            for m in lst_of_modules:
                # Concatenate 'test_' + module.py
                test_module = test_file_prefix + m
                if test_module in ut_files:
                    # read in the file, count the number of lines begining with def (or 'def test')
                    # read the number of lines in file
                    with open(os.path.join(ut_dir, test_module)) as fp:
                        content = fp.readlines()
                    test_defs = [c for c in content if bool(re.search(f'^def {test_def_prefix}', c.lstrip()))]
                    has_unit_tests, num_test_def, num_test_lines = True, len(test_defs), len(content)
                else:
                    has_unit_tests, num_test_def, num_test_lines = False, 0, 0

                full_dict[pkg_name][m] = {"has_unit_test": has_unit_tests,
                                          "num_test_def": num_test_def,
                                          "num_test_lines": num_test_lines}
        else:
            print(f"Excluding package '{pkg_name}' as it does not have subpackage 'tests'.")

    df = pd.DataFrame.from_dict({(i, j): full_dict[i][j]
                                 for i in full_dict.keys()
                                 for j in full_dict[i].keys()},
                                orient="index")
    df.index.names = ["Package", "Module"]
    df = df.reset_index()

    if ignore_modules:
        print(f'Ignoring modules: {ignore_modules}')
        df = df.loc[~df['Module'].isin(ignore_modules)]

    if ignore_packages:
        print(f'Ignoring packages: {ignore_packages}')
        df = df.loc[~df['Package'].isin(ignore_packages)]

    print("\n")
    print('-' * 60)
    # files with unit tests
    fwut = pd.pivot_table(df, index=['Package'], values='has_unit_test', aggfunc='mean')
    fwut.sort_values('has_unit_test', ascending=False, inplace=True)
    print('Unit Test Coverage (% of modules with unit test per package)')
    print('-' * 60)
    fwut['has_unit_test'] *= 100
    fwut.rename(columns={'has_unit_test': 'Coverage %'}, inplace=True)
    print(fwut.reset_index(), "\n\n")

    # unit tests per package
    num_test_per_pkg = pd.pivot_table(df, index=['Package'], values='num_test_def', aggfunc='sum')
    num_test_per_pkg.sort_values('num_test_def', ascending=False, inplace=True)
    num_test_per_pkg.rename(columns={'num_test_def': 'Test Functions Count'}, inplace=True)
    print(num_test_per_pkg.reset_index(), "\n\n")

    return df


def run_tests(src_dir, paths):
    t = time()
    test_summary = dict()
    for pth in paths:
        print("\n")
        print('-' * 60)
        print(f"\nRunning tests in: {pth}\n")
        print('-' * 60)
        loader = unittest.TestLoader()
        tp = os.path.join(src_dir, pth)
        suite = loader.discover(tp, pattern="test_*.py")

        # Change buffer to False if you want don't want to suppress print statements
        runner = unittest.TextTestRunner(verbosity=2, buffer=True).run(suite)
        if runner.failures or runner.errors:
            status = "FAILED"
        else:
            status = "PASSED"
        test_summary[pth] = {"STATUS": status,
                             "FAILURES": len(runner.failures),
                             "ERRORS": len(runner.errors)}
    print(f"\nAll tests finished after {(time() - t)} seconds.")
    print(pd.DataFrame.from_dict(test_summary, orient="index"))


if __name__ == "__main__":

    # Point to src folder
    main_dir = os.path.abspath(os.path.dirname(__file__))

    summary = unit_test_analysis(src_dir=main_dir,
                                 test_file_prefix='test_',
                                 test_def_prefix='test_', ignore_modules=['__init__.py'])

    run_tests(src_dir=main_dir, paths=["src/tests"])