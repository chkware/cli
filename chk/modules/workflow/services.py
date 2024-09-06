"""
Workflow services module
"""

from chk.modules.workflow import ChkwareTask, WorkflowUses, ChkwareValidateTask


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
