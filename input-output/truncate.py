import os
import re

def truncate(path):
  files = os.listdir(path)
  
  for file in files:
    is_image = bool(re.search("(png|jpg|gif|jpeg)", file))
    if is_image:
      os.remove(path + "/" + file)