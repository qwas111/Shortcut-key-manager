import json
import os
import sys
import asyncio
import threading
import winreg
import subprocess
from PyQt5.QtCore import QObject, pyqtSignal

class ShortcutBackend(QObject):
    shortcutTriggered = pyqtSignal(str)
    statusUpdate = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.configFile = "shortcuts.json"
        self.shortcuts = {}
        self.isRunning = False
        self.loop = None
        self.thread = None
        self.loadConfig()

    def loadConfig(self):
        #加载配置文件#
        try:
            if os.path.exists(self.configFile):
                with open(self.configFile, 'r', encoding='utf-8') as f:
                    self.shortcuts = json.load(f)
            self.statusUpdate.emit(f"已加载 {len(self.shortcuts)} 个快捷键")
        except Exception as e:
            self.statusUpdate.emit(f"加载配置失败: {str(e)}")
            self.shortcuts = {}

    def saveConfig(self):
        #保存配置到文件#
        try:
            with open(self.configFile, 'w', encoding='utf-8') as f:
                json.dump(self.shortcuts, f, ensure_ascii=False, indent=2)
            self.statusUpdate.emit("配置保存成功")
            return True
        except Exception as e:
            self.statusUpdate.emit(f"保存配置失败: {str(e)}")
            return False

    def addShortcut(self, shortcut, command, description=""):
        #添加快捷键#
        # 标准化快捷键格式
        shortcut = self.normalize_shortcut(shortcut)
        
        self.shortcuts[shortcut] = {
            "command": command,
            "description": description
        }
        self.saveConfig()
        self.statusUpdate.emit(f"添加快捷键: {shortcut}")
        # 重新注册快捷键
        if self.isRunning:
            self.restartListener()

    def normalize_shortcut(self, shortcut):
        #标准化快捷键格式#
        parts = shortcut.split('+')
        normalized_parts = []
        
        for part in parts:
            part_lower = part.lower().strip()
            if part_lower in ['ctrl', 'control']:
                normalized_parts.append('ctrl')
            elif part_lower in ['alt']:
                normalized_parts.append('alt')
            elif part_lower in ['shift']:
                normalized_parts.append('shift')
            elif part_lower in ['win', 'windows', 'super']:
                normalized_parts.append('windows')
            else:
                # 保持其他键的原样
                normalized_parts.append(part)
        
        return '+'.join(normalized_parts)

    def removeShortcut(self, shortcut):
        #删除快捷键#
        if shortcut in self.shortcuts:
            del self.shortcuts[shortcut]
            self.saveConfig()
            self.statusUpdate.emit(f"删除快捷键: {shortcut}")
            # 重新注册快捷键
            if self.isRunning:
                self.restartListener()
            return True
        return False

    def executeCommand(self, command):
        #执行命令#
        try:
            if command.startswith("http://") or command.startswith("https://"):
                os.startfile(command)
            else:
                # 使用shell执行命令，但避免弹出命令行窗口
                subprocess.Popen(command, shell=True, 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            self.statusUpdate.emit(f"执行命令: {command}")
        except Exception as e:
            self.statusUpdate.emit(f"执行失败: {str(e)}")

    def setStartup(self, enable):
        #设置开机自启动#
        try:
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
                if enable:
                    exe_path = os.path.abspath(sys.argv[0])
                    winreg.SetValueEx(reg_key, "ShortcutManager", 0, winreg.REG_SZ, exe_path)
                    self.statusUpdate.emit("已启用开机自启动")
                else:
                    try:
                        winreg.DeleteValue(reg_key, "ShortcutManager")
                        self.statusUpdate.emit("已禁用开机自启动")
                    except FileNotFoundError:
                        self.statusUpdate.emit("开机自启动未设置")
        except Exception as e:
            self.statusUpdate.emit(f"设置自启动失败: {str(e)}")

    def checkStartup(self):
        #检查是否设置了开机自启动#
        try:
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_READ) as reg_key:
                try:
                    winreg.QueryValueEx(reg_key, "ShortcutManager")
                    return True
                except FileNotFoundError:
                    return False
        except Exception:
            return False

    async def shortcutListener(self):
        #异步快捷键监听器#
        self.statusUpdate.emit("快捷键监听器已启动")
        try:
            import keyboard
            # 清除所有已注册的快捷键
            keyboard.unhook_all()
            
            # 注册新的快捷键
            for shortcut in self.shortcuts.keys():
                # 确保快捷键格式正确
                normalized_shortcut = self.normalize_shortcut(shortcut)
                try:
                    keyboard.add_hotkey(normalized_shortcut, 
                                      lambda s=shortcut: self.handleShortcut(s))
                    self.statusUpdate.emit(f"注册快捷键: {shortcut}")
                except Exception as e:
                    self.statusUpdate.emit(f"注册快捷键失败 {shortcut}: {str(e)}")
            
            # 保持监听
            while self.isRunning:
                await asyncio.sleep(0.1)
                
        except ImportError:
            self.statusUpdate.emit("请安装keyboard库: pip install keyboard")
        except Exception as e:
            self.statusUpdate.emit(f"快捷键监听错误: {str(e)}")

    def handleShortcut(self, shortcut):
        #处理快捷键触发#
        if shortcut in self.shortcuts:
            command = self.shortcuts[shortcut]["command"]
            self.shortcutTriggered.emit(f"快捷键 {shortcut} 触发: {command}")
            self.executeCommand(command)

    def startListener(self):
        #启动监听线程#
        if not self.isRunning:
            self.isRunning = True
            self.thread = threading.Thread(target=self.runAsync)
            self.thread.daemon = True
            self.thread.start()

    def runAsync(self):
        #运行异步事件循环#
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(self.shortcutListener())
        except Exception as e:
            self.statusUpdate.emit(f"监听器错误: {str(e)}")

    def stopListener(self):
        #停止监听#
        self.isRunning = False
        try:
            import keyboard
            keyboard.unhook_all()
        except ImportError:
            pass
        
        if self.loop and self.loop.is_running():
            self.loop.stop()

    def restartListener(self):
        #重启监听器以应用新的快捷键#
        self.stopListener()
        # 给一点时间让监听器完全停止
        import time
        time.sleep(0.5)
        self.startListener()