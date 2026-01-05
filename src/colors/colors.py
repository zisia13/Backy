from zModules.zExtensions import public, private

class Colors:

    def __init__(self):
        self.WHITE = self.b(255, 255, 255)
        self.BLACK = self.b(0, 0, 0)
        self.GRAY = self.b(128, 128, 128)
        
        self.RED = self.b(255, 0, 0)
        self.GREEN = self.b(0, 255, 0)
        self.BLUE = self.b(0, 0, 255)
        
        self.YELLOW = self.b(255, 255, 0)
        self.CYAN = self.b(0, 255, 255)
        self.MAGENTA = self.b(255, 0, 255)

        self.ORANGE = self.b(255, 165, 0)
        self.PURPLE = self.b(128, 0, 128)
        self.PINK = self.b(255, 192, 203)
        self.LIME = self.b(0, 255, 0)
        self.OLIVE = self.b(128, 128, 0)
        self.NAVY = self.b(0, 0, 128)

        self.PASTELL_GREEN = self.b(144, 238, 144)
        self.PASTELL_RED = self.b(255, 114, 118)
        
        self._reset = self.b(255, 255, 255)
    
    @private
    def b(self, r, g, b): #! build color
        return f"\033[38;2;{r};{g};{b}m"

    @public
    def c_print(self, c, t):
        print(f"{c}{t}{self._reset}")

    @public
    def cm_print(self, c1, c2, t1, t2): #todo not working idk why
        print(f"{c1}{t1}{c2}{t2}{self._reset}")
