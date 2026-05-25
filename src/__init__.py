"""Top-level package exports for notebook-friendly imports.

Examples:
    import src
    from src import plots, eval
    from src.utils import data_utils
    from src.modeling import train
"""

from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .modeling import eval, predict, train
    from .utils import data_utils
    from .visualization import eda_utils, plots

_MODULE_PATHS = {
    "eval": ".modeling.eval",
    "plots": ".visualization.plots",
    "predict": ".modeling.predict",
    "train": ".modeling.train",
    "data_utils": ".utils.data_utils",
    "eda_utils": ".visualization.eda_utils",
}

__all__ = [
    "eval",
    "plots",
    "predict",
    "train",
    "data_utils",
    "eda_utils",
]


def __getattr__(name):
    if name not in _MODULE_PATHS:
        raise AttributeError(f"module 'src' has no attribute '{name}'")
    module = import_module(_MODULE_PATHS[name], __name__)
    globals()[name] = module
    return module
