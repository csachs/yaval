# by Christian C. Sachs

# correctly prime everything for PySide2

import PySide2

import matplotlib
import vispy.app

matplotlib.use('Qt5Agg')

_ = vispy.app.use_app(backend_name='PySide2')

# noinspection PyPep8
from .plugin_matplotlib import MatplotlibPlugin
# noinspection PyPep8
from .plugin_vispy import VispyPlugin
# noinspection PyPep8
from .values import Values
# noinspection PyPep8
from .visualizer import Visualizer
