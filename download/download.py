import json
import sys
import os
import time

import urllib.request
import urllib.parse
from datetime import time, datetime
import time
import threading

from tkinter import LabelFrame, LEFT, BOTH
import PIL.Image

sys.path.insert(0, 'components')
from app_photo import App_Photo
from app_toast import App_Toast

sys.path.insert(0, 'styles')
from styles import get_styles

class Download(object):
  """docstring for Download"""
  def __init__(self, photo_container, root):
    super(Download, self).__init__()

    self.photo_container = photo_container
    self.root = root

    self.thumbnail_width = int(root.winfo_width() / 8)

    self.hits = None

    self.num_downloaded = 0
    self.photo_width = self.thumbnail_width

    self.app_photo_arr = []

    self.styles = get_styles()
    self.init_photo_row = LabelFrame(self.photo_container, bg=self.styles['bg'], borderwidth=0)
    self.init_photo_row.pack()
    self.photo_row_arr = [self.init_photo_row]
    self.photo_row_index = 0
    self.curr_photo_row_width = 0

  def get(self, url, parse=False):
    contents = urllib.request.urlopen(url).read()
    if parse == True:
      contents = json.loads(contents)
    return contents

  def set_query(self, query):
    self.query = query
    self.underscored_query = self.query.replace(" ", "_")

  def set_amount(self, amount):
    self.amount = amount

  def set_savepath(self, savepath):
    self.savepath = savepath

  def set_window_width(self, window_width):
    self.window_width = window_width

  def set_progressbar(self, progressbar):
    self.progressbar = progressbar
  
  def set_hits(self):
    api_key = "5174554-1e0b4ebd36d5f2f2c16e1da1f"

    encoded_query = urllib.parse.quote_plus(self.query)

    url = "https://pixabay.com/api/?key=" + api_key + "&q=" + encoded_query

    self.hits = self.get(url, parse=True)
    return self.hits['totalHits']

  def get_datetime_str(self):
    return str(time.time()).replace(".", "-")

  def write_photo(self, url, data, count=True):
    extension = url.split(".")[-1]
      
    now = self.get_datetime_str()

    if count:
      self.num_downloaded += 1
    
    photoname = "{}_{}_{}.{}".format(self.underscored_query, now, self.num_downloaded, extension)

    photo_path = self.savepath + "/" + photoname

    with open(photo_path, "wb") as photo_handle:
      photo_handle.write(data)

    return photo_path

  def add_history(self, name):
    name = str(name)
    with open("userdata/history.txt", "a+") as history_handle:
      history_handle.write(name + "\n")

  def get_history(self):
    with open("userdata/history.txt", "r") as history_handle:
      return history_handle.read().strip().split("\n")

  def add_row(self):
    addit_photo_row = LabelFrame(self.photo_container, bg=self.styles['bg'], borderwidth=0)
    addit_photo_row.pack()
    self.photo_row_arr.append(addit_photo_row)
    self.curr_photo_row_width = 0
    if len(self.photo_row_arr) > 1:
      self.photo_row_index += 1

  def show_photo(self, photo_path, fullsize_path=None):
    pil_photo = PIL.Image.open(photo_path)

    wpercent = (self.thumbnail_width/float(pil_photo.size[0]))
    hsize = int((float(pil_photo.size[1])*float(wpercent)))
    pil_photo = pil_photo.resize((self.thumbnail_width,hsize), PIL.Image.ANTIALIAS)

    padx = 10

    self.curr_photo_row_width += self.photo_width + padx
    if self.curr_photo_row_width > self.window_width or len(self.photo_row_arr) == 0:
      self.add_row()

    try:
      photo_container = self.photo_row_arr[self.photo_row_index]
    except:
      self.add_row()
      self.photo_row_index -= 1
      
    print(len(self.photo_row_arr))

    photo_label = App_Photo(photo_container, 
      pil_photo=pil_photo, 
      styles=self.styles, 
      root=self.root,
      fullsize_path=fullsize_path,
      hide_cmd=lambda:self.hide_photo(photo_label=photo_label),
      del_cmd=lambda:self.del_photo(photo_label=photo_label, photo_path=fullsize_path))
    photo_label.pack(side=LEFT)
    self.app_photo_arr.append(photo_label)


  def download_and_show(self):
    total_hits = len(self.hits['hits'])

    if total_hits < self.amount:
      real_amount = total_hits
    else:
      real_amount = self.amount

    photo_index = 0

    self.pct_completed = 25


    while real_amount != 0:
      photo_info = self.hits['hits'][photo_index]

      photo_url = photo_info['largeImageURL']

      thumbnail_url = photo_info['previewURL']
      thumbnail_width = photo_info['previewWidth']

      photo_id = str(photo_info['id'])

      history = self.get_history()
      
      if photo_id not in history:
        photo_data = self.get(photo_url)
        thumbnail_data = self.get(thumbnail_url)
        self.add_history(photo_id)

        def write_show_process():
          self.photo_path_location = self.write_photo(url=photo_url, data=photo_data)
          self.thumbnail_path_location = self.write_photo(url=thumbnail_url, data=thumbnail_data, count=False)
          self.pct_completed += int(75 / real_amount / 2)
          self.progressbar.set_pct(self.pct_completed)
          self.pct_completed += int(75 / real_amount / 2)
          self.show_photo(self.thumbnail_path_location, self.photo_path_location)
          self.progressbar.set_pct(self.pct_completed)

          os.remove(self.thumbnail_path_location)

        t = threading.Thread(target=write_show_process)
        t.daemon = True
        t.start()
      
      photo_index += 1

      if self.num_downloaded == real_amount or photo_index+1 == total_hits:
        self.num_downloaded = 0
        self.progressbar.set_pct(95)
        def wait():
          time.sleep(1)
          self.progressbar.hide()
        t = threading.Thread(target=wait)
        t.daemon = True
        t.start()
        if photo_index+1 == total_hits:
          toast = App_Toast(self.root, text="All out of photos", styles=self.styles, root=self.root)
          del toast
        else:
          toast = App_Toast(self.root, text="Finished", styles=self.styles, root=self.root)
          del toast
        break

  def clean_photo_rows(self):
    for row in self.photo_row_arr:
      if len(row.winfo_children()) == 0:
        index = self.photo_row_arr.index(row)
        del self.photo_row_arr[index]
        row.destroy()

  def hide_photo(self, event=None, photo_label=None, edit_arr=True):
    photo_label.destroy()
    if edit_arr:
      index = self.app_photo_arr.index(photo_label)
      del self.app_photo_arr[index]
    self.clean_photo_rows()

  def del_photo(self, event=None, photo_label=None, photo_path=None,edit_arr=True):
    os.remove(photo_path)
    self.hide_photo(photo_label=photo_label, edit_arr=edit_arr)
    self.clean_photo_rows()
        
  def del_photo_rows(self):
    for row in self.photo_row_arr:
      index = self.photo_row_arr.index(row)
      del self.photo_row_arr[index]
      row.destroy()



