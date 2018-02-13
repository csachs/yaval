from .qt import *


class Value(object):

    name = None
    label = None

    resulting_layout = None

    def _set_name_label(self, name, label):
        self.name = name
        if label is None:
            self.label = ' '.join(s.capitalize() for s in name.split('_'))
        else:
            self.label = label

    def generate_widget(self):
        raise RuntimeError('Virtual function call')

    def get_widget(self):
        if self.resulting_layout:
            return self.resulting_layout

        self.resulting_layout = self.generate_widget()

        return self.resulting_layout


class ListValue(Value):
    def __init__(self, value=None, choice=None, name="value", label=None):
        self._set_name_label(name, label)
        self.choice = list(choice)

        if value is None:
            value = choice[0]
        self.value = value

    def generate_widget(self):

        resulting_layout = QHBoxLayout()

        combobox = QComboBox()

        for item in self.choice:
            combobox.addItem(str(item))

        combobox.setCurrentIndex(self.choice.index(self.value))

        def index_changed():
            value_index = combobox.currentIndex()
            self.value = self.choice[value_index]

            if self.callback is not None:
                self.callback(self.name, self.value)

        combobox.currentIndexChanged.connect(index_changed)

        label = QLabel()
        label.setText(self.label)

        resulting_layout.addWidget(label)
        resulting_layout.addWidget(combobox)

        index_changed()

        return resulting_layout


class Action(Value):
    def __init__(self, name="value", label=None, callback=None):
        self._set_name_label(name, label)
        self.callback = callback
        self.value = False

    def generate_widget(self):

        resulting_layout = QHBoxLayout()

        pushbutton = QPushButton()

        pushbutton.setText(self.label)

        def pressed():
            if self.callback is not None:
                self.value = True
                self.callback(self.name, self.value)
                self.value = False

        pushbutton.pressed.connect(pressed)

        resulting_layout.addWidget(pushbutton)

        return resulting_layout


class Label(Value):
    def __init__(self, name="label", label=None, value=None):
        self._set_name_label(name, label)
        self.value = value

        self._label = label

    def update(self, value=None):
        if value is not None:
            self.value = value

        if self._label:
            if '%' in self.label:
                self._label.setText(self.label % (self.value,))
            else:
                self._label.setText(self.label)

    def generate_widget(self):
        resulting_layout = QHBoxLayout()
        self._label = QLabel()
        self.update()
        resulting_layout.addWidget(self._label)
        return resulting_layout


class NumericValue(Value):
    def __init__(self,
                 name="value", value=0.0, label=None, type_=float, minimum=0.0, maximum=1.0, callback=None, unit=""
                 ):
        self.value = value

        self._set_name_label(name, label)

        self.type_ = type_
        self.minimum = minimum
        self.maximum = maximum
        self.callback = callback

        self.unit = unit

        self.interval = None

        self.resulting_layout = None

    def format_label(self, value):
        return str(value)

    def generate_widget(self):

        resulting_layout = QHBoxLayout()

        slider = QSlider()

        textbox = QLineEdit()

        slider.setOrientation(Qt.Horizontal)

        rel_mi, rel_ma = 0, 1000
        abs_mi, abs_ma = self.minimum, self.maximum

        slider.setMinimum(rel_mi)
        slider.setMaximum(rel_ma)

        if self.interval:
            slider.setSingleStep(self.interval)

        slider.setMinimumHeight(10)

        rel_delta = rel_ma - rel_mi
        abs_delta = abs_ma - abs_mi

        def update(value):
            if value > abs_ma:
                value = abs_ma
            if value < abs_mi:
                value = abs_mi

            if self.interval:
                value = round((value - abs_mi)/self.interval) * self.interval + abs_mi

            rel_value = ((value-abs_mi) / abs_delta) * rel_delta + rel_mi

            slider.setValue(int(rel_value))

            value = self.type_(value)

            value_str = self.format_label(value)

            textbox.setText(value_str)

            self.value = value

            if self.callback is not None:
                self.callback(self.name, self.value)

        def slider_changed():
            value = slider.value()
            abs_value = ((value - rel_mi) / rel_delta) * abs_delta + abs_mi
            update(abs_value)

        def textbox_changed():
            value = float(textbox.text())
            update(value)

        slider.valueChanged.connect(slider_changed)
        textbox.textEdited.connect(textbox_changed)

        label = QLabel()
        label.setText(self.label)

        unit = QLabel()
        unit.setText(self.unit)

        resulting_layout.addWidget(label)
        resulting_layout.addWidget(slider)
        resulting_layout.addWidget(textbox)
        resulting_layout.addWidget(unit)

        update(self.value)

        return resulting_layout


class IntValue(NumericValue):
    def __init__(self, name="value", value=0.0, label=None, minimum=0.0, maximum=1.0, callback=None, unit="",
                 interval=1):
        super(IntValue, self).__init__(name, value, label, int, minimum, maximum, callback, unit)
        self.interval = interval


class FloatValue(NumericValue):
    def __init__(self, name="value", value=0.0, label=None, minimum=0.0, maximum=1.0, callback=None, digits=4, unit=""):
        super(FloatValue, self).__init__(name, value, label, float, minimum, maximum, callback, unit)
        self.digits = digits

    def format_label(self, value):
        return str(round(value, self.digits))


class Values(object):
    Value = Value
    IntValue = IntValue
    FloatValue = FloatValue
    ListValue = ListValue
    Label = Label
    Action = Action
