import qrcode
from PIL import Image, ImageDraw, ImageFont
import config
import os

def mm_to_pixels(mm, dpi=300):
    """将毫米转换为像素"""
    return int(mm * dpi / 25.4)

def resize_keep_aspect(image, target_size):
    """调整图像大小，保持宽高比"""
    if isinstance(target_size, tuple):
        target_width, target_height = target_size
    else:
        target_width = target_height = target_size
        
    width, height = image.size
    aspect = width / height
    
    if aspect > target_width / target_height:
        new_width = target_width
        new_height = int(target_width / aspect)
    else:
        new_height = target_height
        new_width = int(target_height * aspect)
    
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def generate_qr_code(student_id, name, paper_size_mm=(297, 210), qr_size_percent=0.08, logo_path=None, subject=None):
    """生成标准格式的标签，包含logo、二维码和姓名"""
    try:
        # 将毫米转换为像素
        width_pixels = mm_to_pixels(paper_size_mm[0])
        height_pixels = mm_to_pixels(paper_size_mm[1])
        size = (width_pixels, height_pixels)
        
        # 创建白色背景
        final_image = Image.new('RGB', size, 'white')
        
        # 判断是否使用全画幅布局（当尺寸小于100mm或是自定义尺寸时）
        is_full_layout = (min(paper_size_mm) < 100 or 
                         paper_size_mm not in [config.PAPER_SIZES["A4"], config.PAPER_SIZES["A3"]])
        
        if is_full_layout:
            # 全画幅模式布局
            margin_pixels = mm_to_pixels(2)  # 2mm边距
            content_width = width_pixels - 2 * margin_pixels
            content_height = height_pixels - 2 * margin_pixels
            
            # 计算二维码尺寸（占据45%宽度）
            qr_size = int(content_width * 0.45)
            
            # 创建二维码
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=1,
            )
            qr_data = f"ID:{student_id}\nName:{name}"
            if subject:
                qr_data += f"\nSubject:{subject}"
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # 生成二维码图像
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_image = qr_image.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
            
            # 加载和调整Logo大小（占据45%宽度）
            if logo_path is None:
                logo_path = config.DEFAULT_LOGO
                
            try:
                if os.path.exists(logo_path):
                    logo = Image.open(logo_path)
                    logo_width = int(content_width * 0.45)
                    logo_height = int(content_height * 0.9)  # 高度占90%
                    logo = resize_keep_aspect(logo, (logo_width, logo_height))
            except Exception as e:
                print(f"无法加载Logo: {str(e)}")
                return None
            
            # Logo放在左边
            if logo:
                logo_x = margin_pixels
                # 调整logo垂直位置，考虑文字空间
                font_size = int(min(width_pixels, height_pixels) * 0.12)  # 增大字体尺寸
                text_space = int(font_size * 3)  # 为两行文字和间距预留空间
                logo_y = (height_pixels - logo.size[1] - text_space) // 2
                final_image.paste(logo, (logo_x, logo_y))
                
                # 在Logo下方添加文字
                draw = ImageDraw.Draw(final_image)
                try:
                    font = ImageFont.truetype(config.FONT_PATH, font_size)
                except:
                    font = ImageFont.load_default()
                
                # 计算文字位置（在Logo下方）
                text_x = logo_x
                text_y = logo_y + logo.size[1] + margin_pixels
                
                # 绘制姓名行
                name_text = f"姓名：{name}"
                draw.text((text_x, text_y), name_text, fill="black", font=font)
                
                # 绘制ID行
                id_text = f"ID：{student_id}"
                draw.text((text_x, text_y + int(font_size * 1.5)), id_text, fill="black", font=font)
                
                # 绘制课程主题行
                if subject:
                    subject_text = f"主题：{subject}"
                    draw.text((text_x, text_y + int(font_size * 3)), subject_text, fill="black", font=font)
            
            # 二维码放在右边，垂直居中
            qr_x = width_pixels - qr_size - margin_pixels
            qr_y = (height_pixels - qr_size) // 2
            final_image.paste(qr_image, (qr_x, qr_y))
            
        else:
            # 标准布局模式（右下角小尺寸）
            # 计算二维码基础尺寸（以较短边的8%为基准）
            base_size = min(width_pixels, height_pixels)
            qr_size = int(base_size * qr_size_percent)
            
            # 创建二维码
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=1,
            )
            qr_data = f"ID:{student_id}\nName:{name}"
            if subject:
                qr_data += f"\nSubject:{subject}"
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # 生成二维码图像
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_image = qr_image.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
            
            # 加载logo
            logo = None
            if logo_path is None:
                logo_path = config.DEFAULT_LOGO
                
            # 计算字体大小（二维码尺寸的15%）
            font_size = int(qr_size * 0.15)
            # 确保字体大小不超过合理范围
            max_font_size = mm_to_pixels(3)  # 最大3mm
            font_size = min(font_size, max_font_size)
            
            # 计算文字高度
            text_height = int(font_size * 3.3)  # 三行文字加间距
            
            # 计算logo应该的高度（总高度减去文字高度和间距）
            logo_height = qr_size - text_height - mm_to_pixels(1)  # 1mm为文字间距
            
            try:
                if os.path.exists(logo_path):
                    logo = Image.open(logo_path)
                    # 调整logo大小，宽度为二维码宽度，高度为计算出的高度
                    logo = resize_keep_aspect(logo, (qr_size, logo_height))
            except Exception as e:
                print(f"无法加载Logo: {str(e)}")
                return None
            
            # 计算边距（以毫米为单位）
            margin_mm = 5
            margin_pixels = mm_to_pixels(margin_mm)
            
            if logo:
                # 计算左侧整体高度（logo + 文字）
                left_total_height = logo.size[1] + mm_to_pixels(1) + text_height  # 1mm间距
                
                # 计算整体宽度
                total_width = qr_size * 2 + mm_to_pixels(2)  # 两个相同宽度的元素加2mm间距
                
                # 计算整体的起始位置（靠右对齐）
                start_x = width_pixels - margin_pixels - total_width
                
                # 放置Logo（在左边）
                logo_x = start_x
                logo_y = height_pixels - margin_pixels - left_total_height
                final_image.paste(logo, (logo_x, logo_y))
                
                # 添加文字（在Logo下方）
                draw = ImageDraw.Draw(final_image)
                try:
                    font = ImageFont.truetype(config.FONT_PATH, font_size)
                except:
                    font = ImageFont.load_default()
                
                # 计算文字位置
                text_x = logo_x
                text_y = logo_y + logo.size[1] + mm_to_pixels(1)  # 1mm间距
                
                # 绘制姓名行
                name_text = f"姓名：{name}"
                draw.text((text_x, text_y), name_text, fill="black", font=font)
                
                # 绘制ID行（减小行间距）
                id_text = f"ID：{student_id}"
                draw.text((text_x, text_y + int(font_size * 1.1)), id_text, fill="black", font=font)
                
                # 绘制课程主题行
                if subject:
                    subject_text = f"主题：{subject}"
                    draw.text((text_x, text_y + int(font_size * 2.2)), subject_text, fill="black", font=font)
                
                # 放置二维码（在右边）
                qr_x = start_x + qr_size + mm_to_pixels(2)  # 2mm间距
                qr_y = height_pixels - margin_pixels - qr_size
                final_image.paste(qr_image, (qr_x, qr_y))
            else:
                # 如果没有Logo，只显示二维码
                qr_x = width_pixels - margin_pixels - qr_size
                qr_y = height_pixels - margin_pixels - qr_size
                final_image.paste(qr_image, (qr_x, qr_y))
        
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
