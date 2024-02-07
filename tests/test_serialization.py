from utils import serialize

def test_str():
    assert serialize("Hello World") == "+Hello World\r\n"

def test_int():
    assert serialize(50) == ":50\r\n"

def test3():
    assert serialize(None) == "$-1\r\n"

def test_error():
    input = -1
    assert serialize(input) == "-command not implemented\r\n"

def test_empty_str():
    input = ""
    assert serialize(input) == "+\r\n"