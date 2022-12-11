# type: ignore
import urllib.request
from chk.modules.variables.entities import ApiResponse


class TestApiResponse:
    def test_loading_json_pass(self):
        with urllib.request.urlopen(
            "https://jsonplaceholder.typicode.com/posts/3"
        ) as res:
            data = dict(
                code=res.code,
                headers=res.headers,
                body=res.read().decode("utf-8"),
                reason=res.reason,
                version="HTTP/1.1",
            )
            s = ApiResponse.from_dict(data)

            assert len(s.dict()) == 5

            assert isinstance(s.dict().get("body"), dict)
            assert len(s.dict().get("body")) == 4
