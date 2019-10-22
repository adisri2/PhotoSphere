from tkinter import LabelFrame, Label, LEFT
from app_button import App_Button

class App_Confirm(object):
  """docstring for App_Confirm"""
  def __init__(self, master, text, styles, root, size_determiner):
    super(App_Confirm, self).__init__()

    self.master = master
    self.text = text
    self.styles = styles.copy()
    self.size_determiner = size_determiner
    self.font_px_size = self.styles['big_font'].cget("size")

    self.root = root

    self.root_width = self.root.winfo_width()
    self.root_height = self.root.winfo_height()

    self.putConfirm()

  def putConfirm(self):
    self.overlay = LabelFrame(self.master, 
      bg=self.styles['overlay'], 
      fg=self.styles['overlay'], 
      width=self.root_width, 
      height=self.root_height, 
      borderwidth=0)
    
    self.wrapper = LabelFrame(self.master, 
      bg=self.styles['bg'], 
      borderwidth=0,
      pady=19,
      padx=10)

    wraplength = int(len(self.size_determiner) * self.font_px_size)

    self.label = Label(self.wrapper, 
      bg=self.styles['bg'], 
      fg=self.styles['fg'],
      text=self.text,
      wraplength=wraplength,
      font=self.styles['big_font'],
      padx=18,
      pady=10)
    self.label.pack()

    choice_wrapper = LabelFrame(self.wrapper, 
      bg=self.styles['bg'], 
      borderwidth=0)
    choice_wrapper.pack()

    no_btn = App_Button(choice_wrapper, 
      text="No", 
      styles=self.styles, 
      command=self.hide)
    no_btn.pack(side=LEFT, padx=10)

    self.yes_btn = App_Button(choice_wrapper, text="Yes", styles=self.styles)
    self.yes_btn.pack(side=LEFT)


  def hide(self):
    self.wrapper.place_forget()
    self.overlay.place_forget()

  def show(self, confirmed_command=None):
    self.wrapper.pack()
    self.root.update_idletasks()

    wrapper_width = self.wrapper.winfo_width()
    wrapper_height = self.wrapper.winfo_height()

    x = (self.root_width / 2) - (wrapper_width / 2)
    y = (self.root_height / 2) - (wrapper_height / 2)

    self.wrapper.place(x=x, y=y)
    self.yes_btn.config(command=confirmed_command)

    self.overlay.place(x=0, y=0)

  def update(self, text):
    self.label.config(text=text)