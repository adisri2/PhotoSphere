import random
import json

class Rand_Word(object):
  """docstring for Rand_Word"""
  def __init__(self):
    super(Rand_Word, self).__init__()

    self.wordlist = []
    self.wordlist_linear = []

    self.set_wordlist()
    self.wordlist_to_linear()

  def set_wordlist(self):
    with open('userdata/myterms.json', 'r') as wordlist:
      self.wordlist = json.loads(wordlist.read())

  def wordlist_to_linear(self):
    master = []

    for _type, sub_type in self.wordlist.items():
      
      for _category, words in sub_type.items():
        master += words['contents']

    self.wordlist_linear = master

  def get_rand_word(self):
    return random.choice(self.wordlist_linear)

  def refresh(self):
    self.write_to_wordlist()
    self.wordlist_to_linear()

  def write_to_wordlist(self):
    with open('userdata/myterms.json', 'w') as wordlist:
      wordlist.write(json.dumps(self.wordlist))

  def enable(self, id_num):
    for _type, sub_type in self.wordlist.items():
      
      for _category, words in sub_type.items():
        if words['id'] == id_num:
          words['active'] = True
          break
      break

    self.refresh()

  def disable(self, id_num):
    for _type, sub_type in self.wordlist.items():
      
      for _category, words in sub_type.items():
        if words['id'] == id_num:
          words['active'] = False
          break
      break

    self.refresh()

  def choices(self, k=1):
    return random.choices(self.wordlist_linear, k=k)
    



