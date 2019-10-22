from tkinter import LabelFrame, Label
import time
import threading

class App_Toast(object):
  """docstring for App_Toast"""
  def __init__(self, master, text, styles, root):
    super(App_Toast, self).__init__()

    self.master = master
    self.text = text
    self.styles = styles
    self.root = root

    self.font_px_size = self.styles['big_font'].cget("size")

    def process():
      self.putToast()
      time.sleep(3)
      self.hide()

    t = threading.Thread(target=process)
    t.daemon = True
    t.start()

  def putToast(self):

    self.label = Label(self.master,
      text=self.text,
      bg=self.styles['fg'],
      fg=self.styles['bg'],
      font=self.styles['big_font'],
      padx=15,
      pady=12)

    self.label.pack()

    self.label.update_idletasks()

    root_width = self.root.winfo_width()
    root_height = self.root.winfo_height()

    text_width = self.label.winfo_width()
    text_height = self.label.winfo_height()

    x_pos = root_width - text_width - 15
    y_pos = root_height - text_height - 15

    self.label.place(x=x_pos, y=y_pos)

  def hide(self):
    self.label.place_forget()
    