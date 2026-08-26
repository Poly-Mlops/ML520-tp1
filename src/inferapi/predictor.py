"""Defining an ABC to represent a model at serving-time

There are various ways / paradigms to (attempt to) make models uniform.
One of them is using Abstract Base Classes (ABC) and have your
MLE/MLOps/DS subclass them.

Here we concentrate on the serving side.

So the job of the Predictor is to say:
> I am something that can predict, and I support .predict()

Note that you can end up with more ABCs if you want to formalize other
parts of your lifecycle. Is is not rare to see things like:

- MLModel
- DataLoader

This is less of a concern when you are using a single ecosystem / library.
However this is not something that you can guarantee, especially in bigger
corporate context.
"""

from abc import ABC, abstractmethod
from pathlib import Path

import joblib
import pandas as pd

from inferapi.utils import file_creation_time


class Predictor(ABC):
    """Represents a model that predicts things

    NOTE(LAB): The best ABC is yet to be discovered, varies per use case.
    """

    @abstractmethod
    def predict(self, features: pd.DataFrame) -> tuple[int, float]:
        """Return (label, subscription probability) for a single-row frame of raw features."""

    # NOTE(LAB): Default implementation, should override
    def get_version(self) -> str:
        """Whatever identifies the weights being served."""
        return "unknown"


# TODO(LAB): implement SklearnPredictor(Predictor): load the joblib artifact and apply the decision threshold.
class SklearnPredictor(Predictor):
    def __init__(self, artifact_path: Path, threshold: float = 0.5): ...

    ...
