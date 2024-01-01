import pandas as pd
from call_interval_functions import calculate_call_intervals, isBetterCallInterval  #, isBetterCallIntervalPairwise
import numpy as np

def previousCallInterval(df, doc_index, date):
    """
    Returns interval between given date and preceding call date for doc_index.
    Returns np.nan if no preceding call date.
    """

    # Is selecting up to and including the input date, rather than stopping before it to get the previous call date.
    prev_calls = df.loc[doc_index, :date-pd.Timedelta('1D')] == '1'
    prev_calls = prev_calls[prev_calls].index
    #print(f"***********prev_calls = {prev_calls}, date = {date}")    

    if len(prev_calls) > 0:
        last_call = prev_calls[-1]
        return (date - last_call).days
    else:
        # No previous call found
        return np.nan 

def nextCallInterval(df, doc_index, date):
    """
    Returns interval between given date and next call date for doc_index. 
    Returns np.nan if no subsequent call date.
    """
    next_calls = df.loc[doc_index, date+pd.Timedelta('1D'):] == '1'
    next_calls = next_calls[next_calls].index

    if len(next_calls) > 0:
        next_call = next_calls[0]
        return (next_call - date).days
    else:
        # No subsequent call found
        return np.nan


def matches_priority(priority_num, previous_interval, next_interval):

    if priority_num in [0, 8, 16]:
        return previous_interval == 3 and next_interval == 3
    elif priority_num in [1, 9, 17]: 
        return previous_interval == 3 or next_interval == 3
    elif priority_num in [2, 10, 18]:
        return previous_interval == 4 or next_interval == 4
    elif priority_num in [3, 11, 19]:
        return previous_interval == 5 or next_interval == 5
    elif priority_num in [4, 12]:
        return previous_interval == 6 or next_interval == 6
    elif priority_num in [5, 13]:
        return previous_interval == 7 or next_interval == 7
    elif priority_num in [6, 14]:
        return previous_interval == 8 or next_interval == 8
    elif priority_num in [7, 15]:
        return previous_interval == 9 or next_interval == 9
    else:
        return False


def swap_calls_for_better_intervals(df_mapped, df_original):
    num_docs = len(df_mapped)

    num_priorities = 20  # num_priorities = n , As we have priorities from 0 to n-1 , !! refer to matches_priority function
    for priority_num in range(num_priorities):
        #print(f'Optimizing call list {int(priority_num/num_priorities*100)} %')
        for doc_a in range(num_docs):

            # Iterate over all dates where doc_a is on call
            for date_a, on_call_a in df_mapped.iloc[doc_a].items():

                # Check if doc_a's call on date_a is not pre-arranged
                if on_call_a == '1' and df_original.iloc[doc_a][date_a] != '1':
                    previous_interval = previousCallInterval(df_mapped, doc_a, date_a)
                    next_interval = nextCallInterval(df_mapped, doc_a, date_a)

                    ## the following start with search of three consecutive 3 day calls, then to less crazy calls
                    if matches_priority(priority_num, previous_interval, next_interval):

                        #print(f"***********doc_a = {doc_a}, date_a = {date_a}")

                        # Flag to determine if a swap has been made
                        swap_made = False
                        
                        # Now find a date_b where swapping might be beneficial
                        for doc_b in range(doc_a + 1, num_docs):
                            if swap_made:
                                break  # Exit the loop if a swap has been made
                            if doc_a != doc_b:  # Ensure we don't compare the same doctor
                                for date_b, on_call_b in df_mapped.iloc[doc_b].items():
                                    if swap_made:
                                        break  # Exit the loop if a swap has been made
                                    # Ensure we're looking at an on call day for doc_b that is not pre-arranged
                                    # and make sure don't swap if crashed with no-call request of either doctor
                                    if (on_call_b == '1') and (df_original.iloc[doc_b][date_b] != '1') and (df_mapped.loc[doc_a, date_b] != 'x') and (df_mapped.loc[doc_b, date_a] != 'x'):

                                        # Extract the pair DataFrame for the current state
                                        df_pair = df_mapped.iloc[[doc_a, doc_b]].reset_index(drop=True)
                                        intervals_original = calculate_call_intervals(df_pair)

                                        # Perform the swap in df_pair (temporary df)
                                        df_pair.loc[0, date_a], df_pair.loc[1, date_b] = '', ''
                                        df_pair.loc[0, date_b], df_pair.loc[1, date_a] = '1', '1'

                                        intervals_swapped = calculate_call_intervals(df_pair)
                                        
                                        # If the intervals are better, perform the swap
                                        if isBetterCallInterval(intervals_original, intervals_swapped):
                                            # print(f"doc_b = {doc_b}, date_b = {date_b}")
                                            # print(f'intervals_original: {intervals_original}')
                                            # print(f'intervals_swapped: {intervals_swapped}')

                                            # Mark the swap in df_mapped
                                            df_mapped.loc[doc_a, date_a], df_mapped.loc[doc_b, date_b] = '', ''
                                            df_mapped.loc[doc_a, date_b], df_mapped.loc[doc_b, date_a] = '1', '1'

                                            swap_made = True  # Set the flag to indicate a swap has been made
                                        else:
                                            # Undo the swap in the temporary df_pair
                                            df_pair.loc[0, date_a], df_pair.loc[1, date_b] = '1', '1'
                                            df_pair.loc[0, date_b], df_pair.loc[1, date_a] = '', ''

                        if swap_made:
                            break  # Break out of the date_a loop if a swap has been made

    return df_mapped