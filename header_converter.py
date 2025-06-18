import json


def convert_multi_line_http_request_to_headers(http_request):
    headers = {}
    lines = http_request.split('\n')

    for line in lines:
        line = line.strip()

        if line == "":
            continue

        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()

    return headers


def convert_single_line_http_request_to_headers(http_request):
    headers = {}

    # 移除GET部分
    http_request = http_request.split(' ', 2)[-1]

    # 使用冒号加空格拆分字符串
    parts = http_request.split(': ')

    # 对于每个元素，将前一个元素作为键，当前元素作为值，并将冒号加空格添加回值的开头
    for i in range(1, len(parts)):
        key = parts[i - 1].split(' ')[-1]
        value = parts[i].rsplit(' ', 1)[0]
        headers[key] = value

    return headers



def convert_http_request_to_headers(http_request):
    headers = {}

    # 检查输入是否已经是字典模式
    try:
        headers = json.loads(http_request)
        if isinstance(headers, dict):
            return headers
    except json.JSONDecodeError:
        pass

    # 判断输入是否包含换行符，选择合适的处理方法
    if '\n' in http_request:
        return convert_multi_line_http_request_to_headers(http_request)
    else:
        return convert_single_line_http_request_to_headers(http_request)




if __name__ == "__main__":
    http_request1 = '''GET /ChatGPT HTTP/2 Host: poe.com User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0 Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8 Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2 Accept-Encoding: gzip, deflate, br Referer: https://poe.com/ Connection: keep-alive Cookie: p-b=58y0gDkcxMZNwe8Oo57kVg%3D%3D Upgrade-Insecure-Requests: 1 Sec-Fetch-Dest: document Sec-Fetch-Mode: navigate Sec-Fetch-Site: same-origin Sec-Fetch-User: ?1'''
    http_request2 = '''GET /favicon.ico HTTP/2
    Host: nat.dev
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0
    Accept: image/avif,image/webp,*/*
    Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
    Accept-Encoding: gzip, deflate, br
    Referer: https://nat.dev/?payment_success=true
    Connection: keep-alive
    Cookie: __client_uat=1682253385; __session=eyJhbGciOiJSUzI1NiIsImtpZCI6Imluc18yTWtjQlhndjhpbEwxcGNDTnB3MXV5anF0azgiLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwczovL25hdC5kZXYiLCJleHAiOjE2ODIyNTQ4NTcsImlhdCI6MTY4MjI1NDc5NywiaXNzIjoiaHR0cHM6Ly9jbGVyay5uYXQuZGV2IiwianRpIjoiOWQxNjEwNWYzODIzMzYzNjY2ZjIiLCJuYmYiOjE2ODIyNTQ3ODcsInNpZCI6InNlc3NfMk9wTjZETmF6bWtWNHJ2N213eFB5Z0VMS3l2Iiwic3ViIjoidXNlcl8yTnJQbUdPRVBnVnE2RlhSakxpb2Jjb2F1VXoiLCJ1c2VyX2VtYWlsIjoiYWxlbm0xMjA4QGdtYWlsLmNvbSIsInVzZXJfZmlyc3RfbmFtZSI6ImFsZW5tIiwidXNlcl9pZCI6InVzZXJfMk5yUG1HT0VQZ1ZxNkZYUmpMaW9iY29hdVV6IiwidXNlcl9sYXN0X25hbWUiOiJsYWxhIn0.hKYGZwxT98n6zw7AXuIgfUzqFSnweDMF-kXX-meNoDYUJt5HBH5RKRz7TgNbqtUzzxBjORRo97xJJPwK60TtInGNvy0p395GZmRRQl8a7iWQiChtY-s5gvKKxY0S15p0ySBpdDgyUOXZpGM_Xjdi-Aa0LGkmocx3PRoL2lQKxJ17NBpC24dsGNL7CYlRAWQqwrKEPR5Z2jWe_FwZ-Z7fg-jiJ5358fENLLyD7manPHFCBeyM5w0n_i30UUh8ukgpXcWFY2O-GOSsqo0CvQ-31TF3Ni45gF-VMWPqBrPvmQeVJL3kfqy8CK27P6jJNaFknWTjps9mB2pCju1FzVk9Hg
    Sec-Fetch-Dest: image
    Sec-Fetch-Mode: no-cors
    Sec-Fetch-Site: same-origin'''
    headers = convert_http_request_to_headers(http_request1)
    headers2 = convert_http_request_to_headers(http_request2)
    print(headers)
    print(headers2)
    print("请输入 HTTP 请求（字典格式或原始格式），按 Enter 键结束：")
    http_request = ""
    while True:
        line = input()
        if line == "":
            break
        http_request += line
                        # + '\n'
    headers = convert_http_request_to_headers(http_request)
    print("\n转换后的 headers 字典：")
    print(headers)
