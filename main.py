import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QSpinBox, QFileDialog, QMessageBox, QGroupBox,
                            QRadioButton, QButtonGroup, QFrame)
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QPixmap, QPainter, QColor, QImage, QLinearGradient, QPen
from PIL import Image
from PIL.ImageQt import ImageQt
import qrcode
from qr_generator import generate_qr_code
import config
import os
import math

class PreviewWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 400)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background: #F0F2F5;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
    def setPreviewImage(self, image):
        """设置预览图像"""
        if isinstance(image, Image.Image):
            # 转换PIL图像为QPixmap
            qimage = ImageQt(image)
            pixmap = QPixmap.fromImage(qimage)
            
            # 计算预览区域大小
            available_width = self.width() - 40  # 减去padding
            available_height = self.height() - 40
            
            # 保持纸张比例进行缩放
            image_ratio = pixmap.width() / pixmap.height()
            preview_ratio = available_width / available_height
            
            if image_ratio > preview_ratio:
                target_width = available_width
                target_height = int(available_width / image_ratio)
            else:
                target_height = available_height
                target_width = int(available_height * image_ratio)
            
            # 创建预览画布
            preview = QPixmap(target_width + 40, target_height + 40)
            preview.fill(Qt.GlobalColor.transparent)
            
            try:
                painter = QPainter(preview)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                
                # 绘制阴影
                shadow_margin = 20
                for i in range(5):
                    shadow_offset = i * 2
                    shadow_alpha = int(30 - i * 5)
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.setBrush(QColor(0, 0, 0, shadow_alpha))
                    shadow_rect = QRect(
                        shadow_margin + shadow_offset,
                        shadow_margin + shadow_offset,
                        target_width - shadow_offset,
                        target_height - shadow_offset
                    )
                    painter.drawRect(shadow_rect)
                
                # 绘制白色纸张背景
                paper_rect = QRect(shadow_margin, shadow_margin, target_width, target_height)
                painter.setBrush(QColor(255, 255, 255))
                painter.setPen(QPen(QColor(220, 220, 220)))
                painter.drawRect(paper_rect)
                
                # 绘制缩放后的图像
                scaled_image = pixmap.scaled(
                    target_width,
                    target_height,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                painter.drawPixmap(shadow_margin, shadow_margin, scaled_image)
                
            finally:
                painter.end()
            
            # 设置预览图像
            self.setPixmap(preview)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("贝朵亚画纸生成系统 - SparkBoy设计")
        self.setMinimumSize(1200, 800)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 主布局
        layout = QHBoxLayout(main_widget)
        
        # 左侧控制面板
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMaximumWidth(400)
        
        # 学生信息
        info_group = QGroupBox("学生信息")
        info_layout = QVBoxLayout(info_group)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("输入学生姓名")
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("输入学号")
        
        info_layout.addWidget(QLabel("学生姓名:"))
        info_layout.addWidget(self.name_input)
        info_layout.addWidget(QLabel("学号ID:"))
        info_layout.addWidget(self.id_input)
        
        # Logo设置
        logo_group = QGroupBox("Logo设置")
        logo_layout = QVBoxLayout(logo_group)
        
        self.logo_preview = QLabel()
        self.logo_preview.setFixedSize(100, 100)
        self.logo_preview.setStyleSheet("border: 1px solid #ccc")
        self.logo_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logo_btn = QPushButton("选择Logo文件")
        logo_btn.clicked.connect(self.selectLogo)
        
        logo_layout.addWidget(self.logo_preview)
        logo_layout.addWidget(logo_btn)
        
        # 纸张设置
        paper_group = QGroupBox("纸张设置")
        paper_layout = QVBoxLayout(paper_group)
        
        self.paper_group = QButtonGroup(self)
        sizes = [("A4 横向", "A4"), ("A3 横向", "A3"), ("自定义", "custom")]
        
        for text, value in sizes:
            radio = QRadioButton(text)
            self.paper_group.addButton(radio)
            paper_layout.addWidget(radio)
            if value == "A4":
                radio.setChecked(True)
        
        # 自定义尺寸输入
        self.custom_size_widget = QWidget()
        custom_layout = QHBoxLayout(self.custom_size_widget)
        
        self.width_input = QSpinBox()
        self.width_input.setRange(1, 1000)
        self.width_input.setValue(297)
        self.height_input = QSpinBox()
        self.height_input.setRange(1, 1000)
        self.height_input.setValue(210)
        
        custom_layout.addWidget(QLabel("宽(mm):"))
        custom_layout.addWidget(self.width_input)
        custom_layout.addWidget(QLabel("高(mm):"))
        custom_layout.addWidget(self.height_input)
        
        paper_layout.addWidget(self.custom_size_widget)
        self.custom_size_widget.hide()
        
        # 二维码设置
        qr_group = QGroupBox("二维码设置")
        qr_layout = QHBoxLayout(qr_group)
        
        self.qr_size = QSpinBox()
        self.qr_size.setRange(5, 20)
        self.qr_size.setValue(8)
        self.qr_size.setSingleStep(1)
        self.qr_size.setFixedWidth(80)
        self.qr_size.setFixedHeight(32)
        self.qr_size.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        qr_layout.addWidget(QLabel("二维码大小(%):"))
        qr_layout.addWidget(self.qr_size)
        qr_layout.addStretch()
        
        # 打印设置
        print_group = QGroupBox("打印设置")
        print_layout = QHBoxLayout(print_group)
        
        self.copies = QSpinBox()
        self.copies.setRange(1, 100)
        self.copies.setValue(1)
        self.copies.setSingleStep(1)
        self.copies.setFixedWidth(80)
        self.copies.setFixedHeight(32)
        self.copies.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        print_layout.addWidget(QLabel("打印份数:"))
        print_layout.addWidget(self.copies)
        print_layout.addStretch()
        
        # 操作按钮
        button_layout = QHBoxLayout()
        preview_btn = QPushButton("生成预览")
        preview_btn.clicked.connect(self.generatePreview)
        print_btn = QPushButton("打印")
        print_btn.clicked.connect(self.printImage)
        save_btn = QPushButton("保存图片")
        save_btn.clicked.connect(self.saveImage)
        
        button_layout.addWidget(preview_btn)
        button_layout.addWidget(print_btn)
        button_layout.addWidget(save_btn)
        
        # 添加所有组件到左侧面板
        left_layout.addWidget(info_group)
        left_layout.addWidget(logo_group)
        left_layout.addWidget(paper_group)
        left_layout.addWidget(qr_group)
        left_layout.addWidget(print_group)
        left_layout.addLayout(button_layout)
        left_layout.addStretch()
        
        # 右侧预览区域
        preview_group = QGroupBox("预览")
        preview_layout = QVBoxLayout(preview_group)
        preview_group.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                margin-top: 12px;
                padding: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #424242;
                font-weight: bold;
            }
        """)
        
        self.preview = PreviewWidget()
        preview_layout.addWidget(self.preview)
        
        # 添加左右面板到主布局
        layout.addWidget(left_panel)
        layout.addWidget(preview_group, stretch=1)
        
        # 连接信号
        self.paper_group.buttonClicked.connect(self.onPaperSizeChanged)
        self.width_input.valueChanged.connect(self.generatePreview)
        self.height_input.valueChanged.connect(self.generatePreview)
        self.qr_size.valueChanged.connect(self.generatePreview)
        
        # 初始化logo路径
        self.logo_path = config.DEFAULT_LOGO
        self.updateLogoPreview()
        
        # 保存预览图像
        self.preview_image = None
        
    def onPaperSizeChanged(self, button):
        is_custom = button.text() == "自定义"
        self.custom_size_widget.setVisible(is_custom)
        self.generatePreview()
    
    def selectLogo(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "选择Logo文件",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_name:
            self.logo_path = file_name
            self.updateLogoPreview()
            self.generatePreview()
    
    def updateLogoPreview(self):
        try:
            pixmap = QPixmap(self.logo_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    QSize(100, 100),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.logo_preview.setPixmap(scaled_pixmap)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"无法加载Logo: {str(e)}")
    
    def getPaperSize(self):
        checked_button = self.paper_group.checkedButton()
        if checked_button.text() == "A4 横向":
            return (297, 210)
        elif checked_button.text() == "A3 横向":
            return (420, 297)
        else:
            return (self.width_input.value(), self.height_input.value())
    
    def generatePreview(self):
        name = self.name_input.text().strip()
        student_id = self.id_input.text().strip()
        
        if not name or not student_id:
            QMessageBox.warning(self, "提示", "请输入学生姓名和学号！")
            return
            
        try:
            # 生成二维码图片
            paper_size = self.getPaperSize()
            qr_size_percent = self.qr_size.value() / 100
            
            image = generate_qr_code(
                student_id,
                name,
                paper_size_mm=paper_size,
                qr_size_percent=qr_size_percent,
                logo_path=self.logo_path
            )
            
            # 更新预览
            self.preview.setPreviewImage(image)
            self.preview_image = image
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成二维码失败：{str(e)}")
    
    def printImage(self):
        if self.preview_image is None:
            QMessageBox.warning(self, "提示", "请先生成预览！")
            return
        
        try:
            # 保存临时文件
            temp_file = "temp_print.png"
            self.preview_image.save(temp_file)
            
            # 打印文件
            copies = self.copies.value()
            os.startfile(temp_file, "print")
            
            QMessageBox.information(self, "提示", f"已发送{copies}份打印任务到打印机")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"打印失败：{str(e)}")
    
    def saveImage(self):
        if self.preview_image is None:
            QMessageBox.warning(self, "提示", "请先生成预览！")
            return
            
        try:
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "保存图片",
                f"{self.name_input.text()}_{self.id_input.text()}.png",
                "PNG文件 (*.png);;所有文件 (*.*)"
            )
            
            if file_name:
                self.preview_image.save(file_name)
                QMessageBox.information(self, "成功", "图片保存成功！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存图片失败：{str(e)}")

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()