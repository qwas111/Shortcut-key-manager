import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, 
    QLabel, QMessageBox, QFormLayout, QCheckBox, QHeaderView,
    QAction, QMenu, QDialog, QSystemTrayIcon, QStyle, QFrame)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import (QIcon, QColor, QFont, QPainter, 
                         QLinearGradient, QPen)

import warnings
warnings.filterwarnings('ignore', message='sipPyTypeDict() is deprecated')

# 导入后端
try:
    from backend import ShortcutBackend
except ImportError as e:
    print(f"导入后端模块失败: {e}")
    ShortcutBackend = None
    
def resource_path(relative_path):
    #获取资源的绝对路径，适用于开发环境和打包后环境"""
    if hasattr(sys, '_MEIPASS'):
        # 打包后的临时目录
        return os.path.join(sys._MEIPASS, relative_path)
    # 开发环境的当前目录
    return os.path.join(os.path.abspath("."), relative_path)

class TechButton(QPushButton):
    #科技风格按钮"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(35)
        self.setCursor(Qt.PointingHandCursor)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 创建渐变
        gradient = QLinearGradient(0, 0, 0, self.height())
        if self.isDown():
            gradient.setColorAt(0, QColor(0, 150, 255))
            gradient.setColorAt(1, QColor(0, 100, 200))
        elif self.underMouse():
            gradient.setColorAt(0, QColor(0, 180, 255))
            gradient.setColorAt(1, QColor(0, 120, 220))
        else:
            gradient.setColorAt(0, QColor(0, 120, 220))
            gradient.setColorAt(1, QColor(0, 80, 180))
        
        # 绘制圆角矩形背景
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 5, 5)
        
        # 绘制边框
        painter.setPen(QPen(QColor(100, 180, 255), 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(0, 0, self.width()-1, self.height()-1, 5, 5)
        
        # 绘制文字
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

class TechLineEdit(QLineEdit):
    #科技风格输入框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(35)
        self.setStyleSheet("""
            QLineEdit {
                background-color: rgba(30, 30, 40, 200);
                border: 2px solid rgba(100, 150, 255, 100);
                border-radius: 8px;
                padding: 5px 10px;
                color: #ffffff;
                font-size: 12px;
                selection-background-color: rgba(0, 150, 255, 150);
            }
            QLineEdit:focus {
                border: 2px solid rgba(0, 150, 255, 200);
                background-color: rgba(35, 35, 45, 200);
            }
            QLineEdit:hover {
                border: 2px solid rgba(100, 180, 255, 150);
            }
        """)

class TechTableWidget(QTableWidget):
    #科技风格表格"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QTableWidget {
                background-color: rgba(25, 25, 35, 180);
                border: 1px solid rgba(100, 150, 255, 80);
                border-radius: 8px;
                gridline-color: rgba(100, 150, 255, 50);
                color: #e0e0e0;
                font-size: 11px;
                outline: none;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(100, 150, 255, 30);
            }
            QTableWidget::item:selected {
                background-color: rgba(0, 150, 255, 150);
                color: white;
            }
            QTableWidget::item:hover {
                background-color: rgba(100, 150, 255, 50);
            }
            QHeaderView::section {
                background-color: rgba(20, 20, 30, 220);
                color: #00a8ff;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 11px;
                border-bottom: 2px solid rgba(0, 168, 255, 100);
            }
            QScrollBar:vertical {
                background-color: rgba(30, 30, 40, 150);
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(100, 150, 255, 120);
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(100, 180, 255, 180);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

class TechCheckBox(QCheckBox):
    #科技风格复选框"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QCheckBox {
                color: #b0b0b0;
                font-size: 11px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid rgba(100, 150, 255, 150);
                border-radius: 3px;
                background-color: rgba(30, 30, 40, 200);
            }
            QCheckBox::indicator:hover {
                border: 2px solid rgba(100, 180, 255, 200);
            }
            QCheckBox::indicator:checked {
                background-color: rgba(0, 150, 255, 200);
                border: 2px solid rgba(0, 150, 255, 200);
            }
            QCheckBox::indicator:checked:hover {
                background-color: rgba(0, 180, 255, 200);
                border: 2px solid rgba(0, 180, 255, 200);
            }
        """)

class AddShortcutDialog(QDialog):
    shortcutCaptured = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.is_capturing = False
        self.captured_keys = set()
        self.modifier_keys = {'ctrl', 'alt', 'shift', 'windows'}
        self.hook = None

    def setupUi(self):
        #设置对话框的UI界面"""
        self.setWindowTitle("添加快捷键")
        self.setFixedSize(450, 300)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #1a1a2a, stop: 0.5 #16213e, stop: 1 #0f3460);
                border: 1px solid rgba(100, 150, 255, 100);
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("添加快捷键")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #00a8ff;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background-color: rgba(20, 20, 30, 150);
                border-radius: 8px;
                border: 1px solid rgba(100, 150, 255, 80);
            }
        """)
        layout.addWidget(title_label)
        
        # 状态标签
        self.statusLabel = QLabel("点击'捕获快捷键'按钮开始捕获组合键")
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setStyleSheet("""
            QLabel {
                color: #00d4ff;
                background-color: rgba(20, 25, 40, 180);
                padding: 12px;
                border-radius: 8px;
                border: 1px solid rgba(0, 212, 255, 80);
                font-size: 12px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.statusLabel)
        
        # 表单布局
        layout_form = QFormLayout()
        layout_form.setLabelAlignment(Qt.AlignRight)
        layout_form.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout_form.setHorizontalSpacing(15)
        layout_form.setVerticalSpacing(12)
        
        # 快捷键输入
        shortcut_label = QLabel("快捷键:")
        shortcut_label.setStyleSheet("color: #b0b0ff; font-weight: bold; font-size: 12px;")
        self.shortcutInput = TechLineEdit()
        self.shortcutInput.setPlaceholderText("捕获后自动填充快捷键")
        self.shortcutInput.setReadOnly(True)
        layout_form.addRow(shortcut_label, self.shortcutInput)
        
        # 命令输入
        command_label = QLabel("命令:")
        command_label.setStyleSheet("color: #b0b0ff; font-weight: bold; font-size: 12px;")
        self.commandInput = TechLineEdit()
        self.commandInput.setPlaceholderText("程序路径或URL")
        layout_form.addRow(command_label, self.commandInput)
        
        # 描述输入
        description_label = QLabel("描述:")
        description_label.setStyleSheet("color: #b0b0ff; font-weight: bold; font-size: 12px;")
        self.descriptionInput = TechLineEdit()
        self.descriptionInput.setPlaceholderText("可选描述")
        layout_form.addRow(description_label, self.descriptionInput)

        layout.addLayout(layout_form)
        layout.addSpacing(10)

        # 按钮布局
        buttonLayout = QHBoxLayout()
        self.testButton = TechButton("捕获快捷键")
        self.testButton.clicked.connect(self.capture_shortcut_from_user)
        buttonLayout.addWidget(self.testButton)
        
        self.saveButton = TechButton("保存快捷键")
        self.saveButton.clicked.connect(self.accept)
        
        self.cancelButton = TechButton("取消")
        self.cancelButton.clicked.connect(self.reject)
        
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.cancelButton)

        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        
        # 连接信号
        self.shortcutCaptured.connect(self.on_shortcut_captured)

    def on_shortcut_captured(self, shortcut):
        #处理捕获到的快捷键"""
        self.shortcutInput.setText(shortcut)
        self.statusLabel.setText(f"已捕获快捷键: {shortcut}")

    def capture_shortcut_from_user(self):
        #从用户键盘输入捕获快捷键组合"""
        if not self.is_capturing:
            self.start_capturing()
        else:
            self.stop_capturing()

    def start_capturing(self):
        #开始捕获快捷键"""
        try:
            import keyboard
        except ImportError:
            self.show_message("错误", "请安装keyboard库: pip install keyboard", "警告")
            return
            
        self.is_capturing = True
        self.captured_keys.clear()
        self.statusLabel.setText("请按下快捷键组合... (按ESC取消)")
        self.statusLabel.setStyleSheet("""
            QLabel {
                color: #ffaa00;
                background-color: rgba(40, 30, 20, 180);
                padding: 12px;
                border-radius: 8px;
                border: 1px solid rgba(255, 170, 0, 100);
                font-size: 12px;
                font-weight: bold;
            }
        """)
        self.testButton.setText("停止捕获")
        self.shortcutInput.setText("")
        self.shortcutInput.setPlaceholderText("正在捕获...")
        
        # 设置键盘钩子
        self.hook = keyboard.on_press(self.on_key_press)
        
    def stop_capturing(self):
        #停止捕获快捷键"""
        self.is_capturing = False
        if self.hook:
            try:
                import keyboard
                keyboard.unhook(self.hook)
            except Exception:
                pass
            self.hook = None
            
        self.statusLabel.setText("点击'捕获快捷键'按钮开始捕获组合键")
        self.statusLabel.setStyleSheet("""
            QLabel {
                color: #00d4ff;
                background-color: rgba(20, 25, 40, 180);
                padding: 12px;
                border-radius: 8px;
                border: 1px solid rgba(0, 212, 255, 80);
                font-size: 12px;
                font-weight: bold;
            }
        """)
        self.testButton.setText("捕获快捷键")
        self.shortcutInput.setPlaceholderText("测试后自动填充快捷键")

    def on_key_press(self, event):
        #键盘按下事件处理"""
        if not self.is_capturing:
            return
            
        try:
            import keyboard
            
            # 获取标准化的键名
            key_name = event.name.lower()
            
            # 处理特殊键名
            if key_name == 'esc':
                # ESC键取消捕获
                self.stop_capturing()
                self.statusLabel.setText("捕获已取消")
                return
                
            # 标准化修饰键名称
            if key_name in ['left ctrl', 'right ctrl', 'ctrl']:
                key_name = 'ctrl'
            elif key_name in ['left alt', 'right alt', 'alt']:
                key_name = 'alt'
            elif key_name in ['left shift', 'right shift', 'shift']:
                key_name = 'shift'
            elif key_name in ['left windows', 'right windows', 'windows']:
                key_name = 'windows'
            elif key_name == 'space':
                key_name = 'space'
            elif len(key_name) == 1 and key_name.isalpha():
                key_name = key_name.upper()
            
            # 添加到捕获的键集合
            if key_name not in self.captured_keys:
                self.captured_keys.add(key_name)
                
            # 生成快捷键字符串
            modifiers = []
            regular_keys = []
            
            for key in self.captured_keys:
                if key in self.modifier_keys:
                    modifiers.append(key)
                else:
                    regular_keys.append(key)
            
            # 排序修饰键（保持一致性）
            modifier_order = ['ctrl', 'alt', 'shift', 'windows']
            modifiers.sort(key=lambda x: modifier_order.index(x) if x in modifier_order else 99)
            
            # 组合快捷键
            if modifiers and regular_keys:
                shortcut = '+'.join(modifiers + [regular_keys[0]])
                # 通过信号发送到主线程
                self.shortcutCaptured.emit(shortcut)
                # 延迟一点时间再停止捕获，确保UI已更新
                QTimer.singleShot(100, self.stop_capturing)
                
        except Exception as e:
            print(f"按键捕获错误: {e}")

    def closeEvent(self, event):
        #对话框关闭事件"""
        self.stop_capturing()
        super().closeEvent(event)

    def show_message(self, title, message, icon="信息"):
        #显示消息提示窗口"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        # 设置消息框样式
        msg_box.setStyleSheet("""
            QMessageBox {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #1a1a2a, stop: 0.5 #16213e, stop: 1 #0f3460);
                border: 1px solid rgba(100, 150, 255, 100);
                border-radius: 10px;
            }
            QMessageBox QLabel {
                color: #e0e0e0;
                font-size: 12px;
            }
            QMessageBox QPushButton {
                background-color: rgba(0, 120, 220, 180);
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: rgba(0, 150, 255, 200);
            }
        """)
        
        if icon == "信息":
            msg_box.setIcon(QMessageBox.Information)
        elif icon == "警告":
            msg_box.setIcon(QMessageBox.Warning)
        else:
            msg_box.setIcon(QMessageBox.Information)
            
        msg_box.exec_()
    
    def getData(self):
        return {
            "shortcut": self.shortcutInput.text().strip(),
            "command": self.commandInput.text().strip(),
            "description": self.descriptionInput.text().strip()
        }


class ShortcutManagerFrontend(QMainWindow):
    def __init__(self):
        super().__init__()
        if ShortcutBackend is None:
            QMessageBox.critical(self, "错误", "无法初始化后端模块")
            sys.exit(1)
            
        self.backend = ShortcutBackend()
        self.setup_ui()
        self.setup_backend_connections()
        self.setup_tray_icon()
        self.load_settings()
        
    def setup_backend_connections(self):
        #设置后端信号连接#
        self.backend.statusUpdate.connect(self.update_status)
        self.backend.shortcutTriggered.connect(self.on_shortcut_triggered)
        
    def update_status(self, message):
        #更新状态栏#
        self.statusLabel.setText(message)
        
    def on_shortcut_triggered(self, message):
        #处理快捷键触发#
        self.statusLabel.setText(message)
        
    def show_message(self, title, message, icon="信息"):
        #显示消息提示窗口#
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        # 设置消息框样式
        msg_box.setStyleSheet("""
            QMessageBox {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #1a1a2a, stop: 0.5 #16213e, stop: 1 #0f3460);
                border: 1px solid rgba(100, 150, 255, 100);
                border-radius: 10px;
            }
            QMessageBox QLabel {
                color: #e0e0e0;
                font-size: 12px;
            }
            QMessageBox QPushButton {
                background-color: rgba(0, 120, 220, 180);
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: rgba(0, 150, 255, 200);
            }
        """)
        
        if icon == "信息":
            msg_box.setIcon(QMessageBox.Information)
        elif icon == "警告":
            msg_box.setIcon(QMessageBox.Warning)
        else:
            msg_box.setIcon(QMessageBox.Information)
            
        msg_box.exec_()
        
    def setup_ui(self):
        #设置主窗口界面"""
        self.setWindowTitle("快捷键管理软件")
        self.setFixedSize(900, 650)
        
        # 设置主窗口图标
        try:
            icon_path = resource_path("icon.ico")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            print(f"设置窗口图标失败: {e}")
        
        self.set_dark_tech_theme()
        
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 标题标签
        self.titleLabel = QLabel("快捷键管理器")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("""
            QLabel {
                color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00a8ff, stop:0.5 #00d4ff, stop:1 #00a8ff);
                background-color: rgba(20, 20, 30, 180);
                padding: 15px;
                border-radius: 10px;
                border: 2px solid rgba(0, 168, 255, 100);
            }
        """)
        layout.addWidget(self.titleLabel)
        
        # 快捷键表格
        self.tableWidget = TechTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["快捷键", "命令", "描述"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tableWidget)
        
        # 按钮区域
        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(10)
        
        self.add_shortcut = TechButton("添加快捷键")
        self.add_shortcut.clicked.connect(self.add_shortcut_dialog)
        
        self.edit_shortcut = TechButton("编辑")
        self.edit_shortcut.clicked.connect(self.edit_selected_shortcut)
        
        self.remove_shortcut = TechButton("删除")
        self.remove_shortcut.clicked.connect(self.remove_selected_shortcut)
        
        self.startup_checkbox = TechCheckBox("开机自启动")
        self.startup_checkbox.stateChanged.connect(self.toggle_startup)
        
        buttonLayout.addWidget(self.add_shortcut)
        buttonLayout.addWidget(self.edit_shortcut)
        buttonLayout.addWidget(self.remove_shortcut)
        buttonLayout.addWidget(self.startup_checkbox)
        buttonLayout.addStretch()
        
        layout.addLayout(buttonLayout)
        
        # 状态栏
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(20, 25, 40, 180);
                border: 1px solid rgba(100, 150, 255, 80);
                border-radius: 8px;
                padding: 5px;
            }
        """)
        status_layout = QHBoxLayout(status_frame)
        self.statusLabel = QLabel("系统就绪")
        self.statusLabel.setStyleSheet("color: #00d4ff; font-size: 11px; font-weight: bold;")
        status_layout.addWidget(self.statusLabel)
        layout.addWidget(status_frame)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.refresh_table()

    def setup_tray_icon(self):
        #"设置系统托盘图标"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
            
        self.tray_icon = QSystemTrayIcon(self)
        
        # 使用自定义图标而不是系统图标
        try:
            # 尝试加载自定义图标
            icon_path = resource_path("icon.ico")
            if os.path.exists(icon_path):
                self.tray_icon.setIcon(QIcon(icon_path))
            else:
                # 如果图标文件不存在，使用系统图标作为备用
                self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        except Exception as e:
            print(f"加载托盘图标失败: {e}")
            # 备用方案：使用系统图标
            self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        # 创建托盘菜单
        tray_menu = QMenu()
        tray_menu.setStyleSheet("""
            QMenu {
                background-color: rgba(30, 30, 45, 220);
                border: 1px solid rgba(100, 150, 255, 100);
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                color: #e0e0e0;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: rgba(0, 150, 255, 150);
            }
        """)
        
        show_action = QAction("显示", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        hide_action = QAction("隐藏", self)
        hide_action.triggered.connect(self.hide)
        tray_menu.addAction(hide_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
        
    def tray_icon_activated(self, reason):
        #托盘图标激活处理"""
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.activateWindow()
                
    def closeEvent(self, event):
        #关闭事件处理"""
        if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            self.quit_application()
            
    def quit_application(self):
        #退出应用程序"""
        self.backend.stopListener()
        QApplication.quit()

    def set_dark_tech_theme(self):
        #设置深色科技主题"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #0c0c1a, stop: 0.3 #1a1a2a, stop: 0.7 #16213e, stop: 1 #0f3460);
                color: #e0e0e0;
            }
            QWidget {
                background: transparent;
            }
        """)
    
    def add_shortcut_dialog(self):
        #显示添加快捷键对话框"""
        dialog = AddShortcutDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.getData()
            if all([data["shortcut"], data["command"]]):
                # 使用后端添加快捷键
                self.backend.addShortcut(data["shortcut"], data["command"], data["description"])
                self.refresh_table()
            else:
                self.show_message("错误", "请填写完整的快捷键和命令", "警告")
    
    def refresh_table(self):
        #刷新表格显示"""
        self.tableWidget.setRowCount(len(self.backend.shortcuts))
        for row, (shortcut, data) in enumerate(self.backend.shortcuts.items()):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(shortcut))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(data["command"]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(data.get("description", "")))
    
    def remove_selected_shortcut(self):
        #删除选中的快捷键"""
        current_row = self.tableWidget.currentRow()
        if current_row >= 0:
            shortcut = self.tableWidget.item(current_row, 0).text()
            reply = QMessageBox.question(
                self, "确认删除",
                f"确定要删除快捷键 '{shortcut}' 吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.backend.removeShortcut(shortcut)
                self.refresh_table()
    
    def edit_selected_shortcut(self):
        #编辑选中的快捷键"""
        current_row = self.tableWidget.currentRow()
        if current_row < 0:
            self.show_message("错误", "请选择一个快捷键进行编辑", "警告")
            return
        shortcut = self.tableWidget.item(current_row, 0).text()
        data = self.backend.shortcuts.get(shortcut)
        if not data:
            self.show_message("错误", "未找到快捷键数据", "警告")
            return
        dialog = AddShortcutDialog(self)
        dialog.shortcutInput.setText(shortcut)
        dialog.commandInput.setText(data["command"])
        dialog.descriptionInput.setText(data.get("description", ""))
        dialog.statusLabel.setText("编辑现有快捷键")
        if dialog.exec_() == QDialog.Accepted:
            new_data = dialog.getData()
            if new_data["shortcut"] and new_data["command"]:
                # 先删除旧的，再添加新的
                self.backend.removeShortcut(shortcut)
                self.backend.addShortcut(new_data["shortcut"], new_data["command"], new_data["description"])
                self.refresh_table()
            else:
                self.show_message("错误", "请填写完整的快捷键和命令", "警告")
    
    def toggle_startup(self, state):
        #切换开机自启动"""
        self.backend.setStartup(state == Qt.Checked)
        
    def load_settings(self):
        #加载设置"""
        # 检查自启动状态
        if self.backend.checkStartup():
            self.startup_checkbox.setChecked(True)
        
        # 启动快捷键监听
        self.backend.startListener()