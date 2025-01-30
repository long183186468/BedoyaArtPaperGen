# 贝朵亚画纸生成系统

一个用于生成带有Logo、二维码和学生信息的画纸标签的桌面应用程序。

## 功能特点

- 支持输入学生姓名和学号
- 自动生成包含学生信息的二维码
- 支持自定义Logo
- 支持多种纸张尺寸（A4、A3、自定义）
- 实时预览生成效果
- 支持批量打印
- 可保存为图片文件

## 技术栈

- Python 3.10
- PyQt6（GUI界面）
- qrcode（二维码生成）
- Pillow（图像处理）

## 安装说明

### 方式一：直接运行可执行文件

1. 从 [Releases](../../releases) 页面下载最新版本的可执行文件
2. 双击运行 `贝朵亚画纸生成系统.exe`

### 方式二：从源码运行

1. 克隆仓库
```bash
git clone [repository-url]
cd [repository-name]
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行程序
```bash
python main.py
```

## 使用说明

1. 输入学生信息
   - 填写学生姓名
   - 填写学号

2. 选择纸张尺寸
   - A4 横向（297×210mm）
   - A3 横向（420×297mm）
   - 自定义尺寸

3. 调整二维码大小
   - 使用百分比控制（5%-20%）

4. 生成预览
   - 点击"生成预览"按钮查看效果

5. 打印或保存
   - 点击"打印"按钮直接打印
   - 点击"保存图片"保存为PNG文件

## 开发说明

### 项目结构
```
├── main.py            # 主程序入口
├── qr_generator.py    # 二维码生成模块
├── config.py          # 配置文件
├── logo.png           # 默认Logo
├── requirements.txt   # 依赖列表
└── README.md         # 项目说明
```

### 打包说明

使用 PyInstaller 打包：
```bash
python build.py
```

## 许可证

Copyright (C) 2024 SparkBoy. 保留所有权利。

## 联系方式

- 开发者：SparkBoy
- 邮箱：183186468@qq.com
- QQ：183186468 