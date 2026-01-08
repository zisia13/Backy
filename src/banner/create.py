from zModules.zBanner.recolor_horizontal import recolor_horizontal

try: from banner import banner_string, banner_string_2, banner_string_3, banner_color_left, banner_color_right
except: from .banner import banner_string, banner_string_2, banner_string_3, banner_color_left, banner_color_right

BANNER = recolor_horizontal(
    text = banner_string_3,
    start_color = banner_color_left,
    end_color = banner_color_right
)

if __name__ == "__main__":
    import os
    os.system("")
    print(BANNER)