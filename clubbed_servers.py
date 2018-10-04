import sys
sys.dont_write_bytecode = True
from common import  CLUBBED_SERVERS, file_data

data = file_data(CLUBBED_SERVERS, True, False, '')
country_keys = data.keys()

for key in country_keys:
    print key + " : " + data[key]