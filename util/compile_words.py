import os
import json

master_folder = "wordlist"

tree = [x for x in os.walk(master_folder)]
id_num = 0

master = {}

for branch in tree:
  dirpath, dirnames, filenames = branch

  slug = "-".join(str(dirpath).split('\\')[1:])

  if len(dirnames) == 0 and len(filenames) > 0 and len(slug) > 0:
    
    slug_dict = {}

    for file in filenames:
      name = file.split(".")[0]

      with open(dirpath.replace("\\", "/") + "/" + file, "r") as handle:
        contents = handle.read().strip().split("\n")          
        slug_dict[name] = {"id": id_num, 
                           "active": True, 
                           "contents": contents}
        id_num += 1

    master[slug] = slug_dict

with open("wordlist-1.json", "w") as target:
  target.write(json.dumps(master))
