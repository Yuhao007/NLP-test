# aduio file named wav, actually mp3

import os
import pandas as pd
from edge_tts import Communicate
import re

# 提取支持英语的人声库
zh_voices = [
    "zh-CN-XiaoxiaoNeural",
    "zh-CN-XiaoyiNeural",
    "zh-CN-YunjianNeural",
    "zh-CN-YunxiNeural",
    "zh-CN-YunxiaNeural",
    "zh-CN-YunyangNeural",
    "zh-CN-liaoning-XiaobeiNeural",
    "zh-CN-shaanxi-XiaoniNeural",
    "zh-HK-HiuGaaiNeural",
    "zh-HK-HiuMaanNeural",
    "zh-HK-WanLungNeural",
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

# 使用示例
excel_file = 'input_file.xlsx'
output_dir = 'output_audio'

# 使用异步函数
import asyncio
asyncio.run(generate_audio(excel_file, output_dir))
