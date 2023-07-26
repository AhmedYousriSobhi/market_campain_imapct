"""
    This script contains all the required functions for data cleaning required for this project
"""
# Importing nessecary libararies and packages
import pandas as pd
import numpy as np

# Main function: data_cleaning
def data_preprocess(_df:pd.DataFrame)->pd.DataFrame:
    """
        Used to create all defined possible cleaning steps in the data.

        PARAMETERS
            _df: pandas dataframe, input dataframe.

        RETURN
            pandas DataFrame with created features.
    """

    # Create a copy of input dataframe
    df = _df.copy()

    # Handling Duplicated unique ID
    dependant_cols = {
        'time_to_delivery':'max',
        'down_payment':'min'
    }
    df = filter_duplicated_records(df, 'detailed_property_id', dependant_cols)

    # Handling negative values in time_to_delivery
    # Replace values <=0 in time_to_delivery with nans
    df.loc[df.time_to_delivery <= 0, 'time_to_delivery'] = np.nan

    # Fill nan values based on selected dependant features
    df = fill_missing_values(df, 'time_to_delivery', ['english_prop_type_name'], 'mean')

    # Handling Missing Values
    fill_value_dict = {
        'numeric' : 'mean',
        'category' : 'mode'
    }

    dependant_cols = ['english_prop_type_name']

    df = fill_missing_columns(df, dependant_cols, fill_value_dict)

    # Handling Outliers
    cols_to_drop = ['detailed_property_id']
    dependant_cols = ['english_prop_type_name']
    df = remove_outlier(df, cols_to_drop, dependant_cols)
    
    return df


def data_preprocess_inference(_df:pd.DataFrame)->pd.DataFrame:
    """
        Used to create all defined possible cleaning steps in the [validation, testing] data sets.

        PARAMETERS
            _df: pandas dataframe, input dataframe.

        RETURN
            pandas DataFrame with created features.
    """

    # Create a copy of input dataframe
    df = _df.copy()

    # Handling negative values in time_to_delivery
    # Replace values <=0 in time_to_delivery with nans
    df.loc[df.time_to_delivery <= 0, 'time_to_delivery'] = np.nan

    # Fill nan values based on selected dependant features
    df = fill_missing_values(df, 'time_to_delivery', ['english_prop_type_name'], 'mean')

    # Handling Missing Values
    fill_value_dict = {
        'numeric' : 'mean',
        'category' : 'mode'
    }

    dependant_cols = ['english_prop_type_name']

    df = fill_missing_columns(df, dependant_cols, fill_value_dict)

    return df

# Function to drop duplicated records
def filter_duplicated_records(df:pd.DataFrame, target_col:str, dependant_cols=dict)-> pd.DataFrame:
    """
        Used to filter out records of certain input target column, based on specific values in dependant columns.

        PARAMETERS
            df: pandas dataframe, input dataset.
            target_col: str, Target column which required to drop duplicated from.
            dependant_cols: dict, describe the dependant columns and their aggeration function.

        RETURN 
            pandas DataFrame after dropping the duplicated values.
    """

    # Create a copy of input dataframe
    df_copy = df.copy()

    # Select unique ids, where time_to_delivery is maximum, and down_payment is minimum
    df_unique = (
        df_copy.groupby(target_col, as_index=False)
        .agg(dependant_cols)
    )

    dependant_cols_lst = list(dependant_cols.keys())

    # append target_col
    dependant_cols_lst.append(target_col)

    df_copy = df_copy.merge(
        df_unique,
        how='inner',
        on=dependant_cols_lst,
        )

    # Final filter step, drop out whole duplicated rows
    df_copy.drop_duplicates(subset=[target_col], inplace=True)

    # Return modified dataframe
    return df_copy

# Function to handle missing values
def fill_missing_values(df:pd.DataFrame, nan_col:str, feature_depend:list, method:str)->pd.DataFrame:
    """
        Used to fill missing values in certain column,
        based on selected metric, calculated according to certain features.

        PARAMETERS
            df: pandas DataFrame, input dataset.
            nan_col: str, input column with required to fill missing values in.
            feature_depend: str, feature which we will calculate the filling values based on.
            method:str, selected aggregation function, [mean, mode]

        RETURN
            pandas Series of filled column.
    """

    # Create a copy of input dataFrame 
    df_copy = df.copy()

    # Calculate the average value for nan_col based on each feature_col.
    df_fill_value = (
        df_copy.groupby(feature_depend, as_index=False)
        .agg({nan_col:method})
        .round()
    )
    
    # Merge with actually dataFrame
    df_copy = df_copy.merge(
        df_fill_value,
        on=feature_depend,
        how='left',
        suffixes=('','_fill')
        )

    # Fill missing values
    df_copy.loc[df_copy[nan_col].isna(), nan_col] = df_copy.loc[df_copy[nan_col].isna(), nan_col+'_fill']

    return df_copy.drop(nan_col+'_fill', axis=1)


def fill_missing_columns(df:pd.DataFrame, dependant_cols:list, fill_value_dict:dict)->pd.DataFrame:
    """
       Given input dataset, and required to fill all missing values in all columns,
       Talking into consideration whether that column is numerical or categorical, 
       and fill its missing values based on filling aggeration function required, of certain input dependant cols.

       PARAMETERS
            df: pandas DataFrame, input dataset with missing values.
            dependant_cols: list, features which target missing columns depends on during the filling.
            fill_value_dict: dictionary, describe each method used for filling value in case of numerical and categorical.

       RETURN
            pandas DataFrame with missing values filled.
    """
    # Create a copy of input dataframe
    df_copy = df.copy()

    # Extract columns with nans values
    cols_with_nans = df_copy.columns[df_copy.isna().sum()>0].tolist()
    
    # Extract numeric & catetorical cols
    numeric_cols = df_copy.select_dtypes('number').columns.tolist()

    category_cols = df_copy.select_dtypes('object').columns.tolist()

    # Iterate over each column with nan values
    for col in cols_with_nans:
        
        # Check if column is numerical or categorical
        if col in numeric_cols:
            df_copy =  fill_missing_values(df_copy, col, dependant_cols, fill_value_dict['numeric'])
        
        elif col in category_cols:
            df_copy.fillna({col: fill_value_dict['category']}, inplace=True)

        else:
            # Skip these column, will be handled later
            continue

    return df_copy


# Function to handle outliers
def remove_outlier_iqr(_df:pd.DataFrame, features_lst:list, target_col:str)->pd.DataFrame:
    """
        Used to remove outliers based on input selected features in the dataframe.
        Outlier removal method is IQR

        PARAMETERS
            df: pandas DataFrame, describe input dataframe which require outliers removal
            features_lst: list, describe the input columns features list.
            target_col: str, describe the target column which we need to remove outlier from.

        RETURN
            Pandas DataFrame, after removing outliers
    """

    # Make a copy of input dataframe
    df_copy = _df.copy()

    # Create empty list for records storing, to be converted into dataframe later.
    Q1 = df_copy.groupby(features_lst)[target_col].transform('quantile', 0.25)
    Q3 = df_copy.groupby(features_lst)[target_col].transform('quantile', 0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR

    upper_bound = Q3 + 1.5 * IQR

    return df_copy[df_copy[target_col].between(lower_bound, upper_bound, inclusive='both')]


def remove_outlier(df:pd.DataFrame, neglected_cols:list, dependant_cols:list)->pd.DataFrame:
    """
        Used to extract numerical columns and drop used input neglected columns,
        Then remove outliers from these columns based on selected dependant features
        using IQR

        PARAMETERS
            df: pandas DataFrame, user input dataframe.
            neglected_cols: list, numerical columns to drop and not interested in removing outliers for.
            dependant_cols: lst, columns to remove ouliters based on them.

        RETURN
            pandas DataFrame after removing outliers.    
    """

    # Create a copy of input dataset
    df_copy = df.copy()

    # Select numerical columns
    numeric_cols = df_copy.select_dtypes('number').columns.tolist()

    # Remove neglected columns
    for col in neglected_cols:
        numeric_cols.remove(col)    

    # Iterate over each numerical col and remove ouliers
    for col in numeric_cols:

        # Using Iqr to remove outliers
        df_copy = remove_outlier_iqr(df_copy, dependant_cols, col)

    # It is a nesessary step to reset_index
    df_copy.reset_index(drop=True, inplace=True)

    return df_copy
