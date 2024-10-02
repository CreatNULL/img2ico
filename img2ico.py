import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QSpinBox, QLineEdit
)
from PySide6.QtGui import QIcon, QFont
from PIL import Image, ImageDraw

class ImageConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Converter To Ico")
        self.setGeometry(100, 100, 500, 400)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "icon.ico")))  # 使用相对路径设置窗口图标

        # 设置主布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 设置样式
        self.setStyleSheet(""" 
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
                margin: 10px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QSpinBox {
                font-size: 14px;
                margin: 10px;
            }
            QLineEdit {
                padding: 10px;
                font-size: 14px;
            }
            """)

        # 添加控件
        self.label = QLabel("请选择 JPG 或 PNG 文件进行转换")
        self.layout.addWidget(self.label)

        self.button_select = QPushButton("选择文件")
        self.button_select.clicked.connect(self.select_file)
        self.layout.addWidget(self.button_select)

        self.size_label = QLabel("指定输出大小 (宽 x 高):")
        self.layout.addWidget(self.size_label)

        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(1, 512)
        self.width_spinbox.setValue(64)
        self.layout.addWidget(self.width_spinbox)

        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(1, 512)
        self.height_spinbox.setValue(64)
        self.layout.addWidget(self.height_spinbox)

        self.corner_radius_label = QLabel("指定圆角大小:")
        self.layout.addWidget(self.corner_radius_label)

        self.corner_radius_spinbox = QSpinBox()
        self.corner_radius_spinbox.setRange(0, 100)
        self.corner_radius_spinbox.setValue(10)
        self.layout.addWidget(self.corner_radius_spinbox)

        # 添加选择输出文件夹按钮
        self.output_folder_label = QLabel("选择输出文件夹 (默认当前目录):")
        self.layout.addWidget(self.output_folder_label)

        self.output_folder_input = QLineEdit()
        self.layout.addWidget(self.output_folder_input)

        self.button_select_folder = QPushButton("选择文件夹")
        self.button_select_folder.clicked.connect(self.select_folder)
        self.layout.addWidget(self.button_select_folder)

        self.button_convert = QPushButton("转换为 ICO")
        self.button_convert.clicked.connect(self.convert_to_ico)
        self.layout.addWidget(self.button_convert)

        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        # 设置字体
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图像文件", "", "Images (*.jpg *.png)", options=options)
        if file_path:
            self.selected_file = file_path
            self.label.setText(f"已选择: {os.path.basename(file_path)}")

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择输出文件夹", "", QFileDialog.Options())
        if folder_path:
            self.output_folder_input.setText(folder_path)

    def convert_to_ico(self):
        if hasattr(self, 'selected_file'):
            try:
                img = Image.open(self.selected_file)

                # 调整图像大小
                width = self.width_spinbox.value()
                height = self.height_spinbox.value()
                img = img.resize((width, height), Image.LANCZOS)

                # 添加圆角
                corner_radius = self.corner_radius_spinbox.value()
                if corner_radius > 0:
                    mask = Image.new('L', (width, height), 0)
                    draw = ImageDraw.Draw(mask)
                    draw.rounded_rectangle((0, 0, width, height), radius=corner_radius, fill=255)
                    img.putalpha(mask)

                # 获取输出路径
                output_folder = self.output_folder_input.text().strip()
                if not output_folder:
                    output_folder = os.getcwd()  # 默认输出到当前工作目录

                # 确保输出路径是有效的
                output_path = os.path.join(output_folder, os.path.splitext(os.path.basename(self.selected_file))[0] + ".ico")

                img.save(output_path, format='ICO', sizes=[(width, height)])

                self.status_label.setText(f"成功转换为: {output_path}")
            except Exception as e:
                self.status_label.setText(f"错误: {str(e)}")
        else:
            self.status_label.setText("请先选择文件。")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageConverter()
    window.show()
    sys.exit(app.exec())
