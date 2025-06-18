import json
import re
import demjson
from jsoncsv.jsontool import convert_json, expand, restore
import time
import os
import glob


def preprocess_json(input_file):
    # 读取文件内容
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


def convert_to_csv(input_folder, output_file):
    files_glob = os.path.join(input_folder, '*.html')
    for file_path in glob.glob(files_glob):
        # 预处理 JSON 文件，生成临时文件
        json_data = preprocess_json(file_path)
        # 打开临时文件和输出文件
        temp_file = f"temp_{int(time.time())}.json"
        with open(temp_file, 'w', encoding='utf-8_sig') as fin:
            fin.write(json.dumps(json_data))
        with open(temp_file, 'r', encoding='utf-8_sig') as fin, open(output_file, 'a+', encoding='utf-8_sig') as fout:
            try:
                convert_json(fin, fout, func=expand, separator=".", safe=False, json_array=False)
                fin.close()
                fout.close()
            except:
                convert_json(fin, fout, func=restore, separator=".", safe=False, json_array=False)
                fin.close()
                fout.close()
        os.remove(temp_file)


if __name__ == '__main__':
    input_folder = './raw'
    output_file = 'output.csv'
    convert_to_csv(input_folder, output_file)
