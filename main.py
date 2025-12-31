import tkinter as tk
from config import Config
from crosshair import Crosshair
from tray_icon import TrayIcon
from settings_window import SettingsWindow
import ctypes

class CrosshairApp:
    def __init__(self):
        self.config = Config()
        self.window = None
        self.canvas = None
        self.crosshair = None
        self.settings_window = None
        self.tray_icon = None
        
        self.setup_gui()
        self.setup_tray_icon()
        
        # 直接显示设置窗口，不需要延迟
        self.show_settings_on_start()

    def show_settings_on_start(self):
        """程序启动时显示设置窗口"""
        if self.settings_window:
            self.settings_window.show()
    
    def setup_gui(self):
        """设置GUI并启用点击穿透"""
        self.window = tk.Tk()
        self.window.attributes("-fullscreen", True)
        self.window.attributes("-topmost", True)
        self.window.attributes("-transparentcolor", "white")
        self.window.overrideredirect(True)
        self.window.configure(bg='white')
        self.window.attributes("-disabled", True)
        
        self.canvas = tk.Canvas(self.window, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        
        self.crosshair = Crosshair(self.canvas, self.config)
        
        # 在窗口显示后设置点击穿透
        self.window.after(100, self.set_click_through)
    
    def set_click_through(self):
        """设置窗口为点击穿透模式"""
        try:
            hwnd = ctypes.windll.user32.GetParent(self.window.winfo_id())
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            WS_EX_TRANSPARENT = 0x00000020
            
            current_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            new_style = current_style | WS_EX_LAYERED | WS_EX_TRANSPARENT
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_style)
            
            print("点击穿透模式已启用")
        except Exception as e:
            print(f"设置点击穿透失败: {e}")
    
    def setup_tray_icon(self):
        """设置系统托盘图标"""
        self.settings_window = SettingsWindow(self.config, self.on_config_update)
        self.tray_icon = TrayIcon(
            self.config, 
            self.settings_window.show, 
            self.quit_app
        )
    
    def on_config_update(self, preview=False, **kwargs):
        """配置更新时的回调"""
        if self.crosshair:
            if preview:
                # 使用新的预览方法
                dot_size = kwargs.get('dot_size', self.config.dot_size)
                line_color = kwargs.get('line_color', self.config.line_color)
                self.crosshair.preview_crosshair(dot_size, line_color)
            else:
                # 正式应用
                self.crosshair.update_crosshair()
    
    def quit_app(self):
        """退出应用程序"""
        if self.window:
            self.window.quit()
            self.window.destroy()

    def run(self):
        """运行应用程序"""
        try:
            self.window.mainloop()
        except KeyboardInterrupt:
            self.quit_app()

if __name__ == '__main__':
    app = CrosshairApp()
    app.run()