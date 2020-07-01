from .plugin import MetaPlugin
from vispy import scene
from vispy.scene.visuals import Image


class VispyPlugin(MetaPlugin):
    def __init__(self):
        self.canvas = scene.SceneCanvas()
        self.view = self.canvas.central_widget.add_view()

        self.widget = self.canvas.native

    def add_pan_zoom_camera(self):
        self.view.camera = scene.PanZoomCamera(aspect=1)
        self.view.camera.flip = (0, 1, 0)

    def add_turntable_camera(self):
        self.view.camera = scene.TurntableCamera()

    def add_flight_camera(self):
        self.view.camera = scene.FlyCamera()
        self.view.camera.flip = (0, 1, 0)

    def add_image(self, image_data):
        image = Image(data=image_data, parent=self.view.scene)
        if self.view.camera:
            self.view.camera.set_range()
        return image

    def before_update(self):
        pass

    def after_update(self):
        pass
