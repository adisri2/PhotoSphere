from tkinter import *
from tkinter.font import Font
import threading

sys.path.insert(0, 'components')
from app_checkbox import App_Checkbox

sys.path.insert(0, 'input-output')
from randword import Rand_Word

sys.path.insert(0, 'styles')
from styles import get_styles

class Edit_Myterms(Frame):
  """docstring for Edit_Myterms"""
  def __init__(self, master):
    super(Edit_Myterms, self).__init__()

    Frame.__init__(self, master)

    self.master = master

    self.styles = get_styles()
    self.scroll_thread_arr = []
    
    self.init_window()

  def init_window(self):
    self.master.title("Edit MyTerms")
    self.master.iconbitmap("images/icon_16.ico")
    self.master.state("zoomed")

    self.window_width = self.master.winfo_width()

    self.configure(bg=self.styles['bg'])
    self.pack(fill=BOTH, expand=1)

    self.bind("<MouseWheel>", self.scroll)

    self.rand_word = Rand_Word()

    self.wordlist = self.rand_word.wordlist

    self.container = LabelFrame(self, bg=self.styles['bg'], borderwidth=0)
    self.container.bind("<MouseWheel>", self.scroll)
    self.container.pack()
    self.container.place(x=10, y=0)

    self.putEditor()

  def putEditor(self):

    header = Label(self.container, text="Edit MyTerms. MyTerms are the groups of words that are used in AutoGet. AutoGet is a fast and quick way to bulk download a lot of pictures. All of the categories that are checked will be the categories of photos that are used in AutoGet. Just check or uncheck the desired categories", 
      fg=self.styles['fg'], 
      bg=self.styles['bg'], 
      font=self.styles['font'],
      wraplength=self.window_width - 60)
    header.pack(pady=20)
    header.bind("<MouseWheel>", self.scroll)

    for _type, sub_type in self.wordlist.items():

      section = LabelFrame(self.container, bg=self.styles['bg'], borderwidth=1, padx=10, pady=9)
      section.pack(padx=10, pady=10)
      section.bind("<MouseWheel>", self.scroll)

      type_parent = Label(section, 
        text=_type.title(),
        font=self.styles['big_font'],
        fg=self.styles['fg'],
        bg=self.styles['bg'])
      type_parent.pack(pady=10)
      type_parent.bind("<MouseWheel>", self.scroll)

      row_width = 0

      row_arr = []
      row_arr_index = 0

      init_row = LabelFrame(section, bg=self.styles['bg'], borderwidth=0)
      init_row.pack()

      row_arr.append(init_row)

      for _category, words in sub_type.items():

        # _id_num = 


        checkbox_width = int(((67/7) * len(_category)) + (498/7))

        if row_width + checkbox_width > self.window_width:
          addit_row = LabelFrame(section, bg=self.styles['bg'], borderwidth=0)
          addit_row.pack()

          row_arr.append(addit_row)
          row_arr_index += 1

          row_width = 0
          

        category = App_Checkbox(row_arr[row_arr_index], 
          text=self.to_title("_", _category), 
          styles=self.styles, 
          checked=True if words['active'] else False,
          checkbox_id=words['id'],
          oncheck=self.check,
          onuncheck=self.uncheck)

        category.pack(side=LEFT)
        category.scroll_bind("<MouseWheel>", self.scroll)
        
        row_width += checkbox_width

    self.update_idletasks()
    self.init_container_y = self.container.winfo_y()

    self.container_height = self.container.winfo_height()
    self.window_width = self.master.winfo_width()
    self.window_height = self.master.winfo_height()

    self.scrollbar_wrapper = LabelFrame(self, 
      bg=self.styles['placeholder_fg'], 
      borderwidth=0, 
      width=15, 
      height=self.window_height)
    self.scrollbar_wrapper.pack()
    self.scrollbar_wrapper.place(x=self.window_width-15, y=0)

    self.scrollbar_thumb_height = (self.window_height / self.container_height) * self.window_height
    self.scrollbar_thumb = LabelFrame(self.scrollbar_wrapper, 
      bg=self.styles['fg'], 
      borderwidth=0,
      width=15,
      height=self.scrollbar_thumb_height)
    self.scrollbar_thumb.pack()
    self.scrollbar_thumb.place(x=0, y=0)
    # self.scrollbar_thumb.bind("<Button-1>", self.click_thumb)
    # self.scrollbar_thumb.bind("<ButtonRelease-1>", self.release_thumb)

  def scroll(self, event=None, by=0):
    def process():
      container_x_pos = self.container.winfo_x()
      container_y_pos = self.container.winfo_y()

      scrollbar_y_pos = self.scrollbar_thumb.winfo_y()

      if by == 0 and event != None:
        container_amount = 60
        scrollbar_amount = (self.container_height - self.window_height) / container_amount + 6

        scrollbar_increment = 0
        container_increment = 0

        if (event.num == 4 or event.delta == 120) and (container_y_pos < self.init_container_y):
          container_increment = container_amount
          scrollbar_increment = -scrollbar_amount

        if (event.num == 5 or event.delta == -120) and container_y_pos > -(self.container_height - self.window_height):
          container_increment = -container_amount
          scrollbar_increment = scrollbar_amount

        self.container.place(x=container_x_pos, y=container_y_pos + container_increment)

        self.scrollbar_thumb.place(x=0, y=scrollbar_y_pos + scrollbar_increment)
        self.master.update_idletasks()

      elif event == None and by != 0:
        self.container.place(x=container_x_pos, y=container_y_pos - (by * 3))

        self.scrollbar_thumb.place(x=0, y=scrollbar_y_pos + by)
        self.master.update_idletasks()
    t = threading.Thread(target=process)
    t.daemon = True
    t.start()

  def click_thumb(self, event):
    clicked_y = event.y
    self.scrollbar_thumb.bind("<B1-Motion>", lambda e: self.drag_thumb(e, clicked_y))

  def drag_thumb(self, event, start_y):
    self.scroll(by=event.y - start_y)

  def release_thumb(self, event):
    self.scrollbar_thumb.unbind("<B1-Motion>")

  def check(self, id_num):
    self.rand_word.enable(id_num)

  def uncheck(self, id_num):
    self.rand_word.disable(id_num)

  def to_title(self, delimiter, string):
    str_arr = string.split(delimiter)
    
    str_arr = [section.title() for section in str_arr]
    joined_str = " ".join(str_arr)
    return joined_str
