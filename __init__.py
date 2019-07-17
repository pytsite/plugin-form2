"""PytSite Form2 Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from ._api import store, dispense
from ._form import Form


def plugin_load():
    from plugins import http_api
    from . import _http_api
    from ._const import GET_WIDGETS_PATH, SUBMIT_PATH

    http_api.handle('GET', GET_WIDGETS_PATH, _http_api.GetWidgets, 'form2@widgets')
    http_api.handle('POST', SUBMIT_PATH, _http_api.Submit, 'form2@submit')
