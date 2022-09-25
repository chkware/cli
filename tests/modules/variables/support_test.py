from chk.modules.variables.support import parse_args


class TestParseArgs:
    def test_parse_args_pass_for_unique(self):
        argv_s = ['Var1=Val1', 'Var2=Val2', 'Var3=Val3', 'Var=Val']
        response = parse_args(argv_s)

        assert isinstance(response, dict)
        assert len(response) == 4

    def test_parse_args_pass_for_override(self):
        argv_s = ['Var1=Val1', 'Var2=Val2', 'Var3=Val3', 'Var1=Val4']
        response = parse_args(argv_s)

        assert isinstance(response, dict)
        assert len(response) == 3
