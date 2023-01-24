"""
Presenting assert data
"""
from dataclasses import dataclass

from chk.modules.http.presentation import present_dict


@dataclass
class AssertResult:
    """
    Holds assertion result after test run complete
    """

    name: str
    name_run: str
    actual_original: str
    is_success: bool = True
    message: str = ""
    assert_fn: str = ""


def present_assertion_result(ar: AssertResult) -> str:
    status = "Success" if ar.is_success else "Fail"
    resp = f"- Running `{ar.name}` on `{ar.actual_original}` [{status}]"

    if ar.is_success is False:
        resp += "\r\n---\r\n"
        resp += ar.message

    return resp


def present_assertion_result_list(assertion_results: list[AssertResult]) -> str:
    resp = ""

    for item in assertion_results:
        resp += present_assertion_result(item)
        resp += "\r\n"

    return resp


def present_result(exposable: list) -> str:
    printables: list[str] = []

    for item in exposable:
        if isinstance(item, AssertResult):
            printables.append(present_assertion_result(item))

        elif isinstance(item, dict):
            printables.append(present_dict(item))

        elif isinstance(item, list):
            printables.append(present_assertion_result_list(item))

        else:
            printables.append(str(item))

    return "\r\n\r\n".join(printables)
