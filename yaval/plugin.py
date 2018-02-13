
class MetaPlugin(object):

    widget = None

    def get_widget(self):
        return self.widget

    def before_update(self):
        pass

    def after_update(self):
        pass
