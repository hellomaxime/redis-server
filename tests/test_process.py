import time
from utils import process, implemented_commands, redis_dict

def test_ping():
    input = ["*1", "$4", "PING"]
    assert process(input) == "PONG"

def test_lower_case():
    input = ["*1", "$4", "ping"]
    assert process(input) == "PONG"

def test_command_not_exist():
    input = ["*1", "$3", "ABC"]
    assert process(input) == -1

def test_echo():
    input = ["*2", "$4", "ECHO", "$11", "Hello World"]
    assert process(input) == "Hello World"

def test_echo_none():
    input = ["*2", "$4", "ECHO"]
    assert process(input) == None

def test_set():
    input = ["*3", "$3", "set", "$3", "mykey", "$2", "10"]
    assert process(input) == "OK"
    assert "mykey" in redis_dict

def test_get_int():
    input = ["*2", "$3", "GET", "$5", "mykey"]
    assert process(input) == 10

def test_set_str():
    input = ["*3", "$3", "set", "$3", "mykeystr", "$7", "myvalue"]
    assert process(input) == "OK"
    assert "mykeystr" in redis_dict

def test_get_str():
    input = ["*2", "$3", "GET", "$5", "mykeystr"]
    assert process(input) == "myvalue"

def test_set_empty():
    input = ["*3", "$3", "set", "$3", "mykeyempty"]
    assert process(input) == "OK"
    assert "mykeyempty" in redis_dict
    assert redis_dict["mykeyempty"] == ""

def test_set_expiry():
    input = ["*2", "$3", "SET", "$5", "mykeyexp", "$9", "myvalueexp", "$2", "EX", "$2", "2"]
    assert process(input) == "OK"
    assert "mykeyexp" in redis_dict

def test_get_expiry():
    input = ["*2", "$3", "GET", "$5", "mykeyexp"]
    assert process(input) == "myvalueexp"
    time.sleep(3)
    assert process(input) == None