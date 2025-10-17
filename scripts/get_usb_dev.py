import pyudev
import sounddevice as sd
import subprocess
import os

def run_command(cmd):
    """执行系统命令并返回输出"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"命令执行失败: {e.stderr}"

def get_usb_device_suspend_status():
    """获取所有USB设备的自动挂起状态"""
    usb_suspend_status = []
    # 遍历所有USB设备目录
    for dev_path in os.listdir('/sys/bus/usb/devices/'):
        full_path = os.path.join('/sys/bus/usb/devices/', dev_path)
        # 只处理设备目录（排除子系统等特殊目录）
        if not os.path.isdir(full_path) or ':' in dev_path:
            continue
        
        try:
            # 获取设备基本信息
            with open(os.path.join(full_path, 'product'), 'r', errors='ignore') as f:
                product_name = f.read().strip() or "未知设备"
            
            with open(os.path.join(full_path, 'idVendor'), 'r', errors='ignore') as f:
                vid = f.read().strip() or "未知"
            
            with open(os.path.join(full_path, 'idProduct'), 'r', errors='ignore') as f:
                pid = f.read().strip() or "未知"
            
            # 获取自动挂起状态（power/control文件）
            control_path = os.path.join(full_path, 'power/control')
            if os.path.exists(control_path):
                with open(control_path, 'r') as f:
                    suspend_status = f.read().strip()
            else:
                suspend_status = "无法获取状态"
            
            usb_suspend_status.append({
                'device_path': dev_path,
                'product_name': product_name,
                'vid': vid,
                'pid': pid,
                'suspend_status': suspend_status,
                'is_suspended': suspend_status == 'auto'  # 是否启用自动挂起
            })
        except Exception as e:
            # 忽略权限不足或不支持的设备（如USB控制器本身）
            continue
    
    return usb_suspend_status

def get_usb_audio_devices():
    """获取所有USB音频设备（包括输入和输出）及自动挂起状态"""
    context = pyudev.Context()
    usb_audio_devices = []
    
    # 1. 获取所有USB设备的自动挂起状态
    usb_suspend_status = get_usb_device_suspend_status()
    
    # 2. 显示系统所有USB设备（通过lsusb）
    print("===== 系统所有USB设备（lsusb输出） =====")
    print(run_command("lsusb"))
    
    # 3. 获取sounddevice识别的所有音频设备（输入+输出）
    all_audio_devices = sd.query_devices()
    input_devices = [
        (i, dev) for i, dev in enumerate(all_audio_devices) 
        if dev['max_input_channels'] > 0
    ]
    output_devices = [
        (i, dev) for i, dev in enumerate(all_audio_devices) 
        if dev['max_output_channels'] > 0
    ]
    print(f"\n===== sounddevice识别的设备 =====")
    print(f"输入设备 ({len(input_devices)}个):")
    for idx, dev in input_devices:
        print(f"  ID: {idx}, 名称: {dev['name']}")
    print(f"输出设备 ({len(output_devices)}个):")
    for idx, dev in output_devices:
        print(f"  ID: {idx}, 名称: {dev['name']}")
    
    # 4. 匹配名称中包含"USB"的音频设备
    usb_named_devices = []
    # 处理输入设备
    for dev_id, dev in input_devices:
        if 'usb' in dev['name'].lower():
            usb_named_devices.append({
                'type': '输入',
                'sounddevice_id': dev_id,
                'name': dev['name'],
                'channels': dev['max_input_channels'],
                'usb_info': '名称包含USB，但系统未识别为USB设备',
                'suspend_status': '未找到对应USB设备'  # 初始化为未找到
            })
    # 处理输出设备
    for dev_id, dev in output_devices:
        if 'usb' in dev['name'].lower():
            usb_named_devices.append({
                'type': '输出',
                'sounddevice_id': dev_id,
                'name': dev['name'],
                'channels': dev['max_output_channels'],
                'usb_info': '名称包含USB，但系统未识别为USB设备',
                'suspend_status': '未找到对应USB设备'
            })
    
    # 5. 补充系统级USB信息和自动挂起状态
    for device in context.list_devices(subsystem='usb'):
        if 'audio' in device.properties.get('ID_USB_INTERFACES', ''):
            vid = device.properties.get('ID_VENDOR_ID', '未知')
            pid = device.properties.get('ID_MODEL_ID', '未知')
            name = device.properties.get('ID_MODEL', '未知')
            # 匹配音频设备并补充信息
            for dev in usb_named_devices:
                if name in dev['name'] or vid in dev['name']:
                    dev['usb_info'] = f"VID: {vid}, PID: {pid}, 名称: {name}"
                    # 查找对应的自动挂起状态
                    for suspend_dev in usb_suspend_status:
                        if suspend_dev['vid'] == vid and suspend_dev['pid'] == pid:
                            dev['suspend_status'] = f"{suspend_dev['suspend_status']} (路径: {suspend_dev['device_path']})"
    
    return usb_audio_devices, usb_suspend_status

if __name__ == "__main__":
    print("===== USB音频设备综合检测（含自动挂起状态） =====")
    audio_devices, all_usb_suspend = get_usb_audio_devices()
    
    # 打印所有USB设备的自动挂起状态
    print("\n===== 所有USB设备自动挂起状态 =====")
    print(f"共检测到 {len(all_usb_suspend)} 个USB设备：")
    for dev in all_usb_suspend:
        status_str = "启用自动挂起" if dev['is_suspended'] else "禁用自动挂起"
        print(f"  设备: {dev['product_name']} (VID:{dev['vid']}, PID:{dev['pid']})")
        print(f"  路径: {dev['device_path']}, 状态: {dev['suspend_status']} ({status_str})")
        print("  ------------------------")
    
    # 打印检测到的USB音频设备
    print("\n===== 检测到的USB音频设备 =====")
    if not audio_devices:
        print("未找到任何名称包含USB的音频设备")
    else:
        for i, dev in enumerate(audio_devices):
            print(f"设备 {i + 1}:")
            print(f"  类型: {dev['type']}")
            print(f"  名称: {dev['name']}")
            print(f"  sounddevice ID: {dev['sounddevice_id']}（可用作程序中的设备ID）")
            print(f"  通道数: {dev['channels']}")
            print(f"  USB信息: {dev['usb_info']}")
            print(f"  自动挂起状态: {dev['suspend_status']}")
            print("-----------------------------------")
    
    print("\n===== 排查建议 =====")
    print("1. 若音频设备自动挂起状态为'auto'（启用）：")
    print("   - 建议禁用：sudo sh -c 'echo on > /sys/bus/usb/devices/<设备路径>/power/control'")
    print("   - 永久生效需添加udev规则（参考之前的方法）")
    print("2. 若设备在lsusb中显示，但未被识别为音频设备：")
    print("   - 安装驱动：sudo apt install linux-firmware")
    print("3. 若设备不在lsusb中：")
    print("   - 换USB端口重试；检查设备是否需要外接电源")
