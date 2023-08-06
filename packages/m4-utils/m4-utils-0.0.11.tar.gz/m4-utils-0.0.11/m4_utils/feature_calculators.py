"""
module feature_calculators.py
--------------------------------
 Utility functions for calculating features from arbitrary data.
"""
import pandas as pd
import numpy as np

def get_elapsed_time_in_days(end_dt: pd.Series, start_dt: pd.Series):
    elapsed_time = (end_dt - start_dt).dt.total_seconds()
    # to hours
    elapsed_time /= 60**2
    #to days
    elapsed_time /= 24
    return elapsed_time

def get_elapsed_time_in_seconds(end_dt: pd.Series, start_dt: pd.Series):
    elapsed_time = (end_dt - start_dt).dt.total_seconds()
    return elapsed_time

def is_month_start(dt:pd.Series):
    return dt.dt.day <= 10

def is_month_end(dt:pd.Series):
    return dt.dt.day >= 20

def is_mid_month(dt:pd.Series):
    return ((dt.dt.day > 10) & (dt.dt.day < 20))

def is_weekend(dt:pd.Series):
    return dt.dt.day_of_week > 4

def is_morning(dt:pd.Series):
    return dt.dt.hour.between(6,11, inclusive='both')

def is_afternoon(dt:pd.Series):
    return dt.dt.hour.between(12,17, inclusive='both')

def is_evening(dt:pd.Series):
    return dt.dt.hour.between(18,23, inclusive='both')

def is_night(dt:pd.Series):
    return dt.dt.hour.between(0,5, inclusive='both')
