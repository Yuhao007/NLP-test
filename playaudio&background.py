import pandas as pd
import numpy as np
import pyaudio
import wave
import os

# 读取 Excel 表格
df = pd.read_excel('audio_paths.xlsx')

# 硬编码音频输出设备序号（用于播放 Excel 表格中的音频）
output_device_id_main = 7

# 硬编码要循环播放的音频文件路径
fixed_audio_path = r'D:\Audio\10mmusic3.wav'

# 初始化 PyAudio
pa = pyaudio.PyAudio()

# 获取当前系统默认的声音设备索引
default_output_device_index = pa.get_default_output_device_info()['index']

# 确保输出设备 ID 是有效的
num_devices = pa.get_device_count()
if output_device_id_main >= num_devices:
    print("The output device ID for main audio is invalid. Please check the device ID.")
    pa.terminate()
    exit()

# 播放固定音频的函数，使用系统默认设备循环播放
def play_fixed_audio_loop(pa, audio_path, device_index):
    with wave.open(audio_path, 'rb') as wave_file:
        frames = wave_file.readframes(wave_file.getnframes())
        data = np.frombuffer(frames, dtype=np.int16)
        fs = wave_file.getframerate()
        num_channels = wave_file.getnchannels()

    stream = pa.open(format=pa.get_format_from_width(wave_file.getsampwidth()),
                      channels=num_channels,
                      rate=fs,
                      output=True,
                      output_device_index=device_index)

    #print(f"Playing fixed audio loop: {audio_path}")
    while True:  # 循环播放固定音频
        stream.write(data.tobytes())

# 在单独的线程播放固定音频循环
import threading
fixed_audio_thread = threading.Thread(target=play_fixed_audio_loop, args=(pa, fixed_audio_path, default_output_device_index))
fixed_audio_thread.daemon = True  # 设置为守护线程
fixed_audio_thread.start()

# 循环播放 Excel 表格中的每个音频文件，使用指定的声卡
for index, row in df.iterrows():
    audio_path = row['wavepath']
    audio_path = os.path.abspath(audio_path)
    
    #print(f"Playing audio: {audio_path}")
    
    with wave.open(audio_path, 'rb') as wave_file:
        frames = wave_file.readframes(wave_file.getnframes())
        data = np.frombuffer(frames, dtype=np.int16)
        fs = wave_file.getframerate()
        num_channels = wave_file.getnchannels()
    
    stream = pa.open(format=pa.get_format_from_width(wave_file.getsampwidth()),
                      channels=num_channels,
                      rate=fs,
                      output=True,
                      output_device_index=output_device_id_main)
    
    stream.write(data.tobytes())
    stream.stop_stream()
    stream.close()

    print(f"Finished playing audio: {audio_path}")

# 等待固定音频循环播放线程结束（这里只是为了避免直接退出，实际使用中可能需要其他条件来停止线程）
fixed_audio_thread.join()

# 终止 PyAudio
pa.terminate()
