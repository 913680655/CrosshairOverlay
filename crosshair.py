import ctypes

class Crosshair:
    def __init__(self, canvas, config):
        self.canvas = canvas
        self.config = config

        # 使用 ctypes 获取屏幕尺寸，无需 pyautogui
        try:
            user32 = ctypes.windll.user32
            self.screen_width = user32.GetSystemMetrics(0)
            self.screen_height = user32.GetSystemMetrics(1)
        except:
            self.screen_width, self.screen_height = (1920, 1080)

        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2
        self.update_crosshair()

    def update_crosshair(self):
        self.canvas.delete("all")
        r = self.config.dot_size
        self.canvas.create_oval(
            self.center_x - r, self.center_y - r,
            self.center_x + r, self.center_y + r,
            fill=self.config.line_color, outline=""
        )

    def preview_crosshair(self, dot_size, line_color):
        self.canvas.delete("all")
        self.canvas.create_oval(
            self.center_x - dot_size, self.center_y - dot_size,
            self.center_x + dot_size, self.center_y + dot_size,
            fill=line_color, outline=""
        )