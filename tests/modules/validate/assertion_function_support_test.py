# type: ignore

"""
Test module for assertion Functions support func
"""
import chk.modules.validate.assertion_function as asrt


class TestAMessages:
    @staticmethod
    def test_get_pass_assert_msg_for_passes():
        msgs = asrt._AMessages
        assert asrt.get_pass_assert_msg_for("equal") == msgs["equal"]["pass"]

    @staticmethod
    def test_get_pass_assert_msg_for_fails():
        assert asrt.get_pass_assert_msg_for("equals") == ""

    @staticmethod
    def test_get_fail_assert_msg_for_passes():
        msgs = asrt._AMessages
        assert asrt.get_fail_assert_msg_for("equal") == msgs["equal"]["fail"]

    @staticmethod
    def test_get_fail_assert_msg_for_fails():
        assert asrt.get_fail_assert_msg_for("equals") == ""
