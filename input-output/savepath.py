import os

def get_path():
  if not os.path.isfile("userdata/path_to_save.txt"):
    f = open("userdata/path_to_save.txt", "w")
    f.close()
    return "<None>"
  else:
    with open("userdata/path_to_save.txt", "r") as f:
      path = f.read()
      if len(path) == 0:
        return "<None>"
      return path



def set_path(path):
  with open("userdata/path_to_save.txt", "w") as f:
    f.write(path)