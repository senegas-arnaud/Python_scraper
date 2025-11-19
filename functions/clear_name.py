import re
import sys
sys.stdout.reconfigure(encoding='utf-8')




def clear_name(name):
    return re.sub(r'[\\/:"*?<>|]+', "_", name)