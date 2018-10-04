import json
from util import read_json, SAVED_COMMANDS

def write_file(filename, data):
    with open(filename, 'w') as saved_commands:
        saved_commands.write(json.dumps(data, sort_keys=True, indent=4))

command_name = raw_input('Enter command name:').strip()
command = raw_input('Enter command with {} for parameters: ').strip()
command = command.replace('{', '{{').replace('}', '}}')
json_data = read_json(SAVED_COMMANDS)
json_data[command_name] = command

write_file(SAVED_COMMANDS, json_data)