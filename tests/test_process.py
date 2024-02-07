from utils import process

def test1():
    input = ["*1", "$4", "PING"]
    assert process(input) == "PONG"