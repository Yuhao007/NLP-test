import os
import pandas as pd
from edge_tts import Communicate
import re

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
    # 初始化一个计数器，用于生成顺序数字
    audio_index = 1

    for index, row in df.iterrows():
        text = row['txt']

        # 这里不再使用文本内容生成文件名，而是使用顺序数字
        file_name = f"{audio_index:02d}.mp3"  # 使用4位数的格式，不足的前面补0
        output_path = os.path.join(output_dir, file_name)

        # 使用 edge-tts 库生成音频文件
        voice_name = voices[(index % len(voices)) if len(voices) > 0 else 0]
        communicate = Communicate(text, voice=voice_name)
        await communicate.save(output_path)

    # 增加计数器，为下一个文件名做准备
        audio_index += 1

        print(f"已生成音频文件: {output_path} 使用人声库: {voice_name}")

        # 更新人声库索引
        voice_index += 1

# 使用示例
excel_file = 'input_file.xlsx'
output_dir = 'output_audio'

# 使用异步函数
import asyncio
asyncio.run(generate_audio(excel_file, output_dir))
