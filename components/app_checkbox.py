from tkinter import LabelFrame, Label, LEFT

class App_Checkbox(object):
  """docstring for App_Checkbox"""
  def __init__(self, master, text, styles, checked=True, checkbox_id=None,oncheck=None, onuncheck=None):
    super(App_Checkbox, self).__init__()
    self.master = master
    self.text = text
    self.styles = styles
    self.checked = checked

    self.checkbox_id = checkbox_id
    self.oncheck = oncheck
    self.onuncheck = onuncheck

    self.num_toggles = 0 if self.checked else 1

    self.putCheckbox()

  def putCheckbox(self):
    self.wrapper = LabelFrame(self.master, 
      bg=self.styles['bg'],
      borderwidth=0,
      padx=5,
      pady=6,
      cursor="hand2")

    self.box = LabelFrame(self.wrapper,
      bg=self.styles['bg'],
      width=30,
      height=30,
      borderwidth=1,
      cursor="hand2")
    self.box.bind("<Button-1>", self.toggle_check)
    self.box.pack(side=LEFT)

    self.label = Label(self.wrapper,
      fg=self.styles['fg'] if self.checked else self.styles['placeholder_fg'],
      bg=self.styles['bg'],
      text=self.text,
      font=self.styles['font'],
      cursor="hand2")
    self.label.bind("<Button-1>", self.toggle_check)
    self.label.pack(side=LEFT, padx=6)

    self.check = Label(self.wrapper,
      fg=self.styles['fg'],
      bg=self.styles['bg'],
      text="✔",
      font=self.styles['checkbox_font'],
      cursor="hand2")
    if self.checked:
      self.check.place(x=4, y=3)

    self.check.bind("<Button-1>", self.toggle_check)

  def toggle_check(self, event):
    self.num_toggles += 1
    if self.num_toggles % 2 == 0:
      self.check.place(x=4, y=3)
      self.label.config(fg=self.styles['fg'])

      if self.oncheck != None:
        self.oncheck(self.checkbox_id)

    else:
      self.check.place_forget()
      self.label.config(fg=self.styles['placeholder_fg'])

      if self.onuncheck != None:
        self.onuncheck(self.checkbox_id)
    
  def pack(self, *args, **kwargs):
    self.wrapper.pack(*args, **kwargs)

  def winfo_width(self, *args, **kwargs):
    return self.wrapper.winfo_width(*args, **kwargs)

  def scroll_bind(self, *args, **kwargs):
    self.wrapper.bind(*args, **kwargs)
    self.box.bind(*args, **kwargs)
    self.label.bind(*args, **kwargs)
    self.check.bind(*args, **kwargs)