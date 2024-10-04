# type: ignore
"""
Testing Entities for workflow
"""
from pathlib import Path

import pytest
from pydantic import ValidationError

from chk.modules.workflow.entities import ChkwareTask, ChkwareValidateTask

fp = f"{Path.cwd()}/tests/resources/storage/spec_docs/workflow_cases/simple"


class TestChkwareTask:
    @staticmethod
    def test_from_dict_pass():

        task = ChkwareTask(
            fp,
            **{
                "name": "Sample fetch",
                "uses": "fetch",
                "file": "./coinstats-usd-validate.chk",
            },
        )

        assert task.uses == "fetch"
        assert task.file == f"{fp}/coinstats-usd-validate.chk"


class TestChkwareValidateTask:
    @staticmethod
    def test_from_dict_pass():
        task = ChkwareValidateTask(
            fp,
            **{
                "name": "Sample validate",
                "uses": "validate",
                "file": "./coinstats-usd-validate.chk",
            },
        )

        assert task.uses == "validate"
        assert task.file == f"{fp}/coinstats-usd-validate.chk"
        assert isinstance(task.arguments, ChkwareValidateTask.ChkwareTaskDataArgument)

        task = ChkwareValidateTask(
            fp,
            **{
                "name": "Sample validate - 2",
                "uses": "validate",
                "file": "./coinstats-usd-validate.chk",
                "arguments": {"data": {"some": 12, "data": [1, "a"]}},
            },
        )

        assert task.arguments and "data" in task.arguments.model_dump()

    @staticmethod
    def test_from_dict_fail():
        with pytest.raises(ValidationError):
            ChkwareValidateTask(
                fp,
                **{
                    "name": "Sample validate - 3",
                    "uses": "validate",
                    "file": "./coinstats-usd-validate.chk",
                    "arguments": {
                        "data": {"some": 12, "data": [1, "a"]},
                        "other_data": 1,
                    },
                },
            )

        with pytest.raises(ValidationError):
            ChkwareValidateTask(
                fp,
                **{
                    "name": "Sample validate - 4",
                    "uses": "validate",
                    "file": "./coinstats-usd-validate.chk",
                    "other_data": 1,
                    "arguments": {"data": {"some": 12, "data": [1, "a"]}},
                },
            )
