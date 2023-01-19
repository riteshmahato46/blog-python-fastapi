
from app.main import ping


def test_ping():
    str = ping()
    result = {"Ping": "Ok"}
    assert str == result
