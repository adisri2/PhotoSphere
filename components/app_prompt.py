from tkinter import LabelFrame, Label, LEFT
from app_button import App_Button
from app_num_select import App_Num_Select

class App_Prompt(object):
  """docstring for App_Prompt"""
  def __init__(self, master, structure, styles, root, command):
    super(App_Prompt, self).__init__()

    self.master = master
    self.structure = structure
    self.command = command
    self.styles = styles.copy()
    self.font_px_size = self.styles['big_font'].cget("size")

    self.root = root

    self.root_width = self.root.winfo_width()
    self.root_height = self.root.winfo_height()

    self.putPrompt()

  def putPrompt(self):
    self.overlay = LabelFrame(self.master, 
      bg=self.styles['overlay'], 
      fg=self.styles['overlay'], 
      width=self.root_width, 
      height=self.root_height, 
      borderwidth=0)
    
    self.wrapper = LabelFrame(self.master, 
      bg=self.styles['bg'], 
      borderwidth=0,
      pady=25,
      padx=19)

    self.widget_arr = []
    for section in self.structure:
      row = LabelFrame(self.wrapper, 
        bg=self.styles['bg'], 
        borderwidth=0)
      row.pack(padx=10, pady=(0, 15))

      label = Label(row, 
        bg=self.styles['bg'], 
        fg=self.styles['fg'],
        text=section['label'],
        font=self.styles['big_font'])
      label.pack(side=LEFT)

      widget_name = section['widget_class']
      widget_args = section['widget_args']
      if widget_name == "App_Num_Select":
        widget = App_Num_Select(row, **widget_args)
        widget.pack(side=LEFT)
      self.widget_arr.append(widget)

    choice_wrapper = LabelFrame(self.wrapper, 
      bg=self.styles['bg'], 
      borderwidth=0)
    choice_wrapper.pack()

    no_btn = App_Button(choice_wrapper, 
      text="Cancel", 
      styles=self.styles, 
      command=self.hide)
    no_btn.pack(side=LEFT, padx=10)

    self.yes_btn = App_Button(choice_wrapper, text="Submit", styles=self.styles, command=self.exec_command)
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

  def exec_command(self):
    results = []

    for widget in self.widget_arr:
      results.append(widget.get())

    self.command(results)
    self.hide()