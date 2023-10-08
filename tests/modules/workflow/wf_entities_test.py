# type: ignore
"""
Testing Entities for workflow
"""
from chk.modules.workflow.entities import ChkwareTask


class TestChkwareTask:
    @staticmethod
    def test_from_dict_pass():
        task = ChkwareTask.from_dict({"uses": "fetch", "file": "file.chk"})

        assert task.uses == "fetch"
        assert task.file == "file.chk"
