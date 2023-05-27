"""
Symbol template management
"""
import jinja2


def get_template_from_str(template_str: str) -> jinja2.Template:
    """Create template from string

    Args:
        template_str: str, Template string

    Returns:
        jinja template

    """

    env = jinja2.Environment(autoescape=True)
    return env.from_string(template_str)
