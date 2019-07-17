"""PytSite Form2 Plugin HTTP API
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import formatters
from pytsite.http import JSONResponse
from pytsite.routing import Controller
from pytsite.validation import ValidatorError
from . import _api


class GetWidgets(Controller):
    """Get Widgets Controller
    """

    def __init__(self):
        super().__init__()

        self.args.add_formatter('step', formatters.AboveZeroInt())

    def exec(self) -> list:
        return [w.as_jsonable() for w in _api.dispense(self.arg('uid')).get_widgets(self.arg('step'))]


class Submit(Controller):
    """Validation Controller
    """

    def __init__(self):
        super().__init__()

        self.args.add_formatter('step', formatters.AboveZeroInt())

    def exec(self) -> dict:
        step = self.arg('step')
        form = _api.dispense(self.arg('uid'))
        form.fill(self.args, step)

        try:
            form.validate(step)

            if step == form.steps:
                form.submit()
                _api.forget(form.uid)

            return {'status': True}

        except ValidatorError as e:
            raise self.server_error(response=JSONResponse({'errors': e.errors}))
