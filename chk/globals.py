"""
Global application functionality
"""
import pydoc
from typing import Dict
from contextvars import ContextVar
from dotmap import DotMap


class App:
    """Global app"""
    config = DotMap({
        'error': pydoc.locate('chk.constants.messages.error.messages'),
    })


# global application object
app_context: ContextVar[App] = ContextVar('app_context', default=App())


def current_app():
    """Get global app context"""
    return app_context.get()


def l10n(message: str, data: Dict | None = None) -> str:
    """get localized message from locale file"""
    message = str(message)
    if data is None: data = {}

    return message.format(**data)
