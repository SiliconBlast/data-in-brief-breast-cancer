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

# def create_baseline_characteristics_table(data):
#     """
#     This function takes a Pandas DataFrame and creates a baseline characteristics table for the dataset.
#     """

    # Separate numeric and categorical variables
    numeric_vars = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_vars = data.select_dtypes(include=['object', 'category']).columns.tolist()

    # Create baseline characteristics table for numeric variables
    numeric_table = data[numeric_vars].describe().loc[['mean', 'std']].T

    # Create baseline characteristics table for categorical variables
    categorical_table_big = {}
    for var in categorical_vars:
        categorical_table = pd.DataFrame(columns=['Category', 'Count', 'Percentage'])
        counts = data[var].value_counts()
        cat_table = pd.DataFrame({'Category': counts.index, 'Count': counts, 'Percentage': counts / counts.sum() * 100})
        categorical_table = pd.concat([categorical_table, cat_table])
        categorical_table_big[var] = categorical_table

    # Return the baseline characteristics table
    return numeric_table, categorical_table_big


def export_baseline_characteristics_table(data, file_path):
    """
    This function takes a Pandas DataFrame and exports a baseline characteristics table to an Excel file.
    """
    # Separate numeric and categorical variables
    numeric_vars = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_vars = data.select_dtypes(include=['object', 'category']).columns.tolist()

    # Create baseline characteristics table for numeric variables
    numeric_table = data[numeric_vars].describe().loc[['mean', 'std']].T

    # Create baseline characteristics table for categorical variables
    categorical_table_big = {}
    for var in categorical_vars:
        categorical_table = pd.DataFrame(columns=['Category', 'Count', 'Percentage'])
        counts = data[var].value_counts()
        cat_table = pd.DataFrame({'Category': counts.index, 'Count': counts, 'Percentage': counts / counts.sum() * 100})
        categorical_table = pd.concat([categorical_table, cat_table])
        categorical_table_big[var] = categorical_table

    # Extract keys and values from the categorical table
    keys = list(categorical_table_big.keys())
    values = list(categorical_table_big.values())

    # Create a list of tuples for the categorical data
    cat_data = []
    for i in range(len(keys)):
        cat_data.extend([(keys[i], cat, count, per) for cat, count, per in zip(values[i]['Category'], values[i]['Count'], values[i]['Percentage'])])

    # Create a DataFrame from the categorical data
    df = pd.DataFrame(cat_data, columns=["Variable", "Category", "Count", "Percentage"])

    # Export the DataFrame to an Excel file
    with pd.ExcelWriter(file_path) as writer:
        numeric_table.to_excel(writer, sheet_name='Numeric', index=True)
        df.to_excel(writer, sheet_name='Categorical', index=False)

    print(f"Baseline characteristics table exported to: {file_path}")