import pandas as pd
import re
from Levenshtein import distance
from difflib import SequenceMatcher
import tiktoken

# Excel 文件路径和编码
input_excel_path = 'data.xlsx'  # Excel 输入文件路径
output_excel_path = 'output_data.xlsx'  # Excel 输出文件路径
encoding_name = 'cl100k_base'  # Tiktoken 编码方式

# 读取Excel文件
df = pd.read_excel(input_excel_path)

# 加载 Tiktoken 编码
encoding = tiktoken.get_encoding(encoding_name)

# 定义一个函数来清洗和分割文本
def tokenize_text(text):
    # 使用 Tiktoken 进行分词
    tokens = encoding.encode(text)
    return tokens

# 应用函数对'text'和'R_text'列进行分词
df['expected_tokens'] = df['text'].apply(tokenize_text)
df['actual_tokens'] = df['R_text'].apply(tokenize_text)

# 定义一个函数来计算WER和编辑操作
def calculate_wer_and_edits(row):
    expected = row['expected_tokens']
    actual = row['actual_tokens']
    expected_len = len(expected)
    actual_len = len(actual)

    # 计算编辑距离
    edit_distance = distance(expected, actual)

    # 使用SequenceMatcher来获取详细的编辑操作
    seq_match = SequenceMatcher(None, expected, actual)
    operations = seq_match.get_opcodes()

    # 初始化编辑操作计数
    substitutions = 0
    deletions = 0
    insertions = 0

    # 计算每种编辑操作的数量
    for operation in operations:
        tag, i1, i2, j1, j2 = operation
        if tag == 'replace':
            substitutions += i2 - i1
        elif tag == 'delete':
            deletions += i2 - i1
        elif tag == 'insert':
            insertions += j2 - j1

    total_edits = substitutions + deletions + insertions
    word_error_rate = total_edits / max(expected_len, actual_len)

    # 检查句子是否有错
    sentence_error = int(substitutions > 0 or deletions > 0 or insertions > 0)

    return pd.Series({
        'expected_len': expected_len,
        'actual_len': actual_len,
        'substitutions': substitutions,
        'deletions': deletions,
        'insertions': insertions,
        'word_error_rate': word_error_rate,
        'sentence_error': sentence_error
    })

# 应用WER和编辑操作计算函数
df[['expected_len', 'actual_len', 'substitutions', 'deletions', 'insertions', 'word_error_rate', 'sentence_error']] = df.apply(calculate_wer_and_edits, axis=1)

# 选择需要的列进行输出
output_columns = ['text', 'R_text', 'expected_tokens', 'actual_tokens', 'expected_len', 'actual_len', 'substitutions', 'deletions', 'insertions', 'word_error_rate', 'sentence_error']
output_df = df[output_columns]

# 创建新的sheet页面
with pd.ExcelWriter(output_excel_path, engine='xlsxwriter') as writer:
    # 将原始数据写入第一个sheet页面
    output_df.to_excel(writer, sheet_name='Data', index=False)

    # 计算总词语数、修改词语数量、词错率和句错率
    total_expected_tokens = output_df['expected_len'].sum()
    total_actual_tokens = output_df['actual_len'].sum()
    total_substitutions = output_df['substitutions'].sum()
    total_deletions = output_df['deletions'].sum()
    total_insertions = output_df['insertions'].sum()
    total_edits = total_substitutions + total_deletions + total_insertions
    word_error_rate = total_edits / total_expected_tokens * 100

    total_sentences = len(output_df)
    total_sentence_errors = output_df['sentence_error'].sum()
    sentence_error_rate = total_sentence_errors / total_sentences * 100

    # 创建新的sheet页面并写入统计数据
    summary_data = pd.DataFrame({
        'Metric': ['Total Expected Tokens', 'Total Actual Tokens', 'Total Substitutions', 'Total Deletions', 'Total Insertions', 'Total Edits', 'Word Error Rate', 'Total Sentences', 'Total Sentence Errors', 'Sentence Error Rate'],
        'Value': [total_expected_tokens, total_actual_tokens, total_substitutions, total_deletions, total_insertions, total_edits, f"{word_error_rate:.2f}%", total_sentences, total_sentence_errors, f"{sentence_error_rate:.2f}%"]
    })
    summary_data.to_excel(writer, sheet_name='Summary', index=False)
    print(f"结果已保存到 '{output_excel_path}'")
