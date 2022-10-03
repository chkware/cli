"""
Validation rules and supporting libs for variables module
"""
from chk.modules.variables.constants import VariableConfigNode as VarConf


def allowed_variable_name(name: str) -> bool:
    """Check if the name start or ends with __"""

    if name.startswith("__") or name.endswith("__"):
        raise ValueError("Unsupported variable naming")

    return True


# cerberus validation rules for variables
variable_schema = {
    VarConf.ROOT: {
        "required": False,
        "type": "dict",
        "empty": True,
    }
}
