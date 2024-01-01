import pandas as pd
import numpy as np

def initial_deduct_expected_totals(df, expected_total): 
    ### Minus all the pre-arranged calls from expected totals (and potentially randomly pre-arranged weekend calls on version 3)
    adjusted_expected = expected_total.copy() # Make a copy to avoid modifying the original array
    for doc_index in range(len(expected_total)):
        # Count the number of '1's in the doctor's row
        call_count = df.iloc[doc_index].str.count('1').sum()
        # Subtract the call count from the expected total for the doctor
        adjusted_expected[doc_index] -= call_count
        # Ensure the adjusted total is not less than 0
        if adjusted_expected[doc_index] < 0:
            adjusted_expected[doc_index] = 0
    return adjusted_expected


################
#### post-hoc switching functions


## calculate call intervals for summing vertically ALL doctors in df, for different intervals. 
# But you can input a df with only 2 doctors, for instance. but be careful need to reset the index rather than keeping the original doctor index in df.
# for example df_pair = df_mapped.iloc[[doc_a, doc_b]].reset_index(drop=True) 

def calculate_call_intervals(df):
    num_doctors = df.shape[0]

    call_interval_store_upper_bound = 9   # store call interval from 1 to this value (n day 1 call), which affect the call_interval matrix column numbers

    call_intervals = np.zeros((num_doctors, call_interval_store_upper_bound), dtype=int)

    # Iterate over each doctor
    for doc_index, row in df.iterrows():
        last_call_date = None
        # Iterate over each date
        for date, on_call in row.items():
            if on_call == '1':
                if last_call_date is not None:
                    # Calculate interval
                    interval = (date - last_call_date).days
                    if 1 <= interval <= 7:
                        call_intervals[doc_index, interval - 1] += 1
                # Update last call date
                last_call_date = date
    return call_intervals

# Function to compare call interval matrices
def isBetterCallInterval(call_interval_original, call_interval_new):

    #concerned upper bound for call interval
    call_interval_concerned_upper_bound = 9 # should not be more than call_interval_store_upper_bound in calculate_call_intervals function

    # Compare the total sum of each call interval
    for interval in range(call_interval_concerned_upper_bound):
        original_sum = call_interval_original[:, interval].sum()
        new_sum = call_interval_new[:, interval].sum()
        # If the new sum for this interval is less, it's better
        if new_sum < original_sum:
            return True
        # If the new sum for this interval is more, it's worse
        elif new_sum > original_sum:
            return False
    # If all call intervals are the same, return False
    return False

# # Function to compare call interval matrices for a specific pair of doctors
# def isBetterCallIntervalPairwise(call_interval_original, call_interval_new, doc_pair):
#     # Extract the rows for the specific doctors
#     original_pair = call_interval_original[doc_pair, :]
#     new_pair = call_interval_new[doc_pair, :]
#     # Use the isBetterCallInterval function on the extracted pairs
#     return isBetterCallInterval(original_pair, new_pair)