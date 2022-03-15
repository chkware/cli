"""
Global application functionality
"""

from chk.infrastructure.exception import messages as exception_messages
from dotmap import DotMap


class App:
    """Global app"""

    messages = DotMap({
        'exception': exception_messages
    })


# global application object
app = App()
