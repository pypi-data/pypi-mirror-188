#
# Copyright 2022 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
# pylint: disable=import-error,import-outside-toplevel
import datetime
import enum
import math
import os.path
import re
from collections import OrderedDict
from functools import cached_property
from io import TextIOWrapper
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import click
import jpype
import jpype.imports
import pandas as pd
from dateutil.parser import isoparse
from pandas._libs.missing import (  # type: ignore # pylint: disable=no-name-in-module
    NAType,
)


class ModelType(enum.Enum):
    CLASSIFICATION = 1
    REGRESSION = 2
    TIME_SERIES = 3


class TimeSeriesType(enum.Enum):
    FORECAST = 1
    HISTORICAL = 2


class ScoringCodeModel:
    def __init__(self, jar_path: str):
        if not os.path.exists(jar_path):
            raise ValueError(f"File not found: {jar_path}")

        if not jpype.isJVMStarted():
            jpype.startJVM()

        # Java "imports" has to be done after jpype JVM is started
        from java.io import File
        from java.lang import ClassLoader
        from java.net import URLClassLoader

        # Load Predictors class from model jar using URLClassLoader
        url = File(jar_path).toURI().toURL()
        self._class_loader = URLClassLoader([url], None)
        predictors_class = self._class_loader.loadClass(
            "com.datarobot.prediction.Predictors"
        )

        # Call Predictors.getPredictor(ClassLoader) to load model
        # using the URLClassLoader created above
        method = predictors_class.getDeclaredMethod("getPredictor", ClassLoader)
        self._predictor = method.invoke(None, self._class_loader)

    def predict(
        self,
        data_frame: pd.DataFrame,
        max_explanations: int = 0,
        threshold_high: Optional[float] = None,
        threshold_low: Optional[float] = None,
        time_series_type: TimeSeriesType = TimeSeriesType.FORECAST,
        forecast_point: Optional[datetime.datetime] = None,
        predictions_start_date: Optional[datetime.datetime] = None,
        predictions_end_date: Optional[datetime.datetime] = None,
        prediction_intervals_length: Optional[int] = None,
    ) -> pd.DataFrame:

        """
        Get predictions from Scoring Code model.

        Parameters
        ----------
        data_frame: pd.DataFrame
            Input data.
        max_explanations: int
            Number of prediction explanations to compute.
            If 0, prediction explanations are disabled.
        threshold_high: Optional[float]
            Only compute prediction explanations for predictions above this threshold.
            If None, the default value will be used.
        threshold_low: Optional[float]
            Only compute prediction explanations for predictions below this threshold.
            If None, the default value will be used.
        time_series_type: TimeSeriesType
            Type of time series predictions to compute.
            If TimeSeriesType.FORECAST, predictions will be computed for a single
            forecast point specified by forecast_point.
            If TimeSeriesType.HISTORICAL, predictions will be computed for the range of
            timestamps specified by predictions_start_date and predictions_end_date.
        forecast_point: Optional[datetime.datetime]
            Forecast point to use for time series forecast point predictions.
            If None, the forecast point is detected automatically.
            If not None and time_series_type is not TimeSeriesType.FORECAST,
            ValueError is raised
        predictions_start_date: Optional[datetime.datetime]
            Start date in range for historical predictions.
            If None, predictions will start from the earliest date in the input that
            has enough history.
            If not None and time_series_type is not TimeSeriesType.HISTORICAL,
            ValueError is raised
        predictions_end_date: Optional[datetime.datetime]
            End date in range for historical predictions.
            If None, predictions will end on the last date in the input.
            If not None and time_series_type is not TimeSeriesType.HISTORICAL,
            ValueError is raised
        prediction_intervals_length: Optional[int]
            The percentile to use for the size for prediction intervals. Has to be an
            integer between 0 and 100(inclusive).
            If None, prediction intervals will not be computed.
        Returns
        -------
        pd.DataFrame
            Prediction output
        """

        if prediction_intervals_length is not None and (
            prediction_intervals_length < 1 or prediction_intervals_length > 100
        ):
            raise ValueError("Prediction intervals length must be >0 and <=100")

        if threshold_high and not max_explanations:
            raise ValueError(
                "threshold_high does not make sense without specifying max_explanations"
            )
        if threshold_low and not max_explanations:
            raise ValueError(
                "threshold_low does not make sense without specifying max_explanations"
            )

        _validate_input(data_frame)

        if self.model_type == ModelType.TIME_SERIES:
            return self._predict_ts(
                data_frame,
                time_series_type,
                forecast_point,
                predictions_start_date,
                predictions_end_date,
                prediction_intervals_length,
            )

        if forecast_point:
            raise ValueError(
                "forecast_point is not supported by non time series models"
            )

        if time_series_type != TimeSeriesType.FORECAST:
            raise ValueError(
                "time_series_type is not supported by non time series models"
            )

        if predictions_start_date:
            raise ValueError(
                "predictions_start_date is not supported by non time series models"
            )

        if predictions_end_date:
            raise ValueError(
                "predictions_end_date is not supported by non time series models"
            )

        return self._predict(
            data_frame, max_explanations, threshold_high, threshold_low
        )

    @cached_property
    def model_type(self) -> ModelType:
        """
        Get the model type.

        Returns
        -------
        ModelType
            One of: ModelType.CLASSIFICATION, ModelType.REGRESSION, ModelType.TIME_SERIES
        """
        clazz = self._predictor.getPredictorClass().getSimpleName()
        if clazz == "IClassificationPredictor":
            return ModelType.CLASSIFICATION
        if clazz == "IRegressionPredictor":
            return ModelType.REGRESSION
        if clazz == "ITimeSeriesRegressionPredictor":
            return ModelType.TIME_SERIES

        raise Exception(f"Unexpected predictor class:{clazz}")

    @cached_property
    def model_info(self) -> Optional[Dict[str, str]]:
        """
        Get model metadata.

        Returns
        -------
        Optional[Dict[str, str]]
            Dictionary with metadata if model has any, else None
        """
        info = self._predictor.getModelInfo()
        return {str(key): str(val) for key, val in info.items()} if info else None

    @property
    def date_column(self) -> Optional[str]:
        """
        Get the date column for a Time Series model.

        Returns
        -------
        Optional[str]
            Name of date column if model has one, else None.
        """
        return (
            str(self._predictor.getDateColumnName())
            if self.model_type == ModelType.TIME_SERIES
            else None
        )

    @property
    def series_id_column(self) -> Optional[str]:
        """
        Get the name of the series id column for a Time Series model.

        Returns
        -------
        Optional[str]
            Name of the series id column if model has one, else None.
        """
        return (
            str(self._predictor.getSeriesIdColumnName())
            if self.model_type == ModelType.TIME_SERIES
            else None
        )

    @property
    def time_step(self) -> Optional[Tuple[int, str]]:
        """
        Get the time step for a Time Series model.

        Returns
        -------
        Optional[Tuple[int, str]]
            Time step as (quantity, time unit) if model has this, else None.
            Example: (3, "DAYS")
        """
        if self.model_type != ModelType.TIME_SERIES:
            return None

        step = self._predictor.getTimeStep()
        return int(step.getKey()), str(step.getValue())

    @property
    def feature_derivation_window(self) -> Optional[Tuple[int, int]]:
        """
        Get the feature derivation window for a Time Series model.

        Returns
        -------
        Optional[Tuple[int, int]]
            Feature derivation window as (begin, end) if model has this, else None.
        """
        if self.model_type != ModelType.TIME_SERIES:
            return None

        window = self._predictor.getFeatureDerivationWindow()
        return int(window.getKey()), int(window.getValue())

    @property
    def forecast_window(self) -> Optional[Tuple[int, int]]:
        """
        Get the forecast window for a Time Series model.

        Returns
        -------
        Optional[Tuple[int, int]]
            Forecast window as (begin, end) if model has this, else None.
        """
        if self.model_type != ModelType.TIME_SERIES:
            return None

        window = self._predictor.getForecastWindow()
        return int(window.getKey()), int(window.getValue())

    @cached_property
    def date_format(self) -> Optional[str]:
        """
        Get the date format for a Time Series model.

        Returns
        -------
        Optional[str]
            Date format having the syntax expected by datetime.strftime() or None
            if model is not time series.
        """
        if self.model_type != ModelType.TIME_SERIES:
            return None

        return _java_date_format_to_python(str(self._predictor.getDateFormat()))

    @property
    def class_labels(self) -> Optional[Sequence[str]]:
        """
        Get the class labels for the model.

        Returns
        -------
        Optional[Sequence[str]]
            List of class labels if model is a classification model, else None.
        """
        return (
            [str(label) for label in self._predictor.getClassLabels()]
            if self.model_type == ModelType.CLASSIFICATION
            else None
        )

    @cached_property
    def features(self) -> Dict[str, type]:
        """
        Get features names and types for the model.

        Returns
        -------
        OrderedDict[str, type]
            Dictionary mapping feature name to feature type, where feature type is
            either str or float. The ordering of features is the same as it was during
            model training.
        """

        def feature_type(java_type: Any) -> type:
            simple = java_type.getSimpleName()
            if simple == "Double":
                return float
            if simple == "String":
                return str
            raise Exception(f"Unexpected java type {simple}")

        features = OrderedDict()
        for key, val in self._predictor.getFeatures().items():
            features[key] = feature_type(val)
        return features

    @property
    def model_id(self) -> str:
        """
        Get the model id.

        Returns
        -------
        str
            The model id.
        """
        return str(self._predictor.getModelId())

    def _predict(
        self,
        data_frame: pd.DataFrame,
        max_explanations: int,
        threshold_high: Optional[float],
        threshold_low: Optional[float],
    ) -> pd.DataFrame:
        from java.util import HashMap

        row_count = len(data_frame.index)
        columns = self.class_labels or ["PREDICTION"]
        output_data: Dict[str, List[Any]] = {
            str(label): [0.0 for _ in range(row_count)] for label in columns
        }
        if max_explanations:
            explanations_names: List[List[Union[str, NAType]]] = [
                [] for _ in range(max_explanations)
            ]
            explanations_values: List[List[Union[str, NAType]]] = [
                [] for _ in range(max_explanations)
            ]
            explanations_strength: List[List[Union[str, NAType]]] = [
                [] for _ in range(max_explanations)
            ]
            explanations_qualitative_strength: List[List[Union[str, NAType]]] = [
                [] for _ in range(max_explanations)
            ]

        hash_map = HashMap()
        for row_index, row in enumerate(data_frame.values):
            for column, value in zip(data_frame.columns.to_list(), row):
                if (
                    isinstance(value, float)
                    and math.isnan(value)
                    and self.features.get(column) == str
                ):
                    value = ""
                hash_map[column] = value

            if max_explanations:
                explanation_params = self._predictor.getDefaultPredictionExplanationParams().withMaxCodes(
                    max_explanations
                )
                if threshold_high:
                    explanation_params = explanation_params.withThresholdHigh(
                        threshold_high
                    )
                if threshold_low:
                    explanation_params = explanation_params.withThresholdLow(
                        threshold_low
                    )

                score = self._predictor.scoreWithExplanations(
                    hash_map, explanation_params
                )
                prediction = score.getScore()

                explanations = score.getPredictionExplanation()
                for explanation_index in range(max_explanations):
                    explanation = (
                        explanations.get(explanation_index)
                        if (explanations and explanation_index < explanations.size())
                        else None
                    )
                    explanations_names[explanation_index].append(
                        str(explanation.getFeatureName()) if explanation else pd.NA
                    )
                    explanations_values[explanation_index].append(
                        str(explanation.getFeatureValue()) if explanation else pd.NA
                    )
                    explanations_strength[explanation_index].append(
                        explanation.getStrengthScore() if explanation else pd.NA
                    )
                    explanations_qualitative_strength[explanation_index].append(
                        str(explanation.getStrength()) if explanation else pd.NA
                    )
            else:
                prediction = self._predictor.score(hash_map)

            if self.model_type == ModelType.CLASSIFICATION:
                for key, val in prediction.items():
                    output_data[str(key)][row_index] = val
            else:
                output_data["PREDICTION"][row_index] = prediction

        if self.model_type == ModelType.CLASSIFICATION:
            target_name = (
                self.model_info["Target-Name"] if self.model_info else "target"
            )
            for key in list(output_data.keys()):
                output_data[f"{target_name}_{key}_PREDICTION"] = output_data.pop(key)

        for explanation_index in range(max_explanations):
            output_data[
                f"EXPLANATION_{explanation_index + 1}_FEATURE_NAME"
            ] = explanations_names[explanation_index]
            output_data[
                f"EXPLANATION_{explanation_index + 1}_ACTUAL_VALUE"
            ] = explanations_values[explanation_index]
            output_data[
                f"EXPLANATION_{explanation_index + 1}_STRENGTH"
            ] = explanations_strength[explanation_index]
            output_data[
                f"EXPLANATION_{explanation_index + 1}_QUALITATIVE_STRENGTH"
            ] = explanations_qualitative_strength[explanation_index]

        return pd.DataFrame(data=output_data)

    def _predict_ts(
        self,
        data_frame: pd.DataFrame,
        time_series_type: TimeSeriesType,
        forecast_point: Optional[datetime.datetime],
        predictions_start_date: Optional[datetime.datetime],
        predictions_end_date: Optional[datetime.datetime],
        prediction_intervals_length: Optional[int],
    ) -> pd.DataFrame:
        import java.lang
        from java.util import ArrayList, HashMap

        if time_series_type == TimeSeriesType.FORECAST:
            if predictions_start_date:
                raise ValueError(
                    "Predictions start date is not supported when time_series_type is FORECAST"
                )
            if predictions_end_date:
                raise ValueError(
                    "Predictions end date is not supported when time_series_type is FORECAST"
                )
        else:
            if forecast_point:
                raise ValueError(
                    "Forecast point is not supported when time_series_type is HISTORICAL"
                )

        row_list = ArrayList()
        for row in data_frame.to_dict("records"):
            hash_map = HashMap()
            for key, value in row.items():
                hash_map[key] = value
            row_list.append(hash_map)

        time_series_options_class = jpype.JClass(
            "com.datarobot.prediction.TimeSeriesOptions", loader=self._class_loader
        )
        builder = time_series_options_class.newBuilder()
        if prediction_intervals_length:
            builder.computeIntervals(True)
            builder.setPredictionIntervalLength(
                java.lang.Integer(prediction_intervals_length)
            )

        assert self.date_format is not None
        if time_series_type == TimeSeriesType.FORECAST:
            if forecast_point:
                options = builder.buildSingleForecastPointRequest(
                    forecast_point.strftime(self.date_format)
                )
            else:
                options = builder.buildSingleForecastPointRequest()
        else:
            start_date = (
                predictions_start_date.strftime(self.date_format)
                if predictions_start_date
                else None
            )
            end_date = (
                predictions_end_date.strftime(self.date_format)
                if predictions_end_date
                else None
            )
            options = builder.buildForecastDateRangeRequest(start_date, end_date)

        scores = self._predictor.score(row_list, options)

        return _assemble_ts_result(scores, prediction_intervals_length)


def _validate_input(data_frame: pd.DataFrame) -> None:
    for column in data_frame.columns:
        if pd.api.types.is_datetime64_any_dtype(data_frame[column]):
            raise ValueError(
                f"Column {column} has unsupported type {data_frame[column].dtype}. "
                f"Date/time columns must be converted to string. "
                f"The expected date/time format can be queried "
                f"using ScoringCodeModel.date_format"
            )


def _assemble_ts_result(scores: Any, intervals_length: Optional[int]) -> pd.DataFrame:
    predictions = []
    series_ids = []
    forecast_points = []
    timestamps = []
    forecast_distances = []
    if intervals_length:
        intervals_low = []
        intervals_high = []

    for score in scores:
        predictions.append(score.getScore())
        series_ids.append(str(score.getSeriesId() or ""))
        forecast_points.append(str(score.getForecastPoint()))
        timestamps.append(str(score.getForecastTimestamp()))
        forecast_distances.append(score.getForecastDistance())
        if intervals_length:
            low, high = score.getInterval()
            intervals_low.append(low)
            intervals_high.append(high)

    data = {
        "PREDICTION": predictions,
        "Forecast Point": pd.to_datetime(forecast_points, utc=True),
        "Timestamp": pd.to_datetime(timestamps, utc=True),
        "Forecast Distance": forecast_distances,
        "Series Id": series_ids,
    }

    if intervals_length:
        data[f"PREDICTION_{intervals_length}_PERCENTILE_LOW"] = intervals_low
        data[f"PREDICTION_{intervals_length}_PERCENTILE_HIGH"] = intervals_high

    return pd.DataFrame(data=data)


def _java_date_format_to_python(java_format: str) -> str:
    # The order is important. Longer identifiers needs to come before shorter ones
    # yyyy before yy and MM before M
    replace = OrderedDict(
        [
            ("%", "%%"),
            ("yyyy", "%Y"),
            ("yy", "%y"),
            ("a", "%p"),
            ("E", "%a"),
            ("dd", "%d"),
            ("MM", "%m"),
            ("M", "%b"),
            ("HH", "%H"),
            ("hh", "%I"),
            ("mm", "%M"),
            ("S", "%f"),
            ("ss", "%S"),
            ("Z", "%z"),
            ("z", "%Z"),
            ("D", "%j"),
            ("w", "%U"),
            ("'T'", "T"),
            ("'Z'", "Z"),
        ]
    )

    return re.sub(
        "|".join(replace.keys()), lambda match: replace[match[0]], java_format
    )


@click.command()
@click.argument("model", type=click.Path(exists=True))
@click.argument("input_csv", type=click.File(mode="r"))
@click.argument("output_csv", type=click.File(mode="w"))
@click.option("--forecast_point")
@click.option("--predictions_start_date")
@click.option("--predictions_end_date")
@click.option("--with_explanations", is_flag=True)
@click.option("--prediction_intervals_length")
def cli(
    model: str,
    input_csv: TextIOWrapper,
    output_csv: TextIOWrapper,
    forecast_point: Optional[str],
    predictions_start_date: Optional[str],
    predictions_end_date: Optional[str],
    with_explanations: bool,
    prediction_intervals_length: int,
) -> None:
    """
    Command Line Interface main function.

    Parameters
    ----------
    model
    input_csv
    output_csv
    forecast_point
    predictions_start_date
    predictions_end_date
    with_explanations
    prediction_intervals_length
    """
    scoring_code_model = ScoringCodeModel(model)

    ts_type = (
        TimeSeriesType.HISTORICAL
        if (predictions_start_date or predictions_end_date)
        else TimeSeriesType.FORECAST
    )

    df = pd.read_csv(input_csv, float_precision="round_trip", keep_default_na=False)
    result = scoring_code_model.predict(
        df,
        forecast_point=(isoparse(forecast_point) if forecast_point else None),
        predictions_start_date=(
            isoparse(predictions_start_date) if predictions_start_date else None
        ),
        predictions_end_date=(
            isoparse(predictions_end_date) if predictions_end_date else None
        ),
        time_series_type=ts_type,
        max_explanations=(3 if with_explanations else 0),
        prediction_intervals_length=prediction_intervals_length,
    )

    result.to_csv(output_csv, index=False, date_format="%Y-%m-%dT%H:%M:%S.%fZ")


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
