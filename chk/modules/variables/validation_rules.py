"""
Validation rules and supporting libs for variables module
"""
import re
from collections.abc import Callable

from chk.modules.variables.constants import VariableConfigNode as VarConf


def allowed_variable_name(field: object, value: str, error: Callable) -> None:
    """Check if the name start or ends with __"""
    if not re.findall(r"(^[a-zA-Z0-9]+)\w$", value):
        error(field, f"Unsupported variable naming: `{value}`")


# cerberus validation rules for variables
variable_schema = {
    VarConf.ROOT: {
        "required": False,
        "type": "dict",
        "empty": True,
        "nullable": True,
        "keysrules": {
            "type": "string",
            "check_with": allowed_variable_name
        },
    }
}

# cerberus validation rules for variables
expose_schema = {
    VarConf.EXPOSE: {
        "required": False,
        "type": "list",
        "empty": True,
        "nullable": True,
    }
}
