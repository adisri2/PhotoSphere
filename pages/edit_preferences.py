from tkinter import *
from tkinter.font import Font

sys.path.insert(0, 'components')
from app_checkbox import App_Checkbox

sys.path.insert(0, 'styles')
from styles import get_styles

sys.path.insert(0, 'input-output')
from preferences import *

class Edit_Preferences(Frame):
  """docstring for Edit_Preferences"""
  def __init__(self, master):
    super(Edit_Preferences, self).__init__()

    Frame.__init__(self, master)

    self.master = master

    self.styles = get_styles()
    
    self.init_window()

  def init_window(self):
    self.master.title("Preferences")
    self.master.iconbitmap("images/icon_16.ico")
    self.master.geometry("500x200")

    self.window_width = self.master.winfo_width()

    self.configure(bg=self.styles['bg'])
    self.pack(fill=BOTH, expand=1)

    self.putPreferences()

  def putPreferences(self):

    header = Label(self, text="User Preferences", 
      fg=self.styles['fg'], 
      bg=self.styles['bg'], 
      font=self.styles['big_font'])
    header.pack(pady=20)
          

    category = App_Checkbox(self, 
      text='Keep Duplicates', 
      styles=self.styles, 
      checked=get_duplicate_bool(),
      checkbox_id=0,
      oncheck=self.check,
      onuncheck=self.uncheck)

    category.pack()

  def check(self, num):
    enable_duplicates()

  def uncheck(self, num):
    disble_duplicates()

