# type: ignore
"""
Testing Entities for workflow
"""
import pytest
from pydantic import ValidationError

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
            {"uses": "validate", "file": "validate-file-1.chk"}
        )

        assert task.uses == "validate"
        assert task.file == "validate-file-1.chk"
        assert task.arguments is None

        task = ChkwareValidateTask.from_dict(
            {
                "uses": "validate",
                "file": "validate-file.chk",
                "arguments": {"data": {"some": 12, "data": [1, "a"]}},
            }
        )

        assert task.arguments and "data" in task.arguments.model_dump()

    @staticmethod
    def test_from_dict_fail():
        with pytest.raises(ValidationError):
            ChkwareValidateTask.from_dict(
                {
                    "uses": "validate",
                    "file": "validate-file.chk",
                    "arguments": {
                        "data": {"some": 12, "data": [1, "a"]},
                        "other_data": 1,
                    },
                }
            )

        with pytest.raises(ValidationError):
            ChkwareValidateTask.from_dict(
                {
                    "uses": "validate",
                    "file": "validate-file.chk",
                    "other_data": 1,
                    "arguments": {"data": {"some": 12, "data": [1, "a"]}},
                }
            )
