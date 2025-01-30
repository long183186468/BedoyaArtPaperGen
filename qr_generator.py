import qrcode
from PIL import Image, ImageDraw, ImageFont
import config
import os

def mm_to_pixels(mm, dpi=300):
    """将毫米转换为像素"""
    return int(mm * dpi / 25.4)

def resize_keep_aspect(image, target_height):
    """调整图像大小，保持宽高比，以高度为准"""
    if isinstance(target_height, tuple):
        target_height = target_height[1]
    width, height = image.size
    aspect = width / height
    new_height = target_height
    new_width = int(target_height * aspect)
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def generate_qr_code(student_id, name, paper_size_mm=(297, 210), qr_size_percent=0.08, logo_path=None):
    """生成标准格式的标签，包含logo、二维码和姓名"""
    try:
        # 将毫米转换为像素
        width_pixels = mm_to_pixels(paper_size_mm[0])
        height_pixels = mm_to_pixels(paper_size_mm[1])
        size = (width_pixels, height_pixels)
        
        # 创建白色背景
        final_image = Image.new('RGB', size, 'white')
        
        # 计算二维码尺寸（以纸张高度的百分比为准）
        qr_size = int(height_pixels * qr_size_percent)
        
        # 创建二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=1,
        )
        qr.add_data(f"ID:{student_id}\nName:{name}")
        qr.make(fit=True)
        
        # 生成二维码图像
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image = qr_image.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        
        # 加载logo
        logo = None
        logo_height = int(qr_size * 0.8)  # Logo高度为二维码的80%
        if logo_path is None:
            logo_path = config.DEFAULT_LOGO
            
        try:
            if os.path.exists(logo_path):
                logo = Image.open(logo_path)
                # 保持logo原始比例
                logo = resize_keep_aspect(logo, logo_height)
        except Exception as e:
            print(f"无法加载Logo: {str(e)}")
            return None
        
        # 计算右下角标签区域
        margin_mm = 5  # 边距5mm
        margin_pixels = mm_to_pixels(margin_mm)
        
        # 计算二维码位置（右下角）
        qr_x = width_pixels - qr_size - margin_pixels
        qr_y = height_pixels - qr_size - margin_pixels - mm_to_pixels(5)  # 留出文字空间
        
        # 如果有logo，计算logo位置（在二维码左侧）
        if logo:
            logo_x = qr_x - logo.size[0] - mm_to_pixels(3)  # 间距3mm
            logo_y = qr_y + (qr_size - logo.size[1]) // 2  # 垂直居中对齐
            final_image.paste(logo, (logo_x, logo_y))
        
        # 放置二维码
        final_image.paste(qr_image, (qr_x, qr_y))
        
        # 添加文字
        draw = ImageDraw.Draw(final_image)
        try:
            # 字体大小为二维码尺寸的15%
            font_size = int(qr_size * 0.15)
            font = ImageFont.truetype(config.FONT_PATH, font_size)
        except:
            font = ImageFont.load_default()
        
        # 在二维码下方显示姓名和学号
        text = f"{name} {student_id}"
        text_width = draw.textlength(text, font=font)
        text_x = qr_x + (qr_size - text_width) // 2  # 在二维码下方居中
        text_y = qr_y + qr_size + mm_to_pixels(1)    # 二维码下方1mm
        
        # 绘制文字
        draw.text((text_x, text_y), text, fill="black", font=font)
        
        return final_image
    except Exception as e:
        print(f"生成二维码失败: {str(e)}")
        return None

def get_logo_image(logo_path, target_height):
    """获取Logo图像，保持宽高比"""
    try:
        logo = Image.open(logo_path)
        return resize_keep_aspect(logo, target_height)
    except Exception as e:
        print(f"无法加载Logo: {str(e)}")
        return None
