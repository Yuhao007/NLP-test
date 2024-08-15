import pandas as pd
import re
import tiktoken
from difflib import SequenceMatcher

def clean_text(text):
    #清洗文本，移除标点符号和多余空格
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_wer_and_edits(row):
    #计算词错误率(WER)及编辑操作
    expected = row['encoded_text']
    actual = row['encoded_r_text']

    # 计算编辑距离
    seq_match = SequenceMatcher(None, expected, actual)
    operations = seq_match.get_opcodes()
    
    substitutions, deletions, insertions = 0, 0, 0

    # 计算每种操作的数量
    for operation in operations:
        tag, i1, i2, j1, j2 = operation
        if tag == 'replace':
            substitutions += i2 - i1
        elif tag == 'delete':
            deletions += i2 - i1
        elif tag == 'insert':
            insertions += j2 - j1

    total_edits = substitutions + deletions + insertions
    word_error_rate = total_edits / max(len(expected), len(actual), 1)

    sentence_error = int(substitutions > 0 or deletions > 0 or insertions > 0)

    return pd.Series({
        'expected_len': len(expected),
        'actual_len': len(actual),
        'substitutions': substitutions,
        'deletions': deletions,
        'insertions': insertions,
        'word_error_rate': word_error_rate,
        'sentence_error': sentence_error
    })

def main():
    # 读取Excel文件
    file_path = 'ASR-test.xlsx'
    df = pd.read_excel(file_path)

    # 对文本进行清洗
    df['clean_text'] = df['text'].apply(clean_text)
    df['clean_r_text'] = df['r_text'].apply(clean_text)

    # 使用tiktoken进行编码
    encoder = tiktoken.get_encoding('cl100k_base')
    encoder.lowercase = True
    
    df['encoded_text'] = df['clean_text'].apply(encoder.encode)
    df['encoded_r_text'] = df['clean_r_text'].apply(encoder.encode)

    # 应用WER和编辑操作计算函数
    edits_df = df.apply(calculate_wer_and_edits, axis=1)
    df = pd.concat([df, edits_df], axis=1)

    # 选择需要的列进行输出
    output_columns = ['text', 'r_text', 'encoded_text', 'encoded_r_text', 'expected_len', 'actual_len', 'substitutions', 'deletions', 'insertions', 'word_error_rate', 'sentence_error']
    output_df = df[output_columns]

    # 输出结果到新的Excel文件
    output_excel_path = 'output_with_wer.xlsx'
    with pd.ExcelWriter(output_excel_path, engine='xlsxwriter') as writer:
        # 将原始数据写入第一个sheet页面
        output_df.to_excel(writer, sheet_name='Data', index=False)

        # 计算统计数据
        total_expected_tokens = output_df['expected_len'].sum()
        total_actual_tokens = output_df['actual_len'].sum()
        total_edits = output_df[['substitutions', 'deletions', 'insertions']].sum().sum()
        word_error_rate = total_edits / total_expected_tokens * 100 if total_expected_tokens > 0 else 0

        total_sentences = len(output_df)
        total_sentence_errors = output_df['sentence_error'].sum()
        sentence_error_rate = total_sentence_errors / total_sentences * 100 if total_sentences > 0 else 0

        # 创建新的sheet页面并写入统计数据
        summary_data = pd.DataFrame({
            'Metric': ['Total Expected Tokens', 'Total Actual Tokens', 'Total Edits', 'Word Error Rate', 'Total Sentences', 'Total Sentence Errors', 'Sentence Error Rate'],
            'Value': [
                total_expected_tokens, 
                total_actual_tokens, 
                total_edits, 
                f"{word_error_rate:.2f}%", 
                total_sentences, 
                total_sentence_errors, 
                f"{sentence_error_rate:.2f}%"
            ]
        })
        summary_data.to_excel(writer, sheet_name='Summary', index=False)
        print(f"结果已保存到 '{output_excel_path}'")

if __name__ == "__main__":
    main()
