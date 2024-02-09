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
    input = "*2\r\n$3\r\nset\r\n$3\r\nkey\r\n"
    assert deserialize(input) == ["*2", "$3", "set", "$3", "key"]

def test_set_no_key():
    input = "*1\r\n$3\r\nset\r\n"
    assert deserialize(input) == ["*1", "$3", "set"]

def test_echo():
    input = "*2\r\n$4\r\nECHO\r\n$11\r\nHello World\r\n"
    assert deserialize(input) == ["*2", "$4", "ECHO", "$11", "Hello World"]

def test_get():
    input = "*2\r\n$3\r\nGET\r\n$5\r\nmykey\r\n"
    assert deserialize(input) == ["*2", "$3", "GET", "$5", "mykey"]

def test_set_expiry():
    input = "*5\r\n$3\r\nset\r\n$3\r\nkey\r\n$6\r\nmyvalue\r\n$2\r\nEX\r\n$2\r\n10"
    assert deserialize(input) == ["*5", "$3", "set", "$3", "key", "$6", "myvalue", "$2", "EX", "$2", "10"]

def test_exists():
    input = "*1\r\n$6\r\nEXISTS\r\n"
    assert deserialize(input) == ["*1", "$6", "EXISTS"]

def test_exists_key():
    input = "*2\r\n$6\r\nEXISTS\r\n$3\r\nkey\r\n"
    assert deserialize(input) == ["*2", "$6", "EXISTS", "$3", "key"]

def test_exists_keys():
    input = "*3\r\n$6\r\nEXISTS\r\n$3\r\nkey\r\n$4\r\nkey2\r\n"
    assert deserialize(input) == ["*3", "$6", "EXISTS", "$3", "key", "$4", "key2"]

def test_del_no_key():
    input = "*1\r\n$3\r\nDEL\r\n"
    assert deserialize(input) == ["*1", "$3", "DEL"]

def test_del_key():
    input = "*2\r\n$3\r\nDEL\r\n$3\r\nkey\r\n"
    assert deserialize(input) == ["*2", "$3", "DEL", "$3", "key"]

def test_del_keys():
    input = "*3\r\n$3\r\nDEL\r\n$3\r\nkey\r\n$4\r\nkey2\r\n"
    assert deserialize(input) == ["*3", "$3", "DEL", "$3", "key", "$4", "key2"]