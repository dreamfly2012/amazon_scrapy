from bs4 import BeautifulSoup
import random
import time
import grequests
import requests
import sys


# 设置 headers


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.1945.0",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Origin":"https://www.amazon.com"
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


# 按照类别查找包含“currently unavailable”的商品页面链接
def search_items(category, page):
    url = f"https://www.amazon.com/s?k={category}&page={page}"
    # url = f"https://www.amazon.com/s?k=children&i=stripbooks&crid=1L9OYESEPZ0XQ&sprefix=child%2Cstripbooks%2C1188&ref=nb_sb_noss_2"

    response = requests.get(url, headers=headers, proxies=proxies)
    
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
def get_total_page(content):
    # url = f"https://www.amazon.com/s?k={category}"
    # response = requests.get(url, headers=headers, proxies=proxies)
    
    # if response.status_code != 200:
    #     print("request failed")
    #     sys.exit()
    
    # soup = BeautifulSoup(response.text, "html.parser")
    
    # page = soup.find_all("div", {"data-component-type": "s-search-result"})
    
    return 6
    

def scrapy_items(category):
    total_links = []

    page = get_total_page()
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
    with open("result.txt", "w") as outfile:
        outfile.write("\n".join(result_links))


if __name__ == "__main__":
    # 测试
    category = "chairs"  # 请将此处替换为您感兴趣的商品类别

    scrapy_items(category)
