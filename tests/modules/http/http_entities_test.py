# type: ignore
import tests

from chk.modules.http.entities import HttpSpec
from chk.infrastructure.file_loader import ChkFileLoader, FileContext
from chk.infrastructure.work import handle_worker


class TestHttpSpec:
    def test_get_plain_pass(self):
        file = tests.RES_DIR + 'pass_cases/GET-Plain.chk'

        ChkFileLoader.is_file_ok(file)
        f_mangled, f_hash = ChkFileLoader.get_mangled_name(file)

        file_ctx = FileContext(
            filepath=file,
            filepath_mangled=f_mangled,
            filepath_hash=f_hash,
            options={"result": True},
        )

        http = HttpSpec(file_ctx)
        response = handle_worker(http)
        assert isinstance(response, list)
