"""PytSite Form2 Plugin API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import cache, logger, router
from pytsite.http import Request
from ._form import Form

_CACHE_TTL = 604800  # 1 week
_FORMS = cache.create_pool('form2@forms')


def store(form: Form):
    """Put a form into the cache
    """
    _FORMS.put(form.uid, form, _CACHE_TTL)


def dispense(uid: str, request: Request = None) -> Form:
    """Dispense a form from the cache
    """
    try:
        if not _FORMS.has(uid):
            raise KeyError(f"Form '{uid}' is not found")

        form = _FORMS.get(uid)
        form.request = request or router.request()
        return form

    except Exception as e:
        logger.error(e)
        raise RuntimeError('Unexpected form exception')


def forget(uid: str):
    """Remove a form from teh cache
    """
    _FORMS.rm(uid)
