__version__ = '0.7.8'
from google.colab import _message
import ast 
import re
import os 
import traceback
import time
import pipreqs
import subprocess

def get_dependencies(path):
    subprocess.run(["pipreqs", path])

def deploy():
  print("Begun deployment.. ")

  print("Converting notebook to python and generating requirements.txt 🐍")
  os.mkdir("./berri_files/")
  # Obtain the notebook JSON as a string
  notebook_json_string = _message.blocking_request('get_ipynb', request='', timeout_sec=5)

  # save to temporary file
  lines = []
  for cell in notebook_json_string["ipynb"]["cells"]:
    for line in cell["source"]:
      if line.startswith("!pip install"):
        continue
      elif not line.startswith("!"):
        lines.append(line)
  
  f = open("./berri_files/agent_code.py", "w")
  for line in lines:
    if "initialize_agent(" in line:
      initialization_line = line.split("=", 1)
      initialization_line = "agent = " + initialization_line[1]
      print(initialization_line)
      f.write(initialization_line + "\n")
    else:
      f.write(line + "\n")
  f.close()
  
  get_dependencies("./berri_files")    
  print("Building docker image 😱")

  print("Deploying endpoint ... ⌛️")
  
  # assume you're in a google colab 
  print("hello world")
  