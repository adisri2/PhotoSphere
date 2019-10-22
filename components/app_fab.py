from tkinter import LabelFrame, Label, BOTTOM
import sys

sys.path.insert(0, 'components')
from app_button import App_Button

class App_Fab(object):
  """docstring for App_Fab"""
  def __init__(self, master, structure, styles, root):
    super(App_Fab, self).__init__()
    self.master = master
    self.structure = structure
    self.styles = styles
    self.root = root

    self.styles = styles.copy()
    self.styles['big_font'] = styles['font']
    self.styles['btn_bg'] = styles['menu_bg']
    self.styles['padx'] = 15
    self.styles['pady'] = 11

    self.num_times_toggled = 0
    self.menu_item_arr = []

    self.putFab()

  def putFab(self):
    self.wrapper = LabelFrame(self.master, bg=self.styles['bg'], borderwidth=0, padx=20, pady=20)
    self.wrapper.bind("<Enter>", lambda e: self.toggle_menu(action="show"))
    self.wrapper.bind("<Leave>", lambda e: self.toggle_menu(action="hide"))

    self.fab = App_Button(self.wrapper, text="Menu Ӝ", styles=self.styles, command=self.toggle_menu)
    self.fab.bind_wrapper("<Enter>", lambda e: self.toggle_menu(action="show"))
    self.fab.bind_wrapper("<Leave>", lambda e: self.toggle_menu(action="hide"))
    self.fab.pack(side=BOTTOM, anchor="se")

    for menu_item in reversed(self.structure):
      text = menu_item['text']
      title = menu_item['title']
      command = menu_item['command']

      menu_item_btn = App_Button(self.wrapper, text=text, styles=self.styles, command=command, title=title)
      menu_item_btn.bind_wrapper("<Enter>", lambda e: self.toggle_menu(action="show"))
      # menu_item_btn.bind_wrapper("<Leave>", lambda e: self.toggle_menu(action="hide"))
      self.menu_item_arr.append(menu_item_btn)

  def show_menu(self, event=None, menu_item_btn=None):
    menu_item_btn.pack(side=BOTTOM, anchor="se")

  def hide_menu(self, event=None, menu_item_btn=None):
    menu_item_btn.pack_forget()

  def toggle_menu(self, action=None):
    for menu_item_btn in self.menu_item_arr:
      if action == None:
        if self.num_times_toggled % 2 == 0:
          self.show_menu(menu_item_btn=menu_item_btn)
        else:
          self.hide_menu(menu_item_btn=menu_item_btn)
      else:
        if action == "show":
          self.show_menu(menu_item_btn=menu_item_btn)
        elif action == "hide":
          self.hide_menu(menu_item_btn=menu_item_btn)


    self.num_times_toggled += 1

  def put(self):
    window_width = self.root.winfo_width()
    window_height = self.root.winfo_height()
    self.wrapper.place(anchor="se", x=window_width-15, y=window_height-15)