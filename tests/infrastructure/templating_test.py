# type: ignore
"""
test templating
"""

import pytest

from chk.infrastructure.templating import JinjaTemplate


class TestJinjaTemplate:
    @staticmethod
    def test_basic_tpl_create():
        data = {
            "a": {
                "b": {
                    "c": [1, 2],
                    "cstr": "Some string",
                    "cfloat": 0.0025,
                }
            }
        }

        tpl = JinjaTemplate.make("<% a.b.c %>")
        assert tpl.render(data) == [1, 2]

        tpl = JinjaTemplate.make("Some <% a.b.c %>")
        assert tpl.render(data) == "Some [1, 2]"

    @staticmethod
    def test_basic_tpl_create_fail():
        with pytest.raises(ValueError):
            JinjaTemplate.make("")
