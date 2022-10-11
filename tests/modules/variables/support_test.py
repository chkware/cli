from chk.infrastructure.containers import App
from chk.infrastructure.file_loader import FileContext
from chk.modules.variables.support import parse_args, VariableMixin


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


class HavingVariables(VariableMixin):
    def __init__(self, file_ctx: FileContext) -> None:
        self.file_ctx = file_ctx

    def get_file_context(self) -> FileContext:
        return self.file_ctx


class TestVariablePrepareValueTable:

    def test_variable_prepare_value_table_pass(self):
        app = App()
        config = {
            'var_1': "bar",
            'var_2': 2,
            'var_3': 'ajax{$var_1}',
            'var_4': 'ajax{$Var_1}',
            'var_5': '{$var_2}',
        }

        file_ctx = FileContext(filepath_hash='ab12')
        app.set_compiled_doc(file_ctx.filepath_hash, part="variables", value=config)
        ver = HavingVariables(file_ctx)

        ver.variable_prepare_value_table()

        variables = app.get_compiled_doc(file_ctx.filepath_hash, part="variables")

        assert variables == {
            'var_1': "bar",
            'var_2': 2,
            'var_3': 'ajaxbar',
            'var_4': 'ajax{$Var_1}',
            'var_5': '2',
        }

    def test_variable_handle_value_table_for_absolute_pass(self):
        app = App()

        config = {
            'var_1': "bar",
            'var_2': 2,
            'var_3': 'ajax{$var_1}',
            'var_4': 'ajax{$Var_1}',
            'var_5': '{$var_2}',
        }

        file_ctx = FileContext(filepath_hash='ab12')
        app.set_compiled_doc(file_ctx.filepath_hash, part="variables", value=config)
        ver = HavingVariables(file_ctx)

        variables: dict = {}
        variables_orig = app.get_compiled_doc(file_ctx.filepath_hash, part="variables")
        ver.variable_handle_value_table_for_absolute(variables_orig, variables)

        assert len(variables) == 2
        assert variables == {'var_1': "bar", 'var_2': 2}

    def test_variable_handle_value_table_for_composite_pass(self):
        app = App()

        config = {
            'var_1': "bar",
            'var_2': 2,
            'var_3': 'ajax{$var_1}',
            'var_4': 'ajax{$Var_1}',
            'var_5': '{$var_2}',
        }

        file_ctx = FileContext(filepath_hash='ab12')
        app.set_compiled_doc(file_ctx.filepath_hash, part="variables", value=config)
        ver = HavingVariables(file_ctx)

        variables: dict = {'var_1': "bar", 'var_2': 2}
        variables_orig = app.get_compiled_doc(file_ctx.filepath_hash, part="variables")
        ver.variable_handle_value_table_for_composite(variables_orig, variables)

        assert len(variables) == 5
        assert variables == {'var_1': "bar", 'var_2': 2, 'var_3': 'ajaxbar', 'var_4': 'ajax{$Var_1}', 'var_5': '2',}
