import re
from urllib.parse import urlparse, urlunparse
import urllib

# 查找两个相同长度的 URL 之间的数字差异
def find_pattern_v1(url1, url2):
    parsed1 = urlparse(url1)
    parsed2 = urlparse(url2)
    path_query1 = parsed1.path + '?' + parsed1.query
    path_query2 = parsed2.path + '?' + parsed2.query
    num1 = [int(x) for x in re.findall(r'\d+', path_query1)]
    num2 = [int(x) for x in re.findall(r'\d+', path_query2)]
    print(num1)
    print(num2)
    num_diff = []
    # 遍历两个URL中的数字
    for n1, n2 in zip(num1, num2):
        # 如果数字递增，则计算差值
        if n2 > n1:
            num_diff.append(n2 - n1)
        else:
            num_diff.append(None)
    print(num_diff)
    return num_diff

def find_pattern_v2(url1, url2):
    # 提取两个 URL 的路径
    parsed1 = urlparse(url1)
    parsed2 = urlparse(url2)
    # 提取路径中的数字
    path_query1 = parsed1.path + '?' + parsed1.query
    path_query2 = parsed2.path + '?' + parsed2.query
    num1 = [int(x) for x in re.findall(r'\d+', path_query1)]
    num2 = [int(x) for x in re.findall(r'\d+', path_query2)]
    print(num1)
    print(num2)

    # 补充num1列表
    if len(num2) > len(num1):
        extra_num = num2[len(num1)]
        if extra_num == 2:
            num1.append(1)
        elif extra_num == 1:
            num1.append(0)
        else:
            num1.append(0)

    num_diff = []
    for n1, n2 in zip(num1, num2):
        if n2 > n1:
            num_diff.append(n2 - n1)
        elif n1 == 0:
            num_diff.append(1)
        else:
            num_diff.append(None)
    print(num_diff)

    return num_diff


# 根据输入的 URL 长度选择适当的查找数字差异的方法
def find_pattern(url1, url2):
    # 提取两个 URL 的路径
    parsed1 = urlparse(url1)
    parsed2 = urlparse(url2)
    path_query1 = parsed1.path + '?' + parsed1.query
    path_query2 = parsed2.path + '?' + parsed2.query

    # 提取路径中的数字
    num1 = [int(x) for x in re.findall(r'\d+', path_query1)]
    num2 = [int(x) for x in re.findall(r'\d+', path_query2)]

    if len(num1) == len(num2):
        return find_pattern_v1(url1, url2)
    else:
        return find_pattern_v2(url1, url2)


def apply_pattern_with_index(num_diff, url1_decoded, url2_decoded, pages):
    # 将前两个输入的URL添加到URL列表中，同时添加序号
    url_list = [(1, url1_decoded), (2, url2_decoded)]
    url = url2_decoded
    # 生成剩余的URL
    for idx in range(3, pages + 1):
        # 从当前URL中提取数字
        parsed = urlparse(url)
        path = parsed.path
        query = parsed.query
        path_query = path + '?' + query
        num = [int(x) for x in re.findall(r'\d+', path_query)]
        print('num', num)
        # 根据数字差异计算下一个URL中的数字
        next_num = [n + diff if diff is not None else n for n, diff in zip(num, num_diff)]
        print('next_num', next_num)

        # 用计算得到的下一个数字替换原始URL中的数字，生成下一个URL
        next_path_query = path_query
        print('next_path_query', next_path_query)

        replaced = set()
        new_path_query = ""

        while next_path_query:
            match = re.search(r'\d+', next_path_query)

            if match:
                n = int(match.group())
                if n in num and n not in replaced:
                    idx_new = num.index(n)
                    new_path_query += next_path_query[:match.start()] + str(next_num[idx_new])
                    replaced.add(n)
                else:
                    new_path_query += next_path_query[:match.end()]

                next_path_query = next_path_query[match.end():]

            else:
                new_path_query += next_path_query
                next_path_query = ""

        next_path, next_query = new_path_query.split('?', 1)
        print('next_path', next_path)

        next_url = urlunparse((parsed.scheme, parsed.netloc, next_path, parsed.params, next_query, parsed.fragment))
        url_list.append((idx, next_url))
        url = next_url
    return url_list



# 主函数，预测指定数量的URL
def predict_next_urls(url1, url2, pages):
    # 对URL进行解码
    url1_decoded = urllib.parse.unquote(url1)
    url2_decoded = urllib.parse.unquote(url2)

    # 查找数字差异
    num_diff = find_pattern(url1_decoded, url2_decoded)

    # 应用数字差异，生成指定数量的URL
    next_urls_decoded = apply_pattern_with_index(num_diff, url1_decoded, url2_decoded, pages)

    # 对生成的URL进行编码
    encoded_urls = []

    for url_tuple in next_urls_decoded:
        url_index = url_tuple[0]
        url = url_tuple[1]
        encoded_url = urllib.parse.quote(url, safe=':/?=&[]{}_%')
        encoded_urls.append((url_index, encoded_url))

    return encoded_urls


if __name__ == "__main__":
    url1 = input("请输入第一个URL：")
    url2 = input("请输入第二个URL：")
    pages = int(input("请输入页数："))

    try:
        # 根据输入的 URL 和页数预测接下来的 URL
        next_urls = predict_next_urls(url1, url2, pages)
        print("预测的URL列表如下：")
        for url in next_urls:
            print(url)
    except ValueError as e:
        print(e)
