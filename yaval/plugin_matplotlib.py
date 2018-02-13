from .plugin import MetaPlugin

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib import pyplot as plt

from .qt import *


class MatplotlibPlugin(MetaPlugin):

    def __init__(self, with_toolbar=False, with_zoom=False):

        self.plt = plt
        self.figure = self.plt.figure()

        layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.canvas = FigureCanvasQTAgg(self.figure)

        self.current_axis = None

        if with_toolbar:
            self.toolbar = NavigationToolbar2QT(self.canvas, self.canvas)
            layout.addWidget(self.toolbar)
            self.toolbar.pan()

        layout.addWidget(self.canvas)

        if with_zoom:
            def _zoom(e):
                factor = 2 if e.button == 'down' else 0.5
                xlim, ylim = self.current_axis.get_xlim(), self.current_axis.get_ylim()
                self.current_axis.set_xlim(
                    xlim[0] + (xlim[1] - xlim[0])*0.5 - (xlim[1] - xlim[0])*0.5*factor,
                    xlim[0] + (xlim[1] - xlim[0])*0.5 + (xlim[1] - xlim[0])*0.5*factor
                )
                self.current_axis.set_ylim(
                    ylim[0] + (ylim[1] - ylim[0])*0.5 - (ylim[1] - ylim[0])*0.5*factor,
                    ylim[0] + (ylim[1] - ylim[0])*0.5 + (ylim[1] - ylim[0])*0.5*factor
                )
                self.canvas.draw()
            self.canvas.mpl_connect('scroll_event', _zoom)

    def update(self):
        self.canvas.draw()

    def axis(self):
        self.current_axis = self.figure.add_subplot(111)
        return self.current_axis
