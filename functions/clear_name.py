import re
import sys
sys.stdout.reconfigure(encoding='utf-8')



# Clean a string to make it safe for use as a file name
def clear_name(name):
    return re.sub(r'[\\/:"*?<>|]+', "_", name)