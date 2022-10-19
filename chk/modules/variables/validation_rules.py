"""
Validation rules and supporting libs for variables module
"""
import re

from chk.modules.variables.constants import VariableConfigNode as VarConf


def allowed_variable_name(name: str) -> bool:
    """Check if the name start or ends with __"""
    if not re.findall(r"(^[a-zA-Z0-9]+)\w$", name):
        raise ValueError(f"Unsupported variable naming: `{name}`")

    return True


# cerberus validation rules for variables
variable_schema = {
    VarConf.ROOT: {
        "required": False,
        "type": "dict",
        "empty": True,
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
