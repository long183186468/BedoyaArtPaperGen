import json
import os

CONFIG_FILE = "settings.json"

# 获取当前文件所在目录的绝对路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 默认logo路径
DEFAULT_LOGO = os.path.join(CURRENT_DIR, "logo.png")

# 默认字体路径（使用Windows系统字体）
FONT_PATH = "C:\\Windows\\Fonts\\simhei.ttf"  # 使用黑体

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
QR_CODE_SIZE_PERCENT = config["QR_CODE_SIZE_PERCENT"]
QR_MARGIN = config["QR_MARGIN"]
QR_NAME_FONT_SIZE = config["QR_NAME_FONT_SIZE"]
LOGO_SIZE_PERCENT = config["LOGO_SIZE_PERCENT"]
LOGO_MARGIN = config["LOGO_MARGIN"]
FONT_SIZE = config["FONT_SIZE"]
FONT_PATH = config["FONT_PATH"]
