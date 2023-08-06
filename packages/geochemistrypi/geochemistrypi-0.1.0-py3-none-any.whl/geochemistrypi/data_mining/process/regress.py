# -*- coding: utf-8 -*-
from ..model.regression import PolynomialRegression, XgboostRegression, DecisionTreeRegression, ExtraTreeRegression,\
    RandomForestRegression, RegressionWorkflowBase, SVMRegression, DNNRegression, LinearRegression2
from ..data.data_readiness import num_input, float_input, tuple_input, limit_num_input
from ..global_variable import SECTION, DATASET_OUTPUT_PATH
from multipledispatch import dispatch
import pandas as pd


class RegressionModelSelection(object):
    """Simulate the normal way of training regression algorithms."""

    def __init__(self, model):
        self.model = model
        self.reg_workflow = RegressionWorkflowBase()

    @dispatch(object, object, object, object, object, object)
    def activate(self, X: pd.DataFrame, y: pd.DataFrame, X_train: pd.DataFrame,
                 X_test: pd.DataFrame, y_train: pd.DataFrame, y_test: pd.DataFrame) -> None:
        """Train by Scikit-learn framework."""

        self.reg_workflow.data_upload(X=X, y=y, X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)

        # Model option
        if self.model == "Polynomial Regression":
            print("-*-*- Hyper-parameters Specification -*-*-")
            print("Please specify the maximal degree of the polynomial features.")
            poly_degree = num_input(SECTION[2], "@Degree: ")
            self.reg_workflow = PolynomialRegression(degree=poly_degree)
            X_train, X_test = self.reg_workflow.poly(X_train, X_test)
            self.reg_workflow.data_upload(X_train=X_train, X_test=X_test)
        elif self.model == "Xgboost":
            self.reg_workflow = XgboostRegression()
        elif self.model == "Decision Tree":
            print("-*-*- Hyper-parameters Specification -*-*-")
            print("Please specify the max depth of the decision tree regression.")
            dts_max_depth = num_input(SECTION[2], "@Max_depth:")
            self.reg_workflow = DecisionTreeRegression(max_depth=dts_max_depth)
        elif self.model == "Extra-Trees":
            self.reg_workflow = ExtraTreeRegression()
        elif self.model == "Random Forest":
            self.reg_workflow = RandomForestRegression()
        elif self.model == "Support Vector Machine":
            self.reg_workflow = SVMRegression()
        elif self.model == "Deep Neural Networks":
            print("-*-*- Hyper-parameters Specification -*-*-")
            print("Learning Rate: It controls the step-size in updating the weights.")
            print("Please specify the initial learning rate of the the neural networks, such as 0.001.")
            learning_rate = float_input(0.05, SECTION[2], "@Learning Rate: ")
            print("Hidden Layer Sizes: The ith element represents the number of neurons in the ith hidden layer.")
            print("Please specify the size of hidden layer and the number of neurons in the each hidden layer.")
            hidden_layer = tuple_input((50, 25, 5), SECTION[2], "@Hidden Layer Sizes: ")
            # batch_size = limit_num_input()
            self.reg_workflow = DNNRegression(learning_rate_init=learning_rate,
                                              hidden_layer_sizes=hidden_layer)
        elif self.model == "Linear Regression":
            self.reg_workflow = LinearRegression2()

        self.reg_workflow.show_info()

        # Use Scikit-learn style API to process input data
        self.reg_workflow.fit(X_train, y_train)
        y_test_predict = self.reg_workflow.predict(X_test)
        y_test_predict = self.reg_workflow.np2pd(y_test_predict, y_test.columns)
        self.reg_workflow.data_upload(y_test_predict=y_test_predict)

        # Common components for every regression algorithm
        self.reg_workflow.common_components()

        # Special components of different algorithms
        self.reg_workflow.special_components()

        # Save the prediction result
        self.reg_workflow.data_save(y_test_predict, "Y Test Predict", DATASET_OUTPUT_PATH, "Model Prediction")

        # Save the trained model
        self.reg_workflow.save_model()

    @dispatch(object, object, object, object, object, object, bool)
    def activate(self, X: pd.DataFrame, y: pd.DataFrame, X_train: pd.DataFrame, X_test: pd.DataFrame,
                 y_train: pd.DataFrame, y_test: pd.DataFrame, is_automl: bool) -> None:
        """Train by FLAML framework + RAY framework."""

        self.reg_workflow.data_upload(X=X, y=y, X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)

        # Model option
        if self.model == "Polynomial Regression":
            # TODO(Sany sanyhew1097618435@163.com): Find the proper way for polynomial regression
            print("Please specify the maximal degree of the polynomial features.")
            poly_degree = num_input(SECTION[2], "@Degree:")
            self.reg_workflow = PolynomialRegression(degree=poly_degree)
            X_train, X_test = self.reg_workflow.poly(X_train, X_test)
        elif self.model == "Xgboost":
            self.reg_workflow = XgboostRegression()
        elif self.model == "Decision Tree":
            self.reg_workflow = DecisionTreeRegression()
        elif self.model == "Extra-Trees":
            self.reg_workflow = ExtraTreeRegression()
        elif self.model == "Random Forest":
            self.reg_workflow = RandomForestRegression()
        elif self.model == "Support Vector Machine":
            self.reg_workflow = SVMRegression()
        elif self.model == "Deep Neural Networks":
            self.reg_workflow = DNNRegression()
        elif self.model == "Linear Regression":
            self.reg_workflow = LinearRegression2()

        self.reg_workflow.show_info()

        # Use Scikit-learn style API to process input data
        self.reg_workflow.fit(X_train, y_train, is_automl)
        y_test_predict = self.reg_workflow.predict(X_test, is_automl)
        y_test_predict = self.reg_workflow.np2pd(y_test_predict, y_test.columns)
        self.reg_workflow.data_upload(y_test_predict=y_test_predict)

        # Common components for every regression algorithm
        self.reg_workflow.common_components(is_automl)

        # Special components of different algorithms
        self.reg_workflow.special_components(is_automl)

        # Save the prediction result
        self.reg_workflow.data_save(y_test_predict, "Y Test Predict", DATASET_OUTPUT_PATH, "Model Prediction")

        # Save the trained model
        self.reg_workflow.save_model(is_automl)
