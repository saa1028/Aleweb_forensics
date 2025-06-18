import demjson
import csv
import os
import glob
import re
import json


# 加载 JSON 文件并提取数据字典部分（忽略初始化对象名称）
def load_json_file(input_file):
    with open(input_file, 'r', encoding='utf-8_sig') as fin:
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


# 找到 JSON 中最大数据量的键
def find_largest_data_key(json_data):
    largest_key = None
    max_value_length = 0

    for key, value in json_data.items():
        value_length = len(value) if isinstance(value, list) else len(str(value))

        if value_length > max_value_length:
            max_value_length = value_length
            largest_key = key

    return largest_key


# 查找最大列表，直到找到列表为止
def find_largest_list(json_data):
    largest_key = find_largest_data_key(json_data)

    if largest_key is None:
        return None

    value = json_data[largest_key]

    if isinstance(value, list):
        return value
    elif isinstance(value, dict):
        return find_largest_list(value)
    else:
        return None


# 保存数据到 CSV 文件
def save_to_csv(file_path, headers, data_rows):
    with open(file_path, 'a+', newline='', encoding='utf-8_sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for row in data_rows:
            writer.writerow([row[header] for header in headers])


# 保存数据到 CSV 文件
def save_to_csv_no_header(file_path, data_rows):
    with open(file_path, 'a+', newline='', encoding='utf-8_sig') as csvfile:
        writer = csv.writer(csvfile)
        for row in data_rows:
            writer.writerow(row)


# 处理单个 JSON 文件
def process_single_file(file_path, output_file):
    json_data = load_json_file(file_path)
    data_rows = find_largest_list(json_data)
    try:
        if data_rows is None:
            largest_key = find_largest_data_key(json_data)
            data_rows = [json_data[largest_key]]
        headers = list(data_rows[0].keys()) if data_rows else []
        save_to_csv(output_file, headers, data_rows)
    except Exception as data_err:
        try:
            print(data_err)
            save_to_csv_no_header(output_file, data_rows)
        except Exception as e:
            print(e)


# 处理指定文件夹下的所有 JSON 文件
def process_files(input_folder, output_file):
    files_glob = os.path.join(input_folder, '*.html')
    for file_path in glob.glob(files_glob):
        process_single_file(file_path, output_file)


if __name__ == '__main__':
    process_files('./raw', './output.csv')
# 输出的是最大的列表，用csv库写入表格
