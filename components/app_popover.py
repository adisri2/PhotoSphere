from tkinter import LabelFrame, Label, LEFT, RIGHT

class App_Popover(object):
  """docstring for App_Popover"""
  def __init__(self, master, styles):
    super(App_Popover, self).__init__()

    self.master = master
    self.styles = styles

    self.putPopover()

  def putPopover(self):
    self.wrapper = LabelFrame(self.master, 
      bg=self.styles['bg'], 
      borderwidth=0)

    self.arrow = Label(self.wrapper, 
      text="→",
      font=self.styles['big_font'],
      bg=self.styles['bg'],
      fg=self.styles['fg_error'])
    self.arrow.pack(side=RIGHT, padx=4)

    self.text = Label(self.wrapper, 
      text="",
      font=self.styles['big_font'],
      bg=self.styles['bg'],
      fg=self.styles['fg_error'])
    self.text.pack(side=RIGHT)

  def set_text(self, text):
    self.text.config(text=text)

  def move(self, target, anchor="left"):
    self.wrapper.pack()

    self.wrapper.update_idletasks()

    target_rootx = target.winfo_rootx()
    target_rooty = target.winfo_rooty()
    target_width = target.winfo_width()
    target_height = target.winfo_height()

    wrapper_width = self.wrapper.winfo_width()
    wrapper_height = self.wrapper.winfo_height()

    y_pos = target_rooty - (wrapper_height / 2)

    if anchor == "left":
      self.arrow.config(text="→")
      x_pos = target_rootx - wrapper_width
      self.arrow.pack(side=RIGHT, padx=4)
      self.text.pack(side=RIGHT)

    elif anchor == "right":
      self.arrow.config(text="←")
      x_pos = target_rootx + target_width

      self.arrow.pack(side=LEFT)
      self.text.pack(side=LEFT, padx=4)

    self.wrapper.place(x=x_pos, y=y_pos)

  def hide(self):
    self.wrapper.place_forget()