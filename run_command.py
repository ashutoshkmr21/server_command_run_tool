import os, json, getpass, subprocess, readline, socket
from datetime import datetime
from util import CLUBBED_SERVERS, SAVED_COMMANDS, LOG_FILE, read_json, PORT_NO
DELIMETER = ','

soc = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = PORT_NO

country_list_json = read_json(CLUBBED_SERVERS)
command_list_json = read_json(SAVED_COMMANDS)
saved_keys = command_list_json.keys()

def completer(text, state):
    options = [key for key in saved_keys if key.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None

readline.set_completer(completer)
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

def perform_action(servers, action):
    print "Executing Commands :"
    soc.connect((host, port))
    for server in servers:
        if server:
            command = "ssh tomcat-user@" + server + ' ' + action
            print command
            command_output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            print command_output
            soc.send('append ' + str(datetime.now()) + ' '+ getpass.getuser() + ' ' + command + '\n' + command_output)
    soc.close

user_input = raw_input('Enter a saved or new command to run: ').strip()
command_keys = user_input.split(" ")

if command_list_json.get(command_keys[0]):
    command_value = command_list_json[command_keys[0]]

    if len(command_keys) == command_value.count('{}') + 1:
        user_actions = tuple(command_keys[1:])
        command = command_value.format(*user_actions)
    else:
        print 'Invalid no of arguments for command, existing command is: ' + command_value
        quit()
else:
    command = user_input

saved_keys = country_list_json.keys()
readline.set_completer(completer)

user_input = raw_input('Enter file path or country name or comma separated servers name: ').strip()

if os.path.isfile(user_input):
    servers = open(user_input).read().splitlines()
else:
    if user_input == 'all':
        server = ''
        for key, value in country_list_json.iteritems():
            server += value + ','
        servers = [server]
    else:
	servers = [country_list_json[user_input]] if user_input in country_list_json.keys() else [user_input]

servers = servers[0].split(DELIMETER) if DELIMETER in servers[0] else servers
perform_action(servers, command)