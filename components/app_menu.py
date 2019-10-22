from tkinter import LabelFrame, Label, NORMAL
from app_button import App_Button

class App_Menu(object):
  """docstring for App_Menu"""
  def __init__(self, master, root, styles, structure):
    super(App_Menu, self).__init__()

    self.master = master
    self.structure = structure
    self.root = root

    self.styles = styles.copy()
    self.styles['big_font'] = styles['font']
    self.styles['btn_bg'] = styles['menu_bg']
    self.font_px_size = self.styles['big_font'].cget("size")

    self.putMenu()

  def putMenu(self):
    self.wrapper = LabelFrame(self.master,
      borderwidth=0)

    menu_padx = (self.root.winfo_width() / 2)
    menu_pady = (self.root.winfo_height() * 0.015)

    self.background = Label(self.wrapper, 
      fg=self.styles['menu_bg'],
      bg=self.styles['menu_bg'],
      font=self.styles['big_font'],
      text=" ",
      padx=menu_padx,
      pady=menu_pady
    )
    self.background.pack()

    heading_offset = 0

    self.heading_arr = []
    self.offset_arr = []

    for heading in self.structure:
      text = heading['text']
      title = heading['title']
      command = heading['command']
      disabled = heading['disabled']

      heading_styles = self.styles.copy()
      if disabled:
        heading_styles['btn_fg'] = heading_styles['h_bg']

      _heading = App_Button(self.background, text=text, styles=heading_styles, command=command, title=title, disabled=disabled)
      
      _heading.place(x=heading_offset, y=0)
      self.offset_arr.append(heading_offset)
      self.heading_arr.append(_heading)

      # heading_offset += (len(text) * self.font_px_size) + self.styles['padx'] + 10
      self.root.update_idletasks()
      heading_offset += _heading.winfo_width()
        

  def pack(self, *args, **kwargs):
    self.wrapper.pack(*args, **kwargs)

  def winfo_height(self, *args, **kwargs):
    return self.wrapper.winfo_height(*args, **kwargs)
    
  def set_tooltip(self, index, text):
    self.heading_arr[index].set_tooltip(text=text)

  def set_text(self, index, text):
    self.heading_arr[index].config(text=text)