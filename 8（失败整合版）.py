#想把所有的小块合在一起，没完成

import tkinter as tk
import re
import requests
import bs4
import os
import time

# 创建一个 Tkinter 窗口
window = tk.Tk()
window.geometry("400x300")  # 设置窗口大小
text_box = tk.Text(window)

# 创建一个变量来保存选择的题目难度，默认为暂无评定
difficulty_var = tk.StringVar(window, "暂无评定")

# 创建一个标签来显示选择的题目难度
label = tk.Label(window, textvariable=difficulty_var)
label.pack(side="top", pady=10)  # 设置标签在顶部，并添加一定的上边距

# 创建一个下拉菜单来选择题目难度
difficulty_menu = tk.OptionMenu(window, difficulty_var, "暂无评定", "入门", "普及-", "普及/提高-", "普及+/提高", "提高+/省选-", "省选/NOI-", "NOI/NOI+/CTSC")
difficulty_menu.pack(side="top", pady=10)  # 设置下拉菜单在顶部，并添加一定的上边距

# 定义一个函数，当选择的题目难度发生变化时被调用
def difficulty_changed(*args):
    selected_difficulty = difficulty_var.get()
    #print("选择的题目难度：", selected_difficulty)

# 监听题目难度的变化
difficulty_var.trace("w", difficulty_changed)

# 定义一个函数，当点击“开始爬取”按钮时被调用
def start_crawling():
    selected_difficulty = difficulty_var.get()
    difficulty_index = ["暂无评定", "入门", "普及-", "普及/提高-", "普及+/提高", "提高+/省选-", "省选/NOI-", "NOI/NOI+/CTSC"].index(selected_difficulty)
    print("开始爬取题目，难度选项：", selected_difficulty, "，对应的数字：", difficulty_index)
    url = f"https://www.luogu.com.cn/problem/list?difficulty={difficulty_index}"
    print("选择的题目难度：", selected_difficulty, "，对应的数字：", difficulty_index)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76"
    }

    save_path = f"/洛谷题目集/{selected_difficulty}"  # 存储题目的文件夹路径

    response = requests.get(url, headers=headers)
    html = response.text
    bs = bs4.BeautifulSoup(html, "html.parser")

    all_divs = bs.find("div")
    all_titles = all_divs.find_all("a")
    count = 0
    while count < 50:
        for title in all_titles:
            link = title.get("href")
            if "P" in link:
                num = int(link[1:])
                base_url = f"https://www.luogu.com.cn/problem/P{num}"
                #print(base_url)
                text_box.insert(tk.END, "正在爬取 P{}...\n".format(num))

                html = get_html(base_url)
                if html == "error":
                    text_box.insert(tk.END, "爬取失败，可能是不存在该题或无权查看\n")
                else:

                    bs = bs4.BeautifulSoup(html, "html.parser")
                    title = bs.find("h1")  # 标题名称

                    problemMD = get_MD(html)
                    save_file_name = os.path.join(save_path, "P" + str(num) + title.string + ".md")
                    save_data(problemMD, save_file_name)
                    text_box.insert(tk.END, " 爬取成功！已保存\n")

                window.update()


                count += 1

        time.sleep(1)  # 添加延迟，暂停1秒

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




# 创建一个“开始爬取”按钮
start_button = tk.Button(window, text="开始爬取", command=start_crawling)
start_button.pack(side="bottom", pady=10)  # 设置按钮在顶部，并添加一定的上边距

# 运行 Tkinter 窗口的主循环
window.mainloop()
