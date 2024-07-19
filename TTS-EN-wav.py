import os
import pandas as pd
from edge_tts import Communicate
import re
import asyncio
import subprocess

# 提取支持英语的人声库
voices = [
    "en-AU-NatashaNeural", "en-AU-WilliamNeural",
    "en-CA-ClaraNeural", "en-CA-LiamNeural",
    "en-GB-LibbyNeural", "en-GB-MaisieNeural", "en-GB-RyanNeural", "en-GB-SoniaNeural", "en-GB-ThomasNeural",
    "en-HK-SamNeural", "en-HK-YanNeural",
    "en-IE-ConnorNeural", "en-IE-EmilyNeural",
    "en-IN-NeerjaExpressiveNeural", "en-IN-NeerjaNeural", "en-IN-PrabhatNeural",
    "en-KE-AsiliaNeural", "en-KE-ChilembaNeural",
    "en-NG-AbeoNeural", "en-NG-EzinneNeural",
    "en-NZ-MitchellNeural", "en-NZ-MollyNeural",
    "en-PH-JamesNeural", "en-PH-RosaNeural",
    "en-SG-LunaNeural", "en-SG-WayneNeural",
    "en-TZ-ElimuNeural", "en-TZ-ImaniNeural",
    "en-US-AnaNeural", "en-US-AndrewMultilingualNeural", "en-US-AndrewNeural", "en-US-AriaNeural",
    "en-US-AvaMultilingualNeural", "en-US-AvaNeural", "en-US-BrianMultilingualNeural", "en-US-BrianNeural",
    "en-US-ChristopherNeural", "en-US-EmmaMultilingualNeural", "en-US-EmmaNeural", "en-US-EricNeural",
    "en-US-GuyNeural", "en-US-JennyNeural", "en-US-MichelleNeural", "en-US-RogerNeural", "en-US-SteffanNeural",
    "en-ZA-LeahNeural", "en-ZA-LukeNeural"
]

async def generate_audio(excel_file, output_dir):
    # 读取 Excel 表格
    df = pd.read_excel(excel_file)

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 循环使用人声库
    voice_index = 0

    # 遍历 'txt' 列的每一个值
    for index, row in df.iterrows():
        text = row['txt']
        # 清理文件名中的特殊字符
        file_name = re.sub(r'[^\w\-_\. ]', '_', text) + ".wav"
        output_path = os.path.join(output_dir, file_name)

        # 使用 edge-tts 库生成音频文件
        voice_name = voices[voice_index % len(voices)]
        communicate = Communicate(text, voice=voice_name)
        await communicate.save(output_path)

        print(f"已生成音频文件: {output_path} 使用人声库: {voice_name}")

        # 更新人声库索引
        voice_index += 1

def convert_audio(input_dir, output_dir):
    # 遍历当前文件夹下的所有文件
    for filename in os.listdir(input_dir):
        # 检查文件是否为 MP3 格式
        if filename.endswith('.mp3'):
            # 构建输入和输出文件路径
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.wav')

            # 使用 FFmpeg 进行转换
            try:
                subprocess.run(['ffmpeg', '-i', input_path, '-c:a', 'pcm_s16le', '-ar', '16000', '-ac', '1', output_path], check=True)
                print(f"Successfully converted {filename} to {os.path.basename(output_path)}")
                
                # 删除原始的 MP3 文件
                os.remove(input_path)
                print(f"Deleted original MP3 file: {filename}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting {filename}: {e}")

# 使用示例
excel_file = 'input_file.xlsx'
output_dir = 'output_audio'

# 使用异步函数生成音频文件
asyncio.run(generate_audio(excel_file, output_dir))

# 转换音频文件格式
convert_audio(output_dir, output_dir)
