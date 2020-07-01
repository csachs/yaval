import time

from yaval.plugin import MetaPlugin
from yaval.values import Values

from .qt import *


class Visualizer(QDialog):

    title = "Visualizer"

    result_table = False
    print_update_time = False

    Values = Values

    def __init__(self, parent=None):

        super(Visualizer, self).__init__(parent)
        self.plugin = MetaPlugin()
        self.setWindowTitle(self.title)
        self.setWindowFlags((self.windowFlags() & Qt.CustomizeWindowHint)
                            | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)

        if False:
            menu_bar = QMenuBar()

            menu_file = menu_bar.addMenu("File")

            open_action = menu_file.addAction("Open")

            def _dummy():
                print("CLICKED")
            open_action.triggered.connect(_dummy)
            print(menu_file.addAction("Exit"))

        outer_layout = QVBoxLayout()

        layout = QHBoxLayout()
        value_container = QVBoxLayout()
        splitter = QSplitter()

        layout.addWidget(splitter)

        self.values = []
        self.value_input_target = value_container

        self.setLayout(outer_layout)

        # outer_layout.addWidget(menu_bar)
        outer_layout.addLayout(layout)

        # layout.addWidget(canvas.native)
        # layout.addLayout(value_container)

        receptor_widget = QWidget()
        receptor = QVBoxLayout()
        receptor_widget.setLayout(receptor)

        self.receptor = receptor

        # receptor.addWidget()

        # receptor.addWidget(canvas.native)

        splitter.addWidget(receptor_widget)

        empty = QWidget()
        empty.setLayout(value_container)

        splitter.addWidget(empty)

        model = ListOfDictsModel()

        model.update_data([
            #    {"a": 2, "b": 3, "c": 4},
            #    {"a": 12, "b": 23, "c": 54},
            #    {"a": 22, "b": 33, "c": 764},
            #    {"a": 32, "b": 43, "c": 74}
        ])

        # QApplication.clipboard().setText(model.get_clipboard_str())

        self.output_model = model

        tv = QTableView()
        tv.setModel(model)
        tv.setEditTriggers(QAbstractItemView.NoEditTriggers)

        result_layout = QVBoxLayout()

        result_layout.addWidget(tv)

        copy_button = QPushButton()
        copy_button.setText("Copy to Clipboard")

        def _copy():
            QApplication.clipboard().setText(model.get_clipboard_str())

        copy_button.clicked.connect(_copy)

        result_layout.addWidget(copy_button)

        result_layout_widget = QWidget()
        result_layout_widget.setLayout(result_layout)

        if self.result_table:
            splitter.addWidget(result_layout_widget)

        self.visualization_callback = self.visualization()

        self.plugin.before_update()
        self.visualization_callback(self.get_values())
        self.plugin.after_update()

    def register_plugin(self, plugin):
        self.receptor.addWidget(plugin.get_widget())
        self.plugin = plugin
        return plugin

    def visualization_callback(self, values):
        pass

    # noinspection PyUnusedLocal
    def value_change_callback(self, what, to):
        before = time.time()
        values = self.get_values()
        values['_modified'] = what
        self.plugin.before_update()
        self.visualization_callback(values)
        self.plugin.after_update()
        elapsed = time.time() - before
        if self.print_update_time:
            print("whole update took %.4fs" % (elapsed,))

    def add_values(self, *values):
        for value in values:
            if isinstance(value, Values.Value):
                self.add_value(value)
            else:
                for inner_value in value:
                    self.add_value(inner_value)

    def add_value(self, value):
        if value not in self.values:
            value.callback = self.value_change_callback
            self.values.append(value)
            self.value_input_target.addLayout(value.get_widget())

    def get_values(self):

        class AccessByMemberDict(dict):
            def __getattr__(self, item):
                if item in self:
                    return self[item]

        return AccessByMemberDict({value.name: value.value for value in self.values})

    def visualization(self):
        def _vis(_):
            pass
        return _vis

    @classmethod
    def run(cls):
        import vispy
        app = vispy.app.use_app('PySide2')
        _ = app.native
        c_ = cls()
        c_.show()
        app.run()


class ListOfDictsModel(QStandardItemModel):
    _data = None
    _header = None

    _float_precision = 4

    def __init__(self, float_precision=4):
        self._float_precision = float_precision
        super(ListOfDictsModel, self).__init__()

    def _format_value(self, value):
        if isinstance(value, float):
            return ('%%.%df' % self._float_precision) % value
        elif isinstance(value, int):
            return str(value)
        else:
            return str(value)

    def update_data(self, data, header=None):

        self._data = data

        if header is None:
            try:
                self._header = list(sorted(data[0].keys()))
            except IndexError:
                self._header = []
        else:
            self._header = header

        self.setColumnCount(len(self._header))
        self.setRowCount(len(self._data))

        for n, header_item in enumerate(self._header):
            self.setHorizontalHeaderItem(n, QStandardItem(str(header_item)))

        for row, row_items in enumerate(self._data):
            for n, header_item in enumerate(self._header):
                self.setItem(row, n, QStandardItem(self._format_value(row_items[header_item])))

    def get_clipboard_str(self):
        result = ""

        result += "\t".join(str(h) for h in self._header) + "\n"

        for row, row_items in enumerate(self._data):
            result += "\t".join(str(row_items[h]) for h in self._header) + "\n"

        return result
