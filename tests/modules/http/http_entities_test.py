import tests

from chk.modules.http.entities import HttpSpec_V072
from chk.infrastructure.file_loader import ChkFileLoader, FileContext
from chk.infrastructure.work import handle_worker


class TestHttpSpec_V072:
    def test_get_plain_pass(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-Plain.chk')
        file_ctx = FileContext(None, None, None, doc)

        http = HttpSpec_V072(file_ctx)
        response = handle_worker(http)
        assert type(response) == dict