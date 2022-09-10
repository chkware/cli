from chk.modules.execute.support import ExecutionContext, ExecutionContextBuilder
from chk.modules.testcase.constants import ExecuteConfigNode


class TestExecutionContextBuilder:
    def test_from_testcase_spec_pass(self):
        spec_d = {ExecuteConfigNode.FILE: 'file', ExecuteConfigNode.WITH: ['arg1', 'arg2']}
        response = ExecutionContextBuilder.from_testcase_spec(spec_d)
        assert isinstance(response, ExecutionContext)
