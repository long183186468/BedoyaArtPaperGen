import PyInstaller.__main__
import os
import sys

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 图标路径
icon_path = os.path.join(current_dir, "logo(1).png")

# 确保所需文件存在
required_files = ["main.py", "qr_generator.py", "config.py", "logo.png", "logo(1).png"]
for file in required_files:
    if not os.path.exists(file):
        print(f"错误: 找不到必需文件 {file}")
        sys.exit(1)

# PyInstaller参数
params = [
    'main.py',                            # 主程序文件
    '--name=贝朵亚画纸生成系统',           # 生成的exe名称
    '--windowed',                         # 使用GUI模式
    f'--icon={icon_path}',               # 设置图标
    '--noconfirm',                       # 覆盖输出目录
    '--add-data=logo.png;.',             # 添加资源文件
    '--add-data=logo(1).png;.',          # 添加图标文件
    '--add-data=config.py;.',            # 添加配置文件
    '--add-data=qr_generator.py;.',      # 添加二维码生成模块
    '--hidden-import=PIL',
    '--hidden-import=PIL._imagingtk',
    '--hidden-import=PIL._tkinter_finder',
    '--hidden-import=PyQt6',
    '--hidden-import=PyQt6.QtCore',
    '--hidden-import=PyQt6.QtGui',
    '--hidden-import=PyQt6.QtWidgets',
    '--collect-all=qrcode',
    '--clean',                           # 清理临时文件
    '--onefile',                         # 打包成单个文件
    '--log-level=DEBUG',                 # 显示详细日志
]

print("开始打包...")
print(f"当前目录: {current_dir}")
print("检查文件:")
for file in required_files:
    print(f"- {file}: {'存在' if os.path.exists(file) else '不存在'}")

try:
    # 运行PyInstaller
    PyInstaller.__main__.run(params)
    print("\n打包完成!")
    print(f"可执行文件应该在: {os.path.join(current_dir, 'dist', '贝朵亚画纸生成系统.exe')}")
except Exception as e:
    print(f"\n打包失败: {str(e)}") 