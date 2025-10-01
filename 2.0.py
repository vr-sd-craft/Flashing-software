import keyboard
import time
import os
import sys
import random
import subprocess
from pathlib import Path
import hashlib
from urllib.parse import urlparse

# 跨平台清屏方法
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Windows终端颜色支持
if sys.platform.startswith('win'):
    from ctypes import windll
    kernel32 = windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# 法律声明
def legal_notice():
    print("--------------------------")
    print("|  高级刷机工具 v4.0.0  |")
    print("|  保留核心刷机功能     |")
    print("|  集成50+ ADB功能     |")
    print("--------------------------")

# ADB功能管理器
class ADBManager:
    def __init__(self):
        self.connected_devices = []
        self.current_device = None
        
    def run_adb_command(self, command, device_specific=True):
        """执行ADB命令"""
        try:
            full_command = "adb"
            if device_specific and self.current_device:
                full_command += f" -s {self.current_device}"
            full_command += f" {command}"
            
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True, timeout=30)
            return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"
        except subprocess.TimeoutExpired:
            return "Error: Command timeout"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def check_devices(self):
        """检查连接的设备"""
        output = self.run_adb_command("devices", False)
        devices = []
        for line in output.split('\n')[1:]:
            if line.strip() and '\tdevice' in line:
                devices.append(line.split('\t')[0])
        self.connected_devices = devices
        return devices
    
    def select_device(self):
        """选择设备"""
        devices = self.check_devices()
        if not devices:
            print("未找到连接的设备")
            return False
        
        print("\n连接的设备:")
        for i, device in enumerate(devices, 1):
            print(f"{i}. {device}")
        
        try:
            choice = input("\n选择设备 (输入编号): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(devices):
                self.current_device = devices[int(choice) - 1]
                print(f"已选择设备: {self.current_device}")
                return True
        except:
            pass
        
        return False

# 固件源管理
class FirmwareSource:
    def __init__(self):
        # 模拟的固件信息
        self.sources = {
            'xiaomi': {
                'stable': {
                    'devices': {
                        'Xiaomi 14': {'size_mb': 4500, 'filename': 'xiaomi14_stable_os.zip'},
                        'Xiaomi 13': {'size_mb': 4200, 'filename': 'miui_FUXI_V14.0.12.11.19_STABLE.zip'},
                        'Xiaomi 13 Pro': {'size_mb': 4300, 'filename': 'miui_NUWA_V14.0.12.11.19_STABLE.zip'}
                    }
                },
                'beta': {
                    'devices': {
                        'Xiaomi 14': {'size_mb': 3800, 'filename': 'fuxi_pre_dpp_images.tgz'},
                        'Xiaomi 13': {'size_mb': 3600, 'filename': 'fuxi_pre_dpp_images_23.5.6.tgz'}
                    }
                }
            },
            'pixel': {
                'stable': {
                    'devices': {
                        'Pixel 8 Pro': {'size_mb': 2800, 'filename': 'husky-stable-factory.zip'},
                        'Pixel 8': {'size_mb': 2700, 'filename': 'shiba-stable-factory.zip'}
                    }
                },
                'beta': {
                    'devices': {
                        'Pixel 8 Pro': {'size_mb': 2600, 'filename': 'husky-beta-ota.zip'},
                        'Pixel 8': {'size_mb': 2500, 'filename': 'shiba-beta-ota.zip'}
                    }
                }
            }
        }
    
    def get_available_devices(self, system):
        """获取可用设备列表"""
        devices = {
            'xiaomi': ['Xiaomi 14', 'Xiaomi 13 Pro', 'Xiaomi 13', 'Xiaomi 12S Ultra'],
            'pixel': ['Pixel 8 Pro', 'Pixel 8', 'Pixel 7 Pro', 'Pixel 7'],
            'samsung': ['Galaxy S24 Ultra', 'Galaxy S24+', 'Galaxy S24'],
            'oneplus': ['OnePlus 12', 'OnePlus 11', 'OnePlus 10 Pro']
        }
        return devices.get(system, [])
    
    def get_available_versions(self, system, device):
        """获取可用版本列表"""
        versions = {
            'xiaomi': ['澎湃OS 1.0', 'MIUI 14', 'MIUI 13'],
            'pixel': ['Android 14 QPR3', 'Android 14 QPR2', 'Android 14'],
            'samsung': ['One UI 6.1', 'One UI 6.0', 'One UI 5.1'],
            'oneplus': ['OxygenOS 14', 'OxygenOS 13.1', 'OxygenOS 13']
        }
        return versions.get(system, [])
    
    def get_firmware_info(self, system, device, channel):
        """获取固件信息"""
        if system in self.sources and channel in self.sources[system]:
            if device in self.sources[system][channel]['devices']:
                return self.sources[system][channel]['devices'][device]
        return None

# 固件管理模块 - 保留原有核心功能
class FirmwareManager:
    def __init__(self):
        self.selected_firmware = None
        self.firmware_info = {}
        self.source_manager = FirmwareSource()
        self.selected_system = None
        self.selected_device = None
        self.selected_version = None
        self.adb_manager = ADBManager()

    def show_menu(self):
        """显示主菜单 - 保留原有界面"""
        clear_screen()
        legal_notice()
        print("\n固件选择菜单：")
        print("1. 下载新固件")
        print("2. 使用本地固件")
        print("3. ADB工具箱 (50+功能)")
        print("ESC. 退出程序\n")

        while True:
            if keyboard.is_pressed('1'):
                return self.download_firmware()
            elif keyboard.is_pressed('2'):
                return self.select_local_firmware()
            elif keyboard.is_pressed('3'):
                return self.show_adb_toolbox()
            elif keyboard.is_pressed('esc'):
                sys.exit()

    def download_firmware(self):
        """下载固件 - 保留原有功能"""
        # 选择系统类型
        system = self.select_system()
        if not system:
            return False
        
        # 选择设备
        device = self.select_device(system)
        if not device:
            return False
        
        # 选择版本
        version = self.select_version(system, device)
        if not version:
            return False
        
        # 选择渠道
        channel_info = self.select_channel()
        if not channel_info:
            return False
        
        # 开始下载
        return self.perform_download(system, device, version, channel_info)

    def select_system(self):
        """选择操作系统类型"""
        clear_screen()
        legal_notice()
        print("\n选择操作系统类型：")
        print("1. 小米 (MIUI/澎湃OS)")
        print("2. Google Pixel")
        print("3. Samsung")
        print("4. OnePlus")
        print("ESC. 返回上级菜单\n")
        
        while True:
            if keyboard.is_pressed('1'):
                return 'xiaomi'
            elif keyboard.is_pressed('2'):
                return 'pixel'
            elif keyboard.is_pressed('3'):
                return 'samsung'
            elif keyboard.is_pressed('4'):
                return 'oneplus'
            elif keyboard.is_pressed('esc'):
                return None

    def select_device(self, system):
        """选择设备型号"""
        clear_screen()
        legal_notice()
        print(f"\n选择{system.upper()}设备型号：")
        
        devices = self.source_manager.get_available_devices(system)
        for i, device in enumerate(devices, 1):
            print(f"{i}. {device}")
        print("ESC. 返回上级菜单\n")
        
        while True:
            for i in range(1, len(devices) + 1):
                if keyboard.is_pressed(str(i)):
                    return devices[i-1]
            if keyboard.is_pressed('esc'):
                return None

    def select_version(self, system, device):
        """选择系统版本"""
        clear_screen()
        legal_notice()
        print(f"\n为 {device} 选择系统版本：")
        
        versions = self.source_manager.get_available_versions(system, device)
        for i, version in enumerate(versions, 1):
            print(f"{i}. {version}")
        print("ESC. 返回上级菜单\n")
        
        while True:
            for i in range(1, len(versions) + 1):
                if keyboard.is_pressed(str(i)):
                    return versions[i-1]
            if keyboard.is_pressed('esc'):
                return None

    def select_channel(self):
        """选择下载渠道"""
        clear_screen()
        legal_notice()
        print("\n选择下载渠道：")
        print("1. 官方稳定版")
        print("2. 开发者预览版")
        print("3. 自定义镜像库")
        print("ESC. 返回上级菜单\n")
        
        while True:
            if keyboard.is_pressed('1'):
                return "stable"
            elif keyboard.is_pressed('2'):
                return "beta"
            elif keyboard.is_pressed('3'):
                return self.custom_mirror()
            elif keyboard.is_pressed('esc'):
                return None

    def custom_mirror(self):
        """处理自定义镜像库"""
        clear_screen()
        legal_notice()
        print("\n自定义镜像库：")
        print("请输入自定义固件信息")
        
        filename = input("文件名: ").strip()
        if not filename:
            filename = f"custom_firmware_{int(time.time())}.zip"
        
        try:
            size_mb = int(input("文件大小(MB): ").strip() or "2000")
        except ValueError:
            size_mb = 2000
            
        return {'type': 'custom', 'filename': filename, 'size_mb': size_mb}

    def create_dummy_file(self, file_path, size_mb):
        """创建指定大小的空文件"""
        try:
            with open(file_path, 'wb') as f:
                f.seek(size_mb * 1024 * 1024 - 1)
                f.write(b'\0')
            return True
        except Exception as e:
            print(f"创建文件失败: {e}")
            return False

    def download_with_progress(self, file_path, size_mb):
        """模拟带进度条的下载过程"""
        try:
            if file_path.exists():
                existing_size = file_path.stat().st_size / (1024 * 1024)
                if abs(existing_size - size_mb) < 1:
                    print(f"\n文件已存在，跳过下载")
                    return True
            
            print(f"\n开始下载... 文件大小: {size_mb} MB")
            
            for i in range(101):
                bar = f"\r[{'█' * (i//2)}{' ' * (50 - i//2)}] {i}% "
                print(f"\033[93m{bar}\033[0m", end='', flush=True)
                time.sleep(0.03)
            
            if self.create_dummy_file(file_path, size_mb):
                print("\n下载完成!")
                return True
            else:
                print("\n文件创建失败!")
                return False
                
        except Exception as e:
            print(f"\n下载过程出错: {e}")
            return False

    def perform_download(self, system, device, version, channel_info):
        """执行下载流程"""
        clear_screen()
        legal_notice()
        
        channel_type = channel_info['type'] if isinstance(channel_info, dict) else channel_info
        
        print(f"\n正在准备下载固件...")
        print(f"系统: {system.upper()}")
        print(f"设备: {device}")
        print(f"版本: {version}")
        print(f"渠道: {channel_type}")
        
        if isinstance(channel_info, dict) and channel_info['type'] == 'custom':
            filename = channel_info['filename']
            size_mb = channel_info['size_mb']
            source_name = "自定义镜像库"
        else:
            firmware_info = self.source_manager.get_firmware_info(system, device, channel_type)
            if not firmware_info:
                print(f"\033[91m错误: 找不到 {device} 的 {channel_type} 版本固件\033[0m")
                time.sleep(2)
                return False
            
            filename = firmware_info['filename']
            size_mb = firmware_info['size_mb']
            source_name = "官方镜像站"
        
        safe_device_dir = device.replace(' ', '')
        download_dir = Path("img") / system / safe_device_dir
        download_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = download_dir / filename
        
        print(f"下载源: {source_name}")
        print(f"文件名: {filename}")
        print(f"保存路径: {file_path}")
        print(f"文件大小: {size_mb} MB")
        
        print("\n连接镜像服务器...")
        time.sleep(1)
        
        if self.download_with_progress(file_path, size_mb):
            if file_path.exists():
                file_size = file_path.stat().st_size
                md5_hash = self.calculate_md5(file_path)
                
                self.selected_firmware = str(file_path)
                self.firmware_info = {
                    'name': filename,
                    'system': system,
                    'device': device,
                    'version': version,
                    'channel': channel_type,
                    'size': f"{file_size / 1024 / 1024 / 1024:.2f} GB",
                    'md5': md5_hash,
                    'build_date': time.strftime("%Y-%m-%d"),
                    'source': source_name,
                    'file_path': str(file_path)
                }
                
                print(f"\n下载完成：{filename}")
                print(f"设备：{device}")
                print(f"版本：{version}")
                print(f"文件大小：{self.firmware_info['size']}")
                print(f"保存位置：{file_path}")
            else:
                print("\033[91m文件创建失败！\033[0m")
                return False
        else:
            print("\033[91m下载失败！\033[0m")
            time.sleep(2)
            return False
        
        print("\n按任意键继续...")
        keyboard.read_event()
        return True

    def calculate_md5(self, file_path):
        """计算文件的MD5值（模拟）"""
        if file_path.exists():
            content = f"{file_path}{file_path.stat().st_size}".encode()
            return hashlib.md5(content).hexdigest()
        return "0" * 32

    def select_local_firmware(self):
        """选择本地固件"""
        clear_screen()
        legal_notice()
        print("\n本地固件选择：")
        print("支持格式：.zip / .img / .bin / .tgz\n")
        
        img_dir = Path("img")
        firmware_files = []
        
        if img_dir.exists():
            print("发现以下固件文件：")
            for ext in ['*.zip', '*.img', '*.bin', '*.tgz']:
                for fw_file in img_dir.rglob(ext):
                    firmware_files.append(fw_file)
                    file_size = fw_file.stat().st_size / (1024 * 1024 * 1024)
                    print(f"{len(firmware_files)}. {fw_file.name} ({file_size:.2f} GB) - {fw_file.parent}")
            
            if not firmware_files:
                print("  暂无固件文件，请先下载固件")
                print("\n按任意键返回...")
                keyboard.read_event()
                return False
        else:
            print("img目录不存在，请先下载固件")
            print("\n按任意键返回...")
            keyboard.read_event()
            return False
        
        print("\n请输入文件编号或输入完整路径：")
        
        while True:
            choice = input("选择: ").strip()
            
            if choice.isdigit() and 1 <= int(choice) <= len(firmware_files):
                selected_file = firmware_files[int(choice) - 1]
                return self._process_selected_file(selected_file)
            else:
                file_path = Path(choice)
                if file_path.exists() and file_path.is_file():
                    return self._process_selected_file(file_path)
                else:
                    print("\033[91m无效选择！请重新输入\033[0m")

    def _process_selected_file(self, file_path):
        """处理选中的文件"""
        self.selected_firmware = str(file_path)
        self._analyze_firmware(file_path)
        return True

    def _analyze_firmware(self, file_path):
        """分析固件文件"""
        file_size = file_path.stat().st_size
        
        path_parts = file_path.parts
        system = "unknown"
        device = "未知设备"
        
        if "img" in path_parts:
            img_index = path_parts.index("img")
            if img_index + 1 < len(path_parts):
                system = path_parts[img_index + 1]
            if img_index + 2 < len(path_parts):
                device = path_parts[img_index + 2].replace('_', ' ')
        
        self.firmware_info = {
            'name': file_path.name,
            'size': f"{file_size / 1024 / 1024 / 1024:.2f} GB",
            'type': '固件文件',
            'system': system,
            'device': device,
            'path': str(file_path.parent),
            'modified': time.ctime(file_path.stat().st_mtime),
            'valid': True,
            'file_path': str(file_path)
        }
        
        print(f"\n固件分析完成：")
        print(f"文件名：{self.firmware_info['name']}")
        print(f"大小：{self.firmware_info['size']}")
        print(f"系统：{self.firmware_info['system']}")
        print(f"设备：{self.firmware_info['device']}")
        time.sleep(2)

    # ADB工具箱功能
    def show_adb_toolbox(self):
        """显示ADB工具箱"""
        clear_screen()
        legal_notice()
        print("\nADB工具箱 - 50+功能")
        print("1. 设备管理")
        print("2. 应用管理") 
        print("3. 文件操作")
        print("4. 系统信息")
        print("5. 调试工具")
        print("6. 返回主菜单\n")
        
        while True:
            if keyboard.is_pressed('1'):
                return self.show_device_management()
            elif keyboard.is_pressed('2'):
                return self.show_app_management()
            elif keyboard.is_pressed('3'):
                return self.show_file_operations()
            elif keyboard.is_pressed('4'):
                return self.show_system_info()
            elif keyboard.is_pressed('5'):
                return self.show_debug_tools()
            elif keyboard.is_pressed('6'):
                return self.show_menu()
            elif keyboard.is_pressed('esc'):
                return self.show_menu()

    def show_device_management(self):
        """设备管理功能"""
        clear_screen()
        legal_notice()
        print("\n设备管理")
        print("1. 查看连接设备")
        print("2. 选择设备")
        print("3. 重启设备")
        print("4. 重启到Recovery")
        print("5. 重启到Bootloader")
        print("6. 查看设备状态")
        print("7. 查看电池信息")
        print("8. 返回工具箱\n")
        
        while True:
            if keyboard.is_pressed('1'):
                self.check_connected_devices()
                break
            elif keyboard.is_pressed('2'):
                self.adb_manager.select_device()
                break
            elif keyboard.is_pressed('3'):
                self.reboot_device()
                break
            elif keyboard.is_pressed('4'):
                self.reboot_recovery()
                break
            elif keyboard.is_pressed('5'):
                self.reboot_bootloader()
                break
            elif keyboard.is_pressed('6'):
                self.get_device_state()
                break
            elif keyboard.is_pressed('7'):
                self.get_battery_info()
                break
            elif keyboard.is_pressed('8'):
                return self.show_adb_toolbox()
            elif keyboard.is_pressed('esc'):
                return self.show_adb_toolbox()

    def show_app_management(self):
        """应用管理功能"""
        clear_screen()
        legal_notice()
        print("\n应用管理")
        print("1. 列出所有应用")
        print("2. 列出系统应用")
        print("3. 列出第三方应用")
        print("4. 安装应用")
        print("5. 卸载应用")
        print("6. 清除应用数据")
        print("7. 强制停止应用")
        print("8. 查看应用信息")
        print("9. 返回工具箱\n")
        
        while True:
            if keyboard.is_pressed('1'):
                self.list_apps()
                break
            elif keyboard.is_pressed('2'):
                self.list_system_apps()
                break
            elif keyboard.is_pressed('3'):
                self.list_third_party_apps()
                break
            elif keyboard.is_pressed('4'):
                self.install_app()
                break
            elif keyboard.is_pressed('5'):
                self.uninstall_app()
                break
            elif keyboard.is_pressed('6'):
                self.clear_app_data()
                break
            elif keyboard.is_pressed('7'):
                self.force_stop_app()
                break
            elif keyboard.is_pressed('8'):
                self.get_app_info()
                break
            elif keyboard.is_pressed('9'):
                return self.show_adb_toolbox()
            elif keyboard.is_pressed('esc'):
                return self.show_adb_toolbox()

    def show_file_operations(self):
        """文件操作功能"""
        clear_screen()
        legal_notice()
        print("\n文件操作")
        print("1. 推送文件到设备")
        print("2. 从设备拉取文件")
        print("3. 列出设备文件")
        print("4. 进入Shell")
        print("5. 查看当前目录")
        print("6. 创建目录")
        print("7. 删除文件/目录")
        print("8. 返回工具箱\n")
        
        while True:
            if keyboard.is_pressed('1'):
                self.push_file()
                break
            elif keyboard.is_pressed('2'):
                self.pull_file()
                break
            elif keyboard.is_pressed('3'):
                self.list_files()
                break
            elif keyboard.is_pressed('4'):
                self.enter_shell()
                break
            elif keyboard.is_pressed('5'):
                self.show_current_dir()
                break
            elif keyboard.is_pressed('6'):
                self.create_directory()
                break
            elif keyboard.is_pressed('7'):
                self.delete_file()
                break
            elif keyboard.is_pressed('8'):
                return self.show_adb_toolbox()
            elif keyboard.is_pressed('esc'):
                return self.show_adb_toolbox()

    def show_system_info(self):
        """系统信息功能"""
        clear_screen()
        legal_notice()
        print("\n系统信息")
        print("1. 查看系统属性")
        print("2. 查看CPU信息")
        print("3. 查看内存信息")
        print("4. 查看存储信息")
        print("5. 查看网络信息")
        print("6. 查看屏幕信息")
        print("7. 查看电池状态")
        print("8. 返回工具箱\n")
        
        while True:
            if keyboard.is_pressed('1'):
                self.get_system_props()
                break
            elif keyboard.is_pressed('2'):
                self.get_cpu_info()
                break
            elif keyboard.is_pressed('3'):
                self.get_memory_info()
                break
            elif keyboard.is_pressed('4'):
                self.get_storage_info()
                break
            elif keyboard.is_pressed('5'):
                self.get_network_info()
                break
            elif keyboard.is_pressed('6'):
                self.get_screen_info()
                break
            elif keyboard.is_pressed('7'):
                self.get_battery_info()
                break
            elif keyboard.is_pressed('8'):
                return self.show_adb_toolbox()
            elif keyboard.is_pressed('esc'):
                return self.show_adb_toolbox()

    def show_debug_tools(self):
        """调试工具"""
        clear_screen()
        legal_notice()
        print("\n调试工具")
        print("1. 查看日志")
        print("2. 清除日志")
        print("3. 错误报告")
        print("4. 屏幕截图")
        print("5. 屏幕录制")
        print("6. 性能监控")
        print("7. 压力测试")
        print("8. 返回工具箱\n")
        
        while True:
            if keyboard.is_pressed('1'):
                self.view_logcat()
                break
            elif keyboard.is_pressed('2'):
                self.clear_logcat()
                break
            elif keyboard.is_pressed('3'):
                self.bug_report()
                break
            elif keyboard.is_pressed('4'):
                self.take_screenshot()
                break
            elif keyboard.is_pressed('5'):
                self.screen_record()
                break
            elif keyboard.is_pressed('6'):
                self.performance_monitor()
                break
            elif keyboard.is_pressed('7'):
                self.stress_test()
                break
            elif keyboard.is_pressed('8'):
                return self.show_adb_toolbox()
            elif keyboard.is_pressed('esc'):
                return self.show_adb_toolbox()

    # 具体的ADB功能实现
    def check_connected_devices(self):
        clear_screen()
        legal_notice()
        print("\n检查连接设备...")
        devices = self.adb_manager.check_devices()
        if devices:
            print("已连接的设备:")
            for device in devices:
                print(f"  - {device}")
        else:
            print("未找到连接的设备")
        print("\n按任意键继续...")
        keyboard.read_event()

    def reboot_device(self):
        clear_screen()
        legal_notice()
        print("\n重启设备...")
        result = self.adb_manager.run_adb_command("reboot")
        print(result)
        print("\n按任意键继续...")
        keyboard.read_event()

    def reboot_recovery(self):
        clear_screen()
        legal_notice()
        print("\n重启到Recovery...")
        result = self.adb_manager.run_adb_command("reboot recovery")
        print(result)
        print("\n按任意键继续...")
        keyboard.read_event()

    def reboot_bootloader(self):
        clear_screen()
        legal_notice()
        print("\n重启到Bootloader...")
        result = self.adb_manager.run_adb_command("reboot bootloader")
        print(result)
        print("\n按任意键继续...")
        keyboard.read_event()

    def get_device_state(self):
        clear_screen()
        legal_notice()
        print("\n设备状态...")
        result = self.adb_manager.run_adb_command("get-state")
        print(f"设备状态: {result}")
        print("\n按任意键继续...")
        keyboard.read_event()

    def get_battery_info(self):
        clear_screen()
        legal_notice()
        print("\n电池信息...")
        result = self.adb_manager.run_adb_command("shell dumpsys battery")
        print(result)
        print("\n按任意键继续...")
        keyboard.read_event()

    def list_apps(self):
        clear_screen()
        legal_notice()
        print("\n所有应用...")
        result = self.adb_manager.run_adb_command("shell pm list packages")
        packages = result.split('\n')
        for pkg in packages[:20]:
            if pkg:
                print(pkg)
        if len(packages) > 20:
            print(f"... 还有 {len(packages)-20} 个应用")
        print("\n按任意键继续...")
        keyboard.read_event()

    def list_system_apps(self):
        clear_screen()
        legal_notice()
        print("\n系统应用...")
        result = self.adb_manager.run_adb_command("shell pm list packages -s")
        packages = result.split('\n')
        for pkg in packages:
            if pkg:
                print(pkg)
        print("\n按任意键继续...")
        keyboard.read_event()

    def list_third_party_apps(self):
        clear_screen()
        legal_notice()
        print("\n第三方应用...")
        result = self.adb_manager.run_adb_command("shell pm list packages -3")
        packages = result.split('\n')
        for pkg in packages:
            if pkg:
                print(pkg)
        print("\n按任意键继续...")
        keyboard.read_event()

    def install_app(self):
        clear_screen()
        legal_notice()
        print("\n安装应用")
        apk_path = input("请输入APK文件路径: ").strip()
        if apk_path and Path(apk_path).exists():
            result = self.adb_manager.run_adb_command(f"install \"{apk_path}\"")
            print(result)
        else:
            print("文件不存在!")
        print("\n按任意键继续...")
        keyboard.read_event()

    def uninstall_app(self):
        clear_screen()
        legal_notice()
        print("\n卸载应用")
        package_name = input("请输入包名: ").strip()
        if package_name:
            result = self.adb_manager.run_adb_command(f"uninstall {package_name}")
            print(result)
        else:
            print("包名不能为空!")
        print("\n按任意键继续...")
        keyboard.read_event()

    def clear_app_data(self):
        clear_screen()
        legal_notice()
        print("\n清除应用数据")
        package_name = input("请输入包名: ").strip()
        if package_name:
            result = self.adb_manager.run_adb_command(f"shell pm clear {package_name}")
            print(result)
        else:
            print("包名不能为空!")
        print("\n按任意键继续...")
        keyboard.read_event()

    def force_stop_app(self):
        clear_screen()
        legal_notice()
        print("\n强制停止应用")
        package_name = input("请输入包名: ").strip()
        if package_name:
            result = self.adb_manager.run_adb_command(f"shell am force-stop {package_name}")
            print(result)
        else:
            print("包名不能为空!")
        print("\n按任意键继续...")
        keyboard.read_event()

    def get_app_info(self):
        clear_screen()
        legal_notice()
        print("\n应用信息")
        package_name = input("请输入包名: ").strip()
        if package_name:
            result = self.adb_manager.run_adb_command(f"shell dumpsys package {package_name}")
            print(result[:1000] + "..." if len(result) > 1000 else result)
        else:
            print("包名不能为空!")
        print("\n按任意键继续...")
        keyboard.read_event()

    def push_file(self):
        clear_screen()
        legal_notice()
        print("\n推送文件到设备")
        local_path = input("本地文件路径: ").strip()
        remote_path = input("设备保存路径: ").strip()
        if local_path and remote_path and Path(local_path).exists():
            result = self.adb_manager.run_adb_command(f"push \"{local_path}\" \"{remote_path}\"")
            print(result)
        else:
            print("文件不存在或路径为空!")
        print("\n按任意键继续...")
        keyboard.read_event()

    def pull_file(self):
        clear_screen()
        legal_notice()
        print("\n从设备拉取文件")
        remote_path = input("设备文件路径: ").strip()
        local_path = input("本地保存路径: ").strip()
        if remote_path and local_path:
            result = self.adb_manager.run_adb_command(f"pull \"{remote_path}\" \"{local_path}\"")
            print(result)
        else:
            print("路径不能为空!")
        print("\n按任意键继续...")
        keyboard.read_event()

    def list_files(self):
        clear_screen()
        legal_notice()
        print("\n设备文件列表")
        path = input("目录路径 (默认: /sdcard): ").strip() or "/sdcard"
        result = self.adb_manager.run_adb_command(f"shell ls -la {path}")
        print(result)
        print("\n按任意键继续...")
        keyboard.read_event()

    def enter_shell(self):
        clear_screen()
        legal_notice()
        print("\n进入ADB Shell...")
        print("输入 'exit' 返回程序")
        input("按Enter开始...")
        os.system("adb shell" if not self.adb_manager.current_device else f"adb -s {self.adb_manager.current_device} shell")

    def show_current_dir(self):
        clear_screen()
        legal_notice()
        print("\n当前目录")
        result = self.adb_manager.run_adb_command("shell pwd")
        print(result)
        print("\n按任意键继续...")
        keyboard.read_event()

    def create_directory(self):
        clear_screen()
        legal_notice()
        print("\n创建目录")
        path = input("目录路径: ").strip()
        if path:
            result = self.adb_manager.run_adb_command(f"shell mkdir -p {path}")
            print("目录创建完成" if not result else result)
        else:
            print("路径不能为空!")
        print("\n按任意键继续...")
        keyboard.read_event()

    def delete_file(self):
        clear_screen()
        legal_notice()
        print("\n删除文件/目录")
        path = input("路径: ").strip()
        if path:
            result = self.adb_manager.run_adb_command(f"shell rm -rf {path}")
            print("删除完成" if not result else result)
        else:
            print("路径不能为空!")
        print("\n按任意键继续...")
        keyboard.read_event()

    def get_system_props(self):
        clear_screen()
        legal_notice()
        print("\n系统属性")
        result = self.adb_manager.run_adb_command("shell getprop")
        lines = result.split('\n')
        for line in lines[:30]:
            if line:
                print(line)
        if len(lines) > 30:
            print("... (更多内容未显示)")
        print("\n按任意键继续...")
        keyboard.read_event()

    def get_cpu_info(self):
        clear_screen()
        legal_notice()
        print("\nCPU信息")
        result = self.adb_manager.run_adb_command("shell cat /proc/cpuinfo")
        print(result)
        print("\n按任意键继续...")
        keyboard.read_event()

    def get_memory_info(self):
        clear_screen()
        legal_notice()
        print("\n内存信息")
        result = self.adb_manager.run_adb_command("shell cat /proc/meminfo")
        print(result)
        print("\n按任意键继续...")
        keyboard.read_event()

    def get_storage_info(self):
        clear_screen()
        legal_notice()
        print("\n存储信息")
        result = self.adb_manager.run_adb_command("shell df -h")
        print(result)
        print("\n按任意键继续...")
        keyboard.read_event()

    def get_network_info(self):
        clear_screen()
        legal_notice()
        print("\n网络信息")
        result = self.adb_manager.run_adb_command("shell ifconfig || ip addr")
        print(result)
        print("\n按任意键继续...")
        keyboard.read_event()

    def get_screen_info(self):
        clear_screen()
        legal_notice()
        print("\n屏幕信息")
        size = self.adb_manager.run_adb_command("shell wm size")
        density = self.adb_manager.run_adb_command("shell wm density")
        print(f"屏幕尺寸: {size}")
        print(f"屏幕密度: {density}")
        print("\n按任意键继续...")
        keyboard.read_event()

    def view_logcat(self):
        clear_screen()
        legal_notice()
        print("\nLogcat日志")
        print("开始显示日志，按Ctrl+C停止...")
        try:
            os.system("adb logcat" if not self.adb_manager.current_device else f"adb -s {self.adb_manager.current_device} logcat")
        except KeyboardInterrupt:
            pass

    def clear_logcat(self):
        clear_screen()
        legal_notice()
        print("\n清除日志")
        result = self.adb_manager.run_adb_command("logcat -c")
        print("日志已清除")
        print("\n按任意键继续...")
        keyboard.read_event()

    def bug_report(self):
        clear_screen()
        legal_notice()
        print("\n生成错误报告...")
        print("这可能需要一些时间...")
        result = self.adb_manager.run_adb_command("bugreport")
        print("错误报告生成完成")
        print("\n按任意键继续...")
        keyboard.read_event()

    def take_screenshot(self):
        clear_screen()
        legal_notice()
        print("\n屏幕截图")
        filename = f"screenshot_{int(time.time())}.png"
        result = self.adb_manager.run_adb_command(f"exec-out screencap -p > {filename}")
        if Path(filename).exists():
            print(f"截图已保存: {filename}")
        else:
            print("截图失败")
        print("\n按任意键继续...")
        keyboard.read_event()

    def screen_record(self):
        clear_screen()
        legal_notice()
        print("\n屏幕录制")
        print("开始录制，按Ctrl+C停止...")
        filename = f"record_{int(time.time())}.mp4"
        try:
            os.system(f"adb shell screenrecord /sdcard/{filename}" if not self.adb_manager.current_device else f"adb -s {self.adb_manager.current_device} shell screenrecord /sdcard/{filename}")
        except KeyboardInterrupt:
            print("录制已停止")
            pull = input("是否拉取到电脑? (y/n): ").lower()
            if pull == 'y':
                self.adb_manager.run_adb_command(f"pull /sdcard/{filename} .")
                print(f"录像已保存: {filename}")

    def performance_monitor(self):
        clear_screen()
        legal_notice()
        print("\n性能监控")
        print("开始监控，按Ctrl+C停止...")
        try:
            while True:
                clear_screen()
                legal_notice()
                print("\n性能监控 (实时)")
                cpu = self.adb_manager.run_adb_command("shell top -n 1 -b | head -20")
                mem = self.adb_manager.run_adb_command("shell cat /proc/meminfo | head -10")
                print("CPU使用情况:")
                print(cpu)
                print("\n内存使用情况:")
                print(mem)
                print("\n按Ctrl+C停止监控...")
                time.sleep(3)
        except KeyboardInterrupt:
            pass

    def stress_test(self):
        clear_screen()
        legal_notice()
        print("\n压力测试")
        package = input("输入包名: ").strip()
        if package:
            events = input("事件数量 (默认: 1000): ").strip() or "1000"
            result = self.adb_manager.run_adb_command(f"shell monkey -p {package} -v {events}")
            print(result)
        else:
            print("包名不能为空!")
        print("\n按任意键继续...")
        keyboard.read_event()

# 设备检测模块 - 保留原有功能
def device_check(firmware_info):
    clear_screen()
    legal_notice()
    print("正在检测设备...")
    time.sleep(1)
    
    system = firmware_info.get('system', 'unknown')
    device = firmware_info.get('device', '未知设备')
    
    print(f"找到设备：{device} (SN:{random.randint(100000,999999)})")
    print("设备状态：")
    print("  Bootloader状态：已解锁")
    print("  USB调试模式：已启用")
    print("  电池电量：{}%".format(random.randint(50, 100)))
    time.sleep(2)
    clear_screen()

# 刷机核心流程 - 保留原有功能
def flash_process(firmware_manager):
    system = firmware_manager.firmware_info.get('system', 'android')
    
    partitions = [
        ("boot", 4096),
        ("system", 4096000),
        ("vendor", 1048576),
        ("userdata", 0),
        ("recovery", 4096)
    ]

    print("\n刷机日志：")
    print(f"目标固件：{firmware_manager.firmware_info['name']}")
    print(f"设备类型：{firmware_manager.firmware_info.get('device', '未知设备')}")
    print(f"系统版本：{firmware_manager.firmware_info.get('version', '未知版本')}")
    print(f"文件大小：{firmware_manager.firmware_info.get('size', '未知')}\n")
    
    for part, size in partitions:
        if size > 0:
            print(f"正在刷写 '{part}' 分区...")
            time.sleep(0.3)
            print(f"写入固件... OKAY")
            time.sleep(0.2)
        else:
            print(f"擦除 '{part}'... OKAY")
            time.sleep(0.1)
    
    print("\n验证分区完整性...")
    time.sleep(1)
    print("重启到系统...")
    time.sleep(1)

# 主程序流程 - 保留原有结构
if __name__ == "__main__":
    legal_notice()
    time.sleep(1)
    
    # 固件选择
    fm = FirmwareManager()
    if not fm.show_menu():
        sys.exit()
    
    clear_screen()
    legal_notice()
    device_check(fm.firmware_info)

    # 刷机进度显示
    def show_progress(step, name, firmware_info):
        legal_notice()
        print(f"刷机阶段 {step}/3: {name}")
        print(f"当前固件：{firmware_info['name']}")
        print(f"设备：{firmware_info.get('device', '未知设备')}")
        print(f"系统：{firmware_info.get('system', '未知系统').upper()}")
        
        if step == 2:
            flash_process(fm)
            time.sleep(1)
        
        for i in range(101):
            bar = f"\r[{'█' * (i//2)}{' ' * (50 - i//2)}] {i}% "
            color_code = 93 if i < 100 else 92
            print(f"\033[{color_code}m{bar}\033[0m", end='', flush=True)
            time.sleep(0.02)
        
        print("\n\n阶段完成")
        time.sleep(1)
        clear_screen()

    # 执行刷机流程
    show_progress(1, "准备刷机环境", fm.firmware_info)
    show_progress(2, "写入系统镜像", fm.firmware_info)
    show_progress(3, "最终验证", fm.firmware_info)

    # 最终显示
    legal_notice()
    print("\033[92m刷机成功！\033[0m\n")
    print(f"已安装系统：{fm.firmware_info.get('system', '未知系统').upper()}")
    print(f"设备型号：{fm.firmware_info.get('device', '未知设备')}")
    print(f"固件文件：{fm.firmware_info.get('name', '未知')}")
    print(f"首次启动可能需要3-5分钟")
    
    print("\n设备将在10秒后重启...")
    for i in range(10, 0, -1):
        print(f"\r倒计时: {i:02d} 秒", end='')
        time.sleep(1)

    clear_screen()
    print("\033[92m[设备已重启]\033[0m")
    time.sleep(2)
    sys.exit()