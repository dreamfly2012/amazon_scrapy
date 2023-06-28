import unittest
import sys

sys.path.append("..")
import index
import logging
import requests


class IndexTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.1945.0",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Origin":"https://www.amazon.com",
            "cookie":'session-id=141-0198084-0736137; session-id-time=2082787201l; i18n-prefs=USD; ubid-main=130-1285598-8855163; session-token="fFkZTioLhHsg8InE5+vY05YUMVMqiRVweomO4daaj9oLvDXU4vOoiQNiXZNxxPct0Jts9hGZvHqmbT68L5AnaCXC07PjvISaV4X21By96i7NiB0p4sVutfI3m9aqOtdAaAm6LNBzt0DiJ1s+N8CoZ+02SpPBPi8jZ4Yi5hF5tezb6JNpf3N2NXhAsFrwp1jMwGQAQtR7j5YiswQowClNY1LWH/mJDD/UwVmMrUnhAiM="',
        }

        # 设置代理服务器
        self.proxies = {
            "http": "http://127.0.0.1:10809",
            "https": "http://127.0.0.1:10809",
        }
        
        # 设置cookie
        self.cookies = {
            
        }
    
    def test_check_availability(self):
        # content = "test"
        content = "if this item will be back"
        result = index.check_availability(content)

        if index.check_availability(content):
            self.assertEqual(result, True)
        else:
            self.assertEqual(result, True)

    def test_read_result(self):
        result = ""
        with open("result.txt", "r") as f:
            for line in f:
                line = line.rstrip("\n")
                line = line.rstrip("\r")
                result += line

        logging.info(result)
        
    def test_deliver_to(self):
        url = 'https://www.amazon.com/dp/B0735WMNT5'
        
        response = requests.get(url,  headers=self.headers, proxies=self.proxies)
    
        if response.status_code != 200:
            print("request failed")
            sys.exit()
        if "New York" in response.text:
            logging.info("ok")
        else:
            self.assertEqual(1,2)


if __name__ == "__main__":
    unittest.main()
