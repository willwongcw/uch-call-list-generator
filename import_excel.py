import pandas as pd
import calendar
import numpy as np
from datetime import timedelta
from openpyxl.utils import get_column_letter
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import os
from openpyxl.styles import Alignment

def sanitize_value(value):
    #Sanitize the input value to be one of the allowed types: 1, 'x', or np.nan.
    if value == 1 or value == '1' or value == 1.0 or value == '1.0':
        return '1'
    elif value == 'x' or value == 'X':
        return 'x'
    elif pd.isnull(value):
        return 'NA'
    else:
        raise ValueError("Invalid value encountered.")

def read_excel(file_path):
    # Read the Excel file once to get the necessary metadata
    metadata = pd.read_excel(file_path, sheet_name=0, usecols=[1], nrows=5, header=None)

    # Extract year, month, and number of doctors from the metadata
    year = int(metadata.iat[2, 0])
    month = int(metadata.iat[3, 0])
    num_doctors_expected = int(metadata.iat[4, 0])

    # Read the Excel file to get the required data
    df_full = pd.read_excel(file_path, sheet_name=0, header=None, skiprows=7)

    # Extract the required columns into arrays
    expected_total = df_full.iloc[:, 0].values  # Column 'A'
    weekend_priority = df_full.iloc[:, 1].values  # Column 'B'
    sat_priority = df_full.iloc[:, 2].values  # Column 'C'
    sun_priority = df_full.iloc[:, 3].values  # Column 'D'
    drName = df_full.iloc[:, 5].values  # Column 'F'

    # Drop the columns you've already read into arrays and the doctors' names column
    df = df_full.drop(df_full.columns[[0, 1, 2, 3, 4, 5]], axis=1)

    # Generate the date column names based on the year and month
    days_in_month = calendar.monthrange(year, month)[1]
    date_column_names = [pd.Timestamp(year=year, month=month, day=day).strftime('%Y-%m-%d') for day in range(1, days_in_month + 1)]

    # Assign the generated date column names to your dataframe
    df.columns = date_column_names

    # Verify the number of doctors and dates
    num_doctors_actual = df.shape[0]
    num_dates_actual = df.shape[1]

    if num_doctors_actual != num_doctors_expected:
        raise ValueError(f"The number of doctors in the table ({num_doctors_actual}) does not match the expected value ({num_doctors_expected}).")

    if num_dates_actual != len(date_column_names):
        raise ValueError(f"The number of dates in the table ({num_dates_actual}) does not match the expected value ({len(date_column_names)}).")

    #Sanitize all the values in the DataFrame according to the allowed types.

    df = df.apply(lambda col: col.map(sanitize_value))

    # Convert column names to datetime for easier manipulation ************* IMPORTANT!!! remember type name for columns now.
    df.columns = pd.to_datetime(df.columns)

    # Return all the data structures
    return df, drName, expected_total, weekend_priority, sat_priority, sun_priority, year, month