from utils import deserialize

def test1():
    input = "$-1\r\n"
    assert deserialize(input) == ["$-1"]

def test2():
    input = "*1\r\n$4\r\nping\r\n"
    assert deserialize(input) == ["*1", "$4", "ping"]

def test3():
    input = "*3\r\n$3\r\nset\r\n$3\r\nkey\r\n$2\r\n10\r\n"
    assert deserialize(input) == ["*3", "$3", "set", "$3", "key", "$2", "10"]