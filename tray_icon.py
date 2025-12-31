import tkinter as tk
import threading
import os
import sys

class TrayIcon:
    def __init__(self, config, show_settings_callback, quit_callback):
        self.config = config
        self.show_settings_callback = show_settings_callback
        self.quit_callback = quit_callback
        self.create_tray_icon()
    
    def create_tray_icon(self):
        try:
            import pystray
            from PIL import Image
            
            # --- 核心修复：获取正确的资源路径 ---
            if hasattr(sys, '_MEIPASS'):
                # 如果是 PyInstaller 打包后的路径
                icon_path = os.path.join(sys._MEIPASS, "icon.ico")
            else:
                # 如果是编辑器直接运行的路径
                icon_path = "icon.ico"
            
            print(f"正在尝试加载图标: {icon_path}") # 调试信息
            
            if os.path.exists(icon_path):
                image = Image.open(icon_path)
            else:
                # 最后的保底方案：如果还是找不到，画一个简单的点，确保托盘不消失
                print("未找到图标文件，使用保底绘图方案")
                image = Image.new('RGB', (16, 16), color=(40, 40, 40))
            # ----------------------------------

            menu = pystray.Menu(
                pystray.MenuItem("设置", self.show_settings_callback, default=True),
                pystray.MenuItem("退出", self.quit_app)
            )
            
            self.icon = pystray.Icon("crosshair_tool", image, "准星工具", menu)
            threading.Thread(target=self.icon.run, daemon=True).start()
        except Exception as e:
            print(f"托盘图标启动失败: {e}")
            self.show_settings_callback()
    
    def quit_app(self):
        if hasattr(self, 'icon'): self.icon.stop()
        self.quit_callback()