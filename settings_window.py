import tkinter as tk
from tkinter import ttk, colorchooser

class SettingsWindow:
    def __init__(self, config, on_config_update):
        self.config = config
        self.on_config_update = on_config_update
        self.window = None
    
    def show(self):
        """显示设置窗口"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
        
        self.window = tk.Toplevel()
        self.window.title("准星设置")
        self.window.geometry("300x350")  # 调整窗口高度
        self.window.resizable(True, True)
        
        # 使窗口居中
        self.center_window(self.window)
        self.window.transient()
        self.window.grab_set()
        
        self.create_widgets()
    
    def center_window(self, window):
        """窗口居中"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """创建设置窗口的控件"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 固定行高为40
        row_height = 40
        
        # 颜色选择 - 第一行
        color_frame = ttk.Frame(main_frame, height=row_height)
        color_frame.pack(fill=tk.X, pady=5)
        color_frame.pack_propagate(False)
        
        ttk.Label(color_frame, text="颜色:").pack(side=tk.LEFT, padx=(0, 10))
        self.color_button = ttk.Button(color_frame, text="选择颜色", command=self.choose_color, width=12)
        self.color_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 显示当前颜色预览
        self.color_preview = tk.Frame(color_frame, width=30, height=30, relief="solid", borderwidth=1)
        self.color_preview.pack(side=tk.LEFT)
        self.color_preview.pack_propagate(False)
        self.update_color_preview(self.config.line_color)
        
        # 点大小 - 第二行
        size_frame = ttk.Frame(main_frame, height=row_height)
        size_frame.pack(fill=tk.X, pady=5)
        size_frame.pack_propagate(False)
        
        ttk.Label(size_frame, text="点大小:").pack(side=tk.LEFT, padx=(0, 10))
        
        # 滑动条和数值显示在同一行
        slider_value_frame = ttk.Frame(size_frame)
        slider_value_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.dot_size = tk.IntVar(value=self.config.dot_size)
        
        # 创建用于显示的StringVar
        self.dot_size_display = tk.StringVar(value=str(self.config.dot_size))
        
        dot_scale = ttk.Scale(slider_value_frame, from_=1, to=20, variable=self.dot_size, 
                            orient=tk.HORIZONTAL, length=180, command=self.on_slider_change)
        dot_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 修改这里：使用dot_size_display而不是dot_size
        dot_label = ttk.Label(slider_value_frame, textvariable=self.dot_size_display, width=5)
        dot_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        # 按钮框架 - 第三行
        button_frame = ttk.Frame(main_frame, height=row_height)
        button_frame.pack(fill=tk.X, pady=10)
        button_frame.pack_propagate(False)
        
        # 按钮居中
        inner_button_frame = ttk.Frame(button_frame)
        inner_button_frame.pack(expand=True)
        
        # 取消应用按钮，只保留确定和取消
        ttk.Button(inner_button_frame, text="确定", command=self.ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(inner_button_frame, text="取消", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
    
    def update_color_preview(self, color):
        """更新颜色预览"""
        hex_color = color
        self.color_preview.configure(bg=hex_color)
    
    def choose_color(self):
        """打开颜色选择对话框"""
        color = colorchooser.askcolor(
            initialcolor=self.config.line_color, 
            title="选择准星颜色",
            parent=self.window  # 直接使用当前窗口作为父窗口
        )
        
        if color[1]:  # color[1] 是hex颜色值
            self.config.line_color = color[1]
            self.update_color_preview(color[1])
            self.apply_preview()
    
    def on_slider_change(self, value):
        """滑块变化时的回调"""
        int_value = int(float(value))
        self.dot_size_display.set(str(int_value))
        self.apply_preview()
    
    def apply_preview(self):
        """应用预览（不保存到配置文件）"""
        temp_config = {
            'line_color': self.config.line_color,
            'dot_size': self.dot_size.get()
        }
        
        if hasattr(self.on_config_update, '__call__'):
            self.on_config_update(preview=True, **temp_config)
    
    def apply_settings(self):
        """应用设置并保存到配置文件"""
        self.config.update_config(
            line_color=self.config.line_color,
            dot_size=self.dot_size.get()
        )
        self.on_config_update()
    
    def ok(self):
        """确定按钮，应用设置并关闭窗口"""
        self.apply_settings()
        self.window.destroy()