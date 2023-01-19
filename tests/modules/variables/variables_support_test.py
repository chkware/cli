# type: ignore
import pytest

from chk.infrastructure.containers import App
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import data_set
from chk.modules.variables.support import VariableMixin, replace_values


class HavingVariables(VariableMixin):
    def __init__(self, file_ctx: FileContext) -> None:
        self.file_ctx = file_ctx

    def get_file_context(self) -> FileContext:
        return self.file_ctx


class TestVariablePrepareValueTable:
    def test_variable_prepare_value_table_pass(self):
        app = App()
        config = {
            "var_1": "bar",
            "var_2": 2,
            "var_3": "ajax{$var_1}",
            "var_4": "ajax{$Var_1}",
            "var_5": "{$var_2}",
        }

        file_ctx = FileContext(filepath_hash="ab12")
        app.set_compiled_doc(file_ctx.filepath_hash, part="variables", value=config)
        ver = HavingVariables(file_ctx)

        ver.variable_prepare_value_table()

        variables = app.get_compiled_doc(file_ctx.filepath_hash, part="variables")

        assert variables == {
            "var_1": "bar",
            "var_2": 2,
            "var_3": "ajaxbar",
            "var_4": "ajax{$Var_1}",
            "var_5": 2,
        }

    def test_variable_prepare_value_table_pass_with_outer(self):
        app = App()
        config = {
            "var_1": "bar",
            "var_2": 2,
            "var_3": "ajax{$var_1}",
            "var_4": "ajax{$Var_1}",
            "var_5": "{$var_2}",
        }

        outer = {
            "var_1": 1,
            "var_5": 1,
        }

        file_ctx = FileContext(filepath_hash="ab12")
        app.set_outer(file_ctx.filepath_hash, part="variables", val=outer)
        app.set_compiled_doc(file_ctx.filepath_hash, part="variables", value=config)

        ver = HavingVariables(file_ctx)
        ver.variable_prepare_value_table()

        variables = app.get_compiled_doc(file_ctx.filepath_hash, part="variables")

        assert variables == {
            "var_1": 1,
            "var_2": 2,
            "var_3": "ajax1",
            "var_4": "ajax{$Var_1}",
            "var_5": 1,
        }

    def test_variable_prepare_value_table_fails_with_extra_outer(self):
        app = App()
        config = {
            "var_1": "bar",
            "var_2": 2,
            "var_3": "ajax{$var_1}",
            "var_4": "ajax{$Var_1}",
            "var_5": "{$var_2}",
        }

        outer = {
            "var_1": 1,
            "var_6": 1,
        }

        file_ctx = FileContext(filepath_hash="ab12")
        app.set_outer(file_ctx.filepath_hash, part="variables", val=outer)
        app.set_compiled_doc(file_ctx.filepath_hash, part="variables", value=config)

        ver = HavingVariables(file_ctx)
        with pytest.raises(RuntimeError):
            ver.variable_prepare_value_table()

    def test_variable_handle_value_table_for_absolute_pass(self):
        app = App()

        config = {
            "var_1": "bar",
            "var_2": 2,
            "var_3": "ajax{$var_1}",
            "var_4": "ajax{$Var_1}",
            "var_5": "{$var_2}",
        }

        file_ctx = FileContext(filepath_hash="ab12")
        app.set_compiled_doc(file_ctx.filepath_hash, part="variables", value=config)
        ver = HavingVariables(file_ctx)

        variables: dict = {}
        variables_orig = app.get_compiled_doc(file_ctx.filepath_hash, part="variables")
        ver.variable_handle_value_table_for_absolute(variables_orig, variables)

        assert len(variables) == 2
        assert variables == {"var_1": "bar", "var_2": 2}

    def test_variable_handle_value_table_for_absolute_pass_when_spaces(self):
        app = App()

        config = {
            "var_1": "bar",
            "var_2": 2,
            "var_3": "ajax{  $var_1}",
            "var_4": "ajax{ $Var_1     }",
            "var_5": "{$var_2}",
        }

        file_ctx = FileContext(filepath_hash="ab12")
        app.set_compiled_doc(file_ctx.filepath_hash, part="variables", value=config)
        ver = HavingVariables(file_ctx)

        variables: dict = {}
        variables_orig = app.get_compiled_doc(file_ctx.filepath_hash, part="variables")
        ver.variable_handle_value_table_for_absolute(variables_orig, variables)

        assert len(variables) == 2
        assert variables == {"var_1": "bar", "var_2": 2}

    def test_variable_handle_value_table_for_composite_pass(self):
        app = App()

        config = {
            "var_1": "bar",
            "var_2": 2,
            "var_3": "ajax{$var_1}",
            "var_4": "ajax{$Var_1}",
            "var_5": "{$var_2}",
        }

        file_ctx = FileContext(filepath_hash="ab12")
        app.set_compiled_doc(file_ctx.filepath_hash, part="variables", value=config)
        ver = HavingVariables(file_ctx)

        variables: dict = {"var_1": "bar", "var_2": 2}
        variables_orig = app.get_compiled_doc(file_ctx.filepath_hash, part="variables")
        ver.variable_handle_value_table_for_composite(variables_orig, variables)

        assert len(variables) == 5
        assert variables == {
            "var_1": "bar",
            "var_2": 2,
            "var_3": "ajaxbar",
            "var_4": "ajax{$Var_1}",
            "var_5": 2,
        }


class TestVariableMixin:
    """Test VariableMixin"""

    def test_expose_as_dict_pass_for_null_doc(self):
        app = App()
        config = {"expose": []}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.original_doc, file_ctx.filepath_hash, config)

        var = HavingVariables(file_ctx)

        assert var.expose_as_dict() == config

    def test_expose_as_dict_pass_for_doc_value_none(self):
        app = App()
        config = {"expose": None}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.original_doc, file_ctx.filepath_hash, config)

        var = HavingVariables(file_ctx)

        assert var.expose_as_dict() == config

    def test_expose_as_dict_pass_for_doc(self):
        app = App()
        config = {"expose": [".response.code", ".response.headers"]}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.original_doc, file_ctx.filepath_hash, config)

        var = HavingVariables(file_ctx)

        assert var.expose_as_dict() == config

    def test_expose_validated_pass_for_valid_expose(self):
        app = App()
        config = {"expose": [".response.code", ".response.headers"]}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.original_doc, file_ctx.filepath_hash, config)
        var = HavingVariables(file_ctx)

        assert var.expose_validated() == config

    def test_expose_validated_pass_for_no_expose(self):
        app = App()
        config = {}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.original_doc, file_ctx.filepath_hash, config)
        var = HavingVariables(file_ctx)

        assert var.expose_validated() == {"expose": None}

    def test_get_exposable_pass(self):
        app = App()
        compiled_doc = {
            "variables": {"var1": 1, "var2": 2},
            "__local": {
                "_response": {
                    "code": 201,
                    "headers": ["Header 1: Head val 1", "Header 2: Head val 2"],
                }
            },
            "expose": ["$_response.code", "$_response.headers", "$var1:$var2"],
        }

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.compiled_doc, file_ctx.filepath_hash, compiled_doc)

        var = HavingVariables(file_ctx)
        var.make_exposable()
        assert isinstance(var.get_exposable(), list)
        assert var.get_exposable() == [
            201,
            ["Header 1: Head val 1", "Header 2: Head val 2"],
            "1:2",
        ]

    def test_get_symbol_table_pass(self):
        app = App()
        native_vars = {"var1": 1, "var2": 2}
        local_vars = {"var1": 1, "var2": 2}

        file_ctx = FileContext(filepath_hash="ab31")
        # data_set(app.compiled_doc, file_ctx.filepath_hash, native_vars)
        app.set_compiled_doc(file_ctx.filepath_hash, native_vars, "variables")
        app.set_local(file_ctx.filepath_hash, local_vars, "_response")
        app.set_local(file_ctx.filepath_hash, local_vars, "_assertion_results")
        app.set_local(file_ctx.filepath_hash, local_vars, "_execution_results")

        var = HavingVariables(file_ctx)
        assert len(var.get_symbol_table()) == 4

        symbol_keys = var.get_symbol_table().keys()
        assert "_response" in symbol_keys
        assert "_assertion_results" in symbol_keys
        assert "_execution_results" not in symbol_keys

    def test_variable_validated_pass_from_original(self):
        app = App()
        original_doc = {"variables": {"var1": 1, "var2": 2}}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.original_doc, file_ctx.filepath_hash, original_doc)

        var = HavingVariables(file_ctx)
        assert var.variable_validated() == original_doc

    def test_variable_validated_pass_for_null_doc(self):
        app = App()
        original_doc = {"variables": {}}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.original_doc, file_ctx.filepath_hash, original_doc)

        var = HavingVariables(file_ctx)
        assert var.variable_validated() == original_doc

    def test_variable_validated_pass_for_blank_doc(self):
        app = App()
        original_doc = {}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.original_doc, file_ctx.filepath_hash, original_doc)

        var = HavingVariables(file_ctx)
        assert var.variable_validated() == {"variables": {}}

    def test_variable_validated_fail_variable_names_1(self):
        app = App()
        original_doc = {"variables": {"__var1": 1, "var2": 2}}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.original_doc, file_ctx.filepath_hash, original_doc)

        var = HavingVariables(file_ctx)
        with pytest.raises(RuntimeError):
            var.variable_validated()

    def test_variable_validated_fail_variable_names_2(self):
        app = App()
        original_doc = {"variables": {".var1": 1, "var2": 2}}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.original_doc, file_ctx.filepath_hash, original_doc)

        var = HavingVariables(file_ctx)
        with pytest.raises(RuntimeError):
            var.variable_validated()

    def test_variable_validated_fail_variable_names_3(self):
        app = App()
        original_doc = {"variables": {"-var1": 1, "var2": 2}}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.original_doc, file_ctx.filepath_hash, original_doc)

        var = HavingVariables(file_ctx)
        with pytest.raises(RuntimeError):
            var.variable_validated()

    def test_variable_validated_fail_variable_names_4(self):
        app = App()
        original_doc = {"variables": {"$var1": 1, "var2": 2}}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.original_doc, file_ctx.filepath_hash, original_doc)

        var = HavingVariables(file_ctx)
        with pytest.raises(RuntimeError):
            var.variable_validated()

    def test_variable_validated_fail_variable_names_5(self):
        app = App()
        original_doc = {"variables": {"var1.": 1, "var2": 2}}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.original_doc, file_ctx.filepath_hash, original_doc)

        var = HavingVariables(file_ctx)
        with pytest.raises(RuntimeError):
            var.variable_validated()

    def test_variable_validated_fail_if_list(self):
        app = App()
        original_doc = {"variables": ["var1.", 1, "var2", 2]}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.original_doc, file_ctx.filepath_hash, original_doc)

        var = HavingVariables(file_ctx)
        with pytest.raises(RuntimeError):
            var.variable_validated()

    def test_variable_as_dict_pass_from_original(self):
        app = App()
        original_doc = {"variables": {"var1": 1, "var2": 2}}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.original_doc, file_ctx.filepath_hash, original_doc)

        var = HavingVariables(file_ctx)
        assert var.variable_as_dict() == original_doc
        assert var.variable_as_dict(False) == original_doc["variables"]

    def test_variable_as_dict_pass_from_compiled(self):
        app = App()
        original_doc = {"variables": {"var1": 1, "var2": 2}}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.compiled_doc, file_ctx.filepath_hash, original_doc)

        var = HavingVariables(file_ctx)
        assert var.variable_as_dict(compiled=True) == original_doc
        assert var.variable_as_dict(False, True) == original_doc["variables"]

    def test_variable_replace_value_table_pass_for_root_vars(self):
        app = App()
        original_doc = {"variables": {"var1": 1, "var2": 2}}
        replace_doc = {"var1": [1, "a"]}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.compiled_doc, file_ctx.filepath_hash, original_doc)

        var = HavingVariables(file_ctx)
        var.variable_replace_value_table(
            app.compiled_doc[file_ctx.filepath_hash]["variables"], replace_doc
        )

        assert var.get_symbol_table() == {"var1": [1, "a"], "var2": 2}

    def test_variable_replace_value_table_pass_for_local_vars(self):
        app = App()
        original_doc = {"var1": 1, "var2": 2}
        replace_doc = {"var1": [1, "a"]}

        file_ctx = FileContext(filepath_hash="ab31")
        app.set_local(file_ctx.filepath_hash, original_doc, "_some")

        var = HavingVariables(file_ctx)
        var.variable_replace_value_table(
            app.compiled_doc[file_ctx.filepath_hash]["__local"]["_some"], replace_doc
        )

        assert app.get_local(file_ctx.filepath_hash, "_some") == {
            "var1": [1, "a"],
            "var2": 2,
        }

    def test_variable_replace_value_table_fail_when_var_not_found(self):
        app = App()
        original_doc = {"variables": {"var1": 1, "var2": 2}}
        replace_doc = {"var3": [1, "a"]}

        file_ctx = FileContext(filepath_hash="ab31")
        data_set(app.compiled_doc, file_ctx.filepath_hash, original_doc)

        var = HavingVariables(file_ctx)

        with pytest.raises(ValueError):
            var.variable_replace_value_table(
                app.compiled_doc[file_ctx.filepath_hash]["variables"], replace_doc
            )


class TestReplaceValues:
    def test_pass_wth_plain_vars_replace(self):
        variables = {
            "some": 1,
            "goes": "Some {$var1}",
            "here": "{  $var2}",
        }

        values = {
            "var1": "goes here",
            "var2": "HERE",
        }

        repl_variables = {
            "some": 1,
            "goes": "Some goes here",
            "here": "HERE",
        }

        return_doc = replace_values(variables, values)
        assert return_doc == repl_variables
