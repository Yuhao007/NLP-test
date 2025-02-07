import os
import asyncio
import pandas as pd
from edge_tts import Communicate

# 支持的中文语音列表
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

    # 遍历 'txt' 列的每一个值
    audio_index = 1  # 初始化音频文件计数器

    for index, row in df.iterrows():
        text = row['txt']
        voice_name = voices[index % len(voices)]  # 选择语音

        # 生成文件名，使用计数器确保唯一性
        file_name = f"{audio_index:02d}.mp3"
        output_path = os.path.join(output_dir, file_name)

        # 使用 edge-tts 库生成音频文件
        communicate = Communicate(text, voice=voice_name)
        await communicate.save(output_path)

        print(f"已生成音频文件: {output_path}，使用人声库: {voice_name}")
        audio_index += 1  # 更新计数器

# 使用异步函数运行
if __name__ == "__main__":
    excel_file = 'input_file.xlsx'  # 输入的 Excel 文件路径
    output_dir = 'output_audio'    # 输出音频文件的目录
    asyncio.run(generate_audio(excel_file, output_dir))
