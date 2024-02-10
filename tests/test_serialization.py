from utils import serialize

def test_str():
    assert serialize("Hello World") == "+Hello World\r\n"

def test_int():
    assert serialize(50) == ":50\r\n"

def test3():
    assert serialize(None) == "$-1\r\n"

def test_error():
    input = "-1"
    assert serialize(input) == "-command not implemented\r\n"

def test_empty_str():
    input = ""
    assert serialize(input) == "+\r\n"

def test_err1():
    input = "-1"
    assert serialize(input) == "-command not implemented\r\n"

def test_err2():
    input = "-2"
    assert serialize(input) == "-wrong number of arguments (given 0, expected 1)\r\n"

def test_err3():
    input = "-3"
    assert serialize(input) == "-ERR wrong number of arguments for 'exists' command\r\n"

def test_err4():
    input = "-4"
    assert serialize(input) == "-ERR wrong number of arguments for 'del' command\r\n"

def test_err5():
    input = "-5"
    assert serialize(input) == "-ERR wrong number of arguments for 'lpush' command\r\n"

def test_err6():
    input = "-6"
    assert serialize(input) == "-WRONGTYPE Operation against a key holding the wrong kind of value\r\n"

def test_err7():
    input = "-7"
    assert serialize(input) == "-ERR wrong number of arguments for 'rpush' command\r\n"