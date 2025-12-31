CrosshairOverlay - 极轻量化游戏准星工具

CrosshairOverlay 是一款专为独立游戏开发者和竞技玩家设计的屏幕准星辅助工具。本项目基于 Python 开发。

✨ 核心特性

🚀 瞬时启动：采用延迟加载技术并移除了重型库依赖，实现点击即开，无需等待。

🤏 极小占用：精简了 Pillow 编解码器支持，排除 numpy 等大型第三方库，打包体积大幅缩减。

🖱️ 完美穿透：通过 Win32 API 实现硬件级的点击穿透，准星层不干扰任何鼠标操作。

🎨 实时自定义：支持通过 UI 界面实时调整准星的大小和颜色（支持 Hex 颜色码）。

💾 自动保存：所有设置自动持久化到本地 JSON 配置文件，下次启动自动恢复。

🛠️ 原生适配：使用 ctypes 直接调用 Windows 原生 API 获取分辨率，非截图模式，零延迟且兼容性极佳。

🚀 快速上手

1. 下载即用 (推荐)

前往 Releases 页面下载最新的绿色版压缩包，解压后运行 CrosshairTool.exe 即可。

2. 从源码运行

如果你有 Python 环境，可以直接按以下步骤操作：

# 克隆项目
git clone [https://github.com/你的用户名/CrosshairOverlay.git](https://github.com/你的用户名/CrosshairOverlay.git)
cd CrosshairOverlay

# 安装必要的轻量依赖
pip install pystray pillow

# 启动程序
python main.py


🛠️ 打包与优化说明

作为开发者，你可以通过项目内置的 build.py 快速构建自己的版本。

采用的优化方案：

目录模式 (--onedir)：相比单文件模式，大幅提升了启动速度，避免了运行时解压的性能损耗。

依赖剪裁：显式排除了 pyautogui、matplotlib 等库，将 Pillow 精简到仅保留基础图像处理。

延迟初始化：核心准星窗口优先显示，托盘图标等非核心组件异步加载。

执行打包：

python build.py


📂 项目结构

├── main.py             # 程序主入口，处理窗口透明与点击穿透
├── crosshair.py        # 准星渲染引擎（基于原生 API 获取坐标）
├── config.py           # 配置读取与保存 (JSON 格式)
├── tray_icon.py        # 系统托盘图标与右键菜单逻辑
├── settings_window.py  # Tkinter 编写的设置界面
├── build.py            # 自动化打包脚本
└── icon.ico            # 项目图标文件


📝 许可证

本项目采用 MIT License 许可证。您可以自由地在您的个人或商业项目中使用。

🤝 贡献与反馈

如果您在使用过程中发现任何 Bug，或者有更好的体积精简方案（例如 Nuitka 编译建议），欢迎提交 Issue 或 Pull Request！

由独立游戏开发者为开发者打造。