# yaval

yet another visualization abstraction layer

A tiny wrapper library, presenting the library user a nice simplified way to produce (simple) visualization interactions.
The common scheme is input data + user adjustable parameters → visualization.
It is centered around vispy, using PySide(2) as GUI toolkit. Additionally, matplotlib might be used.
See `examples/example_image.py` or `examples/example_plot.py` (cf. below).

**Warning: Alpha stage, subject to change!**

## Example

```python
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

```

Resulting in:

![yaval Visualization Demo](https://csachs.github.io/yaval/example_plot.gif)

## License

BSD