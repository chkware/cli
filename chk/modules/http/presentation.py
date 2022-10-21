"""
Presentation related logics
"""
from chk.infrastructure.contexts import app


class Presentation:
    """Handle presentation of the outputs of chkware commands."""

    display_buffer: list[str] = []

    @classmethod
    def buffer_msg(cls, message: str) -> None:
        """Buffer display message"""

        if not app.config("buffer_access_off"):
            cls.display_buffer.append(message)

    @classmethod
    def present_result(cls, data: list | BaseException) -> None:
        """Shows result of execution."""

        if isinstance(data, dict):
            if not app.config("buffer_access_off"):
                print(cls.displayable_summary())
            print(cls.displayable_result(data))
        if isinstance(data, list):
            if not app.config("buffer_access_off"):
                print(cls.displayable_summary())
            print(cls.displayable_expose(data))
        else:
            if not app.config("buffer_access_off"):
                print(cls.displayable_summary())
            print(str(data))

    @classmethod
    def displayable_expose(cls, exposable: list) -> str:
        return "\r\n\r\n".join([str(item) for item in exposable])

    @classmethod
    def displayable_result(cls, response: dict[str, object]) -> str:
        """Return result in presentable format."""

        def headers(res: dict) -> str:
            """Headers"""
            return "{}".format(
                "\r\n".join(
                    "{}: {}".format(k, v) for k, v in res.get("headers").items()
                ),
            )

        if response.get("have_all"):
            summary = "{} {} {}".format(
                response.get("version"),
                response.get("code"),
                response.get("reason"),
            )
            return "{}\r\n{}\r\n\r\n{}".format(
                summary, headers(response), response.get("body")
            )

        response.pop("have_all")

        for _, val in response.items():
            if val:
                return str(val)

    @classmethod
    def displayable_summary(cls) -> str:
        """Return execution summary in presentable format."""

        info_string = ""

        for item in cls.display_buffer:
            info_string += item + "\r\n"

        return f"{info_string}\r\n===="
