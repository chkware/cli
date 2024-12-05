"""
Assertion services
"""

from collections.abc import Callable
from datetime import datetime

import chk.modules.validate.assertion_function as asrt_f
from chk.infrastructure.helper import Cast
from chk.infrastructure.logging import debug
from chk.infrastructure.templating import JinjaTemplate, is_template_str
from chk.modules.validate.assertion_message import get_assert_msg_for
from chk.modules.validate.assertion_validation import AssertionEntityType
from chk.modules.validate.entities import AssertionEntry, RunDetail, RunReport

MAP_TYPE_TO_FN: dict[str, Callable] = {
    AssertionEntityType.Accepted: asrt_f.accepted,
    AssertionEntityType.Declined: asrt_f.declined,
    AssertionEntityType.Equal: asrt_f.equal,
    AssertionEntityType.NotEqual: asrt_f.not_equal,
    AssertionEntityType.Empty: asrt_f.empty,
    AssertionEntityType.NotEmpty: asrt_f.not_empty,
    AssertionEntityType.Boolean: asrt_f.boolean,
    AssertionEntityType.Integer: asrt_f.integer,
    AssertionEntityType.IntegerBetween: asrt_f.integer_between,
    AssertionEntityType.IntegerGreater: asrt_f.integer_greater,
    AssertionEntityType.IntegerGreaterOrEqual: asrt_f.integer_greater_or_equal,
    AssertionEntityType.IntegerLess: asrt_f.integer_less,
    AssertionEntityType.IntegerLessOrEqual: asrt_f.integer_less_or_equal,
    AssertionEntityType.Float: asrt_f.float_,
    AssertionEntityType.FloatBetween: asrt_f.float_between,
    AssertionEntityType.FloatGreater: asrt_f.float_greater,
    AssertionEntityType.FloatGreaterOrEqual: asrt_f.float_greater_or_equal,
    AssertionEntityType.FloatLess: asrt_f.float_less,
    AssertionEntityType.FloatLessOrEqual: asrt_f.float_less_or_equal,
    AssertionEntityType.Str: asrt_f.str_,
    AssertionEntityType.StrHave: asrt_f.str_have,
    AssertionEntityType.StrDoNotHave: asrt_f.str_do_not_have,
    AssertionEntityType.StrStartsWith: asrt_f.str_starts_with,
    AssertionEntityType.StrDoNotStartsWith: asrt_f.str_do_not_starts_with,
    AssertionEntityType.StrEndsWith: asrt_f.str_ends_with,
    AssertionEntityType.StrDoNotEndsWith: asrt_f.str_do_not_ends_with,
    AssertionEntityType.Date: asrt_f.date,
    AssertionEntityType.DateAfter: asrt_f.date_after,
    AssertionEntityType.DateAfterOrEqual: asrt_f.date_after_or_equal,
    AssertionEntityType.DateBefore: asrt_f.date_before,
    AssertionEntityType.DateBeforeOrEqual: asrt_f.date_before_or_equal,
    AssertionEntityType.List: asrt_f.list_,
    AssertionEntityType.ListContains: asrt_f.list_contains,
    AssertionEntityType.ListDoNotContains: asrt_f.list_do_not_contains,
    AssertionEntityType.ListHasIndex: asrt_f.list_has_index,
    AssertionEntityType.ListDoNotHasIndex: asrt_f.list_do_not_has_index,
    AssertionEntityType.Map: asrt_f.map_,
    AssertionEntityType.MapKeyCount: asrt_f.map_key_count,
    AssertionEntityType.MapHasKeys: asrt_f.map_has_keys,
    AssertionEntityType.MapDoNotHasKeys: asrt_f.map_do_not_has_keys,
    AssertionEntityType.MapExactKeys: asrt_f.map_exact_keys,
    AssertionEntityType.Count: asrt_f.count,
}


class AssertionEntryListRunner:
    """AssertionAntiquary is service class that run assertion"""

    @staticmethod
    def _replace_assertion_values(
        assert_item: AssertionEntry, variable_d: dict
    ) -> AssertionEntry:
        """Replace value for actual and expected data

        Args:
            assert_item: AssertionEntry
            variable_d: dict
        Returns:
            AssertionEntry
        """

        # replace actual value for template
        if isinstance(assert_item.actual, str) and is_template_str(assert_item.actual):
            assert_item.actual_given = assert_item.actual
            str_tpl = JinjaTemplate.make(assert_item.actual)
            assert_item.actual = str_tpl.render(variable_d)

        # convert actual value type
        if assert_item.cast_actual_to != "" and isinstance(assert_item.actual, str):
            assert_item.actual_b4_cast = assert_item.actual

            if assert_item.cast_actual_to == "int_or_float":
                assert_item.actual = Cast.to_int_or_float(assert_item.actual)
            elif assert_item.cast_actual_to == "int":
                assert_item.actual = Cast.to_int(assert_item.actual)
            elif assert_item.cast_actual_to == "float":
                assert_item.actual = Cast.to_float(assert_item.actual)
            elif assert_item.cast_actual_to == "bool":
                assert_item.actual = Cast.to_bool(assert_item.actual)
            elif assert_item.cast_actual_to == "none":
                assert_item.actual = Cast.to_none(assert_item.actual)
            elif assert_item.cast_actual_to in ["map", "list", "str"]:
                assert_item.actual = Cast.to_hashable(assert_item.actual)
            elif assert_item.cast_actual_to == "auto":
                assert_item.actual = Cast.to_auto(assert_item.actual)

        # replace expected value for template
        if isinstance(assert_item.expected, str) and is_template_str(
            assert_item.expected
        ):
            str_tpl = JinjaTemplate.make(assert_item.expected)
            assert_item.expected = str_tpl.render(variable_d)

        return assert_item

    @staticmethod
    def _prepare_test_run_result(
        assert_item: AssertionEntry,
        asrt_resp: ValueError | bool,
    ) -> RunDetail:
        def _prepare_message() -> str:
            asrt_fn_name = MAP_TYPE_TO_FN[assert_item.assert_type].__name__

            if isinstance(asrt_resp, ValueError):
                return get_assert_msg_for(f"{asrt_fn_name}.{str(asrt_resp)}").format(
                    **detail.get_message_values()
                )

            if asrt_resp:
                message = (
                    get_assert_msg_for(f"{asrt_fn_name}.pass")
                    if assert_item.msg_pass == ""
                    else assert_item.msg_pass
                )
            else:
                message = (
                    get_assert_msg_for(f"{asrt_fn_name}.fail")
                    if assert_item.msg_fail == ""
                    else assert_item.msg_fail
                )

            return message.format(**detail.get_message_values())

        detail = RunDetail(assert_entry=assert_item)

        if isinstance(asrt_resp, ValueError):
            detail.is_pass = False
            detail.message = _prepare_message()
        else:
            detail.is_pass = asrt_resp
            detail.message = _prepare_message()

        return detail

    @staticmethod
    def _call_assertion_method(
        assert_item: AssertionEntry,
    ) -> ValueError | bool:
        """Call assertion method

        Args:
            assert_item: AssertionEntry
        Returns:
            ValueError | bool
        """

        asrt_fn = MAP_TYPE_TO_FN[assert_item.assert_type]
        return asrt_fn(**dict(assert_item))

    @staticmethod
    def test_run(assert_list: list[AssertionEntry], variables: dict) -> RunReport:
        """Run the tests

        Args:
            assert_list: list[AssertionEntry]
            variables: dict

        Returns:
            RunReport: Test run report
        """

        run_report = RunReport(count_all=len(assert_list))

        for assert_item in assert_list:
            assert_item = AssertionEntryListRunner._replace_assertion_values(
                assert_item, variables
            )
            debug(assert_item)

            resp: RunDetail = AssertionEntryListRunner._prepare_test_run_result(
                assert_item,
                AssertionEntryListRunner._call_assertion_method(assert_item),
            )
            debug(resp)

            run_report.add_run_detail(resp)

        run_report.time_end = datetime.now()

        return run_report
