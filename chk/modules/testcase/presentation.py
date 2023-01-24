"""
Presenting assert data
"""
from json import dumps as dump_js
from dataclasses import dataclass, asdict
from typing import Union

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


def present_assertion_result(ar: AssertResult, as_json: bool = False) -> str | dict:
    """Representation of a AssertResult"""
    if as_json:
        return asdict(ar)

    status = "Success" if ar.is_success else "Fail"
    resp = f"-> Running `{ar.name}` on `{ar.actual_original}` [{status}]"

    if ar.is_success is False:
        resp += "\r\n---\r\n"
        resp += ar.message

    return resp


def present_assertion_result_list(
    assertion_results: list[AssertResult], as_json: bool = False
) -> list:
    resp = []

    for item in assertion_results:
        resp.append(present_assertion_result(item, as_json))

    return resp


def present_result(exposable: list, as_json: bool = False) -> str:
    printables: list[Union[str, dict, list[dict]]] = []

    for item in exposable:
        if isinstance(item, AssertResult):
            printables.append(present_assertion_result(item, as_json))

        elif isinstance(item, dict):
            printables.append(item if as_json else present_dict(item))

        elif isinstance(item, list):
            items = present_assertion_result_list(item, as_json)
            printables.append(items if as_json else "\r\n".join(items))

        else:
            printables.append(str(item))

    return (
        "\r\n\r\n".join(str(item) for item in printables)
        if not as_json
        else dump_js(printables)
    )
