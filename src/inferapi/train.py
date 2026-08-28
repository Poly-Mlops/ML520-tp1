"""Fit the subscription model, evaluate it and write the artifact.

    make model-train        # or: uv run inferapi train

This is where the notebook's modelling cells land.
Keep the signature and write the body of the functions
"""

import logging
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from inferapi.config import TrainingConfig
from inferapi.data import KNOWN_CATEGORIES, Dataset, get_dataset
from inferapi.utils import file_creation_time

logger = logging.getLogger(__name__)

NUMERIC_COLUMNS = [
    "age",
    "campaign",
    "pdays",
    "previous",
    "emp.var.rate",
    "cons.price.idx",
    "cons.conf.idx",
    "euribor3m",
    "nr.employed",
]
# Categories we know the full list of up front (see data.KNOWN_CATEGORIES)...
FIXED_CATEGORY_COLUMNS = list(KNOWN_CATEGORIES)
# ...and the ones we have to learn from the rows we were given.
LEARNED_CATEGORY_COLUMNS = [
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "poutcome",
]


# TODO(LAB): the pipeline keeps its two named steps, `data_processor` (the
# ColumnTransformer) and `model`. Hyperparameters come from `training`, never from
# literals in this file.
def build_model(training: TrainingConfig) -> Pipeline: 
    data_processor = ColumnTransformer(
        [
            ("numerical", StandardScaler(),NUMERIC_COLUMNS),
            ("categorical_fixed",OneHotEncoder(categories=[KNOWN_CATEGORIES[c] for c in FIXED_CATEGORY_COLUMNS], 
                                               handle_unknown="ignore"), FIXED_CATEGORY_COLUMNS),
            ("categorical_learned", OneHotEncoder(handle_unknown="infrequent_if_exist"), LEARNED_CATEGORY_COLUMNS),

        ]

    )
    return Pipeline(
        [
            ("data_processor", data_processor),
            ("model", RandomForestClassifier(n_estimators=training.n_estimators, 
                                             max_depth=training.max_depth, random_state=training.seed))
        ]
    )
    


# TODO(LAB): Implement the same metrics as the notebook
def get_model_evaluation_metrics(
    model: Pipeline, x: pd.DataFrame, y: pd.Series, decision_threshold: float = 0.5
) -> dict[str, float]: 
    probabilities = model.predict_proba(x)[:,1]
    predictions = (probabilities >= decision_threshold).astype(int)
    return{
        "positive_rate":float(y.mean()),
        "accuracy":accuracy_score(y,predictions),
        "precision":precision_score(y, predictions,zero_division=0),
        "recall":recall_score(y,predictions,zero_division=0),
        "roc_auc":roc_auc_score(y,probabilities),
        "average_precision":average_precision_score(y,probabilities)
    }


# TODO(LAB): fit, and nothing else. Validation/evaluation will be done in training_procedure
# TODO(LAB): Add a debug log statement seeing the split shapes
def train(train_config: TrainingConfig, dataset: Dataset) -> Pipeline:
    model = build_model(train_config)
    # checked in data.py to see the already split training data
    model.fit(dataset.train_x,dataset.train_y)
    logger.debug(...)
    return model


def persist_model(model: Pipeline, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output)


# TODO(LAB): split, fit, score on validation, log one `model_trained` event with
# every number in it, then persist. return (model, metrics)
def training_procedure(
    train_config: TrainingConfig,
    dataframe: pd.DataFrame,
    output_model_path: Path | str,
    overwrite_model: bool = True,
) -> tuple[Pipeline, dict[str, float]]: ...
