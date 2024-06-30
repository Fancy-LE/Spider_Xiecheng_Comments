# -*- coding: utf-8 -*-

import time
import re
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

import warnings
warnings.filterwarnings('ignore')

timeList = []  # 发表时间
scoreList = [] # 评分
comments = []  # 评论文本
def getData(driver, ddl1, j):
    '''获取数据'''
    times = driver.find_elements(By.CSS_SELECTOR, '.commentTime')
    scores = driver.find_elements(By.CSS_SELECTOR, '.averageScore')[1:]
    comment = driver.find_elements(By.CSS_SELECTOR, '.commentDetail')

    for c,t,s in zip(comment, times, scores):
        try:
            timeList.append(re.findall(r'(\d{4}-\d{1,2}-\d{1,2})', t.text)[0])
            scoreList.append(re.findall(r"(.*)分", s.text)[0])
            comments.append(c.text)
        except:
            pass

    print(f"共{int(ddl1)}页，第{j}页下载完成...")

if __name__ == '__main__':
    id = input("请输入景点名称：")   #西湖
    # id = '万佛湖'
    url = input("请输入下载链接：")
    # url = 'https://you.ctrip.com/sight/shucheng2630/65747.html'
    i = 500

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36')
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()

    try:
        driver.get(url)
        time.sleep(4)

        # 获取总的页码
        ddl = driver.find_elements(By.CSS_SELECTOR, '.ant-pagination')
        for t in ddl:
            ddl1= t.text.split("\n")[-2]
        j = 1

        while True:
            t1 = random.uniform(2, 3)
            # 设置随机间隔时间

            getData(driver, ddl1, j)  # 获取数据
            j += 1
            # 翻页
            # element = driver.find_element(By.CSS_SELECTOR, '.ant-pagination-next')
            # element.click()
            xyy = driver.find_element(By.CSS_SELECTOR, value=r'.ant-pagination-next')  # 只需要修改这句
            driver.execute_script("arguments[0].click();", xyy)

            if j == int(ddl1) +1 or j > i:
                break

            time.sleep(t1)

    finally:
        driver.close()

    # save
    data = pd.DataFrame({ "date": timeList,"评分": scoreList, "comments": comments })
    data.to_csv(f"./data/result_{id}.csv", encoding='utf8')
    print("**********done***********")
