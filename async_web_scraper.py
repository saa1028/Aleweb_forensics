import os
import asyncio
import aiofiles
import numpy as np
import multiprocessing as mp
from aiohttp_retry import RetryClient, ExponentialRetry
from urllib.parse import urlparse


# 异步获取网页内容
async def fetch(url, session, semaphore):
    async with semaphore:
        try:
            async with session.get(url[1], timeout=5, ssl=True) as response:
                return await response.text()
        except Exception:
            async with session.get(url[1], timeout=5, ssl=False) as response:
                return await response.text()


# 将内容异步保存到文件
async def save_to_file(file_path, content):
    async with aiofiles.open(file_path, 'w', encoding='utf-8') as file:
        await file.write(content)


# 获取网页内容并保存
async def fetch_and_save(url, session, semaphore):
    try:
        content = await fetch(url, session, semaphore)
        file_name = f"{url[0]}.html"
        parsed_url = urlparse(url[1])
        domain = parsed_url.netloc
        os.makedirs('./html_files/' + domain + '/raw', exist_ok=True)
        file_path = os.path.join('./html_files/' + domain + '/raw', file_name)
        await save_to_file(file_path, content)
    except asyncio.exceptions.TimeoutError:
        # 处理超时错误
        pass


# 异步获取所有网页内容并保存
async def fetch_all(urls, headers, concurrency_limit):
    semaphore = asyncio.Semaphore(concurrency_limit)
    # 网络不稳定时，增加重试次数
    retry_strategy = ExponentialRetry(attempts=2)
    async with RetryClient(headers=headers, retry_options=retry_strategy) as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(fetch_and_save(url, session, semaphore)))
        return await asyncio.gather(*tasks)


# 处理 URL 子列表
def process_urls(urls, headers, concurrency_limit):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_all(urls, headers, concurrency_limit))
    loop.close()

    print("所有文件已保存。")


def process_urls_with_concurrency_limit(args):
    urls, headers, concurrency_limit = args
    return process_urls(urls, headers, concurrency_limit)


def async_cral_websites(urls, headers, concurrency_limit, num_processes):
    # 创建存储 HTML 文件的目录
    os.makedirs('./html_files', exist_ok=True)
    # 将 all_urls 列表分割为指定数量的子列表
    split_urls = np.array_split(urls, num_processes)

    # 使用进程池处理 URL 子列表
    with mp.Pool(processes=num_processes) as pool:
        concurrency_limit = int(concurrency_limit)
        pool.map(process_urls_with_concurrency_limit, [(urls, headers, concurrency_limit) for urls in split_urls])

    print("所有文件已保存。")


if __name__ == "__main__":
    all_urls = [
        (0, 'https://www.example.com'),
        (1, 'https://www.example.org'),
        (2, 'https://www.example.net'),
        (3, 'https://www.example.co.uk'),
        (4, 'https://www.baidu.com'),
        (5, 'https://www.google.cn')
        # 添加更多 URL
    ]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
               'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
               'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none',
               'Sec-Fetch-User': '?1', 'If-Modified-Since': 'Thu, 17 Oct 2019 07:18:26 GMT',
               'If-None-Match': '"3147526947"', 'TE': 'trailers'}

    async_cral_websites(all_urls, headers, 1, 2)
