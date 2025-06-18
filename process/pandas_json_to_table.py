import json
import pandas as pd
from pandas import json_normalize
import os
import glob
import re
import demjson


def read_json_file(input_file):
    """
    读取 json 文件
    """
    with open(input_file, 'r', encoding='utf-8') as fin:
        content = fin.read()

    # 修复缺少逗号分隔符
    content = re.sub(r'}\s*{', '},{', content)

    print(content)  # Add this line to check the content of the JSON file
    pattern = r'\{.*\}'
    # 查找匹配的内容,处理 XX = {xxx}这种类型数据
    match = re.search(pattern, content)
    if match:
        content = match.group(0)
        print(content)
    # 解析 JSON 数据
    try:
        json_data = json.loads(content)
    except json.JSONDecodeError:
        json_data = demjson.decode(content)

    return json_data


def process_json_files(input_folder, output_file):
    html_files_glob = os.path.join(input_folder, '*.html')
    all_data = []
    for file_path in glob.glob(html_files_glob):
        print(file_path)
        json_data = read_json_file(file_path)
        # json_normalize()函数可以将嵌套的JSON数据转换为平面的表格格式，方便进行数据分析和处理
        converted_data = json_normalize(json_data)
        all_data.append(converted_data)
    df = pd.concat(all_data, axis=0, ignore_index=True)
    print(df)
    # 把列中的逗号转化为中文逗号
    df = df.applymap(lambda x: str(x).replace(',', '，'))
    df.to_csv(output_file, mode='a+', index=False)
    print('CSV 文件已保存。')


if __name__ == '__main__':
    process_json_files('./raw', 'output.csv')
