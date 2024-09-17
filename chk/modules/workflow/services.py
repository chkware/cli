"""
Workflow services module
"""

from chk.infrastructure.helper import formatter
from chk.infrastructure.symbol_table import Variables
from chk.modules.workflow import ChkwareTask, ChkwareValidateTask, WorkflowUses


class ChkwareTaskSupport:
    """ChkwareTaskSupport"""

    @classmethod
    def make_task(cls, task_d_: dict, /, **kwargs) -> ChkwareTask:
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


class WorkflowPresenter:
    """WorkflowPresenter"""

    __slots__ = ("data",)

    def __init__(self, var: Variables):
        """Construct"""

        self.data: Variables = var

    def print(self) -> None:
        """print to screen"""

        if "document" in self.data and "name" in self.data["document"]:
            formatter(f"\n\nWorkflow: {self.data['document']['name']}")
            formatter(
                f"Steps total: {self.data['document']['step_count']}, "
                f"failed: {self.data['document']['step_failed']}"
            )
            formatter("-" * 5)

        exposed_data: list[dict] = []

        if "steps" in self.data:
            exposed_data = self.data["steps"]

        for one_exposed_data in exposed_data:
            formatter(f"\nTask: {one_exposed_data['name']}")
            if one_exposed_data["uses"] == "fetch":
                formatter(
                    f"-> {one_exposed_data['request_method']} {one_exposed_data['request_url']}"
                )
            elif one_exposed_data["uses"] == "validate":
                formatter(
                    f"-> Total tests: {one_exposed_data['asserts_count_all']}, Failed: {one_exposed_data['asserts_count_fail']}"
                )

    def printjson(self) -> None: ...
