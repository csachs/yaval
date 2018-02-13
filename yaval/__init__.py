# by christian c. sachs

# correctly prime everything for PySide

import matplotlib
import vispy.app

matplotlib.use('Qt5Agg')
matplotlib.rcParams['backend.qt5'] = 'PySide2'

_ = vispy.app.use_app(backend_name='PySide2')

# noinspection PyPep8
from .plugin_matplotlib import MatplotlibPlugin
# noinspection PyPep8
from .plugin_vispy import VispyPlugin
# noinspection PyPep8
from .values import Values
# noinspection PyPep8
from .visualizer import Visualizer
