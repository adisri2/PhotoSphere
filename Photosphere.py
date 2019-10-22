from tkinter import *
from tkinter.font import Font
from tkinter import filedialog

import threading
import os
import subprocess
import ctypes

sys.path.insert(0, 'components')
from app_tooltip import App_Tooltip
from app_button import App_Button
from app_entry import App_Entry
from app_num_select import App_Num_Select
from app_menu import App_Menu
from app_confirm import App_Confirm
from app_toast import App_Toast
from app_popover import App_Popover
from app_progressbar import App_Progressbar
from app_prompt import App_Prompt
from app_fab import App_Fab

sys.path.insert(0, 'input-output')
from savepath import *
from randword import Rand_Word
from truncate import *

sys.path.insert(0, 'pages')
from edit_myterms import Edit_Myterms
from edit_preferences import Edit_Preferences

sys.path.insert(0, 'styles')
from styles import get_styles

sys.path.insert(0, 'download')
from download import Download

class PhotoSphere(Frame):
    
  def __init__(self, master=None):
   
      Frame.__init__(self, master)   
           
      self.master = master

      self.styles = get_styles()

      self.btn_small_styles = self.styles.copy()
      self.btn_small_styles['padx'] = 7
      self.btn_small_styles['pady'] = 0
      self.btn_small_styles['big_font'] = Font(size=18, family="Century Gothic"),

      self.entry_arr= []

      self.num_spaces = 0

      self.rand_word = Rand_Word()

      # self.zoom_amount = 1.0

      self.init_window()
      

  def init_window(self):
    self.master.title("PhotoSphere")
    self.configure(bg=self.styles['bg'])
    self.pack(fill=BOTH, expand=1)

    # root.tk.call('tk', 'scaling', self.zoom_amount)
    
    self.container = LabelFrame(self, 
      bg=self.styles['bg'], 
      fg=self.styles['fg'], 
      borderwidth=0)
    self.container.pack(fill=BOTH, expand=1)

    # ------------------- The Menu ---------------------------
    self.menu_structure = [
        {
          'text': "ClearFresh ⏚",
          'title': "Delete all photos and history in selected folder",
          'command': self.truncate,
          'disabled': False,
          'static': True
        },
        {
          'text': "MyTerms ↂ",
          'title': "The list of words that will be\nused during the replacement of all your photos",
          'command': self.edit_myterms,
          'disabled': False,
          'static': True
        },
        {
          'text': "AutoGet ∯",
          'title': "Replace all photos with photos based\non keywords that are chosen by you",
          'command': self.autoget,
          'disabled': False,
          'static': True
        },
        {
          'text': "Preferences ƛ",
          'title': None,
          'command': self.edit_preferences,
          'disabled': False,
          'static': True
        },
        {
          'text': "Open Active Folder Θ",
          'title': None,
          'command': self.open_active_folder,
          'disabled': False,
          'static': True
        },
        {
          'text': "Active folder: " + get_path(),
          'title': None,
          'command': '',
          'disabled': True,
          'static': False
        }
      ]
    self.menu = App_Menu(self.container, root=root, styles=self.styles, structure=self.menu_structure)
    self.menu.pack()

    self.progressbar = App_Progressbar(self.container, root=root, below=self.menu,styles=self.styles)

    # ------------------- The Input Form ---------------------------
    input_field_wrapper = LabelFrame(self.container, bg=self.styles['bg'], borderwidth=0)

    # Input
    self.search_entry = App_Entry(input_field_wrapper, 
      placeholder="Search Images", 
      styles=self.styles, 
      entry_arr=self.entry_arr)
    self.search_entry.bind_to_entry("<Return>", self.initiate_download)
    self.search_entry.pack(side=LEFT)

    # Input
    self.rand_word_btn = App_Button(input_field_wrapper, 
      text="⚙", 
      styles=self.btn_small_styles,
      title="Generate a random word, for inspiration",
      command=self.set_rand_word).pack(side=LEFT, padx=15)

    # Input
    self.num_select = App_Num_Select(input_field_wrapper, 
      min_amount=1, 
      styles=self.styles, 
      title="The number of images to download")
    self.num_select.pack(side=LEFT)

    self.path_var = get_path()
    # Input
    self.path_btn = App_Button(input_field_wrapper, 
      text="...",
      styles=self.btn_small_styles,
      command=self.select_file, 
      title="Select the target folder for the images")
    self.path_btn.pack(side=LEFT, padx=10)

    input_field_wrapper.pack(pady=(40, 0))

    # Input
    self.download_btn = App_Button(self.container, 
      text="Download ⤓", 
      styles=self.styles,
      command=self.initiate_download).pack(pady=(30, 0))

    self.photo_container = LabelFrame(self.container, bg=self.styles['bg'], borderwidth=0)
    self.photo_container.pack(fill=BOTH, expand=1)

    self.download_handle = Download(photo_container=self.photo_container, root=root)

    fab_structure = [
      {
        "text": "Hide Ƣ",
        "title": "Hide all Photos on screen",
        "command": self.hide_all_photos
      },
      {
        "text": "Delete ɶ",
        "title": "Delete all Photos on screen",
        "command": self.del_all_photos
      }
    ]
    self.fab = App_Fab(self.container, structure=fab_structure, styles=self.styles, root=root)
    self.fab.put()

    # ---------------------- Other -----------------------
    self.truncate_confirm = App_Confirm(self, 
      text="Are you sure you want to delete all files in \"" + self.path_var + "\"",
      styles=self.styles,
      size_determiner="\"" + self.path_var + "\"",
      root=root)

    self.error = App_Popover(self, styles=self.styles)

  # ---------------------- Functions -----------------------------
  def global_onclick(self, event):
    widget = event.widget
    widget_class = widget.winfo_class()

    if widget_class == "Button":
      widget.config(relief=FLAT)

    widget_parent = widget.winfo_parent()

    entry_name_arr = [e.winfo_pathname(e.winfo_id()) for e in self.entry_arr]

    if widget_parent not in entry_name_arr or widget not in entry_name_arr:

      if widget_parent in entry_name_arr:
        index = entry_name_arr.index(widget_parent)
        self.entry_arr[index]._focus()
      elif widget in entry_name_arr:
        index = entry_name_arr.index(widget.winfo_pathname(widget.winfo_id()))
        self.entry_arr[index]._focus()
      else:
        root.focus()
        for e in self.entry_arr:
          e.blur()
        self.search_entry.check_to_blur()


  def set_rand_word(self):
    word = self.rand_word.get_rand_word()
    self.search_entry.delete(0, END)
    self.search_entry.insert(0, word)
    self.search_entry._focus()
    self.validate()

  def refresh_menu(self, filename):
    space = " " if self.num_spaces % 2 == 0 else ""
    self.num_spaces += 1

    for i in range(len(self.menu_structure)):
      if self.menu_structure[i]['static'] == True:
        self.menu.set_text(i, self.menu_structure[i]['text'] + space)

    self.menu.set_text(5, "Active folder: " + filename)

  def select_file(self):
    filename = filedialog.askdirectory()
    if len(filename) > 0:
      set_path(filename)
      self.path_var = filename

      self.truncate_confirm.update("Are you sure you want to delete all files in " + filename)

      self.refresh_menu(filename)

      toast = App_Toast(self, text="Active Folder Updated", styles=self.styles, root=root)
      del toast
      

  def truncate(self):

    def process():

      def thread():
        truncate(self.path_var)
        self.truncate_confirm.hide()
        toast = App_Toast(self, text="Folder Cleared", styles=self.styles, root=root)
        del toast
        self.download_handle.del_photo_rows()

      t = threading.Thread(target=thread)
      t.daemon = True
      t.start()

    self.truncate_confirm.show(process)

  def validate(self):
    query = self.search_entry.get()
    amount = self.num_select.get()
    savepath = self.path_var

    if len(query) < 1:
      self.error.set_text("Enter a search")
      self.error.move(target=self.search_entry, anchor="left")
      return False

    elif not os.path.isdir(savepath):
      self.error.set_text("Select a valid folder")
      self.error.move(target=self.path_btn, anchor="right")
      return False

    else:
      self.error.hide()
      return True
      
  def initiate_download(self, event=None):
    valid = self.validate()
    self.progressbar.set_pct(3)
    self.progressbar.show()
    if valid:
      query = self.search_entry.get()
      amount = self.num_select.get()
      savepath = self.path_var

      self.download_handle.set_query(query)
      self.download_handle.set_amount(amount)
      self.download_handle.set_savepath(savepath)
      self.download_handle.set_progressbar(self.progressbar)
      self.download_handle.set_window_width(self.winfo_width())

      def process():
        self.progressbar.set_pct(10)
        num_hits = self.download_handle.set_hits()
        if num_hits > 0:
          self.progressbar.set_pct(25)
        else:
          toast = App_Toast(self, text="No Hits, try again", styles=self.styles, root=root)
          del toast
          self.progressbar.hide()

        self.download_handle.download_and_show()

      t = threading.Thread(target=process)
      t.daemon = True
      t.start()

  def edit_myterms(self):
    self.new_window = Toplevel(self)
    self.myterms_window = Edit_Myterms(self.new_window)
    self.myterms_window.focus()

  def edit_preferences(self):
    self.new_window = Toplevel(self)
    self.preferences_window = Edit_Preferences(self.new_window)
    self.preferences_window.focus()

  def autoget(self):
    structure = [
      {
        'label': "Number of Categories: ",
        'widget_class': 'App_Num_Select',
        'widget_args': {'min_amount':1, 'styles':self.styles}
      },
      {
        'label': "Number of Photos in each Categories: ",
        'widget_class': 'App_Num_Select',
        'widget_args': {'min_amount':1, 'styles':self.styles}
      }
    ]
    
    def process(results=None):
      hidden_progressbar = App_Progressbar(self.container, root=root, below=self.menu,styles=self.styles)
      self.pct_complete = 0
      def thread():
        num_categories, num_per_category = results

        self.download_handle.set_window_width(self.winfo_width())
        self.download_handle.set_progressbar(hidden_progressbar)
        self.download_handle.set_savepath(self.path_var)
        self.download_handle.set_amount(num_per_category)
        self.pct_complete += 3
        self.progressbar.set_pct(self.pct_complete)
        self.progressbar.show()

        approved_categories = []
        while True:
          category = self.rand_word.get_rand_word()
          self.download_handle.set_query(category)
          num_hits = self.download_handle.set_hits()
          if num_hits > num_per_category+1:
            approved_categories.append(category)
            self.pct_complete += 15
            self.progressbar.set_pct(self.pct_complete)
          if len(approved_categories) == num_categories:
            break
        categories_str = ", ".join(approved_categories)
        toast = App_Toast(self, text=categories_str, styles=self.styles, root=root)
        del toast
        self.progressbar.set_pct(25)

        for category in approved_categories:
          self.download_handle.set_query(category)
          self.download_handle.download_and_show()
          self.pct_complete += int((100 - self.pct_complete) / num_categories / num_per_category)
          self.progressbar.set_pct(self.pct_complete)

        toast = App_Toast(self, text="Finished", styles=self.styles, root=root)
        del toast
        self.progressbar.hide()

      t = threading.Thread(target=thread)
      t.daemon = True
      t.start()

    prompt = App_Prompt(self, root=root, structure=structure, styles=self.styles, command=process)
    prompt.show()

  def open_active_folder(self):
    def process():
      path = self.path_var
      path = os.path.realpath(path)
      os.startfile(path)
    t = threading.Thread(target=process)
    t.daemon = True
    t.start()

  def hide_all_photos(self, event=None): 
    for i in range(len(self.download_handle.app_photo_arr)):
      app_photo = self.download_handle.app_photo_arr[i]
      self.download_handle.hide_photo(photo_label=app_photo, edit_arr=False)
    self.download_handle.app_photo_arr.clear()


  def del_all_photos(self, event=None):
    for i in range(len(self.download_handle.app_photo_arr)):
      app_photo = self.download_handle.app_photo_arr[i]
      self.download_handle.del_photo(photo_label=app_photo, photo_path=app_photo.fullsize_path, edit_arr=False)
    self.download_handle.app_photo_arr.clear()


if 'win' in sys.platform:
  ctypes.windll.shcore.SetProcessDpiAwareness(1)
root = Tk()
root.state('zoomed')

root.minsize(width=650, height=450)
root.iconbitmap("images/icon_16.ico")
app = PhotoSphere(root)

root.bind("<Button-1>", app.global_onclick)
root.mainloop() 