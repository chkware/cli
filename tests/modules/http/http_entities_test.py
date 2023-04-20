# type: ignore
import tests

from chk.modules.http.entities import HttpSpec
from chk.infrastructure.file_loader import ChkFileLoader, FileContext, FileLoader
from chk.infrastructure.work import handle_worker


class TestHttpSpec:
    def test_get_plain_pass(self):
        file_path = tests.RES_DIR + "pass_cases/GET-Plain.chk"

        ChkFileLoader.is_file_ok(file_path)
        _, f_hash = ChkFileLoader.get_mangled_name(file_path)

        file_ctx = FileContext(
            filepath=file_path,
            filepath_hash=f_hash,
            options={"result": True, "dump": False},
            document=FileLoader.load_yaml(file_path)
        )

        http = HttpSpec(file_ctx)
        response = handle_worker(http)
        assert isinstance(response, list)
