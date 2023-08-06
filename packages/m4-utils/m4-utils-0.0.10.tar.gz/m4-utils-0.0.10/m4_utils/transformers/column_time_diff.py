#!/usr/bin/env python
# coding: utf-8
"""Column Time Diff in Days custom transformer.
"""

import os
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from ..feature_calculators import get_elapsed_time_in_days, get_elapsed_time_in_seconds


class ColumnTimeDiff(TransformerMixin, BaseEstimator):
    """Column Time Diff in Days Transformer;

    TODO: Add type validation.
    Parameters
    ----------
    columns : list of tuples
        List of (column1, column2, out_name) tuples specifying the
        transformer objects to be applied to subsets of the data.

            column1 :  str
                The name of the column1.
            column2 :  str
                The name of the column2.
            
            out_name : str
                Normalized Column output name;
    in_ : str,  'days' | 'seconds'

    
    dtype: np.DType or str
        The output data type;
    

    """

    def __init__(
        self,
        columns: list,
        in_: str = 'days',
        dtype='float32'
    ):
        self._columns = columns
        self._feature_names_out = [
            c[2] for c in self._columns
        ]
        self._dtype = dtype
        self._in = in_.lower()
    
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
            ColumnTimeDiff transformer class instance.
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
        res = dict()
        for (col1, col2, c_name) in self._columns:
            if self._in == 'days':
                res[c_name] = get_elapsed_time_in_days(
                    end_dt=X[col2],
                    start_dt=X[col1],
                ).astype(self._dtype)
            elif self._in == 'seconds':
                res[c_name] = get_elapsed_time_in_seconds(
                    end_dt=X[col2],
                    start_dt=X[col1],
                ).astype(self._dtype)
            else:
                raise ValueError('Time scale not recognizer. The class parameter \'in_\' must be one of : [\'days\', \'seconds\']')
        
        return pd.DataFrame(data=res)

    def inverse_transform(self, X):
        """[NOT IMPLEMENTED] Transform X using the inverse function.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Input array.

        Returns
        -------
        X_out : array-like, shape (n_samples, n_features)
            Transformed input.
        """
        return X

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
        
    def __sklearn_is_fitted__(self):
        """Return True since FunctionTransfomer is stateless."""
        return True
