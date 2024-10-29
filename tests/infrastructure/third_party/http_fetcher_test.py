# type: ignore

import json

import pytest
import requests
from defusedxml.minidom import parseString

from chk.modules.fetch import ApiResponseModel

BODY_JSON = """[
    {
        "userId": 1,
        "id": 10,
        "title": "optio molestias id quia eum",
        "body": "quo et expedita modi cum officia vel magnidoloribus qui repudiandaevero nisi sitquos veniam quod sed accusamus veritatis error"
    },
    {
        "userId": 2,
        "id": 20,
        "title": "doloribus ad provident suscipit at",
        "body": "qui consequuntur ducimus possimus quisquam amet similiquesuscipit porro ipsam ameteos veritatis officiis exercitationem vel fugit aut necessitatibus totamomnis rerum consequatur expedita quidem cumque explicabo"
    },
    {
        "userId": 3,
        "id": 30,
        "title": "a quo magni similique perferendis",
        "body": "alias dolor cumqueimpedit blanditiis non eveniet odio maximeblanditiis amet eius quis tempora quia autem rema provident perspiciatis quia"
    },
    {
        "userId": 4,
        "id": 40,
        "title": "enim quo cumque",
        "body": "ut voluptatum aliquid illo tenetur nemo sequi quo facilisipsum rem optio mollitia quasvoluptatem eum voluptas quiunde omnis voluptatem iure quasi maxime voluptas nam"
    },
    {
        "userId": 5,
        "id": 50,
        "title": "repellendus qui recusandae incidunt voluptates tenetur qui omnis exercitationem",
        "body": "error suscipit maxime adipisci consequuntur recusandaevoluptas eligendi et est et voluptatesquia distinctio ab amet quaerat molestiae et vitaeadipisci impedit sequi nesciunt quis consectetur"
    },
    {
        "userId": 6,
        "id": 51,
        "title": "soluta aliquam aperiam consequatur illo quis voluptas",
        "body": "sunt dolores aut doloribusdolore doloribus voluptates tempora etdoloremque et quocum asperiores sit consectetur dolorem"
    },
    {
        "userId": 7,
        "id": 61,
        "title": "voluptatem doloribus consectetur est ut ducimus",
        "body": "ab nemo optio odiodelectus tenetur corporis similique nobis repellendus rerum omnis facilisvero blanditiis debitis in nesciunt doloribus dicta doloresmagnam minus velit"
    },
    {
        "userId": 8,
        "id": 71,
        "title": "et iusto veniam et illum aut fuga",
        "body": "occaecati a doloribusiste saepe consectetur placeat eum voluptate dolorem etqui quo quia voluptasrerum ut id enim velit est perferendis"
    },
    {
        "userId": 9,
        "id": 82,
        "title": "laudantium voluptate suscipit sunt enim enim",
        "body": "ut libero sit aut totam inventore suntporro sint qui sunt molestiaeconsequatur cupiditate qui iste ducimus adipiscidolor enim assumenda soluta laboriosam amet iste delectus hic"
    },
    {
        "userId": 10,
        "id": 91,
        "title": "aut amet sed",
        "body": "libero voluptate eveniet aperiam sedsunt placeat suscipit molestiassimilique fugit nam natusexpedita consequatur consequatur dolores quia eos et placeat"
    }
]"""

BODY_XML = """<?xml version="1.0" encoding="utf-8"?><ExchangeRatesSeries xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Table>A</Table><Currency>dolar amerykański</Currency><Code>USD</Code><Rates><Rate><No>210/A/NBP/2024</No><EffectiveDate>2024-10-28</EffectiveDate><Mid>4.0207</Mid></Rate></Rates></ExchangeRatesSeries>"""

HEADERS_DICT = {
    "Access-Control-Allow-Credentials": "true",
    "Age": "20952",
    "Alt-Svc": 'h3=":443"; ma=86400',
    "Cache-Control": "max-age=43200",
    "Cf-Cache-Status": "HIT",
    "Cf-Ray": "8da14444ef3e20b7-IAD",
    "Connection": "close",
    # "Content-Type": "application/json; charset=utf-8",
    "Date": "Tue, 29 Oct 2024 06:56:36 GMT",
    "Etag": 'W/"6b80-Ybsq/K6GwwqrYkAsFxqDXGC7DoM"',
    "Expires": "-1",
    "Nel": '{"report_to":"heroku-nel","max_age":3600,"success_fraction":0.005,"failure_fraction":0.05,"response_headers":["Via"]}',
    "Pragma": "no-cache",
    "Report-To": '{"group":"heroku-nel","max_age":3600,"endpoints":[{"url":"https://nel.heroku.com/reports?ts=1729703228&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&s=AxuRVJp0SmBuV73Zqnbc60aGjboR1NIKVZlJvqHKjVQ%3D"}]}',
    "Reporting-Endpoints": "heroku-nel=https://nel.heroku.com/reports?ts=1729703228&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&s=AxuRVJp0SmBuV73Zqnbc60aGjboR1NIKVZlJvqHKjVQ%3D",
    "Server": "cloudflare",
    "Server-Timing": 'cfL4;desc="?proto=TCP&rtt=1928&sent=3&recv=5&lost=0&retrans=0&sent_bytes=2828&recv_bytes=886&delivery_rate=1793188&cwnd=242&unsent_bytes=0&cid=09191dd0e72e32c3&ts=35&x=0"',
    "Transfer-Encoding": "chunked",
    "Vary": "Origin, Accept-Encoding",
    "Via": "1.1 vegur",
    "X-Content-Type-Options": "nosniff",
    "X-Powered-By": "Express",
    "X-Ratelimit-Limit": "1000",
    "X-Ratelimit-Remaining": "999",
    "X-Ratelimit-Reset": "1729703275",
}

REQUEST_DICT_JSON = {
    "code": "200",
    "info": "HTTP/1.1 200 OK",
    "headers": HEADERS_DICT | {"Content-Type": "application/json; charset=utf-8"},
    "body": json.loads(BODY_JSON),
}

REQUEST_DICT_XML = {
    "code": "200",
    "info": "HTTP/1.1 200 OK",
    "headers": HEADERS_DICT | {"Content-Type": "application/xml; charset=utf-8"},
    "body": BODY_XML,
}


@pytest.fixture
def get_posts_json(requests_mock):
    _headers = HEADERS_DICT | {"Content-Type": "application/json; charset=utf-8"}
    requests_mock.get(
        "https://jsonplaceholder.typicode.com/posts",
        json=json.loads(BODY_JSON),
        headers=_headers,
        status_code=200,
        reason="OK",
    )


@pytest.fixture
def get_posts_xml(requests_mock):
    _headers = HEADERS_DICT | {"Content-Type": "application/xml; charset=utf-8"}
    requests_mock.get(
        "https://jsonplaceholder.typicode.com/posts",
        text=parseString(BODY_XML).toxml(),
        headers=_headers,
        status_code=200,
        reason="OK",
    )


class TestApiResponseModel:
    """TestApiResponseModel"""

    @staticmethod
    def test_from_response_pass(get_posts_json):
        get_posts_json

        resp = requests.get("https://jsonplaceholder.typicode.com/posts")
        amodel = ApiResponseModel.from_response(resp)

        assert isinstance(amodel, ApiResponseModel)

    @staticmethod
    def test_info_pass(get_posts_json):
        get_posts_json

        resp = requests.get("https://jsonplaceholder.typicode.com/posts")
        amodel = ApiResponseModel.from_response(resp)

        assert amodel.info == "HTTP/1.1 200 OK"

    @staticmethod
    def test_bool_pass(get_posts_json):
        get_posts_json

        resp = requests.get("https://jsonplaceholder.typicode.com/posts")
        amodel = ApiResponseModel.from_response(resp)

        assert bool(amodel)

    @staticmethod
    def test_from_dict_with_json_pass(get_posts_json):
        get_posts_json

        amodel = ApiResponseModel.from_dict(**REQUEST_DICT_JSON)
        assert bool(amodel)

    @staticmethod
    def test_from_dict_with_xml_pass(get_posts_xml):
        get_posts_xml

        amodel = ApiResponseModel.from_dict(**REQUEST_DICT_XML)
        assert bool(amodel)

    @staticmethod
    def test_mdl_serializer_pass(get_posts_json):
        get_posts_json

        resp = requests.get("https://jsonplaceholder.typicode.com/posts")
        amodel = ApiResponseModel.from_response(resp)

        _dct = amodel.model_dump()

        assert isinstance(_dct, dict)
        assert all(
            [item in _dct.keys() for item in ["code", "info", "headers", "body"]]
        )

    @staticmethod
    def test_body_as_dict_pass(get_posts_json):
        get_posts_json

        resp = requests.get("https://jsonplaceholder.typicode.com/posts")
        amodel = ApiResponseModel.from_response(resp)

        _body = amodel.body_as_dict()

        assert isinstance(_body, list)

    @staticmethod
    def test_body_as_dict_2_pass(get_posts_xml):
        get_posts_xml

        resp = requests.get("https://jsonplaceholder.typicode.com/posts")
        amodel = ApiResponseModel.from_response(resp)

        _body = amodel.body_as_dict()

        assert isinstance(_body, dict)

    @staticmethod
    def test_as_fmt_str_pass(get_posts_xml):
        get_posts_xml

        resp = requests.get("https://jsonplaceholder.typicode.com/posts")
        amodel = ApiResponseModel.from_response(resp)

        _to_display = amodel.as_fmt_str()

        assert "HTTP/1.1 200 OK" in _to_display
        assert "ExchangeRatesSeries xmlns:xsd" in _to_display

    @staticmethod
    def test_as_fmt_str_2_pass(get_posts_json):
        get_posts_json

        resp = requests.get("https://jsonplaceholder.typicode.com/posts")
        amodel = ApiResponseModel.from_response(resp)

        _to_display = amodel.as_fmt_str()

        assert "HTTP/1.1 200 OK" in _to_display
        assert '"userId": 10, "id": 91, "title":' in _to_display
