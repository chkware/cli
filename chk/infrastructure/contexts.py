"""
App() instance for current thread
"""
from cerberus import Validator

from chk.infrastructure.containers import App


# Initiate global level objects
app = App()
validator = Validator()
