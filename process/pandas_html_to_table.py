import os
import pandas as pd


def extract_tables_to_csv(html_folder, output_file):
    # 循环遍历文件夹中的所有 HTML 文件
    for filename in os.listdir(html_folder):
        if filename.endswith('.html'):
            file_path = os.path.join(html_folder, filename)

            # 使用 pandas 直接读取 HTML 文件中的表格
            tables = pd.read_html(file_path)

            # 遍历找到的表格并将其数据保存为 CSV 文件
            for index, table in enumerate(tables):
                table.to_csv(output_file, sep=',', mode='a+', index=False)
                print(f"Table {index + 1} from '{filename}' have been saved")


if __name__ == '__main__':
    # 使用示例：
    html_folder = './fund.eastmoney.com/raw'
    output_file = './output.csv'  # 如果未指定，则默认为 html_folder
    extract_tables_to_csv(html_folder, output_file)

# 用pandas中的read_html必须要先pip install html5lib，依赖html5lib
