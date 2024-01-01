import pandas as pd
from datetime import datetime
from datetime import timedelta

def calculate_availability(df):
    # Convert the column names to datetime to make it easier to work with
    df.columns = pd.to_datetime(df.columns)

    # Initialize lists to hold availability counts
    availDates = []
    availWeekend = []
    availSat = []
    availSun = []

    # Iterate over each doctor (row) in the DataFrame
    for index, row in df.iterrows():
        # Count the total available days, excluding those marked with 'x'
        total_available = row[row != 'x'].count()
        availDates.append(total_available)
        
        # Count the weekend availability
        total_weekend_available = row[(row.index.dayofweek >= 5) & (row != 'x')].count()
        availWeekend.append(total_weekend_available)
        
        # Count Saturdays availability
        total_saturday_available = row[(row.index.dayofweek == 5) & (row != 'x')].count()
        availSat.append(total_saturday_available)
        
        # Count Sundays availability
        total_sunday_available = row[(row.index.dayofweek == 6) & (row != 'x')].count()
        availSun.append(total_sunday_available)

    return availDates, availWeekend, availSat, availSun




def decrement_availabilities(df, date, availDates, availWeekend, availSat, availSun):
    #decrement availabilities for all doctors
    #nonlocal availDates, availWeekend, availSat, availSun
    for i in range(len(availDates)):
        # Check if the doctor is not already marked 'x' for the given date
        if df.at[i, date] != 'x':
            if availDates[i] > 0:
                availDates[i] -= 1
                if date.dayofweek == 5:  # Saturday
                    if availSat[i] > 0: availSat[i] -= 1
                    if availWeekend[i] > 0: availWeekend[i] -= 1
                elif date.dayofweek == 6:  # Sunday
                    if availSun[i] > 0: availSun[i] -= 1
                    if availWeekend[i] > 0: availWeekend[i] -= 1




def update_after_assignment(df, doc_index, expected_total, date, fixed_call):
    # Helper function to update availabilities and the DataFrame after a doctor is assigned
    # nonlocal expected_total

    # only deduct expected_total if it was not pre-arranged or randomly arranged weekends in v3. because they were already deducted in initial_deduct_expected_totals().
    if not fixed_call:
        expected_total[doc_index] -= 1

    # If expected_total for the doctor becomes negative, add 1 to all doctors to maintain the rank
    if expected_total[doc_index] < 0:
        expected_total = [x + 1 for x in expected_total]

    # Mark the next two days as 'x_gen' if they exist in the df, and not already pre-arranged consecutive calls
    for next_day in [1, 2]:
        next_date = date + timedelta(days=next_day)
        if next_date in df.columns and df.at[doc_index, next_date] not in ['x', '1']:
            df.at[doc_index, next_date] = 'x_gen'


def update_weekend_after_assignment(df, doc_index, weekend_priority, date, fixed_call):
    # Helper function to update availabilities and the DataFrame after a doctor is assigned
    # nonlocal expected_total

    # only deduct expected_total if it was not pre-arranged or randomly arranged weekends in v3. because they were already deducted in initial_deduct_expected_totals().
    if not fixed_call:
        expected_total[doc_index] -= 1

    # If expected_total for the doctor becomes negative, add 1 to all doctors to maintain the rank
    if expected_total[doc_index] < 0:
        expected_total = [x + 1 for x in expected_total]

    # Mark the next two days as 'x_gen' if they exist in the df, and not already pre-arranged consecutive calls
    for next_day in [1, 2]:
        next_date = date + timedelta(days=next_day)
        if next_date in df.columns and df.at[doc_index, next_date] not in ['x', '1']:
            df.at[doc_index, next_date] = 'x_gen'