from utils import serialize

def test1():
    assert serialize("Hello World") == "+Hello World\r\n"

def test2():
    assert serialize(50) == ":50\r\n"

def test3():
    assert serialize(None) == "$-1\r\n"