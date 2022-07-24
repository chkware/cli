import tests

from chk.modules.http.entities import HttpSpec
from chk.infrastructure.file_loader import ChkFileLoader, FileContext
from chk.infrastructure.work import handle_worker


class TestHttpSpec:
    def test_get_plain_pass(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-Plain.chk')
        file_ctx = FileContext(None, None, None, doc)

        http = HttpSpec(file_ctx)
        response = handle_worker(http)
        assert type(response) == dict
