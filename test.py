import sounddevice as sd

print(f"🔧 使用的库: {sd._lib}")
print(f"🔧 PortAudio 版本: {sd.get_portaudio_version()}")

print("\n🔍 Host APIs:")
for api in sd.query_hostapis():
    print(f"  {api['name']}")

print("\n🎧 设备列表:")
print(sd.query_devices())
