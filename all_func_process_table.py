import process.pandas_html_to_table
import process.smart_mode_json_to_table
import process.jsontool_json_to_table
import process.pandas_json_to_table
import os
import glob


def all_convert(input_folder, output_folder):
    # 使用4种方式
    output_file1 = os.path.join(output_folder, 'html_to_table.csv')
    output_file2 = os.path.join(output_folder, 'smart_mode_json_to_table.csv')
    output_file3 = os.path.join(output_folder, 'pandas_json_to_table.csv')
    output_file4 = os.path.join(output_folder, 'jsontool_json_to_table.csv')
    if os.path.exists(output_file1):
        os.remove(output_file1)
    if os.path.exists(output_file2):
        os.remove(output_file2)
    if os.path.exists(output_file3):
        os.remove(output_file3)
    if os.path.exists(output_file4):
        os.remove(output_file4)
    files_glob = os.path.join(input_folder, '*.html')
    a = 0
    for file_path in glob.glob(files_glob):
        print(file_path)
        with open(file_path, 'rb') as f:
            content = f.read()
            if b'<html' in content or b'<HTML' in content:
                a = a+1
        # 判断文件内容中是否包含网页文件的特征
    if a != 0:
        try:
            # 尝试使用方法1
            process.pandas_html_to_table.extract_tables_to_csv(input_folder, output_file1)
        except Exception as e:
            # 处理方法1引发的异常
            print(f"Method 1 failed with exception: {e}")
    else:

        try:
            # 尝试使用方法2
            process.smart_mode_json_to_table.process_files(input_folder, output_file2)
        except Exception as e:
            # 处理方法2引发的异常
            print(f"Method 2 failed with exception: {e}")

        try:
            # 尝试使用方法3
            process.pandas_json_to_table.process_json_files(input_folder, output_file3)
        except Exception as e:
            # 处理方法3引发的异常
            print(f"Method 3 failed with exception: {e}")

        try:
            # 尝试使用方法4
            process.jsontool_json_to_table.convert_to_csv(input_folder, output_file4)
        except Exception as e:
            # 处理方法4引发的异常
            print(f"Method 4 failed with exception: {e}")


if __name__ == '__main__':
    # all_convert('./process/txt', './process/')
    all_convert('./html_files/test.com/raw', './html_files/test.com/table')
