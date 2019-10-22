from tkinter import LabelFrame, Entry, Label, FLAT, END, StringVar

class App_Entry(object):
  """docstring for App_Entry"""
  def __init__(self, master, placeholder=None, styles=None, entry_arr=None):
    super(App_Entry, self).__init__()
    
    self.master = master
    self.placeholder = placeholder
    self.styles = styles
    self.entry_arr = entry_arr

    self.placeholder_y = 0

    self.putEntry()

  def putEntry(self):
    self.entry_wrapper = LabelFrame(self.master, 
      # relief=FLAT, 
      borderwidth=1,
      bg=self.styles['bg'], 
      fg=self.styles['fg'],
      padx=2,
      pady=3)

    self.contents = StringVar()

    self.entry = Entry(self.entry_wrapper,
      font=self.styles['entry_font'], 
      bg=self.styles['bg'], 
      fg=self.styles['fg'],
      insertborderwidth=1,
      borderwidth=0,
      width=self.styles['entry_width'],
      textvariable=self.contents,
      selectbackground=self.styles['select_bg'],
      selectforeground=self.styles['select_fg'])
    self.entry.bind("<Control-Key>", self.word_backspace)
    self.entry.bind("<FocusIn>", self._focus)
    self.entry.bind("<FocusOut>", self.check_to_blur)
    self.entry.pack()

    entry_height = self.entry.winfo_height()

    self.placeholder_label = Label(self.entry_wrapper, 
      text=self.placeholder,
      bg=self.styles['bg'], 
      fg=self.styles['placeholder_fg'],
      font=self.styles['placeholder_font'],
      cursor="xterm")
    self.placeholder_label.bind("<Button-1>", self._focus)
    self.placeholder_label.pack()

    placeholder_height = self.placeholder_label.winfo_height()

    self.placeholder_y = int((entry_height / 2) + (placeholder_height / 2) - 2)

    self.placeholder_label.place(x=3, y=self.placeholder_y)
    self.entry_arr.append(self)

  def winfo_id(self):
    return self.entry_wrapper.winfo_id()

  def winfo_pathname(self, _id=None):
    return self.entry_wrapper.winfo_pathname(_id)

  def check_to_blur(self, event=None):
    if len(self.contents.get()) == 0:
      self.blur()
    else:
      self.placeholder_label.place_forget()

  def word_backspace(self, event):

    if event.keycode == 8:
      contents = self.contents.get().strip()
      split_contents = contents.split(" ")
      del split_contents[-1]
      joined = " ".join(split_contents)

      self.contents.set(joined + "e")

  def blur(self, event=None):
    self.placeholder_label.place(x=3, y=self.placeholder_y)

  def _focus(self, event=None):
    self.entry.focus()
    self.placeholder_label.place_forget()

  def pack(self, *args, **kwargs):
    self.entry_wrapper.pack(*args, **kwargs)

  def bind(self, *args, **kwargs):
    self.entry_wrapper.bind(*args, **kwargs)

  def bind_to_entry(self, *args, **kwargs):
    self.entry.bind(*args, **kwargs)

  def delete(self, *args, **kwargs):
    self.entry.delete(*args, **kwargs)

  def insert(self, *args, **kwargs):
    self.entry.insert(*args, **kwargs)

  def get(self):
    return self.entry.get()

  def winfo_rootx(self):
    return self.entry_wrapper.winfo_rootx()

  def winfo_rooty(self):
    return self.entry_wrapper.winfo_rooty()

  def winfo_height(self):
    return self.entry_wrapper.winfo_height()

  def winfo_width(self):
    return self.entry_wrapper.winfo_width()
