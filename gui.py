import tkinter as tk
from tkinter import filedialog
import sqlite3
import index


def save_file():
    # 弹出保存文件路径对话框
    file_path = filedialog.askdirectory()

    # 检查用户是否选择了路径
    if file_path:
        # 保存文件路径到sqlite数据库
        conn = sqlite3.connect("inputs.db")
        c = conn.cursor()
        # 更新代理信息
        c.execute("UPDATE setting SET filepath = ?", (file_path,))
        conn.commit()
        conn.close()


def save_inputs(proxy, cookie, keyword):
    # 连接到sqlite数据库
    conn = sqlite3.connect("inputs.db")
    c = conn.cursor()

    # 创建一个保存输入的表
    c.execute(
        """CREATE TABLE IF NOT EXISTS inputs
                 (proxy TEXT, cookie TEXT, keyword TEXT)"""
    )

    # 插入用户输入到表中
    c.execute("INSERT INTO inputs VALUES (?, ?, ?)", (proxy, cookie, keyword))

    # 提交更改并关闭连接
    conn.commit()
    conn.close()


def show_proxy_input():
    # 创建一个弹出窗口
    popup = tk.Toplevel()
    popup.title("Proxy Input")
    # 设置窗口的大小和位置
    popup.geometry("400x200+200+200")

    # 连接到sqlite数据库
    conn = sqlite3.connect("inputs.db")
    c = conn.cursor()

    # 从inputs表中检索最近保存的cookie
    c.execute("SELECT proxy FROM setting ORDER BY ROWID DESC LIMIT 1")
    result = c.fetchone()

    # 创建一个输入框，用于用户输入代理信息
    proxy_label = tk.Label(popup, text="Proxy:")
    proxy_label.grid(row=0, column=0, padx=(10, 0), pady=10, ipadx=60)
    proxy_entry = tk.Entry(popup, width=50)
    proxy_entry.grid(row=0, column=1, ipadx=60)

    # 如果有最近保存的cookie，则在输入框中显示它
    if result is not None:
        proxy_entry.insert(tk.END, result[0])

    # 创建一个按钮，用于保存用户输入并关闭弹出窗口
    save_button = tk.Button(
        popup, text="Save", command=lambda: save_proxy_input(popup, proxy_entry.get())
    )
    save_button.grid(row=1, column=0, columnspan=2, padx=(10, 0))


def save_proxy_input(popup, proxy):
    # 保存代理信息到sqlite数据库
    conn = sqlite3.connect("inputs.db")
    c = conn.cursor()
    # 更新代理信息
    c.execute("UPDATE setting SET proxy = ?", (proxy,))
    conn.commit()
    conn.close()

    # 关闭弹出窗口
    popup.destroy()


def show_cookie_input():
    # 创建一个弹出窗口
    popup = tk.Toplevel()
    popup.title("Cookie Input")
    # 设置窗口的大小和位置
    popup.geometry("400x200+200+200")

    # 连接到sqlite数据库
    conn = sqlite3.connect("inputs.db")
    c = conn.cursor()

    # 从inputs表中检索最近保存的cookie
    c.execute("SELECT cookie FROM setting ORDER BY ROWID DESC LIMIT 1")
    result = c.fetchone()

    # 创建一个输入框，用于用户输入cookie信息
    cookie_label = tk.Label(popup, text="Cookie:")
    cookie_label.grid(row=0, column=0, padx=10, pady=10, ipadx=60)
    cookie_entry = tk.Entry(popup)
    cookie_entry.grid(row=0, column=1, ipady=50)

    # 如果有最近保存的cookie，则在输入框中显示它
    if result is not None:
        cookie_entry.insert(tk.END, result[0])

    # 创建一个按钮，用于保存用户输入并关闭弹出窗口
    save_button = tk.Button(
        popup, text="Save", command=lambda: save_cookie_input(popup, cookie_entry.get())
    )
    save_button.grid(row=1, column=0, columnspan=2)


def save_cookie_input(popup, cookie):
    # 保存cookie信息到sqlite数据库
    conn = sqlite3.connect("inputs.db")
    c = conn.cursor()
    # 更新cookie信息
    c.execute("UPDATE setting SET cookie = ?", (cookie,))
    conn.commit()
    conn.close()

    # 关闭弹出窗口
    popup.destroy()


def crawl(keyword):
    # 赋值proxy
    index.assign_global_values()
    # 在此处编写爬虫代码
    index.scrapy_items(keyword)
    pass


def run_crawler():
    # 获取用户输入
    keyword = keyword_entry.get()

    print(keyword)

    # 调用爬虫函数
    crawl(keyword)


# 创建一个窗口
window = tk.Tk()
window.title("Web Crawler")

window.geometry("600x400+200+200")

# 创建一个输入框，用于用户输入关键词
keyword_label = tk.Label(window, text="Keyword:")
keyword_label.grid(row=0, column=0, ipadx=100)

keyword_entry = tk.Entry(window)
keyword_entry.grid(row=0, column=1, padx=20, ipadx=100)


# 创建一个按钮，用于触发爬虫程序
crawl_button = tk.Button(window, text="Crawl", command=run_crawler)
crawl_button.grid(row=1, column=0, ipadx=40, ipady=10, pady=50, columnspan=2)


# 创建一个菜单栏
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# 在菜单栏中创建一个“设置”菜单
settings_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Settings", menu=settings_menu)

# 在“设置”菜单中添加一个“代理设置”选项
settings_menu.add_command(label="Proxy Settings", command=show_proxy_input)

# 在“设置”菜单中添加一个“Cookie设置”选项
settings_menu.add_command(label="Cookie Settings", command=show_cookie_input)

# 在“设置”菜单中添加一个“文件路径设置”选项
settings_menu.add_command(label="FilePath Settings", command=save_file)

# 运行窗口
window.mainloop()
