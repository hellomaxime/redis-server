import time

implemented_commands = ["PING", "ECHO", "SET", "GET"]

redis_dict = {}
expiry_dict = {}

def deserialize(data):
    list_commands = data.splitlines()
    return list_commands    

def process(list_commands):

    command = list_commands[2].upper()

    if command not in implemented_commands:
        return -1

    if command == "PING":
        if len(list_commands) > 3:
            return list_commands[4]
        return "PONG"
    elif command == "ECHO":
        if len(list_commands) < 4:
            return None
        return list_commands[4]
    elif command == "SET":
       
        if len(list_commands) < 7:
            redis_dict[list_commands[4]] = ""
        elif list_commands[6].isdigit():
            redis_dict[list_commands[4]] = int(list_commands[6])
        else:
            redis_dict[list_commands[4]] = list_commands[6]

        if len(list_commands) > 7:
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
                return -1

        return "OK"
    
    elif command == "GET":
        if list_commands[4] in redis_dict:
            if list_commands[4] in expiry_dict and expiry_dict[list_commands[4]] < time.time():
                del expiry_dict[list_commands[4]]
                del redis_dict[list_commands[4]]
                return None
            return redis_dict[list_commands[4]]
        return None

def serialize(response):
    if type(response) == str:
        return f"+{response}\r\n"
    elif type(response) == int:
        if response == -1:
            return f"-command not implemented\r\n"
        return f":{response}\r\n"
    else:
        return "$-1\r\n"