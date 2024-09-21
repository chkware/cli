"""
Workflow services module
"""

from __future__ import annotations

import json

from chk.infrastructure.view import PresentationBuilder
from chk.modules.workflow import (
    ChkwareTask,
    ChkwareValidateTask,
    StepResult,
    WorkflowUses,
)


class ChkwareTaskSupport:
    """ChkwareTaskSupport"""

    @classmethod
    def make_task(cls, task_d_: dict, /, **kwargs: dict) -> ChkwareTask:
        """validate task data"""

        if "base_file_path" not in kwargs:
            raise ValueError("`base_file_path` not passed.")

        if "uses" not in task_d_:
            raise RuntimeError("Malformed task item found.")

        if task_d_["uses"] not in (
            WorkflowUses.fetch.value,
            WorkflowUses.validate.value,
        ):
            raise RuntimeError("task.uses unsupported.")

        base_file_path = str(kwargs["base_file_path"])

        return (
            ChkwareTask(base_file_path, **task_d_)
            if task_d_["uses"] == "fetch"
            else ChkwareValidateTask(base_file_path, **task_d_)
        )


class WorkflowPresenter(PresentationBuilder):
    """WorkflowPresenter"""

    def _prepare_dump_data(self) -> dict:
        """prepare dump data"""

        _, exec_report = self.data.extra
        _document = self.data.file_ctx.document

        r_dump = {}

        if _document and "name" in _document:
            r_dump["name"] = _document["name"]

        if exec_report:
            r_dump["step_count"] = len(exec_report)
            r_dump["step_failed"] = len(
                [item for item in exec_report if not item.is_success]
            )

        r_dump["tasks"] = []

        for item in exec_report:
            item: StepResult  # type: ignore

            response_task_dump = {
                "name": item.name,
                "uses": item.uses,
                "is_success": item.is_success,
                "fetch_request_method": (
                    item.others["request_method"]
                    if "request_method" in item.others
                    else ""
                ),
                "fetch_request_url": (
                    item.others["request_url"] if "request_url" in item.others else ""
                ),
                "validate_asserts_count_all": (
                    item.others["count_all"] if "count_all" in item.others else ""
                ),
                "validate_asserts_count_fail": (
                    item.others["count_fail"] if "count_fail" in item.others else ""
                ),
            }

            r_dump["tasks"].append(response_task_dump)
        return r_dump

    def dump_fmt(self) -> str:
        """return formatted string representation"""

        dump_dct: dict = self._prepare_dump_data()

        _computed_str = f"\n\nWorkflow: {dump_dct.get('name', '')}\n"
        _computed_str += f"Steps total: {dump_dct.get('step_count', '')}, "
        _computed_str += f"failed: {dump_dct.get('step_failed', '')}\n"
        _computed_str += "------\n"

        tasks = dump_dct.get("tasks", [])

        for one_task in tasks:
            _computed_str += "\n\n"
            _computed_str += "+ " if one_task["is_success"] else "- "
            _computed_str += f"Task: {one_task['name']}\n"
            if one_task["uses"] == "fetch":
                _computed_str += f">> {one_task['fetch_request_method']} {one_task['fetch_request_url']}"
            elif one_task["uses"] == "validate":
                _computed_str += (
                    f">> Total tests: {one_task['validate_asserts_count_all']}, "
                )
                _computed_str += f"Failed: {one_task['validate_asserts_count_fail']}"

        return _computed_str

    def dump_json(self) -> str:
        """return json representation"""

        return json.dumps(self._prepare_dump_data())
