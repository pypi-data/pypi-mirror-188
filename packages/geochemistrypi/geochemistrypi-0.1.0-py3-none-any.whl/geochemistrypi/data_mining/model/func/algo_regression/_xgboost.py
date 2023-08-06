# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import xgboost
from matplotlib import pyplot as plt
from sklearn.inspection import permutation_importance


def feature_importance(X: pd.DataFrame, trained_model: object, image_config: dict) -> None:
    """Plot the Feature Importance.

    Parameters
    ----------
    X: pd.DataFrame (n_samples, n_components)
        The input data.

    trained_model : sklearn algorithm model
        The sklearn algorithm model trained with X_train data.
    """
    columns_name = X.columns

    # print the feature importance value orderly
    for feature_name, score in zip(list(columns_name), trained_model.feature_importances_):
        print(feature_name, ":", score)
    plt.figure(figsize=(image_config['width'], image_config['height']),dpi=image_config['dpi'])
    plt.bar(range(len(columns_name)), trained_model.feature_importances_, tick_label=columns_name)


def histograms_feature_weights(X: pd.DataFrame, trained_model: object, image_config: dict) -> None:
    """Plot the Feature Importance, histograms present feature weights for XGBoost predictions.

    Parameters
    ----------
    X: pd.DataFrame (n_samples, n_components)
        The input data.

    trained_model : sklearn algorithm model
        The sklearn algorithm model trained with X_train data.
    """

    columns_name = X.columns
    plt.rcParams["figure.figsize"] = (image_config['width'], image_config['height'])
    xgboost.plot_importance(trained_model)


def permutation_importance_(X: pd.DataFrame, X_test: pd.DataFrame, y_test: pd.DataFrame, trained_model: object, image_config: dict) -> None:
    """Plot the permutation Importance.

    Parameters
    ----------
    X: pd.DataFrame (n_samples, n_components)
        The input data.

    X_test : pd.DataFrame (n_samples, n_components)
        The testing target values.

    y_test : pd.DataFrame (n_samples, n_components)
    The testing target values.

    trained_model : sklearn algorithm model
        The sklearn algorithm model trained with X_train data.
    """

    columns_name = X.columns
    plt.figure(figsize=(image_config['width'], image_config['height']),dpi=image_config['dpi'])
    result = permutation_importance(trained_model, X_test,
                                    y_test, n_repeats=10,
                                    random_state=42, n_jobs=2)
    sorted_idx = result.importances_mean.argsort()
    plt.boxplot(
        result.importances[sorted_idx].T,
        vert=False,
        labels=np.array(columns_name),
    )
