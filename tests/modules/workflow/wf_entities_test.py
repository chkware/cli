# type: ignore
"""
Testing Entities for workflow
"""
from chk.modules.workflow.entities import ChkwareTask, ChkwareValidateTask


class TestChkwareTask:
    @staticmethod
    def test_from_dict_pass():
        task = ChkwareTask.from_dict({"uses": "fetch", "file": "file.chk"})

        assert task.uses == "fetch"
        assert task.file == "file.chk"


class TestChkwareValidateTask:
    @staticmethod
    def test_from_dict_pass():
        task = ChkwareValidateTask.from_dict(
            {"uses": "validate", "file": "validate-file.chk"}
        )

        assert task.uses == "validate"
        assert task.file == "validate-file.chk"
        assert task.arguments is None

        task = ChkwareValidateTask.from_dict(
            {
                "uses": "validate",
                "file": "validate-file.chk",
                "arguments": {"data": {"some": 12, "data": [1, "a"]}},
            }
        )

        assert task.arguments and "data" in task.arguments.model_dump()
