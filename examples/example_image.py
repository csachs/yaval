import numpy as np

from yaval import VispyPlugin, Values, Visualizer
from matplotlib.cm import ScalarMappable, cmap_d

# this example needs scikit-image
try:
    from skimage.data import chelsea
    from skimage.filters import threshold_local
except ImportError:
    chelsea = threshold_local = None
    raise SystemExit("This example needs scikit-image.")


class VispyVisualizationTest(Visualizer):
    def visualization(self):
        self.add_values(
            Values.IntValue('block_size', 15, minimum=1, maximum=500, interval=2),
            Values.IntValue('offset', 0.0, minimum=-255.0, maximum=255.0),
            Values.ListValue('gray', sorted(cmap_d.keys()), 'cmap', label="Color Map"),
            Values.Action('refresh'),
            Values.Action('quit')
        )

        img = chelsea().astype(np.float32).mean(axis=2)
        output = np.zeros(img.shape[0:2] + (3,), dtype=np.uint8)

        plugin = self.register_plugin(VispyPlugin())

        plugin.add_pan_zoom_camera()
        image = plugin.add_image(output)

        sm = ScalarMappable()

        def update(values):

            if values.refresh:
                print("just a refresh")
                return
            
            if values.quit:
                raise SystemExit

            print("Current values: %r" % (values,))
            
            sm.set_cmap(values.cmap)

            result = img > threshold_local(img, values.block_size, offset=values.offset)

            result = np.r_[img, 255*result]

            image.set_data(sm.to_rgba(result, bytes=True))
            image.update()

        return update


if __name__ == '__main__':
    VispyVisualizationTest.run()
