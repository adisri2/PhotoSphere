from tkinter import LabelFrame, Label, FLAT, LEFT, RIGHT
from tkinter.font import Font
from app_button import App_Button
from app_tooltip import App_Tooltip


class App_Num_Select(object):
  """docstring for App_Num_Select"""
  def __init__(self, master, min_amount=0, styles=None, title=None):
    super(App_Num_Select, self).__init__()
    
    self.master = master
    self.min_amount = min_amount
    self.styles = styles
    self.title = title

    self.arrow_styles = styles.copy()
    self.arrow_styles['big_font'] = Font(size=7, family="Century Gothic")
    self.arrow_styles['padx'] = 4
    self.arrow_styles['pady'] = 4

    self.putNumSelect()

  def putNumSelect(self):
    self.wrapper = LabelFrame(self.master,  
      borderwidth=1,
      bg=self.styles['bg'], 
      fg=self.styles['fg'],
      cursor="crosshair")

    self.spin_box = Label(self.wrapper, 
      font=self.styles['big_font'],
      text=str(self.min_amount),
      bg=self.styles['bg'], 
      fg=self.styles['fg'],
      padx=7)
    self.spin_box.pack(side=LEFT)

    self.buttons_wrapper = LabelFrame(self.wrapper,  
      borderwidth=1,
      bg=self.styles['bg'], 
      fg=self.styles['fg'])
    self.buttons_wrapper.pack(side=RIGHT)

    self.up_btn = App_Button(self.buttons_wrapper, text="▲", styles=self.arrow_styles, command=lambda: self.increment(direction=1))
    self.up_btn.pack()
    self.down_btn = App_Button(self.buttons_wrapper, text="▼", styles=self.arrow_styles, command=lambda: self.increment(direction=-1))
    self.down_btn.pack()

    self.spin_box.bind("<MouseWheel>", self.increment)
    self.up_btn.bind("<MouseWheel>", self.increment)
    self.down_btn.bind("<MouseWheel>", self.increment)

    if self.title is not None:
      App_Tooltip(self.spin_box, text=self.title)
      App_Tooltip(self.buttons_wrapper, text=self.title)
      # App_Tooltip(self.down_btn, text=self.title)

  def increment(self, event=None, direction=0):
    value = int(self.spin_box.cget("text"))

    if direction == 0:
      if (event.num == 5 or event.delta == -120) and value > self.min_amount:
        value -= 1
      if event.num == 4 or event.delta == 120:
        value += 1

    elif direction == 1:
      value += 1
    elif direction == -1 and value > self.min_amount:
      value -= 1

    self.spin_box.config(text=str(value))

  def get(self):
    return int(self.spin_box.cget("text"))

  def pack(self, *args, **kwargs):
    self.wrapper.pack(*args, **kwargs)