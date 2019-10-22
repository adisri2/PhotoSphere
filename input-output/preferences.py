import json

def get_duplicate_bool():
  with open('userdata/preferences.json', 'r') as read_handle:
    unparsed = read_handle.read()
    parsed = json.loads(unparsed)

    return parsed['get_duplicates']

def enable_duplicates():
  with open('userdata/preferences.json', 'r') as read_handle:
    unparsed = read_handle.read()
    parsed = json.loads(unparsed)

    parsed['get_duplicates'] = True

    with open('userdata/preferences.json', 'w') as write_handle:
      modified_json = json.dumps(parsed)
      write_handle.write(modified_json)

def disble_duplicates():
  with open('userdata/preferences.json', 'r') as read_handle:
    unparsed = read_handle.read()
    parsed = json.loads(unparsed)

    parsed['get_duplicates'] = False

    with open('userdata/preferences.json', 'w') as write_handle:
      modified_json = json.dumps(parsed)
      write_handle.write(modified_json)