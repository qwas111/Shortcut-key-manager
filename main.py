import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont, QIcon
from frontend import ShortcutManagerFrontend  # 添加这行导入语句

def resource_path(relative_path):
    """获取资源的绝对路径，适用于开发环境和打包后环境"""
    if hasattr(sys, '_MEIPASS'):
        # 打包后的临时目录
        return os.path.join(sys._MEIPASS, relative_path)
    # 开发环境的当前目录
    return os.path.join(os.path.abspath("."), relative_path)

def load_custom_font(app):
    """加载自定义字体"""
    try:
        # 方法1：从文件加载字体
        font_path = "MiSans-Light.ttf"  # 替换为您的字体文件路径
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                if font_families:
                    custom_font = QFont(font_families[0])
                    app.setFont(custom_font)
                    print(f"已加载自定义字体: {font_families[0]}")
                    return True
        
        # 方法2：使用系统字体但自定义设置
        custom_font = QFont("Microsoft YaHei UI", 10)  # 使用微软雅黑
        # 或者使用其他字体：
        # custom_font = QFont("Segoe UI", 9)
        # custom_font = QFont("Arial", 9)
        app.setFont(custom_font)
        return True
        
    except Exception as e:
        print(f"加载字体失败: {e}")
        return False

def set_app_icon(app):
    """设置应用程序图标"""
    try:
        icon_path = resource_path("icon.ico")
        if os.path.exists(icon_path):
            # 设置应用程序图标
            app_icon = QIcon(icon_path)
            app.setWindowIcon(app_icon)
            print(f"已设置应用程序图标: {icon_path}")
            return True
        else:
            print(f"图标文件不存在: {icon_path}")
            return False
    except Exception as e:
        print(f"设置应用程序图标失败: {e}")
        return False

def main():
    # 确保程序只运行一个实例
    try:
        from win32event import CreateMutex
        from win32api import GetLastError
        from winerror import ERROR_ALREADY_EXISTS
        
        mutex = CreateMutex(None, False, "ShortcutManagerMutex")
        if GetLastError() == ERROR_ALREADY_EXISTS:
            sys.exit(0)
    except ImportError:
        pass  # 如果pywin32不可用，跳过单实例检查

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # 设置应用程序图标（这会影响任务栏图标）
    set_app_icon(app)
    
    # 加载自定义字体
    load_custom_font(app)
    
    # 创建前端界面
    window = ShortcutManagerFrontend()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()