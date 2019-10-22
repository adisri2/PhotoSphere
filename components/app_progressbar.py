from tkinter import LabelFrame

class App_Progressbar(object):
  """docstring for App_Progressbar"""
  def __init__(self, master, root, below,styles):
    super(App_Progressbar, self).__init__()
    self.master = master
    self.root = root
    self.styles = styles
    self.below = below

    self.putProgressbar()

  def putProgressbar(self):
    self.bar = LabelFrame(self.master, 
      width=0, 
      bg=self.styles['fg'], 
      height=10, 
      borderwidth=0)

  def set_pct(self, pct):
    window_width = self.root.winfo_width()
    desired_px = int(window_width * pct * 0.01)
    self.bar.config(width=desired_px)

  def show(self, *args, **kwargs):
    self.bar.pack()
    self.bar.place(x=0, y=self.below.winfo_height())

  def hide(self, *args, **kwargs):
    self.bar.place_forget(*args, **kwargs)