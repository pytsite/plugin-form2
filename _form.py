"""PytSite Form2 Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import htmler
from typing import Dict, Iterator, Any, Tuple, List
from pytsite.validation import Validator, Rule
from pytsite.util import random_password as random_str
from plugins.widget2 import Widget
from ._const import GET_WIDGETS_PATH, SUBMIT_PATH


class Form:
    """Form
    """

    @property
    def action(self) -> str:
        return self._action

    @action.setter
    def action(self, value: str):
        self._action = value

    @property
    def cid(self) -> str:
        return self._cid

    @property
    def css(self) -> str:
        return self._css

    @css.setter
    def css(self, value: str):
        self._css = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def steps(self) -> int:
        return self._steps

    @property
    def uid(self) -> str:
        return self._uid

    @uid.setter
    def uid(self, value: str):
        self._uid = value

    @property
    def values(self) -> Dict[str, Any]:
        """Get all widgets' values
        """
        return {k: v[1].value for k, v in self._widgets.items()}

    @property
    def widgets(self) -> List[Widget]:
        """Get all widgets
        """
        return [w[1] for w in sorted(self._widgets.values(), key=lambda x: x[1])]

    def __init__(self, uid: str = None, **kwargs):
        """Init
        """
        self._cid = f'{self.__module__}.{self.__class__.__name__}'
        self._uid = uid or random_str(alphanum_only=True)
        self._action = kwargs.get('action', '#')
        self._css = ''
        self._get_widgets_path = kwargs.get('get_widgets_path', GET_WIDGETS_PATH)
        self._name = kwargs.get('name', self._uid)
        self._steps = 1
        self._validator = Validator()
        self._submit_path = kwargs.get('submit_path', SUBMIT_PATH)
        self._widgets = {}  # type: Dict[str, Tuple[int, Widget]]

    def add_widget(self, widget: Widget, step: int = 1):
        """Add a widget
        """
        if step < 1 or step > (self._steps + 1):
            raise ValueError(f'Invalid step number: {step}')

        if widget.uid in self._widgets:
            raise ValueError(f"The form '{self.uid}' already contains the widget '{widget.uid}'")

        if step > self._steps:
            self._steps = step

        self._widgets[widget.uid] = (step, widget)

        return self

    def add_rule(self, widget_uid: str, rule: Rule):
        """Add a validation rule
        """
        self._validator.add_rule(widget_uid, rule)

        return self

    def get_widgets(self, step: int = 1) -> Iterator[Widget]:
        """Get widgets for particular step
        """
        if self._steps < step < 1:
            raise ValueError(f'Invalid step number: {step}')

        return (w[1] for w in self._widgets.values() if w[0] == step)

    def fill(self, values: Dict, step: int = 1):
        """Fill widgets with values
        """
        if self._steps < step < 1:
            raise ValueError(f'Invalid step number: {step}')

        for w in self.get_widgets(step):
            if w.uid in values:
                w.value = values[w.uid]

        return self

    def validate(self, step: int = 1):
        """Validate the form
        """
        if self._steps < step < 1:
            raise ValueError(f'Invalid step number: {step}')

        fields = []
        for w in self.get_widgets(step):
            if self._validator.has_field(w.uid):
                fields.append(w.uid)
                self._validator.set_val(w.uid, w.value)

        self._validator.validate(fields)

        return self

    def submit(self):
        """Submit the form
        """

        return self

    def render(self) -> str:
        """Render the form
        """
        from ._api import store
        store(self)

        return str(htmler.Div(
            css=f'pytsite-form2-container {self._css}'.strip(),
            data_action_url=self._action,
            data_get_widgets_path=self._get_widgets_path,
            data_steps=self._steps,
            data_submit_path=self._submit_path,
            data_name=self._name,
            data_uid=self._uid,
        ))

    def __len__(self) -> int:
        """___len__()
        """
        return len(self._widgets)

    def __str__(self) -> str:
        """__str__()
        """
        return self.render()
