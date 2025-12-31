import PyInstaller.__main__
import os
import shutil
import json

def build():
    # 1. 环境准备：确保配置文件存在
    config_file = "crosshair_config.json"
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            json.dump({"dot_size": 4, "line_color": "#90EE90"}, f, indent=4)

    # 2. 清理
    for p in ['build', 'dist']:
        if os.path.exists(p):
            shutil.rmtree(p)

    # 3. 配置打包参数
    params = [
        'main.py',
        '--name=CrosshairTool',
        '--onedir',         # 目录模式，启动最快
        '--windowed',       # 隐藏控制台
        '--clean',
        '--noconfirm',
        # 将配置文件和图标都打包进去
        '--add-data=crosshair_config.json;.',
        '--add-data=icon.ico;.',
        '--icon=icon.ico',  # 设置 exe 文件本身的图标
    ]

    # 4. 激进的精简策略：排除 Pillow 的各种子模块
    excludes = [
        'numpy', 'matplotlib', 'pyautogui', 'scipy', 'pygame', 'notebook',
        'tkinter.test', 'unittest', 'pydoc', 'email', 'http', 'xml',
        # 排除 Pillow 绘图和不常用的格式支持，显著减小体积
        'PIL.ImageDraw',     # 已经不再需要动态绘图
        'PIL.ImageFont',     # 排除字体处理
        'PIL._webp', 
        'PIL._imagingtk', 
        'PIL._imagingcms', 
        'PIL.ImageQt', 
        'PIL.ImageWin',
        'PIL.BmpImagePlugin',
        'PIL.TiffImagePlugin',
        'PIL.Jpeg2KImagePlugin',
    ]

    for m in excludes:
        params.extend(['--exclude-module', m])

    # 5. 执行
    PyInstaller.__main__.run(params)
    print("\n构建完成！")

if __name__ == '__main__':
    build()