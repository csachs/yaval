import numpy as np
from yaval import MatplotlibPlugin, Values, Visualizer


class PlotVisualizationTest(Visualizer):
    def visualization(self):
        self.add_values(
            Values.FloatValue('factor', 1.0, minimum=-10.0, maximum=10.0),
            Values.FloatValue('offset', 0.0, minimum=-10.0, maximum=10.0)
        )

        plugin = self.register_plugin(MatplotlibPlugin())

        ax = plugin.axis()

        x = np.linspace(0, 100, 1024)
        the_plot, = ax.plot(x, x)

        def update(values):
            y = np.sin(x*values.factor + values.offset)
            the_plot.set_data(x, y)
            ax.relim()
            ax.autoscale_view(True, True, True)

            plugin.update()

        return update


if __name__ == '__main__':
    PlotVisualizationTest.run()
