from app_button import App_Button
from tkinter import LEFT, Label, LabelFrame
import PIL.Image 
import PIL.ImageTk
import os

class App_Photo(object):
  """docstring for App_Photo"""
  def __init__(self, master, pil_photo, styles, root, fullsize_path, hide_cmd=None, del_cmd=None):
    super(App_Photo, self).__init__()

    self.master = master
    self.pil_photo = pil_photo
    self.fullsize_path = fullsize_path

    self.photo = PIL.ImageTk.PhotoImage(pil_photo)

    self.styles = styles
    self.tool_styles = styles.copy()
    self.tool_styles['big_font'] = styles['font']
    self.tool_styles['padx'] = 5
    self.tool_styles['pady'] = 3

    self.root = root

    self.hide_cmd = hide_cmd
    self.del_cmd = del_cmd

    self.putPhoto()

  def putPhoto(self):
    self.wrapper = LabelFrame(self.master, bg=self.styles['bg'], borderwidth=0)
    self.photo_label = Label(self.wrapper, 
      image=self.photo, 
      borderwidth=0, 
      cursor="hand2")

    self.photo_label.bind("<Button-1>", self.zoom)
    self.photo_label.bind("<Enter>", self.show_tools)
    self.photo_label.bind("<Leave>", self.hide_tools)
    self.photo_label.image = self.photo
    self.photo_label.pack()


    self.minimize_tool = App_Button(self.wrapper, 
      text="➖", 
      styles=self.tool_styles,
      command=self.hide_cmd)
    self.minimize_tool.bind_wrapper("<Enter>", self.show_tools)
    self.minimize_tool.place(x=0, y=0)
    self.minimize_tool.place_forget()


    self.delete_tool = App_Button(self.wrapper, 
      text="✕", 
      styles=self.tool_styles,
      command=self.del_cmd)
    self.delete_tool.bind_wrapper("<Enter>", self.show_tools)
    self.delete_tool.place(x=0, y=0)
    self.delete_tool.place_forget()

    self.overlay = LabelFrame(self.root, 
      bg=self.styles['overlay'], 
      fg=self.styles['overlay'],
      borderwidth=0)

    self.overlay_close = App_Button(self.overlay, 
      text="⩁", 
      title="Close the zoomed view",
      styles=self.styles,
      command=self.un_zoom)
    self.overlay_close.place(x=0, y=0)

  def zoom(self, event):
    window_width = self.root.winfo_width()
    window_height = self.root.winfo_height()

    self.overlay.config(width=window_width)
    self.overlay.config(height=window_height)
    self.overlay.place(x=0, y=0)

    zoomed_width = int(window_width * 0.8)
    zoomed_height = int(window_height * 0.8)

    pil_photo = PIL.Image.open(self.fullsize_path)

    wpercent = (zoomed_width/float(pil_photo.size[0]))
    hsize = int((float(pil_photo.size[1])*float(wpercent)))
    zoomed_pil_photo = pil_photo.resize((zoomed_width,hsize), PIL.Image.ANTIALIAS)

    hpercent = (zoomed_height/float(pil_photo.size[1]))
    wsize = int((float(pil_photo.size[0])*float(hpercent)))
    zoomed_pil_photo = pil_photo.resize((wsize,zoomed_height), PIL.Image.ANTIALIAS)

    zoomed_photo = PIL.ImageTk.PhotoImage(zoomed_pil_photo)

    self.zoomed_photo_label = Label(self.root, 
      image=zoomed_photo, 
      borderwidth=0)
    self.zoomed_photo_label.image = zoomed_photo
    self.zoomed_photo_label.pack()

    photo_x_pos = (window_width / 2) - (wsize / 2)
    photo_y_pos = (window_height / 2) - (zoomed_height / 2)

    overlay_close_width = self.overlay_close.winfo_width()

    self.overlay_close.place(x=window_width-overlay_close_width-25, y=25)
    self.zoomed_photo_label.place(x=photo_x_pos, y=photo_y_pos)
    
  def un_zoom(self):
    self.overlay.place_forget()
    self.zoomed_photo_label.place_forget()

  def show_tools(self, event):
    photo_x = self.photo_label.winfo_x()
    photo_y = self.photo_label.winfo_y()
    photo_width = self.photo_label.winfo_width()

    minimize_tool_width = self.minimize_tool.winfo_width()
    delete_tool_width = self.delete_tool.winfo_width()

    minimize_tool_x_pos = photo_x + photo_width - minimize_tool_width - delete_tool_width - 5
    delete_tool_x_pos = photo_x + photo_width - delete_tool_width
    tool_y_pos = photo_y + 5

    self.minimize_tool.place(x=minimize_tool_x_pos, y=tool_y_pos)
    self.delete_tool.place(x=delete_tool_x_pos, y=tool_y_pos)

  def hide_tools(self, event):
    self.minimize_tool.place_forget()
    self.delete_tool.place_forget()

  def bind(self, *args, **kwargs):
    self.wrapper.bind(*args, **kwargs)

  def pack(self, *args, **kwargs):
    self.wrapper.pack(*args, **kwargs)

  def destroy(self, *args, **kwargs):
    self.wrapper.destroy(*args, **kwargs)

