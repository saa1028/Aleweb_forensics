from flask import Flask, render_template, request, flash, get_flashed_messages, send_file
import url_generator
import async_web_scraper
import header_converter
import all_func_process_table
from werkzeug.utils import secure_filename
import os
import zipfile
import hash

app = Flask(__name__)
app.secret_key = 'saa1028'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/intelligent_fix', methods=['GET', 'POST'])
def intelligent_fix():
    if request.method == 'POST':
        first_page_url = request.form['first_page_url']
        print(first_page_url)
        first_page_url = first_page_url.strip()
        second_page_url = request.form['second_page_url']
        second_page_url = second_page_url.strip()
        num_pages = request.form['num_pages']
        num_pages = int(num_pages)
        request_headers = request.form['request_headers']
        # 把原始header转化为字典
        request_headers = header_converter.convert_http_request_to_headers(request_headers)
        print(request_headers)
        num_threads = request.form['num_threads']
        num_threads = int(num_threads)
        num_processes = request.form['num_processes']
        num_processes = int(num_processes)
        all_urls = []
        # 根据接受的第一页，第二页，以及页数，通过url_generator中的predict_next_url函数生成url列表
        try:
            all_urls = url_generator.predict_next_urls(first_page_url, second_page_url, num_pages)
            for a in all_urls:
                print(a)
            print(all_urls, request_headers, num_threads, num_processes)
        except ValueError as e:
            print(e)
        async_web_scraper.async_cral_websites(all_urls, request_headers, num_threads, num_processes)
        flash('后台固定完成', category='success')
    messages = get_flashed_messages(with_categories=True)
    return render_template('intelligent_fix.html', messages=messages)


@app.route('/import_fix', methods=['GET', 'POST'])
def import_fix():
    if request.method == 'POST':
        file = request.files['file']
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        file.save('./uploads/' + secure_filename(file.filename))
        with open('./uploads/' + secure_filename(file.filename), mode="r", encoding='utf-8') as f:
            # 读取txt文件中的所有行，并去除每行末尾的换行符
            urls = [line.rstrip() for line in f.readlines()]

            # 构造所需格式的列表
        url_result = [(i, url) for i, url in enumerate(urls)]
        print(url_result)
        request_headers = request.form['request_headers']
        # 把原始header转化为字典
        request_headers = header_converter.convert_http_request_to_headers(request_headers)
        print(request_headers)
        num_threads = request.form['num_threads']
        num_threads = int(num_threads)
        num_processes = request.form['num_processes']
        num_processes = int(num_processes)
        async_web_scraper.async_cral_websites(url_result, request_headers, num_threads, num_processes)
        # 开始爬取文件中的数据
        flash('后台固定完成', category='success')
    messages = get_flashed_messages(with_categories=True)
    return render_template('import_fix.html', messages=messages)


@app.route('/conversion_table')
def conversion_table():
    dirs = []
    files = []
    path = './html_files'
    for name in os.listdir(path):
        if os.path.isdir(os.path.join(path, name)):
            dirs.append(name)
        else:
            files.append(name)
    return render_template('conversion_table.html', dirs=dirs, files=files)


@app.route('/process', methods=['POST'])
def process():
    folder = request.form['folder']
    action = request.form['action']
    # 在这里根据勾选的文件和选择的处理操作进行处理

    folder_path = os.path.join('./html_files', folder)

    def download():
        os.makedirs('./zip_files', exist_ok=True)
        zip_path = os.path.join('./zip_files', folder + '.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))
        os.makedirs('./hash_files', exist_ok=True)
        hash_file_path = os.path.join('./hash_files', folder + '_hash.txt')
        if os.path.exists(hash_file_path):
            os.remove(hash_file_path)
        hash.record_hash(zip_path, hash_file_path)  # 调用 record_hash 函数计算并记录哈希值到文件中
        os.makedirs('./final_files', exist_ok=True)
        final_zip_path = os.path.join('./final_files', folder + '_final.zip')

        with zipfile.ZipFile(final_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(zip_path, os.path.relpath(zip_path, './zip_files'))
            zipf.write(hash_file_path, os.path.relpath(hash_file_path, './hash_files'))
        return send_file(final_zip_path, as_attachment=True)
    if action == 'download':
        send = download()
        return send
    elif action == 'process':
        # 进行数据处理操作
        # 指定文件夹路径

        # 构造HTML文件的glob表达式
        input_folder = os.path.join('./html_files/' + folder + '/raw')
        os.makedirs('./html_files/' + folder + '/table', exist_ok=True)
        output_folder = os.path.join('./html_files/' + folder + '/table')
        all_func_process_table.all_convert(input_folder, output_folder)
        # 遍历文件夹中的所有HTML文件
        send = download()
        return send
    else:
        # 如果未选择任何操作，则返回错误消息
        return 'Error: no action selected'


@app.route('/operation_manual')
def operation_intelligence():
    return render_template('operation_manual.html')


if __name__ == '__main__':
    app.run(debug=True)
