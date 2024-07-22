import pandas as pd
import tiktoken

# Excel 文件路径和编码
input_excel_path = 'input-text.xlsx'  # Excel 输入文件路径
output_excel_path = 'output-token.xlsx'  # Excel 输出文件路径
encoding_name = 'cl100k_base'  # Tiktoken 编码方式

# 读取 Excel 文件
df = pd.read_excel(input_excel_path)

# 加载 Tiktoken 编码
encoding = tiktoken.get_encoding(encoding_name)

# 初始化输出的 DataFrame
output_df = pd.DataFrame(columns=['Original Text', 'Tokens'])

# 遍历 DataFrame 中的每一行并进行分词
for index, row in df.iterrows():
    # 假设文本在名为 'text' 的列中
    text = row['text']
    # 使用 Tiktoken 进行分词
    tokens = encoding.encode(text)
    # 将原始文本和分词结果添加到 DataFrame
    new_row = pd.DataFrame({'Original Text': [text], 'Tokens': [list(tokens)]})
    output_df = pd.concat([output_df, new_row], ignore_index=True)

# 将分词结果写入新的 Excel 文件
output_df.to_excel(output_excel_path, index=False)

print(f'分词结果已保存到 {output_excel_path} 文件中!')
