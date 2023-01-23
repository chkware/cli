# type: ignore
import sys
from io import TextIOWrapper, BytesIO

from chk.infrastructure.file_loader import FileContext
from tests import RES_DIR
from chk.modules.http.main import execute


class TestExecute:
    @staticmethod
    def test_execute_pass_with_display():
        file = RES_DIR + "pass_cases/GET-Plain.chk"
        ctx = FileContext.from_file(file, options={"result": False, "dump": True})

        old_stdout = sys.stdout
        sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

        execute(ctx)

        # get output
        sys.stdout.seek(0)  # jump to the start
        out = sys.stdout.read()  # read output

        # restore stdout
        sys.stdout.close()
        sys.stdout = old_stdout

        # assert
        assert "Making request [Success]" in out
        assert "Prepare exposable [Success]" in out

    @staticmethod
    def test_execute_pass_without_display():
        file = RES_DIR + "pass_cases/GET-Plain.chk"
        ctx = FileContext.from_file(file, options={"result": True, "dump": False})

        old_stdout = sys.stdout
        sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

        resp = execute(ctx)

        # get output
        sys.stdout.seek(0)  # jump to the start
        out = sys.stdout.read()  # read output

        # restore stdout
        sys.stdout.close()
        sys.stdout = old_stdout

        # assert
        assert len(out) == 0
        assert isinstance(resp, list)

    @staticmethod
    def test_execute_fails_with_wrong_url():
        file = RES_DIR + "fail_cases/GET-Plain-WrongURL.chk"
        ctx = FileContext.from_file(file, options={"result": False, "dump": True})

        old_stdout = sys.stdout
        sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

        execute(ctx)

        # get output
        sys.stdout.seek(0)  # jump to the start
        out = sys.stdout.read()  # read output

        # restore stdout
        sys.stdout.close()
        sys.stdout = old_stdout

        # assert
        assert "Making request [Fail]" in out
        assert "Connection error" in out
