import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QProgressBar, QTextEdit, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from wdf_lib import convert_wdf_to_txt, WDFConversionError

class ConversionThread(QThread):
    progress_updated = pyqtSignal(str, int, int)
    conversion_finished = pyqtSignal()
    error_occurred = pyqtSignal(str, str)

    def __init__(self, input_dir, output_dir):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self._is_running = True

    def run(self):
        try:
            convert_wdf_to_txt(
                self.input_dir,
                self.output_dir,
                progress_callback=self.handle_progress,
                error_callback=self.handle_error
            )
        except WDFConversionError as e:
            self.error_occurred.emit("", str(e))
        self.conversion_finished.emit()

    def handle_progress(self, filename, current, total):
        if self._is_running:
            self.progress_updated.emit(filename, current, total)

    def handle_error(self, filename, error):
        self.error_occurred.emit(filename, error)

    def stop(self):
        self._is_running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WDF文件转换器")
        self.setGeometry(100, 100, 800, 600)
        
        # 初始化UI组件
        self.create_widgets()
        self.setup_layout()
        self.load_preferences()
        
        # 初始化转换线程
        self.conversion_thread = None

    def create_widgets(self):
        # 创建所有UI组件
        self.input_label = QLabel("Input Directory:")
        self.input_edit = QLineEdit()
        self.input_btn = QPushButton("Browse...")
        
        self.output_label = QLabel("Output Directory:")
        self.output_edit = QLineEdit()
        self.output_btn = QPushButton("Browse...")
        
        self.progress_bar = QProgressBar()
        self.log_view = QTextEdit()
        self.start_btn = QPushButton("Start Conversion")
        self.cancel_btn = QPushButton("Cancel")

    def setup_layout(self):
        # 设置布局管理器
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # 输入目录区域
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(self.input_btn)
        
        # 输出目录区域
        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(self.output_btn)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.cancel_btn)
        
        # 组合所有布局
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.log_view)
        main_layout.addLayout(button_layout)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # 连接信号槽
        self.input_btn.clicked.connect(self.select_input_dir)
        self.output_btn.clicked.connect(self.select_output_dir)
        self.start_btn.clicked.connect(self.start_conversion)
        self.cancel_btn.clicked.connect(self.cancel_conversion)

    def select_input_dir(self):
        """处理输入目录选择"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择输入目录")
        if dir_path:
            self.input_edit.setText(dir_path)
            self.save_preferences()

    def select_output_dir(self):
        """处理输出目录选择"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if dir_path:
            self.output_edit.setText(dir_path)
            self.save_preferences()

    def start_conversion(self):
        """开始转换操作"""
        if self.conversion_thread and self.conversion_thread.isRunning():
            return
        
        input_dir = self.input_edit.text()
        output_dir = self.output_edit.text()
        
        if not os.path.isdir(input_dir):
            self.log_view.append("错误：无效的输入目录")
            return
        
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            self.log_view.append(f"错误：{str(e)}")
            return
        
        # 初始化进度条
        self.progress_bar.setValue(0)
        self.log_view.clear()
        
        # 创建并启动转换线程
        self.conversion_thread = ConversionThread(input_dir, output_dir)
        self.conversion_thread.progress_updated.connect(self.update_progress)
        self.conversion_thread.error_occurred.connect(self.handle_error)
        self.conversion_thread.conversion_finished.connect(self.on_conversion_finished)
        self.conversion_thread.start()

    def update_progress(self, filename, current, total):
        """更新进度显示"""
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.log_view.append(f"正在处理：{filename} ({current}/{total})")

    def handle_error(self, filename, error):
        """处理转换错误"""
        error_msg = f"{filename} 发生错误：" if filename else ""
        self.log_view.append(f"❌ {error_msg}{error}")

    def on_conversion_finished(self):
        """转换完成处理"""
        self.log_view.append("转换完成！")
        self.progress_bar.setValue(0)

    def cancel_conversion(self):
        """取消转换操作"""
        if self.conversion_thread and self.conversion_thread.isRunning():
            self.conversion_thread.stop()
            self.log_view.append("用户已取消转换")

    def load_preferences(self):
        """加载用户偏好设置"""
        # 实现从配置文件加载目录路径的逻辑
        pass

    def save_preferences(self):
        """保存用户偏好设置"""
        # 实现保存目录路径到配置文件的逻辑
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
