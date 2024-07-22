# Chinese asr 

import pandas as pd
import numpy as np
from Levenshtein import distance

# 读取 Excel 文件
excel_path = 'dataC.xlsx'
df = pd.read_excel(excel_path)

# 初始化输出列表
output = []
total_expected_chars = 0
total_edit_chars = 0
total_sentences = 0
total_sentence_errors = 0

# 遍历每一行数据
for index, row in df.iterrows():
    # 读取预期结果和实际结果
    expected = ''.join(c for c in str(row['text']) if c.isalnum())
    actual = ''.join(c for c in str(row['R_text']) if c.isalnum())

    # 计算编辑距离
    edit_distance = distance(expected, actual)
    expected_len = len(expected)
    added = max(0, len(actual) - expected_len)
    deleted = max(0, expected_len - len(actual))
    changed = edit_distance - added - deleted

    # 判断是否为正确句子
    sentence_error = 1 if added > 0 or deleted > 0 or changed > 0 else 0
    total_sentences += 1
    total_sentence_errors += sentence_error

    # 添加结果到输出列表
    output.append([expected, actual, expected_len, added, deleted, changed, sentence_error])

    # 更新总字符数
    total_expected_chars += expected_len
    total_edit_chars += (added + deleted + changed)

# 创建输出 DataFrame
output_df = pd.DataFrame(output, columns=['text', 'R_text', 'number', 'insertions', 'deletions', 'substitutions', 'sentence error'])

# 将输出写入新的 Excel 文件
with pd.ExcelWriter('output.xlsx') as writer:
    output_df.to_excel(writer, sheet_name='data', index=False)

    # 添加总字符数、错误率和句错率信息
    stats_df = pd.DataFrame({
        'Metric': ['Total Expected Words', 'Total Actual Words', 'Character Error Rate', 'Sentence Error Rate'],
        'Value': [total_expected_chars, total_edit_chars, f"{total_edit_chars / total_expected_chars:.2%}", f"{total_sentence_errors / total_sentences:.2%}"]
    })
    stats_df.to_excel(writer, sheet_name='Summary', index=False)

print('结果已保存到 output.xlsx 文件中!')
