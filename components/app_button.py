from tkinter import LabelFrame, Button, Label, FLAT, DISABLED
from app_tooltip import App_Tooltip

class App_Button(object):
  """docstring for App_Button"""
  def __init__(self, master, text=None, styles=None, command=None, image=None, title=None, disabled=False):
    super(App_Button, self).__init__()
    
    self.master = master
    self.text = text
    self.styles = styles
    self.command = command
    self.image = image
    self.title = title
    self.disabled = disabled

    self.putButton()

  def putButton(self):
    self.btn_wrapper = LabelFrame(self.master, relief=FLAT, borderwidth=0)

    self.btn = Button(
      self.btn_wrapper, 
      text = self.text, 
      relief=FLAT,
      bg=self.styles['btn_bg'], 
      padx=self.styles['padx'], 
      pady=self.styles['pady'], 
      fg=self.styles['btn_fg'], 
      borderwidth=0, 
      font=self.styles['big_font'],
      command=self.command,
      image=self.image,
      activeforeground=self.styles['a_fg'],
      activebackground=self.styles['a_bg'],
      cursor="hand2")
    self.btn.image = self.image

    if self.disabled:
      self.btn.bind("<Button-1>", lambda x: "break")
    else:
      self.btn.bind("<Enter>", self.mouseover)
      self.btn.bind("<Leave>", self.mouseout)

    self.btn.pack()

    if self.title is not None:
      self.tooltip = App_Tooltip(self.btn, text=self.title)

  def mouseover(self, event):
    self.btn.config(fg=self.styles['h_fg'])
    self.btn.config(bg=self.styles['h_bg'])

  def mouseout(self, event):
    self.btn.config(fg=self.styles['btn_fg'])
    self.btn.config(bg=self.styles['btn_bg'])

  def bind(self, *args, **kwargs):
    self.btn.bind(*args, **kwargs)

  def bind_wrapper(self, *args, **kwargs):
    self.btn_wrapper.bind(*args, **kwargs)

  def pack(self, *args, **kwargs):
    self.btn_wrapper.pack(*args, **kwargs)

  def place(self, *args, **kwargs):
    self.btn_wrapper.place(*args, **kwargs)

  def config(self, *args, **kwargs):
    self.btn.config(*args, **kwargs)

  def set_tooltip(self, text):
    self.tooltip.configure(text=text)

  def pack_forget(self):
    self.btn_wrapper.pack_forget()

  def place_forget(self):
    self.btn_wrapper.place_forget()

  def winfo_rootx(self):
    return self.btn_wrapper.winfo_rootx()

  def winfo_rooty(self):
    return self.btn_wrapper.winfo_rooty()

  def winfo_height(self):
    return self.btn_wrapper.winfo_height()

  def winfo_width(self):
    return self.btn_wrapper.winfo_width()

