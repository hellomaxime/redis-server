
redis_dict = []

def deserialize(data):
    list_commands = data.splitlines()
    return list_commands    

def process(list_commands):
    if list_commands[2] == "PING":
        return "PONG"

def serialize(response):
    if type(response) == str:
        return f"+{response}\r\n"
    elif type(response) == int:
        return f":{response}\r\n"
    else:
        return "$-1\r\n"