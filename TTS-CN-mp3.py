import os
import pandas as pd
import logging
from edge_tts import Communicate
import asyncio
import traceback

# 配置日志
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 文件日志处理器
file_handler = logging.FileHandler('tts_errors.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# 控制台日志处理器 - 简化格式
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('[%(process)d] %(message)s'))

logger.addHandler(file_handler)
logger.addHandler(console_handler)

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

async def generate_audio_with_retry(excel_file, output_dir):
    """带重试机制的音频生成函数"""
    df = pd.read_excel(excel_file)
    os.makedirs(output_dir, exist_ok=True)
    failed_list = []
    
    for index, row in df.iterrows():
        text = str(row['txt'])  # 确保文本为字符串
        file_name = f"{index+1:03d}.mp3"  # 3位数字编号
        output_path = os.path.join(output_dir, file_name)
        voice_name = voices[index % len(voices)]
        
        retry_count = 0
        max_retries = 2
        
        while retry_count <= max_retries:
            try:
                communicate = Communicate(text, voice=voice_name)
                await asyncio.wait_for(communicate.save(output_path), timeout=30.0)
                
                # 验证文件是否生成成功
                if os.path.exists(output_path) and os.path.getsize(output_path) > 1024:
                    logger.info(f"{index+1:03d} 成功 (语音: {voice_name})")
                    break
                else:
                    raise Exception("生成的文件无效（大小<1KB）")
                    
            except Exception as e:
                retry_count += 1
                error_msg = f"{index+1:03d} 尝试{retry_count}/{max_retries}失败: {str(e)}"
                logger.error(error_msg)
                traceback.print_exc()
                
                if retry_count > max_retries:
                    failed_list.append({
                        'row': index+1,
                        'text': text[:50] + "..." if len(text)>50 else text,
                        'error': str(e)
                    })
                    # 创建空文件标记失败
                    with open(output_path+'.failed', 'w') as f:
                        f.write(error_msg)
                    break
                
    # 保存失败记录
    if failed_list:
        pd.DataFrame(failed_list).to_csv(
            os.path.join(output_dir, 'failed_records.csv'),
            index=False,
            encoding='utf-8-sig'
        )
        logger.warning(f"完成处理，失败 {len(failed_list)}/{len(df)} 条记录")

# 使用示例
if __name__ == "__main__":
    excel_file = 'input.xlsx'  # 替换为你的Excel路径, 列名txt
    output_dir = 'output_audio' #输出文件夹
    
    print("开始生成音频...")
    asyncio.run(generate_audio_with_retry(excel_file, output_dir))
    print("处理完成，请查看output_audio目录和tts_errors.log文件")
