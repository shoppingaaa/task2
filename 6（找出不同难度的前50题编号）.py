#把各种难度对应题目的编号找了出来，再根据编号就可以找到对应题目的链接


import requests
import bs4

#先尝试难度等级为1的前50题编号
url = "https://www.luogu.com.cn/problem/list?difficulty=1"


headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76"
    }
response = requests.get(url, headers=headers)
html = response.text
bs = bs4.BeautifulSoup(html, "html.parser")


#找出前50题对应编号，这样就可以找到题目对应的url
all_divs = bs.find("div")
all_titles = all_divs.find_all("a")
for title in all_titles:
    link = title.get("href")
    if "P" in link:
        print(link)