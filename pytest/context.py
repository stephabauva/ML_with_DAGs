#from https://docs.python-guide.org/writing/structure/
#note: to avoid any confusion, "context.py" has nothing to do with "Dagster's context" :)

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import script