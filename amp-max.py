# -*- coding: utf-8 -*-
import wave

def calculate_normalized_amplitude(audio_file_path):
    with wave.open(audio_file_path, 'rb') as wav_file:
        num_channels = wav_file.getnchannels()
        sampwidth = wav_file.getsampwidth()
        num_frames = wav_file.getnframes()

        # 确保是单声道和16位样本
        if num_channels != 1 or sampwidth != 2:
            raise ValueError("Unsupported audio format. Please use mono, 16-bit PCM files.")

        # 初始化最大振幅为可能的最小值
        max_amplitude = -32768  # 16位整数的最小值

        # 读取所有帧数据
        frames = wav_file.readframes(num_frames)

        # 遍历每个样本，计算最大振幅
        for sample in range(0, num_frames * sampwidth, sampwidth):
            sample_bytes = frames[sample:sample + sampwidth]
            amplitude = int.from_bytes(sample_bytes, byteorder='little', signed=True)
            max_amplitude = max(max_amplitude, abs(amplitude))

    # 标准化振幅值
    max_possible_amplitude = 32767  # 16位PCM的最大值
    normalized_amplitude = max_amplitude / max_possible_amplitude if max_possible_amplitude != 0 else 0

    return normalized_amplitude

if __name__ == "__main__":
    # 让用户输入音频文件的路径
    audio_file_path = input("Please enter the wave path: ")

    try:
        normalized_amplitude = calculate_normalized_amplitude(audio_file_path)
        if normalized_amplitude is not None:
            # 打印标准化后的振幅
            print(f"Normalized amplitude: {normalized_amplitude:.6f}")
    except Exception as e:
        print(f"An error occurred: {e}")
