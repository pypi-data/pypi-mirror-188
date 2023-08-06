#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Apr 15 21:46 2021

Preprocessing functionalities for tabular data classification

Content:
    - Preprocessing pipeline (to be applied before train/val/test splitting)
        - Removing all-NA instances
        - Remove constant features
        - Removing features with too many missing values (default > 20% NaNs)

        - TODO: remove samples that have all NA except for label (dropna with thres? for percent missing?)

    - Fold-wise preprocessing pipeline
        - Normalization (standardization per default)
        - Filling missing values using kNN imputation
        - Normalize only numeric features and one-hot encode categorical features

@author: cspielvogel
"""

import warnings
import numbers
import joblib
import os
import re

import numpy as np
import pandas as pd
from pandas.core.common import SettingWithCopyWarning

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import miceforest as mf

# Ignore SettingWithCopyWarning resulting from creating pandas.DataFrames from numpy.ndarrays
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


class TabularPreprocessor:
    """
    Standardized preprocessing pipeline to be used before any training / validation / test splitting procedure is
    applied
    """

    def __init__(self, label_name, max_missing_ratio=0.2, one_hot_encoder_path=None, label_encoder_path=None):
        """
        Constructor
        :param label_name: str indicating column name containing label
        :param max_missing_ratio: float indicating the maximum ratio of missing to all feature values to keep a feature
        :param one_hot_encoder_path: str indicating the file path to save one hot encoder, Not saved if None
        :param label_encoder_path: str indicating the file path to save label encoder; Not saved if None
        :return: None
        """

        # Ensure input parameter validity
        assert isinstance(max_missing_ratio, numbers.Number), "Parameter 'max_missing_ratio' must be float"
        assert max_missing_ratio <= 1, "Parameter 'max_missing_ratio' must be less or equal 1"
        assert max_missing_ratio >= 0, "Parameter 'max_missing_ratio' must be larger or equal to 0"

        # Set attributes
        self.max_missing_ratio = max_missing_ratio
        self.one_hot_encoder_path = one_hot_encoder_path
        self.label_encoder_path = label_encoder_path
        self.label_name = label_name
        self.one_hot_encoder = None
        self.label_encoder = None
        self.categorical_columns = None
        self.is_fit = False

    def _remove_partially_missing(self, data, axis="columns"):
        """
        Removal of features or instances with missing features above the given ratio
        :param data: pandas.DataFrame containing the data to be preprocessed
        :param axis: string (must be one of "rows" or "columns) indicating whether to remove rows or columns
        :return: pandas.DataFrame without rows or columns with missing values above the max_missing_ratio
        """

        # Ensure valid parameters
        assert axis in ["columns", "rows"], "Parameter 'axis' must be one of ['columns', 'rows']"

        iterable = data.columns if axis == "columns" else data.index

        for subset in iterable:
            if axis == "columns":
                missing_ratio = data.loc[:, subset].isnull().sum() / data.shape[0]
            else:
                missing_ratio = data.loc[subset, :].isnull().sum() / data.shape[1]

            if missing_ratio > self.max_missing_ratio:
                data.drop(subset, axis=axis, inplace=True)

        return data

    def fit(self, data):
        """
        Fitting the standard preprocessing pipeline before transformation.
        Includes removal of instances with only missing values, removal of features with more than 20 % missing values,
        kNN-based imputation for missing values, and removal of correlated features.
        :param data: pandas.DataFrame containing the data to be preprocessed
        :return: TabularPreprocessor fitted with the given parameters
        """

        # Ensure valid parameters
        assert isinstance(data, pd.DataFrame), "Parameter 'data' must be an instance of pandas.DataFrame"

        # Fit one hot encoding for categorial features
        categorical_mask = data.dtypes == object
        self.categorical_columns = data.columns[categorical_mask].tolist()

        # Omit label if categorical
        if self.label_name in self.categorical_columns:
            self.categorical_columns.remove(self.label_name)

        # Cast all categorical columns to string to avoid TypeError
        data = data.astype({k: str for k in self.categorical_columns})

        self.one_hot_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)  # TODO: check arguments
        self.one_hot_encoder.fit(data[self.categorical_columns])

        # Set flag indicating conducted fitting
        self.is_fit = True

        return self

    def transform(self, data):
        """
        Transforming data using the fitted TabularPreprocessor
        :param data: pandas.DataFrame containing the data to be preprocessed
        :return: pandas.DataFrame with the fitted data
        """

        # Ensure pipeline instance has been fitted
        assert self.is_fit is True, ".fit() has to be called before transforming any data"

        # Remove instances with missing label
        num_label_nans = data[self.label_name].isnull().sum()
        data.dropna(subset=[self.label_name], inplace=True)

        # Ensure categorical columns are strings
        data = data.astype({k: str for k in self.categorical_columns})

        # Only keep first instance if multiple instances have the same key
        num_instances_before = len(data)
        data = data[~data.index.duplicated(keep="first")]
        num_instances_diff = num_instances_before - len(data)
        if num_instances_diff > 0:
            print(f"[Warning] {num_instances_diff} instance(s) removed due to duplicate keys"
                  f"- only keeping first occurrence!")

        if num_label_nans > 0:
            print(f"[Warning] {num_label_nans} sample(s) removed due to missing label!")

        # Removal of instances with only missing values
        data.dropna(how="all", axis="rows", inplace=True)

        # Remove features with more than given percentage of missing values (self.max_missing_ratio)
        data = self._remove_partially_missing(data, axis="columns")

        # Check whether there are any categorical columns
        if len(self.categorical_columns) != 0:

            # Apply one-hot encoding and save to joblib file
            cat_ohe = self.one_hot_encoder.transform(data[self.categorical_columns])   # Will be all zero if unknown category in transform

            with open(self.one_hot_encoder_path, "wb") as f:
                joblib.dump(self.one_hot_encoder, f)

            ohe_df = pd.DataFrame(cat_ohe,
                                  columns=self.one_hot_encoder.get_feature_names(input_features=self.categorical_columns),
                                  index=data.index)
            data = pd.concat([data, ohe_df], axis="columns")
            data.drop(columns=self.categorical_columns, axis="columns", inplace=True)

        # Remove features with constant value over all instances while ignoring NaNs
        for column in data.columns:
            if data[column].dtype == "int64":
                if np.all(data[column][~np.isnan(data[column])].values ==
                          data[column][~np.isnan(data[column])].values[0]):
                    data = data.drop(column, axis="columns")
            else:
                if np.all(np.array([i for i in data[column] if not i in ['nan', np.nan]]) ==
                          data[column].values[0]):
                    data = data.drop(column, axis="columns")

        # Encode labels as integers
        self.label_encoder = LabelEncoder()
        data[self.label_name] = self.label_encoder.fit_transform(data[self.label_name])

        # Save label encoder to joblib file
        with open(self.label_encoder_path, "wb") as file:
            joblib.dump(self.label_encoder, file)

        return data

    def fit_transform(self, data):
        """
        Standard preprocessing pipeline returning the preprocessed data.
        Includes removal of instances with only missing values, removal of features with more than 20 % missing values,
        kNN-based imputation for missing values, and removal of correlated features.
        :param data: pandas.DataFrame containing the data to be preprocessed
        :return: pandas.DataFrame containing the preprocessed data
        """

        # Fit
        self.fit(data=data)

        # Transform
        data = self.transform(data)

        return data


class TabularIntraFoldPreprocessor:
    """
    Preprocessing pipeline to be conducted for each split / fold in the validation procedure individually to avoid any
    data leakage

    Performs
    - Feature imputation
    - Standardization
    """

    def __init__(self, random_state, imputation_method="knn", k="automated", normalization="standardize",
                 imputer_path=None, scaler_path=None):
        """
        Constructor

        :param random_state: int indicating seed for pseudo random number generator
        :param imputation_method: str indicating imputation method; can be either "mice" or "knn"
        :param k: int indicating the k nearest neighbors for kNN-based imputation; Ignored if imputation is "mice";
                  Use rounded down number of samples divided by 20 but at least 3 as k
        :param normalization: str indicating the typ of normalization, must be one of "standardize", "minmax"
        :param imputer_path: str indicating the file path to save the imputer; Imputer will not be saved if None
        :param scaler_path: str indicating the file path to save the scaler; Scaler will not be saved if None
        :return: None
        """

        # Ensure input parameter validity
        assert imputation_method in ("mice", "knn", "miceforest"), \
            "Parameter 'imputation' must be either 'knn', 'mice' or 'miceforest'"
        assert isinstance(k, numbers.Number) or k == "automated", "Parameter 'k' must either be numeric or 'automated'"
        assert isinstance(random_state, int), "Parameter 'random_state' must be int"
        assert normalization in ("standardize", "minmax"), \
            "Parameter 'normalization' must be one of ('standardize', 'minmax')"

        # Set attributes
        self.random_state = random_state
        self.imputation_method = imputation_method
        self.k = k  # Number of nearest neighbors for kNN imputation
        self.normalization = normalization  # Type of normalization to carry out
        self.is_fit = False

        # Initialize attributes set during processing
        self.scaler = None
        self.imputer = None
        self.imputer_path = imputer_path
        self.scaler_path = scaler_path

    def fit(self, data):
        """
        Fitting the standard preprocessing pipeline before transformation. Includes standardization and kNN-based
        imputation of missing feature values
        :param data: pandas.DataFrame containing the per-fold training data used for fitting
        :return: TabularPreprocessor fitted with the given parameters
        """

        # Ensure valid parameters
        assert isinstance(data, pd.DataFrame), "Parameter 'data' must be an instance of pandas.DataFrame"

        # Ensure that the number of nearest neighbors used for imputation is above zero if not a string
        if isinstance(self.k, numbers.Number):
            assert self.k > 0, "Parameter 'k' must have a value of 1 or larger"
            assert self.k < len(data), "Parameter 'k' must be smaller of equal to the number of instances"

        if self.imputation_method == "mice":
            # Filling missing values using MICE
            lr = LinearRegression()
            imputer = IterativeImputer(estimator=lr,
                                       missing_values=np.nan,
                                       max_iter=10,
                                       verbose=0,
                                       imputation_order='roman',
                                       random_state=self.random_state)
            self.imputer = imputer.fit(data)

        elif data.isnull().values.any() and self.imputation_method == "miceforest":
            # Remove special characters for compliance with LightGBM
            data = data.rename(columns=lambda x: re.sub('[^A-Za-z0-9_]+', '', x))

            # Fill missing values using MICE forest (light GBM MICE)
            self.imputer = mf.ImputationKernel(data,
                                               save_all_iterations=False,
                                               random_state=self.random_state)

        else:   # CAVE: MICE forest defaults to kNN imputation if there are no nan values in training data
            # Fill missing values using k nearest neighbors
            if self.k == "automated":  # Use rounded down number of samples divided by 20 but at least 3 as k
                k = int(np.round(len(data) / 20, 0)) if np.round(len(data) / 20, 0) > 3 else 3
            imputer = KNNImputer(n_neighbors=k)
            self.imputer = imputer.fit(data)

        if self.imputer_path is not None:
            # Save imputer to joblibd file
            with open(self.imputer_path, "wb") as file:
                joblib.dump(self.imputer, file)

        # Normalize features
        if self.normalization == "standardize":
            scaler = StandardScaler()
        elif self.normalization == "minmax":
            scaler = MinMaxScaler()
        self.scaler = scaler.fit(data)

        if self.scaler_path is not None:
            # Save scaler to joblibd file
            with open(self.scaler_path, "wb") as file:
                joblib.dump(self.scaler, file)

        # Set flag to indicate fitting was conducted
        self.is_fit = True

        return self

    def transform(self, data):
        """
        Transforming data using the fitted TabularIntraFoldPreprocessor
        :param data: pandas.DataFrame containing data to transform using the fitted models, use data from fitting
        procedure if None
        :return: pandas.DataFrame containing the transformed data table
        """

        # Ensure pipeline instance has been fitted
        assert self.is_fit is True, ".fit() has to be called before transforming any data"

        # Ensure data is of type pandas.DataFrame
        assert isinstance(data, pd.DataFrame), "Parameter 'data' must be an instance of pandas.DataFrame"

        if self.imputer.__class__.__name__ == "ImputationKernel":   # MICE forest imputer
            # Run the MICE algorithm for 2 iterations
            self.imputer.mice(5)  # TODO: create adjustable parameter in INI file

            # Return the completed dataset.
            data = self.imputer.complete_data()

        else:
            # Apply imputation
            data[:] = self.imputer.transform(data)

        # Apply feature scaler
        data[:] = self.scaler.transform(data)

        return data

    def fit_transform(self, data=None):
        """
        Standard preprocessing pipeline returning the preprocessed data for individual folds.
        Includes removal of instances with only missing values, removal of features with more than 20 % missing values,
        kNN-based imputation for missing values, and removal of correlated features.
        :param data: pandas.DataFrame containing data to transform using the fitted models, use data from fitting
        procedure if None
        :return: pandas.DataFrame containing the preprocessed data
        """

        # Fit pipeline components
        self.fit(data=data)

        # Transform data using the fitted pipeline
        data = self.transform(data)

        return data
