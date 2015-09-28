import os
import traceback

# Loads all *.py files found in the settings folder
print("Loading settings files dynamically...")
files = sorted(os.listdir(os.path.dirname(os.path.abspath(__file__))))
for file_ in files:
  if os.path.splitext(file_)[1] == ".py":
    filename = os.path.splitext(file_)[0]
    if filename != '__init__':
      print(" - " + filename)
      try:
        exec('from .%s import *' % filename)
      except:
        print("Exception in %s. Remainder of file will be skipped..." % filename)
        traceback.print_exc()
        print("")
