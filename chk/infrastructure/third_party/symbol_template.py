"""
Symbol template management
"""
import jinja2

__env = jinja2.Environment()


def get_template_from_str(template_str: str) -> jinja2.Template:
    """Create template from string

    Args:
        template_str: str, Template string

    Returns:
        jinja template

    """

    global __env

    return __env.from_string(template_str)
