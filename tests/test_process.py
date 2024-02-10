import time
import os
from utils import process, redis_dict

def test_ping():
    input = ["*1", "$4", "PING"]
    assert process(input) == "PONG"

def test_lower_case():
    input = ["*1", "$4", "ping"]
    assert process(input) == "PONG"

def test_command_not_exist():
    input = ["*1", "$3", "ABC"]
    assert process(input) == "-1"

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

def test_get_no_key():
    input = ["*2", "$3", "GET"]
    assert process(input) == "-2"

def test_get_int():
    redis_dict["mylist"] = []
    input = ["*2", "$3", "GET", "$5", "mylist"]
    assert process(input) == "-6"

def test_get_list():
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

def test_set_no_key():
    input = ["*1", "$3", "set"]
    assert process(input) == "OK"
    assert "" in redis_dict
    assert redis_dict[""] == None

def test_set_expiry():
    input = ["*2", "$3", "SET", "$5", "mykeyexp", "$9", "myvalueexp", "$2", "EX", "$2", "2"]
    assert process(input) == "OK"
    assert "mykeyexp" in redis_dict

def test_get_expiry():
    input = ["*2", "$3", "GET", "$5", "mykeyexp"]
    assert process(input) == "myvalueexp"
    time.sleep(3)
    assert process(input) == None

def test_no_exp_time():
    input = ["*2", "$3", "SET", "$5", "mykeyexp", "$9", "myvalueexp", "$2", "EX"]
    assert process(input) == "-1"

def test_str_exp_time():
    input = ["*2", "$3", "SET", "$5", "mykeyexp", "$9", "myvalueexp", "$2", "EX", "$4", "TIME"]
    assert process(input) == "-1"

def test_exists_no_key():
    input = ["*1", "$6", "EXISTS"]
    assert process(input) == "-3"

def test_exists_key():
    redis_dict["key"] = "value"
    input = ["*2", "$6", "EXISTS", "$3", "key"]
    assert process(input) == 1

def test_exists_keys():
    redis_dict["key"] = "value"
    redis_dict["key2"] = "value"
    input = ["*3", "$6", "EXISTS", "$3", "key", "$4", "key2"]
    assert process(input) == 2

def test_not_exists():
    input = ["*2", "$6", "EXISTS", "$3", "nokey"]
    assert process(input) == 0

def test_del_no_key():
    input = ["*1", "$3", "DEL"]
    assert process(input) == "-4"

def test_del_key():
    redis_dict["key"] = "value"
    input = ["*2", "$3", "DEL", "$3", "key"]
    assert process(input) == 1

def test_del_keys():
    redis_dict["key"] = "value"
    redis_dict["key2"] = "value"
    input = ["*3", "$3", "DEL", "$3", "key", "$4", "key2"]
    assert process(input) == 2

def test_del_not_exists():
    input = ["*2", "$3", "DEL", "$3", "nokey"]
    assert process(input) == 0

def test_incr_no_key():
    input = ["*1", "$4", "INCR"]
    assert process(input) == "-2"

def test_incr_key():
    redis_dict["key"] = 1
    input = ["*2", "$4", "INCR", "$3", "key"]
    assert process(input) == 2

def test_incr_exp():
    redis_dict["key"] = 10
    input = ["*2", "$4", "INCR", "$3", "key"]
    assert process(input) == 11
    del redis_dict["key"]
    input = ["*2", "$4", "INCR", "$3", "key"]
    assert process(input) == 1

def test_decr_no_key():
    input = ["*1", "$4", "DECR"]
    assert process(input) == "-2"

def test_decr_key():
    redis_dict["key"] = 1
    input = ["*2", "$4", "DECR", "$3", "key"]
    assert process(input) == 0

def test_decr_exp():
    redis_dict["key"] = -10
    input = ["*2", "$4", "DECR", "$3", "key"]
    assert process(input) == -11
    del redis_dict["key"]
    input = ["*2", "$4", "DECR", "$3", "key"]
    assert process(input) == -1

def test_lpush_no_key():
    input = ["*1", "$5", "LPUSH"]
    assert process(input) == "-5"

def test_lpush_key_no_value():
    input = ["*2", "$5", "LPUSH", "$3", "key"]
    assert process(input) == "-5"

def test_lpush_value():
    input = ["*3", "$5", "LPUSH", "$3", "keynew", "$1", "1"]
    assert process(input) == 1

def test_lpush_values():
    input = ["*5", "$5", "LPUSH", "$3", "key2", "$1", "1", "$1", "2", "$1", "3"]
    assert process(input) == 3
    assert redis_dict["key2"] == ["3", "2", "1"]

def test_lpush_wrong_type():
    redis_dict["keywrong"] = 1
    input = ["*3", "$5", "LPUSH", "$8", "keywrong", "$1", "1"]
    assert process(input) == "-6"

def test_rpush_values():
    input = ["*7", "$5", "RPUSH", "$3", "keyright", "$1", "1", "$1", "2", "$1", "3", "$1", "4", "$1", "5"]
    assert process(input) == 5
    assert redis_dict["keyright"] == ["1", "2", "3", "4", "5"]

def test_save():
    if os.path.exists("redis_dict.json"):
        os.remove("redis_dict.json")
    input = ["*1", "$4", "SAVE"]
    assert process(input) == "OK"
    assert os.path.exists("redis_dict.json")
    os.remove("redis_dict.json")