"""
Global application functionality
"""

from chk.infrastructure.exception import messages as exception_messages


class App:
    """Global app"""

    messages = {
        'exception': exception_messages
    }


# global application object
app = App()
