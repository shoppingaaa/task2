#具体一道题目链接的保存

import tkinter as tk
import re
import requests
import bs4
import os
import time

base_url = "https://www.luogu.com.cn/problem/P"
minn = 1250
maxn = 1260  # 最大题号
save_path = "/洛谷题目集"  # 存储题目的文件夹路径

def main():
    # 创建存储题目的文件夹
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    window = tk.Tk()
    window.title("题目爬取工具")

    # 创建文本框用于显示题目和保存状态
    text_box = tk.Text(window, height=20, width=50)
    text_box.pack()

    # 创建开始按钮的点击事件
    def start_crawling():
        for i in range(minn, maxn + 1):
            text_box.insert(tk.END, "正在爬取 P{}...\n".format(i))
            window.update()

            html = get_html(base_url + str(i))
            if html == "error":
                text_box.insert(tk.END, "爬取失败，可能是不存在该题或无权查看\n")
            else:

                bs = bs4.BeautifulSoup(html, "html.parser")
                title = bs.find("h1")   #标题名称

                problemMD = get_MD(html)
                save_file_name = os.path.join(save_path, "P" + str(i) + title.string + ".md")
                save_data(problemMD, save_file_name)
                text_box.insert(tk.END, " 爬取成功！已保存\n")

            window.update()
            time.sleep(1)  # 添加延迟，暂停1秒

        text_box.insert(tk.END, "爬取完毕\n")

    # 创建开始按钮
    start_button = tk.Button(window, text="开始爬取", command=start_crawling)
    start_button.pack()

    window.mainloop()

def get_html(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76"
    }
    try:
        response = requests.get(url, headers=headers)
        html = response.text
        if str(html).find("Exception") == -1:
            return html
        else:
            return "error"
    except requests.exceptions.RequestException as e:
        print("请求异常:", e)

def get_MD(html):
    bs = bs4.BeautifulSoup(html, "html.parser")
    core = bs.select("article")[0]
    md = str(core)
    md = re.sub("<h1>", "# ", md)
    md = re.sub("<h2>", "## ", md)
    md = re.sub("<h3>", "#### ", md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
    return md

def save_data(data, filename):
    file = open(filename, "w", encoding="utf-8")
    file.write(data)
    file.close()

if __name__ == '__main__':
    main()
