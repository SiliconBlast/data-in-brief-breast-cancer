import pandas as pd

def summarize_categorical_data(data, variable):
    """
    This function takes a Pandas DataFrame and a variable name and returns a frequency table and a percentage table for the variable.
    """
    # Calculate the frequency of each category
    freq_table = data[variable].value_counts()

    # Calculate the percentage of each category
    pct_table = freq_table / len(data) * 100

    # Create a DataFrame to hold the tables
    summary_table = pd.concat([freq_table, pct_table], axis=1)

    # Rename the columns
    summary_table.columns = ["Frequency", "Percentage"]

    # Sort the table by frequency in descending order
    summary_table = summary_table.sort_values("Frequency", ascending=False)

    # Return the summary table
    return summary_table

def check_missing_data(data):
    """
    This function loads a CSV file, replaces "#" with NaN, checks for missing values, and prints the results to the console.
    """
    # make data copy for analysis
    data = data.copy()

    # Replace "#" with NaN
    data = data.replace("#", pd.NaT)

    # Check for missing values
    missing = data.isnull().sum()

    # Print missing values
    print("Missing Data:")
    print(missing)