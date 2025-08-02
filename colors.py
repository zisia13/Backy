from zModules.zExtensions import public, private

class Colors:

    def __init__(self):
        self.WHITE = self.build_color(255, 255, 255)
        self.BLACK = self.build_color(0, 0, 0)
        self.GRAY = self.build_color(128, 128, 128)
        
        self.RED = self.build_color(255, 0, 0)
        self.GREEN = self.build_color(0, 255, 0)
        self.BLUE = self.build_color(0, 0, 255)
        
        self.YELLOW = self.build_color(255, 255, 0)
        self.CYAN = self.build_color(0, 255, 255)
        self.MAGENTA = self.build_color(255, 0, 255)

        self.ORANGE = self.build_color(255, 165, 0)
        self.PURPLE = self.build_color(128, 0, 128)
        self.PINK = self.build_color(255, 192, 203)
        self.LIME = self.build_color(0, 255, 0)
        self.OLIVE = self.build_color(128, 128, 0)
        self.NAVY = self.build_color(0, 0, 128)
        
        self._reset = self.build_color(255, 255, 255)
    
    @private
    def build_color(self, r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    @public
    def c_print(self, c, t):
        print(f"{c}{t}{self._reset}")
    

    
    