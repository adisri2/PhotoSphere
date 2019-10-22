from tkinter.font import Font

def get_styles():
  font_family = "Cambria"

  styles = {
    'bg': "white",
    'fg': "#5a5a5a",
    'fg_error': "#FF7851",

    'menu_bg': "#5b9182",

    'btn_fg': "#f8f9fa",
    'btn_bg': '#78c2ad',
    'h_fg': "#f8f9fa",
    'h_bg': "#84ceb9",
    'a_fg': "#f8f9fa",
    'a_bg': "#87c4b3",
    'padx': 29,
    'pady': 5,
    
    'entry_width': 28,
    'placeholder_fg': 'lightgrey',
    'select_fg': '#fff',
    'select_bg': '#79b587',

    'overlay': '#425e56',

    'font': Font(size=13, family=font_family),
    'big_font': Font(size=27, family=font_family),
    'checkbox_font': Font(size=12, family=font_family),
    'entry_font': Font(size=28, family=font_family),
    'placeholder_font': Font(size=26, family=font_family),
    'header_font': Font(size=48, family=font_family)
  }

  return styles