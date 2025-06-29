#!/usr/bin/env python

import logging
import requests
import re
from urllib.parse import urljoin
import pymongo
import multiprocessing

mongo_client = pymongo.MongoClient("mongodb://192.168.6.6:27017/")
db = mongo_client["my_movies"]
collection = db["movies"]

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10


# 抓取某一页面的内容
def scrape_index(page):
    index_url = f'{BASE_URL}/page/{page}'
    return scrape_page(index_url)


# 定义一个函数抓取网页的内容
def scrape_page(url):
    logging.info("正在抓取 %s.....", url)
    # 发起get请求
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            logging.error("抓取 %s 时返回无效的状态码 %s", url, response.status_code)
    except requests.RequestException:
        # 如果发生异常，就报错
        logging.error("抓取%s时发生异常", url, exc_info=True)

    # 解析内容，并提取出详情页面的url


def parse_index(html):
    # 用正则把连接给提取出来
    # print(type(html))
    pattern = re.compile('<a.*href="(.*?)".*?class="name">')
    items = re.findall(pattern, html)
    # print(items)
    if not items:
        return []
    for item in items:
        # 把相对链接转为绝对链接
        detail_url = urljoin(BASE_URL, item)
        # print(detail_url)
        logging.info('找到详情页面了,链接%s', detail_url)
        yield detail_url


def scrape_detail(url):
    return scrape_page(url)


def parse_detail(html):
    #匹配图片的url
    cover_pattern = re.compile(
        'class="el-col.*?<img.*?src="(.*?)".*?class="cover">', re.S)

    # cover_pattern = re.compile(
    #     '<img.*?src="(.*?)".*?class="cover">', re.S)

    #匹配电影名称
    name_pattern = re.compile('<h2.*?>(.*?)</h2>')
    #匹配类别
    categories_pattern = re.compile(
        '<button.*?category.*?<span>(.*?)</span>.*?</button>', re.S)
    #匹配时间
    published_at_pattern = re.compile('(\d{4}-\d{2}-\d{2})\s?上映')
    #匹配剧情简介
    drama_pattern = re.compile('<div.*?drama.*?>.*?<p.*?>(.*?)</p>', re.S)
    #匹配评分
    score_pattern = re.compile('<p.*?score.*?>(.*?)</p>', re.S)

    cover = re.search(cover_pattern, html).group(1).strip() if re.search(cover_pattern, html) else None
    name = re.search(name_pattern, html).group(1).strip() if re.search(name_pattern, html) else None
    categories = re.findall(categories_pattern, html) if re.findall(categories_pattern, html) else []
    published_at = re.search(published_at_pattern, html).group(1) if re.search(published_at_pattern, html) else None
    drama = re.search(drama_pattern, html).group(1).strip() if re.search(drama_pattern, html) else None
    score = float(re.search(score_pattern, html).group(1).strip()) if re.search(score_pattern, html) else None
    # print(type(cover))
    return {
        'cover': cover,
        'name': name,
        'categories': categories,
        'published_at': published_at,
        'drama': drama,
        'score': score
    }


def save_data(data):
    collection.insert_one(data)
    logging.info("数据保存到mongodb成功！！！！")


def main(page):
    # for page in range(1,TOTAL_PAGE+1):
    index_html = scrape_index(page)
    detail_urls = parse_index(index_html)
    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)
        data = parse_detail(detail_html)
        logging.info('get detail data %s', data)
        save_data(data=data)
        logging.info('data saved successfully')


def run_main(page):
    main(page)


if __name__ == '__main__':
    # 获取CPU的核心数量
    num_process = multiprocessing.cpu_count()
    # 创建进程池
    pool = multiprocessing.Pool(num_process)
    # 要抓取的页面数量
    page_to_scrape = list(range(1, TOTAL_PAGE + 1))
    # 使用进程池运行
    pool.map(run_main, page_to_scrape)
    # 关闭进程池
    pool.close()