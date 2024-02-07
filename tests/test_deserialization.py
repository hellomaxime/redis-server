from utils import deserialize

def test_nil():
    input = "$-1\r\n"
    assert deserialize(input) == ["$-1"]

def test_ping():
    input = "*1\r\n$4\r\nping\r\n"
    assert deserialize(input) == ["*1", "$4", "ping"]

def test_set():
    input = "*3\r\n$3\r\nset\r\n$3\r\nkey\r\n$2\r\n10\r\n"
    assert deserialize(input) == ["*3", "$3", "set", "$3", "key", "$2", "10"]

def test_set_empty():
    input = "*3\r\n$3\r\nset\r\n$3\r\nkey\r\n"
    assert deserialize(input) == ["*3", "$3", "set", "$3", "key"]

def test_echo():
    input = "*2\r\n$4\r\nECHO\r\n$11\r\nHello World\r\n"
    assert deserialize(input) == ["*2", "$4", "ECHO", "$11", "Hello World"]

def test_get():
    input = "*2\r\n$3\r\nGET\r\n$5\r\nmykey\r\n"
    assert deserialize(input) == ["*2", "$3", "GET", "$5", "mykey"]