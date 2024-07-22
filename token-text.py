import pandas as pd
import tiktoken
import ast  # 导入 ast 模块

# Excel 文件路径和编码
input_excel_path = 'input-token.xlsx'  # Excel 输入文件路径
output_excel_path = 'output-textn.xlsx'  # Excel 输出文件路径
encoding_name = 'cl100k_base'  # Tiktoken 编码方式

# 读取 Excel 文件
df = pd.read_excel(input_excel_path)

# 加载 Tiktoken 编码
encoding = tiktoken.get_encoding(encoding_name)

# 初始化输出的 DataFrame
output_df = pd.DataFrame(columns=['Original Text'])

# 遍历 DataFrame 中的每一行并进行还原
for index, row in df.iterrows():
    # 假设 token 在名为 'token' 的列中
    tokens_str = row['token']  # 这可能是一个表示列表的字符串，例如 "[1, 2, 3]"
    # 使用 ast.literal_eval 安全地将字符串解析为列表
    tokens_list = ast.literal_eval(tokens_str)
    # 确保 tokens_list 是整数列表
    tokens_int_list = [int(token) for token in tokens_list]
    # 使用 Tiktoken 进行还原
    original_text = encoding.decode(tokens_int_list)
    # 将还原后的文本添加到 DataFrame
    new_row = pd.DataFrame({'Original Text': [original_text]})
    output_df = pd.concat([output_df, new_row], ignore_index=True)

# 将还原结果写入新的 Excel 文件
output_df.to_excel(output_excel_path, index=False)

print(f'还原结果已保存到 {output_excel_path} 文件中!')
