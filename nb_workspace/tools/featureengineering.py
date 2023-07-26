"""
    This script contains all the required functions for feature engineering required for this project
"""

# Importing nessecary libararies and packages
import pandas as pd
import numpy as np

# Main function: Feature Engineer
def feature_engineereing(_df:pd.DataFrame)->pd.DataFrame:
    """
        Used to create all defined possible engineering steps in the data.

        PARAMETERS
            _df: pandas dataframe, input dataframe.

        RETURN
            pandas DataFrame with created features.
    """

    # Create a copy of input dataframe
    df = _df.copy()

    # Feature: Number of bedrooms per unit area
    df['nbedrooms_per_area'] = df['number_of_bedrooms'] / df['unit_area']

    # Feature: down payment time to delivery percentage
    df['downpayment_per_delivery_time'] = df['down_payment'] / df['time_to_delivery']

    # Feature: Time to delivert per unit area
    df['deliverytime_per_area'] = df['time_to_delivery'] / df['unit_area']

    # Feature: Average time_to_delivery for developers
    df = calc_average_delivery_time(df, 'english_prop_type_name', 'developer_name')

    # Feature: Average tiem_to_delivery for Area
    df = calc_average_delivery_time(df, 'english_prop_type_name', 'english_area_name')

    # Feature: developer performance
    df = calc_feature_performance(df, 'english_prop_type_name', 'developer_name')

    # Feature: area performance
    df = calc_feature_performance(df, 'english_prop_type_name', 'english_area_name')

    # Feature: developer market share
    df = calc_feature_market_share(df, 'english_prop_type_name', 'developer_name')

    # Feature: area market share
    df = calc_feature_market_share(df, 'english_prop_type_name', 'english_area_name')

    # Drop unsed columns
    df.drop(['detailed_property_id'], axis=1, inplace=True)
    
    return df


def calc_average_delivery_time(_df:pd.DataFrame, target_col:str, feature_col:str)->pd.DataFrame:
    """
        Used to calculate the averate time_to_delivery for target_col per each input features.

        PARAMETERS
            _df: pandas dataframe, input dataframe.
            target_col: str, represent the target to which we calculate the average time.
            feature_col: str, represent the feature over which we calculate each average time.

        RETURN
            pandas DataFrame with created features.
    """

    # Create a copy of input dataframe
    df = _df.copy()

    df_average_time_to_delivery = (
        df.pivot_table(
            index=feature_col, 
            columns=target_col, 
            values='time_to_delivery', 
            aggfunc='mean'
        )
        .add_suffix(f"_{feature_col}_time")
        .fillna(-1)
        .reset_index()
        .round()
    )

    # Merge it with original dataframe
    df = df.merge(
        df_average_time_to_delivery,
        how='left',
        on=feature_col
    )

    return df


def calc_feature_performance(_df:pd.DataFrame, target_col:str, feature_col:str)->pd.DataFrame:
    """
        Used to calculate the performance for feature_col per each input target_col.

        PARAMETERS
            _df: pandas dataframe, input dataframe.
            target_col: str, represent the target to which we calculate the average time.
            feature_col: str, represent the feature over which we calculate each average time.

        RETURN
            pandas DataFrame with created features.
    """

    # Create a copy of input dataframe
    df = _df.copy()

    df_property_percent = df.pivot_table(
        index=feature_col, 
        columns=target_col, 
        values='detailed_property_id', 
        aggfunc='count'
    ).fillna(0)

    # Calculate the percentage of each property type per developer
    df_property_percent['total'] = df_property_percent.sum(axis=1)

    df_property_percent = (
        df_property_percent
        .div(df_property_percent['total'], axis=0)
        .drop('total', axis=1)
        .add_suffix(f"_{feature_col}_perecntage")
        .reset_index()
    )

    # Merge it with original dataframe
    df = df.merge(
        df_property_percent,
        how='left',
        on=[feature_col]
    )

    return df


def calc_feature_market_share(_df:pd.DataFrame, target_col:str, feature_col:str)->pd.DataFrame:
    """
        Used to calculate the market share for feature_col per each input target_col.

        PARAMETERS
            _df: pandas dataframe, input dataframe.
            target_col: str, represent the target to which we calculate the average time.
            feature_col: str, represent the feature over which we calculate each average time.

        RETURN
            pandas DataFrame with created features.
    """

    # Create a copy of input dataframe
    df = _df.copy()

    df_property_market_share = (
       df.pivot_table(
            index=feature_col, 
            columns=target_col, 
            values='detailed_property_id', 
            aggfunc='count'
        ).fillna(0)
        .add_suffix(f"_{feature_col}_market_share")
    )

    # Calculate the percentage of each property type per developer
    df_sum = df_property_market_share.sum()

    df_property_market_share = df_property_market_share/df_sum

    # Merge with original dataframe
    df = df.merge(
        df_property_market_share.reset_index(),
        how='left',
        on=feature_col
    )

    return df