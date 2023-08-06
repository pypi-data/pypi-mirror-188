"""Base interfaces.

Every estimator in `river` is a class, and as such inherits from at least one base interface.
These are used to categorize, organize, and standardize the many estimators that `river`
contains.

This module contains mixin classes, which are all suffixed by `Mixin`. Their purpose is to
provide additional functionality to an estimator, and thus need to be used in conjunction with a
non-mixin base class.

This module also contains utilities for type hinting and tagging estimators.

"""
from . import tags, typing
from .base import Base
from .classifier import Classifier, MiniBatchClassifier
from .clusterer import Clusterer
from .drift_detector import (
    BinaryDriftAndWarningDetector,
    BinaryDriftDetector,
    DriftAndWarningDetector,
    DriftDetector,
)
from .ensemble import Ensemble, WrapperEnsemble
from .estimator import Estimator
from .multi_output import MultiLabelClassifier, MultiTargetRegressor
from .regressor import MiniBatchRegressor, Regressor
from .transformer import (
    MiniBatchSupervisedTransformer,
    MiniBatchTransformer,
    SupervisedTransformer,
    Transformer,
)
from .wrapper import Wrapper

__all__ = [
    "Base",
    "BinaryDriftDetector",
    "BinaryDriftAndWarningDetector",
    "Classifier",
    "Clusterer",
    "DriftDetector",
    "DriftAndWarningDetector",
    "Ensemble",
    "Estimator",
    "MiniBatchClassifier",
    "MiniBatchSupervisedTransformer",
    "MiniBatchTransformer",
    "MiniBatchRegressor",
    "MultiLabelClassifier",
    "MultiTargetRegressor",
    "Regressor",
    "SupervisedTransformer",
    "tags",
    "Transformer",
    "typing",
    "WrapperEnsemble",
    "Wrapper",
]
