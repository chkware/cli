"""
Workflow services module
"""

from __future__ import annotations

import json
from collections.abc import Iterable

from chk.infrastructure.view import PresentationBuilder
from chk.modules.workflow import (
    ChkwareTask,
    ChkwareValidateTask,
    StepResult,
    WorkflowConfigNode,
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

    def dump_error_json(self, err: object = None) -> str:
        """dump_error_json"""

        if not err:
            err = self.data.exception

        return json.dumps({"error": (repr(err) if err else "Unspecified error")})

    def dump_error_fmt(self, err: object = None) -> str:
        """dump fmt error str"""

        if not err:
            err = self.data.exception

        return (
            f"Workflow error\n------\n{repr(err)}"
            if err
            else "Workflow error\n------\nUnspecified error"
        )

    def _prepare_dump_data(self) -> dict:
        """prepare dump data"""

        exec_report = self.data.extra
        _document = self.data.file_ctx.document

        r_dump = {}

        if _document and "name" in _document:
            r_dump["name"] = _document["name"]

        if exec_report:
            r_dump["step_count"] = len(_document["tasks"])
            r_dump["step_failed"] = len(
                [item for item in exec_report if not item.is_success]
            )

        r_dump["tasks"] = []

        for item in exec_report:
            item: StepResult  # type: ignore

            response_task_dump = {
                "name": item.task.name,
                "uses": item.task.uses,
                "is_success": item.is_success,
                "exception": repr(item.exception),
            }
            if item.task.uses == "fetch":
                response_task_dump["fetch_request_method"] = (
                    item.others["request_method"]
                    if "request_method" in item.others
                    else ""
                )
                response_task_dump["fetch_request_url"] = (
                    item.others["request_url"] if "request_url" in item.others else ""
                )

            if item.task.uses == "validate":
                response_task_dump["validate_asserts_count_all"] = (
                    item.others["count_all"] if "count_all" in item.others else ""
                )
                response_task_dump["validate_asserts_count_fail"] = (
                    item.others["count_fail"] if "count_fail" in item.others else ""
                )
                response_task_dump["validate_asserts_err_messages"] = [
                    f"      >>> {msg}" for msg in item.others["exceptions"]
                ]

            r_dump["tasks"].append(response_task_dump)
        return r_dump

    def dump_fmt(self) -> str:
        """return formatted string representation"""

        exposed_fmt_str = []
        for key, value in self.data.exposed.items():
            node = str(WorkflowConfigNode.NODE)

            if node in key and len(key) == len(node):
                to_append = self._prepare_dump_str_for_steps()
            else:
                # TODO: Need a json.Encoder for specific PresentableExposeTypes
                #       PresentableExposeTypes for RunReport, ApiResponse, etc
                if isinstance(value, dict):
                    for _k, _v in value.items():
                        if isinstance(_v, Iterable):
                            value[_k] = dict(_v) if isinstance(_v, dict) else _v

                to_append = json.dumps(value)

            exposed_fmt_str.append(to_append)

        return "\n======\n".join(exposed_fmt_str)

    def _prepare_dump_str_for_steps(self) -> str:
        """prepare dump str for steps"""

        dump_dct: dict = self._prepare_dump_data()

        _computed_str = f"\n\nWorkflow: {dump_dct.get('name', '')}"
        _computed_str += f"\nSteps total: {dump_dct.get('step_count', '')}, "
        _computed_str += f"failed: {dump_dct.get('step_failed', '')}"

        tasks = dump_dct.get("tasks", [])

        for one_task in tasks:
            _computed_str += "\n------\n"
            _computed_str += "+ [PASS] " if one_task["is_success"] else "- [FAIL] "
            _computed_str += f"Task: {one_task['name']}\n"
            if one_task["uses"] == "fetch":
                _computed_str += f">> {one_task['fetch_request_method']} {one_task['fetch_request_url']}"
                if not one_task["is_success"]:
                    _computed_str += f"\n>> With message: {one_task['exception']}"
            elif one_task["uses"] == "validate":
                _computed_str += (
                    f">> Total tests: {one_task['validate_asserts_count_all']}, "
                )
                _computed_str += f"Failed: {one_task['validate_asserts_count_fail']}"
                if not one_task["is_success"]:
                    _computed_str += f"\n>> With message: {one_task['exception']}\n"
                    _computed_str += "\n".join(
                        one_task["validate_asserts_err_messages"]
                    )

        return _computed_str

    def dump_json(self) -> str:
        """return json representation"""
        exposed_fmt_str = []

        for key, value in self.data.exposed.items():
            node = str(WorkflowConfigNode.NODE)
            _to_append = {}

            if node in key and len(key) == len(node):
                _to_append = self._prepare_dump_data()
            else:
                if isinstance(value, dict):
                    for _k, _v in value.items():
                        if isinstance(_v, Iterable):
                            value[_k] = dict(_v)

                _to_append = value

            exposed_fmt_str.append(_to_append)

        return json.dumps(exposed_fmt_str)
