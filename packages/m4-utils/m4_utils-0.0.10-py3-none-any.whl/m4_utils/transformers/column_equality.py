#!/usr/bin/env python
# coding: utf-8
"""Equality Column custom transformer.
"""

import os
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class ColumnEquality(TransformerMixin, BaseEstimator):
    """Equality Column Transformer;
    Calculates `column1 == column2`;

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
    """

    def __init__(
        self,
        columns: list,
        dtype='bool'
    ):
        self._columns = columns
        self._feature_names_out = [
            c[2] for c in self._columns
        ]
        self._dtype = dtype
    
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
            ColumnEquality transformer class instance.
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
            res[c_name] = (X[col1] == X[col2]).astype(self._dtype)
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
