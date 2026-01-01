import PyInstaller.__main__
import os
import shutil
import json

def build():
    # 1. 环境准备：确保配置文件存在
    config_file = "crosshair_config.json"
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            json.dump({"dot_size": 4, "line_color": "#FF3232"}, f, indent=4)

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
        '--add-data=crosshair_config.json;.',
        '--add-data=icon.ico;.',
        '--icon=icon.ico',  # 设置 exe 文件本身的图标
    ]

    # 4. 精简策略
    excludes = [
        'numpy', 'matplotlib', 'pyautogui', 'scipy', 'pygame', 'notebook',
        'tkinter.test', 'unittest', 'pydoc', 'email', 'http', 'xml',
    ]

    for m in excludes:
        params.extend(['--exclude-module', m])

    params.extend(['--hidden-import', 'PIL.IcoImagePlugin'])
    params.extend(['--hidden-import', 'PIL.ImageWin'])

    # 5. 执行
    PyInstaller.__main__.run(params)
    print("\n构建完成！")

if __name__ == '__main__':
    build()
