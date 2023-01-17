from app.main import ping
def test_ping():
    result = ping()
    print(result)
    assert result == {"Ping": "Ok"}