"""
Excel related automation functions.
"""

import win32com.client
import pandas as pd


def run_excel_macros(path_to_workbook, close_workbook=False, *macros):
    """
    Function to run existing Excel macros

    Parameter
    ---------
    path_to_workbook : str
        Excel file path.
    close_workbook : bool
        Toggle closing the workbook once macros have run.
    macros : str, args
        Naming convention should look something like "module1.macro1", module followed by name of macro.

    """

    x1 = win32com.client.Dispatch("Excel.Application")
    try:
        wb = x1.Workbooks.Open(path_to_workbook)

        for macro in macros:
            wb.Application.Run(macro)

        if close_workbook is True:
            # Saves the workbook too
            wb.Close(True)

        del wb
        del x1

    except Exception as error:
        print(error)


def read_excel(path_to_workbook, sheet=None):
    """Read excel files with multiple sheets"""

    if path_to_workbook.endswith(".csv"):
        df_csv = pd.read_csv(path_to_workbook)
        return df_csv

    else:
        if sheet is not None:
            print(f"Reading sheet '{sheet}' from {path_to_workbook}")
            df_excel_sheet = pd.read_excel(path_to_workbook, sheet_name=sheet)

        else:
            print(f"Reading whole workbook...")
            df_excel_sheet = pd.read_excel(path_to_workbook, sheet_name=None)
            print(f"List of sheet names stored as key in dict: {df_excel_sheet.keys()}")

        return df_excel_sheet