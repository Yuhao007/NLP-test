
import os
import pandas as pd
from edge_tts import Communicate
import re
import asyncio

# 提取支持汉语的人声库
voices = [
    "zh-CN-XiaoxiaoNeural",
    "zh-CN-XiaoyiNeural",
    "zh-CN-YunjianNeural",
    "zh-CN-YunxiNeural",
    "zh-CN-YunxiaNeural",
    "zh-CN-YunyangNeural",
    "zh-TW-HsiaoChenNeural",
    "zh-TW-HsiaoYuNeural",
    "zh-TW-YunJheNeural"
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

asyncio.run(generate_audio(excel_file, output_dir))
