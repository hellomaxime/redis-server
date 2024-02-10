import time
import json
import os

implemented_commands = ["PING", "ECHO", "SET", "GET", "EXISTS", "DEL", "INCR", "DECR", "LPUSH", "RPUSH", "SAVE"]

if os.path.exists("redis_dict.json"):
    with open("redis_dict.json", "r") as file:
        redis_dict = json.load(file)
else:
    redis_dict = {}

expiry_dict = {}

def deserialize(data):
    list_commands = data.splitlines()
    return list_commands    

def process(list_commands):

    command = list_commands[2].upper()

    if command not in implemented_commands:
        return "-1"

    if command == "PING":
        if len(list_commands) > 3:
            return list_commands[4]
        return "PONG"
    elif command == "ECHO":
        if len(list_commands) < 4:
            return None
        return list_commands[4]
    elif command == "SET":  
        if len(list_commands) == 3:
            redis_dict[""] = None
            return "OK"
        if len(list_commands) < 7:
            redis_dict[list_commands[4]] = ""
        elif list_commands[6].isdigit():
            redis_dict[list_commands[4]] = int(list_commands[6])
        else:
            redis_dict[list_commands[4]] = list_commands[6]
        if len(list_commands) >= 9: 
            if len(list_commands) == 9 or not list_commands[10].isdigit():
                return "-1"
            exp_option = list_commands[8].upper()
            if exp_option == "EX":
                expiry_dict[list_commands[4]] = time.time() + int(list_commands[10])
            elif exp_option == "PX":
                expiry_dict[list_commands[4]] = time.time() + int(list_commands[10])/1000
            elif exp_option == "EXAT":
                expiry_dict[list_commands[4]] = int(list_commands[10])
            elif exp_option == "PXAT":
                expiry_dict[list_commands[4]] = int(list_commands[10])/1000
            else:
                return "-1"        
        return "OK"   
    elif command == "GET":        
        if len(list_commands) == 3:
            return "-2"
        if len(list_commands) > 4 and list_commands[4] in redis_dict:
            if type(redis_dict[list_commands[4]]) == list:
                return "-6"
            if list_commands[4] in expiry_dict and expiry_dict[list_commands[4]] < time.time():
                del expiry_dict[list_commands[4]]
                del redis_dict[list_commands[4]]
                return None
            return redis_dict[list_commands[4]]
        return None
    elif command == "EXISTS":
        if len(list_commands) == 3:
            return "-3"
        count = 0
        for key in list_commands[4::2]:
            if key in expiry_dict and expiry_dict[key] < time.time():
                del expiry_dict[key]
                del redis_dict[key]
            else:
                if key in redis_dict:
                    count += 1
        return count
    elif command == "DEL":
        if len(list_commands) == 3:
            return "-4"
        count = 0
        for key in list_commands[4::2]:
            if key in redis_dict:
                del redis_dict[key]
                count += 1
                if key in expiry_dict:
                    del expiry_dict[key]
        return count
    elif command == "INCR" or command == "DECR":
        if len(list_commands) == 3:
            return "-2"
        if len(list_commands) > 4 and list_commands[4] in redis_dict:
            if list_commands[4] in expiry_dict and expiry_dict[list_commands[4]] < time.time():
                del expiry_dict[list_commands[4]]
                redis_dict[list_commands[4]] = 0
            
            if command == "INCR":
                redis_dict[list_commands[4]] += 1
            else:
                redis_dict[list_commands[4]] -= 1
        else:
            if command == "INCR":
                redis_dict[list_commands[4]] = 1
            else:
                redis_dict[list_commands[4]] = -1
        return redis_dict[list_commands[4]]
    elif command == "LPUSH":
        if len(list_commands) <= 5:
            return "-5"
        if list_commands[4] in redis_dict:
            if type(redis_dict[list_commands[4]]) == list:
                redis_dict[list_commands[4]][:0] = list_commands[-1:5:-2]
            else:
                return "-6"
        else:
            redis_dict[list_commands[4]] = list_commands[-1:5:-2]
        return len(redis_dict[list_commands[4]])
    elif command == "RPUSH":
        if len(list_commands) <= 5:
            return "-7"
        if list_commands[4] in redis_dict:
            if type(redis_dict[list_commands[4]]) == list:
                redis_dict[list_commands[4]].extend(list_commands[6::2])
            else:
                return "-6"
        else:
            redis_dict[list_commands[4]] = list_commands[6::2]
        return len(redis_dict[list_commands[4]])
    elif command == "SAVE":
        with open("redis_dict.json", "w") as file:
            json.dump(redis_dict, file)
        return "OK"

def serialize(response):
    if type(response) == str:
        if response == "-1":
            return "-command not implemented\r\n"
        elif response == "-2":
            return "-wrong number of arguments (given 0, expected 1)\r\n"
        elif response == "-3":
            return "-ERR wrong number of arguments for 'exists' command\r\n"
        elif response == "-4":
            return "-ERR wrong number of arguments for 'del' command\r\n"
        elif response == "-5":
            return "-ERR wrong number of arguments for 'lpush' command\r\n"
        elif response == "-6":
            return "-WRONGTYPE Operation against a key holding the wrong kind of value\r\n"
        elif response == "-7":
            return "-ERR wrong number of arguments for 'rpush' command\r\n"
        return f"+{response}\r\n"
    elif type(response) == int:
        return f":{response}\r\n"
    else:
        return "$-1\r\n"