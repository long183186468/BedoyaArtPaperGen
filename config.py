import json
import os
import sys
import platform

CONFIG_FILE = "settings.json"

# 获取当前文件所在目录的绝对路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 默认logo路径
DEFAULT_LOGO = os.path.join(CURRENT_DIR, "logo.png")

# 根据操作系统选择默认字体
def get_default_font_path():
    system = platform.system()
    if system == "Windows":
        font_paths = [
            "C:\\Windows\\Fonts\\simhei.ttf",  # 黑体
            "C:\\Windows\\Fonts\\msyh.ttc",    # 微软雅黑
            "C:\\Windows\\Fonts\\simsun.ttc"   # 宋体
        ]
    elif system == "Darwin":  # macOS
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc"
        ]
    else:  # Linux
        font_paths = [
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
        ]
    
    # 返回第一个存在的字体文件路径
    for path in font_paths:
        if os.path.exists(path):
            return path
            
    # 如果没有找到合适的字体，返回默认值
    return "C:\\Windows\\Fonts\\simhei.ttf"

# 默认字体路径
FONT_PATH = get_default_font_path()

# 默认图片尺寸
DEFAULT_SIZE = (800, 400)  # 宽度800像素，高度400像素

# 默认配置
DEFAULT_CONFIG = {
    "DEFAULT_LOGO": DEFAULT_LOGO,  # 默认logo路径
    
    # 纸张尺寸（单位：毫米，横向）
    "PAPER_SIZES": {
        "A4": (297, 210),  # 横向A4
        "A3": (420, 297)   # 横向A3
    },
    
    # 标签打印尺寸（单位：毫米）
    "LABEL_PRINTER_SIZES": [
        {'width': 102, 'height': 51},  # 102mm x 51mm
        {'width': 102, 'height': 76},  # 102mm x 76mm
        {'width': 102, 'height': 102}  # 102mm x 102mm
    ],
    
    "LABEL_SIZES": [
        {'width': 30, 'height': 20},  # 30mm x 20mm
        {'width': 50, 'height': 30},  # 50mm x 30mm
        {'width': 40, 'height': 20},  # 40mm x 20mm
        {'width': 40, 'height': 30}   # 40mm x 30mm
    ],
    
    # 二维码默认设置
    "QR_CODE_SIZE_PERCENT": 15,    # 二维码大小（相对于纸张短边的百分比）
    "QR_MARGIN": 20,       # 二维码到纸张边缘的距离（毫米）
    "QR_NAME_FONT_SIZE": 24,  # 二维码下方姓名的字体大小
    
    # Logo默认设置
    "LOGO_SIZE_PERCENT": 12,       # Logo大小（相对于纸张短边的百分比）
    "LOGO_MARGIN": 20,     # Logo到纸张边缘的距离（毫米）
    
    # 字体设置
    "FONT_SIZE": 24,       # 姓名字体大小
    "FONT_PATH": FONT_PATH  # 默认字体
}

def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(config):
    """保存配置文件"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"保存配置失败: {e}")

# 加载配置
config = load_config()

# 导出配置项
DEFAULT_LOGO = config["DEFAULT_LOGO"]
PAPER_SIZES = config["PAPER_SIZES"]
LABEL_PRINTER_SIZES = config["LABEL_PRINTER_SIZES"]
LABEL_SIZES = config["LABEL_SIZES"]
QR_CODE_SIZE_PERCENT = config["QR_CODE_SIZE_PERCENT"]
QR_MARGIN = config["QR_MARGIN"]
QR_NAME_FONT_SIZE = config["QR_NAME_FONT_SIZE"]
LOGO_SIZE_PERCENT = config["LOGO_SIZE_PERCENT"]
LOGO_MARGIN = config["LOGO_MARGIN"]
FONT_SIZE = config["FONT_SIZE"]
FONT_PATH = config["FONT_PATH"]
