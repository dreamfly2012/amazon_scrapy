import os
from bs4 import BeautifulSoup
import random
import time
import grequests
import requests
import sqlite3
import sys
import datetime


# 设置 headers


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.1945.0",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Origin":"https://www.amazon.com",
    "Cookie":'csm-sid=497-8476988-7370720; x-amz-captcha-1=1710862803147405; x-amz-captcha-2=ZwQvUP47W4a1V05tvFPyGA==; session-id=147-8766007-3860244; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:FR"; skin=noskin; ubid-main=132-9469537-9901663; session-token=7dn5W4mvqXFNO1Wt2/AVb9gwiKGC1vxoZt38RIDA7A3+w7j4zg1VEr5t2GoXW8LTQXKgrfblhK3NqxVdxZoN/QhQiK6FIVDdVt6xnmt8qR+B9MVGR7pE6khcZd8ecVYU0s6LZ106Ao7Tdq0H9H2m/af7WIW/upDNED7jgzbskjeJXSTVkyusxtuorm30yThavo+w8SFuM1L0mlIrOX3kfMcb+kvMo4+6fQfKHiQaaNhhOYkrB6pmvOcqwy57UWsefoYHpRswWwrIeKH2YxNQK0XayUmmmrYQm53Kwg4qLVviKIE1PeMZJkYmZOq53uAfK3xoO0sjp0KZ07a/CVBzvt/YY6RRVO3I; ext_pgvwcount=0.9; csm-hit=tb:WY3PRMXD2QKRSMPGRXE4+s-QJMK65G8JY35MRG4PEA6|1710855680258&t:1710855680258&adb:adblk_yes',
}

# 设置代理服务器
proxies = {
    "http": "http://127.0.0.1:10809",
    "https": "http://127.0.0.1:10809",
}


# 以下是一個示例代碼，用於在 10 到 60 秒之間進行隨機休眠
def random_sleep():
    sleep_time = random.randint(5, 15)
    print(f"Sleeping for {sleep_time} seconds...")
    time.sleep(sleep_time)
    print("Wake up!")


# 检查商品详情页是否包含指定关键词
def check_availability(content):
    if "if this item will be back" in content:
        return True
    else:
        return False
    

# 获取配置信息，赋值给全局变量
def assign_global_values():
    # 连接到sqlite数据库
    conn = sqlite3.connect('inputs.db')
    c = conn.cursor()
    
    # 从inputs表中检索最近保存的cookie
    c.execute("SELECT proxy FROM setting ORDER BY ROWID DESC LIMIT 1")
    result = c.fetchone()
    proxy = result[0]
    global proxies
    proxies = {
        "http": proxy,
        "https": proxy,
    }


# 按照类别查找包含“currently unavailable”的商品页面链接
def search_items(category, page):
    url = f"https://www.amazon.com/s?k={category}&page={page}"
    # url = f"https://www.amazon.com/s?k=children&i=stripbooks&crid=1L9OYESEPZ0XQ&sprefix=child%2Cstripbooks%2C1188&ref=nb_sb_noss_2"

    response = requests.get(url, headers=headers, proxies=proxies)

    print(response)
    
    if response.status_code != 200:
        print("request failed")
        sys.exit()

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.find_all("div", {"data-component-type": "s-search-result"})
    item_links = []

    for item in items:
        a = item.find(
            "a",
            {
                "class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"
            },
        )

        item_links.append("https://www.amazon.com" + a["href"])
    return item_links

#TODO get max page
def get_total_page(category):
    # url = f"https://www.amazon.com/s?k={category}"
    # response = requests.get(url, headers=headers, proxies=proxies)
    
    # if response.status_code != 200:
    #     print("request failed")
    #     sys.exit()
    
    # soup = BeautifulSoup(response.text, "html.parser")
    
    # page = soup.find_all("div", {"data-component-type": "s-search-result"})
    
    return 6


def get_filepath():
    conn = sqlite3.connect('inputs.db')
    c = conn.cursor()   
    # 从inputs表中检索最近保存的cookie
    c.execute("SELECT filepath FROM setting ORDER BY ROWID DESC LIMIT 1")
    result = c.fetchone()
    filepath = result[0]
    ## 判断路径是否存在
    if filepath and os.path.exists(filepath):
        return filepath
    else:
        return None
   


def write_log(result_links):
    dir_path = get_filepath()
    if dir_path is None:
        print("No directory found")
        sys.exit()
    now = datetime.datetime.now()
    file_name = "log_{}.txt".format(now.strftime("%Y-%m-%d_%H-%M-%S"))
    file_path = os.path.join(dir_path, file_name)
  
    with open(file_path, "w") as outfile:
        outfile.write("\n".join(result_links))

def scrapy_items(category):
    total_links = []
    page = get_total_page(category)
    # 循环页面抓取商品
    for i in range(1, page):
        item_links = search_items(category, i)
        total_links.extend(item_links)
        random_sleep()

    result_links = []

    if not total_links:
        print("failed to scrapy")

    rs = (grequests.get(u, headers=headers, proxies=proxies) for u in total_links)

    responses = grequests.map(rs, size=10)

    # Iterate over the responses and print the results.
    for response in responses:
        if response is not None:
            if check_availability(response.text):
                result_links.append(response.url)

    print(result_links)
    
    write_log(result_links)
    


if __name__ == "__main__":
    # 测试
    category = "chairs"  # 请将此处替换为您感兴趣的商品类别

    scrapy_items(category)
