#!/usr/bin/env python
# coding: utf-8
"""Column Time Diff in Days custom transformer.
"""

import os
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from .. import feature_calculators as fc


class TimePeriodFeatures(TransformerMixin, BaseEstimator):
    """TimePeriodFeatures Transformer;
    Computes the following features:
        - is_month_start;
        - is_month_end;
        - is_mid_month;
        - is_weekend;
        - is_morning;
        - is_afternoon;
        - is_evening;
        - is_night;

    TODO: Add type validation.
    Parameters
    ----------
    column : str
        The datetime column name;
    """

    def __init__(
        self,
        column: str,
    ):
        self._column = column
        self._feature_names_out = [
            'is_month_start',
            'is_month_end',
            'is_mid_month',
            'is_weekend',
            'is_morning',
            'is_afternoon',
            'is_evening',
            'is_night'
        ]
    
    def fit(self, X: pd.DataFrame, y=None):
        """Fit transformer by checking X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Input array.

        y : Ignored
            Not used, present here for API consistency by convention.

        Returns
        -------
        self : object
            TimePeriodFeatures transformer class instance.
        """
        return self

    def transform(self, X):
        """Transform X using the forward function.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Input array.

        Returns
        -------
        X_out : array-like, shape (n_samples, n_features)
            Transformed input.
        """
        # time related features
        features = dict()

        features['is_month_start'] = fc.is_month_start(X[self._column])
        features['is_month_end'] = fc.is_month_end(X[self._column])
        features['is_mid_month'] = fc.is_mid_month(X[self._column])

        features['is_weekend'] = fc.is_weekend(X[self._column])
        features['is_morning'] = fc.is_morning(X[self._column])

        features['is_afternoon'] = fc.is_afternoon(X[self._column])
        features['is_evening'] = fc.is_evening(X[self._column])
        features['is_night'] = fc.is_night(X[self._column])
        
        return pd.DataFrame(data=features)

    def get_feature_names_out(self, input_features=None):
        """Get output feature names for transformation.

        This method is only defined if `feature_names_out` is not None.

        Parameters
        ----------
        input_features : Ignored
            Not used, present here for API consistency by convention.

        Returns
        -------
        feature_names_out : ndarray of str objects
            Transformed feature names.
        """
        return np.asarray(
            self._feature_names_out, 
            dtype=object
        )
        
