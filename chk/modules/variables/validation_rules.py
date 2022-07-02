"""
Validation rules and supporting libs for variables module
"""
from chk.modules.variables.constants import VariableConfigNode as VarConf


variable_schema = {  # cerberus validation rules
    VarConf.ROOT: {
        'required': False,
        'type': 'dict',
        'empty': True,
    }
}
