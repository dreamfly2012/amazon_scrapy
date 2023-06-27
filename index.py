import requests
from bs4 import BeautifulSoup
import random
import time


# 设置 headers


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1935.0",
    "Accept-Language": "en-US, en;q=0.5",
}

# 设置代理服务器
proxies = {
    "http": "http://127.0.0.1:10809",
    "https": "http://127.0.0.1:10809",
}

# 以下是一個示例代碼，用於在 10 到 60 秒之間進行隨機休眠
def random_sleep():
    sleep_time = random.randint(10, 60)
    print(f"Sleeping for {sleep_time} seconds...")
    time.sleep(sleep_time)
    print("Wake up!")


# 检查商品详情页是否包含指定关键词
def check_availability(url):
    response = requests.get(url, headers=headers, proxies=proxies)
    if "Currently unavailable" in response.text:
        return True
    else:
        return False


# 按照类别查找包含“currently unavailable”的商品页面链接
def search_items(category, page):
    url = f"https://www.amazon.com/s?k={category}&page={page}"
    # url = f"https://www.amazon.com/s?k=children&i=stripbooks&crid=1L9OYESEPZ0XQ&sprefix=child%2Cstripbooks%2C1188&ref=nb_sb_noss_2"

    response = requests.get(url, headers=headers, proxies=proxies)

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


# 测试
category = "high+chairs"  # 请将此处替换为您感兴趣的商品类别

total_links = []

# 循环页面抓取商品
for i in range(1, 6):
    item_links = search_items(category, i)
    total_links.append(item_links)
    random_sleep()

result_links = []
for link in total_links:
    if check_availability(link):
        result_links.append(link)

print(result_links)
