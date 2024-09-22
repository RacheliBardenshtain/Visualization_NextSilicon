import random

# Updated list of bright and colorful colors in RGB format
colors = [
    'lime', 'mediumturquoise', 'seashell', 'palevioletred', 'greenyellow' , 'navajowhite'
  , 'blanchedalmond', 'white', 'burlywood', 'moccasin', 'skyblue',
    'whitesmoke', 'lavenderblush', 'powderblue', 'aliceblue', 'ghostwhite', 'springgreen', 'lawngreen', 'turquoise', 'salmon', 'cadetblue',
    'antiquewhite', 'lavender',  'gold', 'cornflowerblue', 'azure', 'beige',
   'honeydew', 'chartreuse', 'palegreen', 'mediumorchid',
    'papayawhip', 'bisque', 'floralwhite', 'lemonchiffon', 'yellowgreen',
    'peachpuff', 'orchid', 'magenta', 'linen', 'thistle', 'goldenrod',
     'cornsilk', 'mistyrose', 'aquamarine', 'mediumspringgreen', 'oldlace', 'tomato',
    'paleturquoise' , 'yellow',
    "#FFC0CB","#F08080","#FFA07A","#FAFAD2","#FFFFE0","#E0FFFF","#87CEFA","#B0C4DE","#ADD8E6","#90EE90","#20B2AA",
    "#FFDAB9", "#EEE8AA","#98FB98", "#AFEEEE","#DB7093","#FFEFD5","#B0E0E6","#BC8F8F","#4169E1","#87CEEB",
    "#FFD700", "#FFFACD", "#ff0000",
    " #fd2f2f",  " #fd5555",    " #f77171",    " #fd9e9e",
    "#fd2f2f", "#fd5555", "#77f8f3", "#45f6f0", "#00fff7", "#820d0d",
    "#266a68", "#1a9591", "#28c5f9", "#3d9290", "#79a09f", "#00bfff",
    "#255767", "#1a8eb5", "#a9dced", "#82d7f4", "#5ad0f7",
    "#4c807f", "#4dc4c2", "#19bcb9", "#72fffd", "#00fffb",
    "#f7ccf1", "#faa6ef", "#fa79e9", "#fd3fe4", "#ff00dd",
    "#9a8497", "#b780b0", "#af45a1", "#ad1d9a", "#b2009a",
    "#5e0c35", "#b21061", "#ff0080", "#dbc2e8", "#de9cff",
    "#c561f8", "#b632f8", "#aa00ff", "#f8d5d5", "#bb1313",
    "#816e8b", "#5f3f6f", "#582472", "#55087c", "#20a73d",
    "#9ef1b0", "#6ef18b", "#20a73d", "#33f35c", "#00ff37",
    "#b6d5fb", "#92c3ff", "#6aadff", "#3f95ff", "#0073ff",
    "#4e7cb4", "#1763c0", "#103c71", "#4e5e71", "#3d5b80",
    "#f4eac6", "#ffedac", "#fadd73", "#f6ce3f", "#ffc800",
    "#7a9b17", "#dcf19d", "#d6f675", "#c6f43d", "#bfff00",
    "#54d4d8", "#99b3b4", "#5a8485", "#4ca5a8", "#00aaaf",
    "#f4c9bc", "#fca58a", "#f38360", "#f66438", "#ff3c00",
    "#288588", "#1c9ca0", "#5a8485", "#4ca5a8", "#c7376c",
    "#670825", "#ab375a", "#dd1f58", "#9e5151", "#ae3737",

]

process_tids_colors = {}

def get_random_color() -> str:
    """Return a random color from the color list."""
    return random.choice(colors)

def get_colors_by_tids(tids: list) -> list:
    """Return a list of colors corresponding to a list of tids."""
    result = []
    for tid in tids:
        if tid not in process_tids_colors:
            process_tids_colors[tid] = get_random_color()
        result.append(process_tids_colors[tid])
    return result
